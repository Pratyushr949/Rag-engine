import json
import logging
from pydantic import BaseModel, Field
from typing import List
from services.llm import LLMService

logger = logging.getLogger(__name__)

class ExtractedEntities(BaseModel):
    persons: List[str] = Field(default_factory=list, description="Names of people")
    organizations: List[str] = Field(default_factory=list, description="Non-company organizations (e.g. NGOs, universities)")
    companies: List[str] = Field(default_factory=list, description="Commercial companies and businesses")
    locations: List[str] = Field(default_factory=list, description="Geographical locations, cities, countries")
    dates: List[str] = Field(default_factory=list, description="Dates and time periods")
    emails: List[str] = Field(default_factory=list, description="Email addresses")
    phones: List[str] = Field(default_factory=list, description="Phone numbers")
    money: List[str] = Field(default_factory=list, description="Monetary values and currencies")
    products: List[str] = Field(default_factory=list, description="Products and services")
    events: List[str] = Field(default_factory=list, description="Events and conferences")

class EntityExtractorService:
    @staticmethod
    def extract_entities(text: str) -> dict:
        llm = LLMService.get_llm()
        
        try:
            structured_llm = llm.with_structured_output(ExtractedEntities)
            result = structured_llm.invoke(f"Extract the requested entities from the text.\n\nText: {text}")
            return result.model_dump()
        except Exception as e:
            logger.warning(f"structured output failed, falling back to JSON format instructions: {e}")
            prompt_str = f"""
            Extract entities from the following text and return them in JSON format.
            The JSON MUST exactly match the following schema:
            {{
                "persons": ["list of strings"],
                "organizations": ["list of strings"],
                "companies": ["list of strings"],
                "locations": ["list of strings"],
                "dates": ["list of strings"],
                "emails": ["list of strings"],
                "phones": ["list of strings"],
                "money": ["list of strings"],
                "products": ["list of strings"],
                "events": ["list of strings"]
            }}
            If no entities are found for a category, use an empty list `[]`.
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
                return json.loads(content)
            except Exception as e_json:
                logger.error(f"Error parsing JSON from LLM: {e_json}")
                return ExtractedEntities().model_dump()
