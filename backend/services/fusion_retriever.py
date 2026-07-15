from typing import List
from langchain_core.documents import Document
from services.knowledge_storage import KnowledgeStorageService
from utils.logger import get_logger

logger = get_logger(__name__)

class FusionRetrieverService:
    @staticmethod
    def get_fused_context(
        search_question: str, 
        vector_docs: List[Document]
    ) -> dict:
        """
        Implements Hybrid Context Builder by combining Vector Retrieval with Knowledge Retrieval.
        Applies deduplication and a basic ranking strategy.
        Returns a list of string contexts to be sent to Gemini.
        """
        logger.info("Starting Fusion Retrieval...")
        
        # 1. Extract vector contents
        vector_contents = [doc.page_content for doc in vector_docs]
        
        # 2. Knowledge Retrieval
        # Extract keywords from the question to search the OKF files
        # A simple split by space, ignoring common stop words, or just searching the whole question
        # For better recall with simple text search, we'll search by words > 4 chars
        words = [w.lower() for w in search_question.split() if len(w) > 4]
        if not words:
            words = [search_question.lower()]
            
        knowledge_results = []
        for word in words:
            results = KnowledgeStorageService.search_okf(word)
            knowledge_results.extend(results)
            
        # Extract meaningful text from OKF graphs
        knowledge_texts = []
        for okf in knowledge_results:
            kg = okf.get("knowledge_graph", {})
            for rel in kg.get("relationships", []):
                source = rel.get('source_entity', '')
                target = rel.get('target_entity', '')
                rel_type = rel.get('relationship_type', '')
                if source and target and rel_type:
                    knowledge_texts.append(f"Knowledge Graph Fact: {source} {rel_type} {target}")
            
            entities = kg.get("entities", {})
            for ent_type, values in entities.items():
                if values:
                    knowledge_texts.append(f"Entity Type '{ent_type}': {', '.join(values)}")

        # 3. Deduplication
        unique_contexts = set(vector_contents + knowledge_texts)
        merged_context = list(unique_contexts)
        
        # 4. Ranking
        # Simple ranking heuristic: prioritize knowledge graph facts, then vector docs
        # We give a slight boost to shorter facts as they are more concise
        def rank_score(item: str) -> float:
            score = 0.0
            if item.startswith("Knowledge Graph Fact:"):
                score += 100.0
            elif item.startswith("Entity Type"):
                score += 50.0
            else:
                score += 10.0 # Standard vector content
            
            # Penalize slightly by length to prefer concise facts at the top
            score -= (len(item) * 0.001)
            return score
            
        merged_context.sort(key=rank_score, reverse=True)
        
        logger.info(f"Fusion complete: {len(vector_contents)} vector docs + {len(knowledge_texts)} knowledge items -> {len(merged_context)} merged items")
        return {
            "merged_context": merged_context,
            "vector_chunks": list(set(vector_contents)),
            "knowledge_facts": list(set(knowledge_texts))
        }
