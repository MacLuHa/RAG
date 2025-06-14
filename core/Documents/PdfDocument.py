from Documents.DocumentInterface import Document
import os
import hashlib
import pickle
from typing import List
from pypdf import PdfReader


class PdfDocument(Document):
    """
    PDF document implementation that extracts and stores text from all pages.
    """
    def __init__(self, path: str, cache_dir: str = '.pdf_cache') -> None:
        """
        Args:
            path (str): Path to the PDF file.
            cache_dir (str): Directory to store cached parsed documents.
        """
        self.path = path
        self.cache_dir = cache_dir
        os.makedirs(self.cache_dir, exist_ok=True)

    def _get_cache_path(self) -> str:
        """Generate unique cache path based on file path."""
        file_hash = hashlib.md5(self.path.encode()).hexdigest()
        return os.path.join(self.cache_dir, f"{file_hash}.pkl")
    
    def _read_pdf(self) -> List[str]:
        """Extracts text from the PDF and returns list of pages."""
        try:
            self.reader = PdfReader(self.path)
        except Exception as error:
            raise RuntimeError(f"Failed to read PDF file '{self.path}': {error}")
        
        return [(page.extract_text() or "").strip() for page in self.reader.pages]


    def get_document(self) -> List[str]:
        """
        Loads document from cache if exists, otherwise reads and caches it.

        Returns:
            List[str]: Text content of PDF pages.
        """
        cache_path = self._get_cache_path()

        if os.path.exists(cache_path):
            try:
                with open(cache_path, 'rb') as f:
                    return pickle.load(f)
            except Exception as error:
                print(f"[Warning] Failed to load cache: {error}")

        content = self._read_pdf()

        try:
            with open(self._get_cache_path(),'wb') as f:
                pickle.dump(content, f)
        except Exception as error:
            print(f"[Warning] Failed to write cache: {error}")

        return content

    def get_filename(self) -> str:
        """Returns the name of the PDF file."""
        return os.path.basename(self.path)

if __name__ == '__main__':
    document = PdfDocument('../examples/Устав внутренней службы ВС РФ.pdf')
    print(document.get_document()[1])
    print(document.get_filename())