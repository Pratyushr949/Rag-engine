import networkx as nx
from fastapi import APIRouter, HTTPException, Path
from typing import Dict, Any
from services.knowledge_storage import KnowledgeStorageService
from utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter()

@router.get(
    "/network/global", 
    response_model=Dict[str, Any],
    summary="Get Global Network Graph Data",
    description="Loads all knowledge graphs, merges them into a unified graph, and returns node-link data."
)
async def get_global_network():
    all_okf = KnowledgeStorageService.get_all_okf()
    
    G = nx.DiGraph()
    node_metadata = {}
    
    for okf_data in all_okf:
        kg = okf_data.get("knowledge_graph", {})
        entities = kg.get("entities", {})
        relationships = kg.get("relationships", [])
        
        # Merge entities
        for ent_type, values in entities.items():
            for val in values:
                if val not in node_metadata:
                    node_metadata[val] = {"id": val, "type": ent_type}
        
        # Merge edges
        for rel in relationships:
            source = rel.get("source_entity")
            target = rel.get("target_entity")
            rel_type = rel.get("relationship_type")
            
            if source and target:
                if not G.has_node(source):
                    # Add directly to graph with Unknown if not in entities
                    G.add_node(source, id=source, type="Unknown")
                if not G.has_node(target):
                    G.add_node(target, id=target, type="Unknown")
                G.add_edge(source, target, label=rel_type)

    # Add metadata nodes to graph
    for node_id, metadata in node_metadata.items():
        if not G.has_node(node_id):
            G.add_node(node_id, **metadata)
        else:
            # Update attributes if it was added as Unknown
            nx.set_node_attributes(G, {node_id: metadata})
            
    # Calculate degree centrality for node sizing
    try:
        if len(G) > 0:
            centrality = nx.degree_centrality(G)
            nx.set_node_attributes(G, centrality, "val")
    except Exception as e:
        logger.warning(f"Could not calculate global centrality: {e}")
        
    return nx.node_link_data(G)

@router.get(
    "/network/{document}", 
    response_model=Dict[str, Any],
    summary="Get Network Graph Data",
    description="Loads the document's knowledge graph and returns a node-link data format suitable for visualization."
)
async def get_network(
    document: str = Path(..., description="The filename of the uploaded document")
):
    okf_data = KnowledgeStorageService.load_okf(document)
    if not okf_data:
        raise HTTPException(status_code=404, detail=f"Knowledge file for document '{document}' not found.")
        
    kg = okf_data.get("knowledge_graph", {})
    entities = kg.get("entities", {})
    relationships = kg.get("relationships", [])
    
    # Build NetworkX graph
    G = nx.DiGraph()
    
    # We want each entity to be a node.
    # First, let's collect all unique entities from relationships
    node_metadata = {}
    
    # Also add entities from the 'entities' mapping
    for ent_type, values in entities.items():
        for val in values:
            if val not in node_metadata:
                node_metadata[val] = {"id": val, "type": ent_type}
    
    # Add nodes to graph
    for node_id, metadata in node_metadata.items():
        G.add_node(node_id, **metadata)
        
    # Add edges
    for rel in relationships:
        source = rel.get("source_entity")
        target = rel.get("target_entity")
        rel_type = rel.get("relationship_type")
        
        if source and target:
            # Ensure nodes exist even if they weren't in the entities mapping
            if not G.has_node(source):
                G.add_node(source, id=source, type="Unknown")
            if not G.has_node(target):
                G.add_node(target, id=target, type="Unknown")
                
            G.add_edge(source, target, label=rel_type)
            
    # Calculate degree centrality for node sizing
    try:
        centrality = nx.degree_centrality(G)
        nx.set_node_attributes(G, centrality, "val") # 'val' is often used by react-force-graph for size
    except Exception as e:
        logger.warning(f"Could not calculate centrality: {e}")
        
    # Export as node-link data
    data = nx.node_link_data(G)
    return data
