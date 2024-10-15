import sqlite3
import time
import logging
from typing import Dict, Any
import importlib
import inspect
import re

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Example module with functions and classes to import
class ExampleModule:
    @staticmethod
    def greet(name):
        return f"Hello, {name}!"

    class MathOperations:
        @staticmethod
        def multiply(*args):
            result = 1
            for arg in args:
                result *= float(arg)
            return result

def example_function(x, y):
    return x + y

class DSLProcessor:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.init_database()
        self.imported_elements = {}
        self.import_all(globals())

    def init_database(self):
        # Create sentences table
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS sentences (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sentence TEXT NOT NULL,
            processed BOOLEAN DEFAULT 0
        )
        ''')

        # Create objects table
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS objects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            value TEXT NOT NULL
        )
        ''')

        self.conn.commit()

    def import_all(self, global_dict):
        for name, obj in global_dict.items():
            if inspect.isfunction(obj) or inspect.isclass(obj):
                self.imported_elements[name] = obj
            elif inspect.ismodule(obj):
                for subname, subobj in inspect.getmembers(obj):
                    if not subname.startswith("_") and (inspect.isfunction(subobj) or inspect.isclass(subobj)):
                        self.imported_elements[f"{name}{subname}"] = subobj

    def load_sentence(self) -> str:
        self.cursor.execute("SELECT id, sentence FROM sentences WHERE processed = 0 LIMIT 1")
        result = self.cursor.fetchone()
        if result:
            self.cursor.execute("UPDATE sentences SET processed = 1 WHERE id = ?", (result[0],))
            self.conn.commit()
            return result[1]
        return ""

    def load_objects(self) -> Dict[str, Any]:
        self.cursor.execute("SELECT name, value FROM objects")
        return {row[0]: eval(row[1]) for row in self.cursor.fetchall()}

    def resolve_class_name(self, name: str) -> str:
        """Convert space-separated words to CamelCase."""
        return ''.join(word.capitalize() for word in name.split())

    def find_matching_element(self, name: str) -> Any:
        """Find matching element in imported_elements using fuzzy matching."""
        camel_case_name = self.resolve_class_name(name)
        for key, value in self.imported_elements.items():
            if key.lower() == camel_case_name.lower():
                return value
        return None

    def process_sentence(self, sentence: str, objects: Dict[str, Any]) -> Any:
        # Convert underscores and dots to spaces in the entire sentence
        sentence = re.sub(r'[_.]', ' ', sentence)
        parts = sentence.split()
        if not parts:
            return None

        # Separate method path and parameters
        method_path = []
        params = []
        for part in parts:
            if self.find_matching_element(' '.join(method_path + [part])):
                method_path.append(part)
            else:
                params = parts[len(method_path):]
                break

        # Replace parameter names with actual object values
        params = [objects.get(param, param) for param in params]

        # Navigate through the method path
        current_obj = self
        current_path = []
        for part in method_path:
            current_path.append(part)
            matched_obj = self.find_matching_element(' '.join(current_path))
            if matched_obj:
                current_obj = matched_obj
                current_path = []
            elif hasattr(current_obj, part):
                current_obj = getattr(current_obj, part)
            else:
                logger.warning(f"Method or attribute {' '.join(current_path + [part])} not found")
                return None

        # Call the method if it's callable
        if callable(current_obj):
            return current_obj(*params)
        else:
            logger.warning(f"{' '.join(method_path)} is not callable")
            return None

    # Example DSL methods
    def print(self, *args):
        logger.info(" ".join(str(arg) for arg in args))

    def add(self, *args):
        return sum(float(arg) for arg in args)

    def concatenate(self, *args):
        return " ".join(str(arg) for arg in args)

    def run(self):
        while True:
            sentence = self.load_sentence()
            if not sentence:
                logger.info("No more sentences to process")
                break

            objects = self.load_objects()
            result = self.process_sentence(sentence, objects)
            logger.info(f"Processed: {sentence}")
            logger.info(f"Result: {result}")

            time.sleep(1)  # Wait for 1 second before processing the next sentence

    def close(self):
        self.conn.close()

# Example usage
if __name__ == "__main__":
    processor = DSLProcessor("dsl_database.db")

    # Example: Populate the database with some test data
    with processor.conn:
        processor.cursor.executemany("INSERT INTO sentences (sentence) VALUES (?)", [
            ("print Hello World",),
            ("add 5 10 15",),
            ("Example Module greet John Doe",),
            ("Example Module Math Operations multiply 2 3 4",),
            ("example function 10 20",),
            ("concatenate Welcome to the DSL world",),
        ])
        processor.cursor.executemany("INSERT INTO objects (name, value) VALUES (?, ?)", [
            ("greeting", "'Hello'"),
            ("number", "42"),
            ("pi", "3.14159"),
        ])

    try:
        processor.run()
    except KeyboardInterrupt:
        logger.info("Process interrupted by user")
    finally:
        processor.close()