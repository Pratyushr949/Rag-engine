import os
import json
import glob
from utils.logger import get_logger

logger = get_logger(__name__)

class KnowledgeStorageService:
    STORAGE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "knowledge_store")

    @classmethod
    def _ensure_storage_dir(cls):
        os.makedirs(cls.STORAGE_DIR, exist_ok=True)

    @classmethod
    def _get_filepath(cls, filename: str) -> str:
        base_filename = os.path.splitext(os.path.basename(filename))[0]
        okf_filename = f"{base_filename}.okf.json"
        return os.path.join(cls.STORAGE_DIR, okf_filename)

    @classmethod
    def save_okf(cls, filename: str, okf_data: dict) -> str:
        cls._ensure_storage_dir()
        filepath = cls._get_filepath(filename)
        
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(okf_data, f, indent=4, ensure_ascii=False)
            logger.info(f"Saved OKF file successfully: {filepath}")
            return filepath
        except Exception as e:
            logger.error(f"Failed to save OKF for {filename}: {e}")
            raise

    @classmethod
    def load_okf(cls, filename: str) -> dict:
        filepath = cls._get_filepath(filename)
        if not os.path.exists(filepath):
            logger.warning(f"OKF file not found: {filepath}")
            return {}
            
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
            logger.info(f"Loaded OKF file: {filepath}")
            return data
        except Exception as e:
            logger.error(f"Failed to load OKF for {filename}: {e}")
            raise

    @classmethod
    def delete_okf(cls, filename: str) -> bool:
        filepath = cls._get_filepath(filename)
        if os.path.exists(filepath):
            try:
                os.remove(filepath)
                logger.info(f"Deleted OKF file: {filepath}")
                return True
            except Exception as e:
                logger.error(f"Failed to delete OKF for {filename}: {e}")
                return False
        logger.warning(f"OKF file not found for deletion: {filepath}")
        return False

    @classmethod
    def search_okf(cls, query: str) -> list:
        """
        Searches all OKF files in the knowledge_store for the given query string.
        Returns a list of matching OKF data dictionaries.
        """
        cls._ensure_storage_dir()
        query = query.lower()
        results = []
        
        try:
            search_pattern = os.path.join(cls.STORAGE_DIR, "*.okf.json")
            for filepath in glob.glob(search_pattern):
                with open(filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    
                # Simple string matching across the serialized JSON
                data_str = json.dumps(data).lower()
                if query in data_str:
                    results.append(data)
                    
            logger.info(f"Search OKF for '{query}' returned {len(results)} results")
            return results
        except Exception as e:
            logger.error(f"Error searching OKF files: {e}")
            return []

    @classmethod
    def get_all_okf(cls) -> list:
        """
        Retrieves all OKF files in the knowledge_store.
        """
        cls._ensure_storage_dir()
        results = []
        try:
            search_pattern = os.path.join(cls.STORAGE_DIR, "*.okf.json")
            for filepath in glob.glob(search_pattern):
                with open(filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    results.append(data)
            logger.info(f"Loaded {len(results)} OKF files from global store.")
            return results
        except Exception as e:
            logger.error(f"Error loading all OKF files: {e}")
            return []
