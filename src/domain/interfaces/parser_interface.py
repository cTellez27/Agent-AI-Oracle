from abc import ABC, abstractmethod
from typing import BinaryIO, Union
from pathlib import Path
from src.domain.entities.document import Document


class BaseParserInterface(ABC):
    """Contrato base para extractores de texto multiformato."""

    @abstractmethod
    def parse(self, file_source: Union[str, Path, BinaryIO], file_name: str, category: str = "General") -> Document:
        """Extrae el texto y metadatos de un archivo."""
        pass

    @abstractmethod
    def supports_extension(self, extension: str) -> bool:
        """Verifica si la extensión del archivo es soportada por el parser."""
        pass
