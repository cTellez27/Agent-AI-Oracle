import uuid
from pathlib import Path
from typing import Union, BinaryIO
from pypdf import PdfReader

from src.domain.entities.document import Document, DocumentMetadata
from src.domain.interfaces.parser_interface import BaseParserInterface


class PDFParser(BaseParserInterface):
    """Extractor de texto para archivos PDF."""

    def supports_extension(self, extension: str) -> bool:
        return extension.lower() in [".pdf"]

    def parse(self, file_source: Union[str, Path, BinaryIO], file_name: str, category: str = "General") -> Document:
        try:
            reader = PdfReader(file_source)
            text_pages = []
            
            for i, page in enumerate(reader.pages):
                extracted = page.extract_text()
                if extracted and extracted.strip():
                    text_pages.append(f"--- Página {i + 1} ---\n{extracted.strip()}")

            full_content = "\n\n".join(text_pages) if text_pages else "Documento PDF sin contenido de texto extraíble."
            
            # Obtener tamaño aproximado
            size_bytes = 0
            if isinstance(file_source, (str, Path)):
                size_bytes = Path(file_source).stat().st_size
            elif hasattr(file_source, "seek") and hasattr(file_source, "tell"):
                file_source.seek(0, 2)
                size_bytes = file_source.tell()
                file_source.seek(0)

            metadata = DocumentMetadata(
                file_name=file_name,
                file_type="PDF",
                file_size_bytes=size_bytes,
                category=category,
                additional_info={"num_pages": len(reader.pages)}
            )

            return Document(
                id=str(uuid.uuid4()),
                content=full_content,
                metadata=metadata
            )
        except Exception as e:
            raise ValueError(f"Error al procesar el archivo PDF '{file_name}': {str(e)}")
