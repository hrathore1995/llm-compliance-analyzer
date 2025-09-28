from abc import ABC, abstractmethod
from pathlib import Path
from typing import Union

from docx import Document
from PyPDF2 import PdfReader


class BaseExtractor(ABC):
    """Abstract base class for all extractors."""

    @abstractmethod
    def extract(self, file_path: Union[str, Path]) -> str:
        """Extract raw text from a file."""


class PDFExtractor(BaseExtractor):
    """Extract text from PDF files."""

    def extract(self, file_path: Union[str, Path]) -> str:
        reader = PdfReader(str(file_path))
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text


class DocxExtractor(BaseExtractor):
    """Extract text from DOCX files."""

    def extract(self, file_path: Union[str, Path]) -> str:
        doc = Document(str(file_path))
        return "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
