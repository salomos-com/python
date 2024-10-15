import logging
from typing import Dict, Any
import inspect
import re
from .db_manager import DBManager

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DSLProcessor:
    def __init__(self, db_path: str):
        self.db_manager = DBManager(db_path)
        self.imported_elements = {}
        self.import_all(globals())

    def import_all(self, global_dict):
        for name, obj in global_dict.items():
            if inspect.isfunction(obj) or inspect.isclass(obj):
                self.imported_elements[name] = obj
            elif inspect.ismodule(obj):
                for subname, subobj in inspect.getmembers(obj):
                    if not subname.startswith("_") and (inspect.isfunction(subobj) or inspect.isclass(subobj)):
                        self.imported_elements[f"{name}{subname}"] = subobj

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
            sentence = self.db_manager.load_sentence()
            if not sentence:
                logger.info("No more sentences to process")
                break

            objects = self.db_manager.load_objects()
            result = self.process_sentence(sentence, objects)
            logger.info(f"Processed: {sentence}")
            logger.info(f"Result: {result}")

            time.sleep(1)  # Wait for 1 second before processing the next sentence

    def close(self):
        self.db_manager.close()
