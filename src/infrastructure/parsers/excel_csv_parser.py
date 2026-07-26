import uuid
import io
import pandas as pd
from pathlib import Path
from typing import Union, BinaryIO

from src.domain.entities.document import Document, DocumentMetadata
from src.domain.interfaces.parser_interface import BaseParserInterface


class ExcelCSVParser(BaseParserInterface):
    """Extractor de datos para tablas en Excel (.xlsx, .xls) y CSV (.csv)."""

    def supports_extension(self, extension: str) -> bool:
        return extension.lower() in [".xlsx", ".xls", ".csv"]

    def parse(self, file_source: Union[str, Path, BinaryIO], file_name: str, category: str = "General") -> Document:
        try:
            ext = Path(file_name).suffix.lower()
            formatted_texts = []
            num_sheets_or_tables = 1

            if ext == ".csv":
                # Intentar lectura con fallbacks de codificación
                try:
                    df = pd.read_csv(file_source, encoding="utf-8")
                except UnicodeDecodeError:
                    if hasattr(file_source, "seek"):
                        file_source.seek(0)
                    df = pd.read_csv(file_source, encoding="latin1")

                formatted_texts.append(self._format_dataframe_to_text(df, sheet_name="Hoja Única"))

            else:  # .xlsx / .xls
                excel_file = pd.ExcelFile(file_source)
                num_sheets_or_tables = len(excel_file.sheet_names)
                for sheet_name in excel_file.sheet_names:
                    df = pd.read_excel(excel_file, sheet_name=sheet_name)
                    if not df.empty:
                        formatted_texts.append(self._format_dataframe_to_text(df, sheet_name=sheet_name))

            full_content = "\n\n".join(formatted_texts) if formatted_texts else "Tabla sin datos válidos."

            size_bytes = 0
            if isinstance(file_source, (str, Path)):
                size_bytes = Path(file_source).stat().st_size
            elif hasattr(file_source, "seek") and hasattr(file_source, "tell"):
                file_source.seek(0, 2)
                size_bytes = file_source.tell()
                file_source.seek(0)

            metadata = DocumentMetadata(
                file_name=file_name,
                file_type=ext.upper().replace(".", ""),
                file_size_bytes=size_bytes,
                category=category,
                additional_info={"num_sheets": num_sheets_or_tables}
            )

            return Document(
                id=str(uuid.uuid4()),
                content=full_content,
                metadata=metadata
            )
        except Exception as e:
            raise ValueError(f"Error al procesar la tabla/hoja de cálculo '{file_name}': {str(e)}")

    def _format_dataframe_to_text(self, df: pd.DataFrame, sheet_name: str) -> str:
        lines = [f"=== Hoja: {sheet_name} ==="]
        # Limpiar filas completamente nulas
        df_clean = df.dropna(how="all").fillna("")
        
        for idx, row in df_clean.iterrows():
            row_items = [f"{col}: {val}" for col, val in row.items() if str(val).strip() != ""]
            if row_items:
                lines.append(f"Fila {idx + 1}: " + " | ".join(row_items))
                
        return "\n".join(lines)
