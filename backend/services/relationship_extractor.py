import json
import logging
from pydantic import BaseModel, Field
from typing import List
from services.llm import LLMService

logger = logging.getLogger(__name__)

class Relationship(BaseModel):
    source_entity: str = Field(description="The source entity in the relationship")
    target_entity: str = Field(description="The target entity in the relationship")
    relationship_type: str = Field(description="The type of relationship (e.g. works_for, located_in, belongs_to, owns, managed_by, created_by, part_of)")

class ExtractedRelationships(BaseModel):
    relationships: List[Relationship] = Field(default_factory=list, description="List of extracted relationships")

class RelationshipExtractorService:
    @staticmethod
    def extract_relationships(text: str, entities: dict = None) -> List[dict]:
        llm = LLMService.get_llm()
        
        entities_context = ""
        if entities:
            entities_context = f"\n\nContext - Extracted Entities:\n{json.dumps(entities, indent=2)}\n"
            
        prompt = f"""
        Extract relationships between entities in the following text.
        Focus on relationships like: works_for, located_in, belongs_to, owns, managed_by, created_by, part_of.
        {entities_context}
        Text: {text}
        """
        
        try:
            structured_llm = llm.with_structured_output(ExtractedRelationships)
            result = structured_llm.invoke(prompt)
            return [rel.model_dump() for rel in result.relationships]
        except Exception as e:
            logger.warning(f"structured output failed for relationships, falling back to JSON format instructions: {e}")
            prompt_str = f"""
            Extract relationships between entities from the following text and return them in JSON format.
            Focus on relationships like: works_for, located_in, belongs_to, owns, managed_by, created_by, part_of.
            {entities_context}
            
            The JSON MUST exactly match the following schema:
            {{
                "relationships": [
                    {{
                        "source_entity": "string",
                        "target_entity": "string",
                        "relationship_type": "string"
                    }}
                ]
            }}
            If no relationships are found, return {{"relationships": []}}.
            Do NOT include any additional markdown formatting. Return purely the JSON object.
            
            Text:
            {text}
            """
            
            try:
                response = llm.invoke(prompt_str)
                content = response.content.strip()
                if content.startswith("```json"):
                    content = content[7:-3].strip()
                elif content.startswith("```"):
                    content = content[3:-3].strip()
                
                parsed_json = json.loads(content)
                return parsed_json.get("relationships", [])
            except Exception as e_json:
                logger.error(f"Error parsing JSON from LLM for relationships: {e_json}")
                return []
