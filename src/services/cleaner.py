import os
import logging

logger = logging.getLogger(__name__)

class Cleaner:
    """
    Service to clean up files after processing.
    """
    
    @staticmethod
    def remove_file(file_path: str):
        """
        Removes a file from the filesystem.
        """
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"Deleted file: {file_path}")
            else:
                logger.warning(f"File not found for deletion: {file_path}")
        except Exception as e:
            logger.error(f"Error deleting file {file_path}: {e}")
