import unittest
import sqlite3
from src.salomos.dsl_processor import DSLProcessor
from src.salomos.example_module import ExampleModule

class TestDSLProcessor(unittest.TestCase):
    def setUp(self):
        self.processor = DSLProcessor(":memory:")  # Use in-memory database for testing

    def tearDown(self):
        self.processor.close()

    def test_init_database(self):
        # Check if tables are created
        tables = self.processor.db_manager.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
        table_names = [table[0] for table in tables]
        self.assertIn('sentences', table_names)
        self.assertIn('objects', table_names)

    def test_load_sentence(self):
        # Insert a test sentence
        self.processor.db_manager.cursor.execute("INSERT INTO sentences (sentence) VALUES (?)", ("test sentence",))
        self.processor.db_manager.conn.commit()

        # Test loading the sentence
        sentence = self.processor.db_manager.load_sentence()
        self.assertEqual(sentence, "test sentence")

        # Check if the sentence is marked as processed
        processed = self.processor.db_manager.cursor.execute("SELECT processed FROM sentences WHERE sentence = ?", ("test sentence",)).fetchone()[0]
        self.assertEqual(processed, 1)

    def test_load_objects(self):
        # Insert test objects
        test_objects = [("obj1", "'value1'"), ("obj2", "42")]
        self.processor.db_manager.cursor.executemany("INSERT INTO objects (name, value) VALUES (?, ?)", test_objects)
        self.processor.db_manager.conn.commit()

        # Test loading objects
        objects = self.processor.db_manager.load_objects()
        self.assertEqual(objects, {"obj1": "value1", "obj2": 42})

    def test_resolve_class_name(self):
        self.assertEqual(self.processor.resolve_class_name("example module"), "ExampleModule")
        self.assertEqual(self.processor.resolve_class_name("math operations"), "MathOperations")

    def test_find_matching_element(self):
        self.assertIsNotNone(self.processor.find_matching_element("Example Module"))
        self.assertIsNotNone(self.processor.find_matching_element("example function"))
        self.assertIsNone(self.processor.find_matching_element("non existent function"))

    def test_process_sentence(self):
        # Test built-in method
        result = self.processor.process_sentence("add 5 10 15", {})
        self.assertEqual(result, 30)

        # Test imported function
        result = self.processor.process_sentence("example function 10 20", {})
        self.assertEqual(result, 30)

        # Test class method
        result = self.processor.process_sentence("Example Module greet John", {})
        self.assertEqual(result, "Hello, John!")

        # Test nested class method
        result = self.processor.process_sentence("Example Module Math Operations multiply 2 3 4", {})
        self.assertEqual(result, 24)

    def test_dsl_methods(self):
        self.assertEqual(self.processor.add(1, 2, 3), 6)
        self.assertEqual(self.processor.concatenate("Hello", "World"), "Hello World")

if __name__ == '__main__':
    unittest.main()
