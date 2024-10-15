import logging
from .db_manager import DBManager
from .dsl_processor import DSLProcessor
from .example_module import ExampleModule
from .example_function import example_function

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Example usage
if __name__ == "__main__":
    db_manager = DBManager("dsl_database.db")
    processor = DSLProcessor(db_manager)

    # Manually add example_function and ExampleModule to imported_elements
    processor.imported_elements['example_function'] = example_function
    processor.imported_elements['ExampleModule'] = ExampleModule

    # Example: Populate the database with some test data
    with db_manager.conn:
        db_manager.cursor.executemany("INSERT INTO sentences (sentence) VALUES (?)", [
            ("print Hello World",),
            ("add 5 10 15",),
            ("Example Module greet John Doe",),
            ("Example Module Math Operations multiply 2 3 4",),
            ("example function 10 20",),
            ("concatenate Welcome to the DSL world",),
        ])
        db_manager.cursor.executemany("INSERT INTO objects (name, value) VALUES (?, ?)", [
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
