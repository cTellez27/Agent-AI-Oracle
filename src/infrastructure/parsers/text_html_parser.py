import uuid
import json
from pathlib import Path
from typing import Union, BinaryIO
from bs4 import BeautifulSoup
import markdown

from src.domain.entities.document import Document, DocumentMetadata
from src.domain.interfaces.parser_interface import BaseParserInterface


class TextHTMLParser(BaseParserInterface):
    """Extractor de texto para archivos Markdown (.md), HTML (.html, .htm), JSON (.json) y Texto plano (.txt)."""

    def supports_extension(self, extension: str) -> bool:
        return extension.lower() in [".md", ".markdown", ".html", ".htm", ".json", ".txt"]

    def parse(self, file_source: Union[str, Path, BinaryIO], file_name: str, category: str = "General") -> Document:
        try:
            ext = Path(file_name).suffix.lower()
            raw_content = ""

            if isinstance(file_source, (str, Path)):
                with open(file_source, "r", encoding="utf-8", errors="ignore") as f:
                    raw_content = f.read()
            elif hasattr(file_source, "read"):
                raw_bytes = file_source.read()
                if isinstance(raw_bytes, bytes):
                    raw_content = raw_bytes.decode("utf-8", errors="ignore")
                else:
                    raw_content = str(raw_bytes)

            processed_content = ""

            if ext in [".html", ".htm"]:
                soup = BeautifulSoup(raw_content, "html.parser")
                # Eliminar scripts y estilos
                for script_or_style in soup(["script", "style"]):
                    script_or_style.extract()
                processed_content = soup.get_text(separator="\n").strip()

            elif ext in [".md", ".markdown"]:
                # Convertir markdown a texto plano usando BeautifulSoup sobre el HTML renderizado
                html_rendered = markdown.markdown(raw_content)
                soup = BeautifulSoup(html_rendered, "html.parser")
                processed_content = soup.get_text(separator="\n").strip()

            elif ext == ".json":
                try:
                    data = json.loads(raw_content)
                    processed_content = json.dumps(data, indent=2, ensure_ascii=False)
                except Exception:
                    processed_content = raw_content

            else:  # .txt
                processed_content = raw_content.strip()

            size_bytes = len(raw_content.encode("utf-8"))

            metadata = DocumentMetadata(
                file_name=file_name,
                file_type=ext.upper().replace(".", ""),
                file_size_bytes=size_bytes,
                category=category,
                additional_info={"character_count": len(processed_content)}
            )

            return Document(
                id=str(uuid.uuid4()),
                content=processed_content if processed_content else "Archivo de texto sin contenido válido.",
                metadata=metadata
            )
        except Exception as e:
            raise ValueError(f"Error al procesar el documento de texto/HTML '{file_name}': {str(e)}")
