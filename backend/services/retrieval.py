from typing import List
from collections import defaultdict
from pydantic import BaseModel
from langchain_core.documents import Document
from backend.config.config import config
from backend.utils.logger import get_logger

logger = get_logger(__name__)

class QueryVariations(BaseModel):
    queries: List[str]

class BaseRetrievalStrategy:
    def retrieve(self, db, model, search_question: str) -> List[Document]:
        raise NotImplementedError("Strategies must implement retrieve method")

class StandardRetrieval(BaseRetrievalStrategy):
    def retrieve(self, db, model, search_question: str) -> List[Document]:
        logger.info("Using Standard Retrieval Strategy")
        retriever = db.as_retriever(search_kwargs={"k": config.TOP_K})
        return retriever.invoke(search_question)

class MultiQueryRetrieval(BaseRetrievalStrategy):
    def retrieve(self, db, model, search_question: str) -> List[Document]:
        logger.info("Using Multi-Query Retrieval Strategy")
        
        # 1. Generate Query Variations
        llm_with_tools = model.with_structured_output(QueryVariations)
        prompt = f"""Generate 3 different variations of this query that would help retrieve relevant documents:
Original query: {search_question}
Return 3 alternative queries that rephrase or approach the same question from different angles."""
        
        try:
            response = llm_with_tools.invoke(prompt)
            queries = response.queries
            logger.info(f"Generated query variations: {queries}")
        except Exception as e:
            logger.error(f"Failed to generate query variations: {e}")
            queries = [search_question]
            
        # 2. Retrieve documents for all queries and pool them
        retriever = db.as_retriever(search_kwargs={"k": config.TOP_K})
        all_docs = []
        unique_contents = set()
        
        for q in queries:
            docs = retriever.invoke(q)
            for d in docs:
                if d.page_content not in unique_contents:
                    unique_contents.add(d.page_content)
                    all_docs.append(d)
                    
        return all_docs[:config.TOP_K]

class RRFRetrieval(BaseRetrievalStrategy):
    def retrieve(self, db, model, search_question: str) -> List[Document]:
        logger.info("Using Reciprocal Rank Fusion Retrieval Strategy")
        
        # 1. Generate variations
        llm_with_tools = model.with_structured_output(QueryVariations)
        prompt = f"""Generate 3 different variations of this query that would help retrieve relevant documents:
Original query: {search_question}
Return 3 alternative queries that rephrase or approach the same question from different angles."""
        
        try:
            response = llm_with_tools.invoke(prompt)
            queries = response.queries
            # include original query
            queries.append(search_question)
        except Exception as e:
            logger.error(f"Failed to generate query variations for RRF: {e}")
            queries = [search_question]
            
        # 2. Search with each query
        retriever = db.as_retriever(search_kwargs={"k": 5}) # Get more docs for RRF
        chunk_lists = []
        for q in queries:
            docs = retriever.invoke(q)
            chunk_lists.append(docs)
            
        # 3. Apply Reciprocal Rank Fusion
        k_val = 60
        rrf_scores = defaultdict(float)
        all_unique_chunks = {}
        
        for chunks in chunk_lists:
            for position, chunk in enumerate(chunks, 1):
                chunk_content = chunk.page_content
                all_unique_chunks[chunk_content] = chunk
                position_score = 1 / (k_val + position)
                rrf_scores[chunk_content] += position_score
                
        # 4. Sort and return top K
        sorted_chunks = sorted(
            [(all_unique_chunks[content], score) for content, score in rrf_scores.items()],
            key=lambda x: x[1],
            reverse=True
        )
        
        fused_results = [item[0] for item in sorted_chunks[:config.TOP_K]]
        return fused_results

class HybridRetrieval(BaseRetrievalStrategy):
    def retrieve(self, db, model, search_question: str) -> List[Document]:
        logger.info("Using Hybrid Search Strategy (Vector + BM25)")
        try:
            from langchain.retrievers import EnsembleRetriever, BM25Retriever
            
            # Note: For BM25 to work properly in this simple architecture without a persistent keyword index, 
            # we pull out a subset of documents from ChromaDB based on a broader semantic search, 
            # or we fetch all. Since get() can be large, we fetch a large pool semantically first.
            vector_retriever = db.as_retriever(search_kwargs={"k": 20})
            pool_docs = vector_retriever.invoke(search_question)
            
            if not pool_docs:
                return []
                
            bm25_retriever = BM25Retriever.from_documents(pool_docs)
            bm25_retriever.k = config.TOP_K
            
            # Redefine vector_retriever to return top K
            vector_retriever.search_kwargs = {"k": config.TOP_K}
            
            hybrid_retriever = EnsembleRetriever(
                retrievers=[vector_retriever, bm25_retriever],
                weights=[0.7, 0.3]
            )
            
            return hybrid_retriever.invoke(search_question)
        except ImportError:
            logger.error("rank_bm25 not installed. Falling back to Standard Retrieval.")
            return StandardRetrieval().retrieve(db, model, search_question)

class RerankerRetrieval(BaseRetrievalStrategy):
    def retrieve(self, db, model, search_question: str) -> List[Document]:
        logger.info("Using Reranker Strategy")
        try:
            from langchain.retrievers.document_compressors import CrossEncoderReranker
            from langchain_community.cross_encoders import HuggingFaceCrossEncoder
            from langchain.retrievers import ContextualCompressionRetriever
            
            # Retrieve a larger pool
            base_retriever = db.as_retriever(search_kwargs={"k": 15})
            
            # Using a tiny reranker model for speed/demo purposes
            hf_model = HuggingFaceCrossEncoder(model_name="cross-encoder/ms-marco-TinyBERT-L-2-v2")
            compressor = CrossEncoderReranker(model=hf_model, top_n=config.TOP_K)
            
            compression_retriever = ContextualCompressionRetriever(
                base_compressor=compressor, 
                base_retriever=base_retriever
            )
            
            return compression_retriever.invoke(search_question)
        except ImportError as e:
            logger.error(f"Reranker dependencies missing ({e}). Falling back to Standard Retrieval.")
            return StandardRetrieval().retrieve(db, model, search_question)
        except Exception as e:
            logger.error(f"Reranker error ({e}). Falling back to Standard Retrieval.")
            return StandardRetrieval().retrieve(db, model, search_question)

# Factory function
def get_retrieval_strategy(strategy_name: str) -> BaseRetrievalStrategy:
    strategies = {
        "standard": StandardRetrieval,
        "multi_query": MultiQueryRetrieval,
        "rrf": RRFRetrieval,
        "hybrid": HybridRetrieval,
        "reranker": RerankerRetrieval
    }
    
    strategy_class = strategies.get(strategy_name.lower())
    if not strategy_class:
        logger.warning(f"Strategy '{strategy_name}' not found. Falling back to Standard.")
        return StandardRetrieval()
        
    return strategy_class()
