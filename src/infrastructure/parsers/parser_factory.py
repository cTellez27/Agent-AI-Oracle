from pathlib import Path
from typing import List, Union, BinaryIO

from src.domain.entities.document import Document
from src.domain.interfaces.parser_interface import BaseParserInterface
from src.infrastructure.parsers.pdf_parser import PDFParser
from src.infrastructure.parsers.docx_parser import DocxParser
from src.infrastructure.parsers.excel_csv_parser import ExcelCSVParser
from src.infrastructure.parsers.pptx_parser import PPTXParser
from src.infrastructure.parsers.text_html_parser import TextHTMLParser


class IngestionParserFactory:
    """Fábrica y fachada para seleccionar e invocar el extractor adecuado para los 8 formatos."""

    def __init__(self):
        self._parsers: List[BaseParserInterface] = [
            PDFParser(),
            DocxParser(),
            ExcelCSVParser(),
            PPTXParser(),
            TextHTMLParser()
        ]

    def get_parser_for_file(self, file_name: str) -> BaseParserInterface:
        ext = Path(file_name).suffix.lower()
        for parser in self._parsers:
            if parser.supports_extension(ext):
                return parser
        raise ValueError(f"Extensión de archivo '{ext}' no soportada. Formatos válidos: PDF, DOCX, XLSX, CSV, PPTX, MD, JSON, HTML, TXT.")

    def parse_document(self, file_source: Union[str, Path, BinaryIO], file_name: str, category: str = "General") -> Document:
        parser = self.get_parser_for_file(file_name)
        return parser.parse(file_source=file_source, file_name=file_name, category=category)
