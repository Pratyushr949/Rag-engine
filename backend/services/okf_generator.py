import datetime
from utils.logger import get_logger
from services.knowledge_storage import KnowledgeStorageService

logger = get_logger(__name__)

class OKFGeneratorService:
    @staticmethod
    def generate_and_store(
        filename: str,
        entities: dict, 
        relationships: list, 
        document_info: dict
    ):
        """
        Combines Entities, Relationships, Metadata, and Document Information 
        into an Open Knowledge Format (OKF) JSON and stores it.
        """
        try:
            okf_data = {
                "document_info": document_info,
                "metadata": {
                    "generated_at": datetime.datetime.utcnow().isoformat() + "Z",
                    "generator": "OKFGeneratorService",
                    "format_version": "1.0"
                },
                "knowledge_graph": {
                    "entities": entities,
                    "relationships": relationships
                }
            }
            
            # Save using KnowledgeStorageService
            okf_filepath = KnowledgeStorageService.save_okf(filename, okf_data)
            
            logger.info(f"Generated and saved OKF file for: {filename}")
            return okf_filepath
        except Exception as e:
            logger.error(f"Error generating OKF file for {filename}: {e}")
            return None
