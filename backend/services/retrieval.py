from typing import List
from collections import defaultdict
from pydantic import BaseModel
from langchain_core.documents import Document
from config.config import config
from utils.logger import get_logger

logger = get_logger(__name__)

class QueryVariations(BaseModel):
    queries: List[str]

class BaseRetrievalStrategy:
    def retrieve(self, db, model, search_question: str) -> List[Document]:
        raise NotImplementedError("Strategies must implement retrieve method")
        
    def _generate_queries(self, model, search_question: str) -> List[str]:
        llm_with_tools = model.with_structured_output(QueryVariations)
        prompt = f"""Generate 3 different variations of this query that would help retrieve relevant documents:
Original query: {search_question}
Return 3 alternative queries that rephrase or approach the same question from different angles."""
        
        try:
            response = llm_with_tools.invoke(prompt)
            queries = response.queries
            logger.info(f"Generated query variations: {queries}")
            return queries
        except Exception as e:
            logger.error(f"Failed to generate query variations: {e}")
            return [search_question]

class StandardRetrieval(BaseRetrievalStrategy):
    def retrieve(self, db, model, search_question: str) -> List[Document]:
        logger.info("Using Standard Retrieval Strategy")
        retriever = db.as_retriever(search_kwargs={"k": config.TOP_K})
        return retriever.invoke(search_question)

class MultiQueryRetrieval(BaseRetrievalStrategy):
    def retrieve(self, db, model, search_question: str) -> List[Document]:
        logger.info("Using Multi-Query Retrieval Strategy")
        
        # 1. Generate Query Variations
        queries = self._generate_queries(model, search_question)
            
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
        queries = self._generate_queries(model, search_question)
        if search_question not in queries:
            queries.append(search_question)
            
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

# Factory function
def get_retrieval_strategy(strategy_name: str) -> BaseRetrievalStrategy:
    strategies = {
        "standard": StandardRetrieval,
        "multi_query": MultiQueryRetrieval,
        "rrf": RRFRetrieval
    }
    
    strategy_class = strategies.get(strategy_name.lower())
    if not strategy_class:
        logger.warning(f"Strategy '{strategy_name}' not found. Falling back to Standard.")
        return StandardRetrieval()
        
    return strategy_class()
