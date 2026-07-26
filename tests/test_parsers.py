import os
import unittest
from pathlib import Path
from src.infrastructure.parsers.parser_factory import IngestionParserFactory
from src.domain.entities.document import Document


class TestParsers(unittest.TestCase):
    def setUp(self):
        self.factory = IngestionParserFactory()

    def test_factory_supports_extensions(self):
        extensions = [".pdf", ".docx", ".xlsx", ".csv", ".pptx", ".md", ".json", ".html", ".txt"]
        for ext in extensions:
            parser = self.factory.get_parser_for_file(f"test_file{ext}")
            self.assertIsNotNone(parser)

    def test_text_html_parser_markdown(self):
        md_content = "# Título Corporativo\n\nEste es un documento de prueba para RH."
        test_path = Path("test_doc.md")
        with open(test_path, "w", encoding="utf-8") as f:
            f.write(md_content)

        try:
            doc: Document = self.factory.parse_document(test_path, "test_doc.md", category="RH")
            self.assertEqual(doc.metadata.file_type, "MD")
            self.assertEqual(doc.metadata.category, "RH")
            self.assertIn("Título Corporativo", doc.content)
        finally:
            if test_path.exists():
                os.remove(test_path)

    def test_text_html_parser_json(self):
        json_content = '{"empresa": "Oracle", "area": "Finanzas", "presupuesto": 50000}'
        test_path = Path("test_doc.json")
        with open(test_path, "w", encoding="utf-8") as f:
            f.write(json_content)

        try:
            doc: Document = self.factory.parse_document(test_path, "test_doc.json", category="Finanzas")
            self.assertEqual(doc.metadata.file_type, "JSON")
            self.assertIn("presupuesto", doc.content)
        finally:
            if test_path.exists():
                os.remove(test_path)


if __name__ == "__main__":
    unittest.main()
