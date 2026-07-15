from fastapi import APIRouter, HTTPException, Path
from typing import Dict, Any, List
from services.knowledge_storage import KnowledgeStorageService
from utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter()

@router.get(
    "/knowledge/global", 
    response_model=Dict[str, Any],
    summary="Get Global Knowledge Graph",
    description="Merges all Open Knowledge Format (OKF) JSON files into a unified knowledge graph."
)
async def get_global_knowledge():
    """
    Returns a unified OKF-like JSON structure where all entities and relationships across all documents are merged.
    """
    all_okf = KnowledgeStorageService.get_all_okf()
    
    merged_entities = {}
    merged_relationships = []
    
    # Track unique relationships to avoid exact duplicates
    seen_rels = set()
    
    for okf in all_okf:
        kg = okf.get("knowledge_graph", {})
        
        # Merge entities
        entities = kg.get("entities", {})
        for ent_type, values in entities.items():
            if ent_type not in merged_entities:
                merged_entities[ent_type] = []
            # Append only unique
            for val in values:
                if val not in merged_entities[ent_type]:
                    merged_entities[ent_type].append(val)
                    
        # Merge relationships
        relationships = kg.get("relationships", [])
        for rel in relationships:
            rel_tuple = (rel.get("source_entity"), rel.get("target_entity"), rel.get("relationship_type"))
            if rel_tuple not in seen_rels:
                seen_rels.add(rel_tuple)
                merged_relationships.append(rel)
                
    return {
        "knowledge_graph": {
            "entities": merged_entities,
            "relationships": merged_relationships
        },
        "documents_merged": len(all_okf)
    }

@router.get(
    "/knowledge/{document}", 
    response_model=Dict[str, Any],
    summary="Get Full OKF Document",
    description="Retrieves the entire Open Knowledge Format (OKF) JSON file for a given document."
)
async def get_knowledge(
    document: str = Path(..., description="The filename of the uploaded document (with or without extension)")
):
    """
    Returns the complete OKF JSON structure including metadata, document info, and the knowledge graph.
    """
    okf_data = KnowledgeStorageService.load_okf(document)
    if not okf_data:
        raise HTTPException(status_code=404, detail=f"Knowledge file for document '{document}' not found.")
    return okf_data

@router.get(
    "/entities/{document}", 
    response_model=Dict[str, List[str]],
    summary="Get Entities",
    description="Retrieves only the extracted entities for a given document."
)
async def get_entities(
    document: str = Path(..., description="The filename of the uploaded document (with or without extension)")
):
    """
    Extracts and returns just the entities from the document's knowledge graph.
    """
    okf_data = KnowledgeStorageService.load_okf(document)
    if not okf_data:
        raise HTTPException(status_code=404, detail=f"Knowledge file for document '{document}' not found.")
        
    kg = okf_data.get("knowledge_graph", {})
    return kg.get("entities", {})

@router.get(
    "/relationships/{document}", 
    response_model=List[Dict[str, str]],
    summary="Get Relationships",
    description="Retrieves only the extracted relationships for a given document."
)
async def get_relationships(
    document: str = Path(..., description="The filename of the uploaded document (with or without extension)")
):
    """
    Extracts and returns just the relationships from the document's knowledge graph.
    """
    okf_data = KnowledgeStorageService.load_okf(document)
    if not okf_data:
        raise HTTPException(status_code=404, detail=f"Knowledge file for document '{document}' not found.")
        
    kg = okf_data.get("knowledge_graph", {})
    return kg.get("relationships", [])

@router.get(
    "/graph/{document}", 
    response_model=Dict[str, Any],
    summary="Get Knowledge Graph",
    description="Retrieves the knowledge graph (both entities and relationships) for a given document."
)
async def get_graph(
    document: str = Path(..., description="The filename of the uploaded document (with or without extension)")
):
    """
    Extracts and returns the knowledge graph section containing both entities and relationships.
    """
    okf_data = KnowledgeStorageService.load_okf(document)
    if not okf_data:
        raise HTTPException(status_code=404, detail=f"Knowledge file for document '{document}' not found.")
        
    return okf_data.get("knowledge_graph", {})
