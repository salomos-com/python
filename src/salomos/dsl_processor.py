import logging
from typing import Dict, Any
import inspect
import re

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DSLProcessor:
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.imported_elements = {}
        self.import_all(globals())
        logger.info(f"Imported elements: {self.imported_elements}")

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
        logger.info(f"Searching for element: {name}")
        
        # First, try a direct match
        if name in self.imported_elements:
            return self.imported_elements[name]
        
        # If no direct match, try CamelCase conversion
        camel_case_name = self.resolve_class_name(name)
        for key, value in self.imported_elements.items():
            logger.info(f"Comparing with: {key}")
            if key.lower() == camel_case_name.lower():
                return value
        return None

    def process_sentence(self, sentence: str, objects: Dict[str, Any]) -> Any:
        # Convert underscores and dots to spaces in the entire sentence
        sentence = re.sub(r'[_.]', ' ', sentence)
        parts = sentence.split()
        if not parts:
            return None

        # First, check if the entire sentence matches a standalone function
        standalone_func = self.find_matching_element(' '.join(parts))
        if standalone_func and inspect.isfunction(standalone_func):
            # Replace parameter names with actual object values
            params = [objects.get(param, param) for param in parts[1:]]
            return standalone_func(*params)

        # If not a standalone function, separate method path and parameters
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

        # Find the matching element for the full method path
        element = self.find_matching_element(' '.join(method_path))

        if not element:
            logger.warning(f"Element {' '.join(method_path)} not found")
            return None

        # If the element is a class, instantiate it and navigate to the method
        if inspect.isclass(element):
            instance = element()
            current_obj = instance
            
            for part in method_path[1:]:  # Skip the class name
                if hasattr(current_obj, part):
                    current_obj = getattr(current_obj, part)
                else:
                    logger.warning(f"Method or attribute {part} not found on {current_obj}")
                    return None

            # Call the method if it's callable
            if callable(current_obj):
                return current_obj(*params)
            else:
                logger.warning(f"{'.'.join(method_path)} is not callable")
                return None
        else:
            logger.warning(f"{' '.join(method_path)} is not a class")
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
