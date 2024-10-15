# Salomos

Salomos is a Python package that provides utilities for processing domain-specific languages (DSLs) and managing associated data.

## Installation

To install Salomos, simply run:

```
pip install salomos
```

## Key Components

### DBManager

The `DBManager` class (`db_manager.py`) handles database operations for the Salomos package. It provides methods to:

- Initialize the database
- Load sentences and objects from the database
- Close the database connection

### DSLProcessor 

The `DSLProcessor` class (`dsl_processor.py`) is responsible for processing DSL sentences. It offers functionality to:

- Import modules and resolve class names
- Find matching elements based on a name
- Process a DSL sentence and execute corresponding actions
- Perform operations like print, add, concatenate

## Usage Example

Here's a basic example of how to use the Salomos package:

```python
from salomos.db_manager import DBManager
from salomos.dsl_processor import DSLProcessor
from dotenv import load_dotenv
import os

load_dotenv()

# Get the logger level from environment variable
LOGGER_LEVEL = os.getenv("LOGGER_LEVEL", "INFO")

# Initialize the database manager
db = DBManager("path/to/database.db")
db.init_database()

# Create a DSL processor instance
processor = DSLProcessor(db)

# Load a DSL sentence and objects from the database
sentence = db.load_sentence()
objects = db.load_objects()

# Process the DSL sentence
result = processor.process_sentence(sentence, objects)

# Print the result
processor.print(result)

# Close the database connection
db.close()
```

This example demonstrates the typical workflow of using Salomos:

1. Load environment variables from a `.env` file using `load_dotenv()`.

2. Get the logger level from the `LOGGER_LEVEL` environment variable, defaulting to "INFO" if not set.

3. Initialize a `DBManager` with the path to your database file and call `init_database()`.

4. Create a `DSLProcessor` instance, passing it the database manager. 

5. Load a DSL sentence and any associated objects from the database using the `load_sentence()` and `load_objects()` methods of the database manager.

6. Process the loaded sentence using the `process_sentence()` method of the DSL processor, passing the sentence and objects. This returns the result of executing the sentence.

7. Use the `print()` method of the DSL processor to display the result.

8. Close the database connection when finished using the `close()` method of the database manager.

## Running the Example Script

The `salomos.py` script provides an example of how to use the Salomos package. It demonstrates:

1. Creating instances of `DBManager` and `DSLProcessor`
2. Manually adding example functions and modules to the `imported_elements` of the processor
3. Populating the database with test data (DSL sentences and objects)
4. Running the processor to execute the DSL sentences
5. Handling keyboard interrupts and closing the database connection

To run the example script from the command line:

1. Ensure you have installed the Salomos package and its dependencies
2. Open a terminal or command prompt
3. Navigate to the directory containing `salomos.py`
4. Run the script using the command:

   ```
   python salomos.py
   ```

   Optionally, you can provide the path to a custom database file as a command-line argument:

   ```
   python salomos.py path/to/custom_database.db
   ```

   If no database file is specified, it will default to "dsl_database.db" in the current directory.

The script will process the test DSL sentences from the specified database and print the results. You can modify the test data or add your own DSL sentences and objects to experiment with the package.

Press `Ctrl+C` to interrupt the script and exit.

## Example DSL Sentences and Executed Functions/Methods/Classes

The `salomos.py` script populates the database with some test DSL sentences. Here's a table showing the example sentences and the corresponding functions, methods, or classes that are executed:

| DSL Sentence                                | Executed Function/Method/Class                                 |
|---------------------------------------------|----------------------------------------------------------------|
| print Hello World                           | `DSLProcessor.print("Hello", "World")`                         |
| add 5 10 15                                 | `DSLProcessor.add(5, 10, 15)`                                  |
| Example Module greet John Doe               | `ExampleModule.greet("John", "Doe")`                           |
| Example Module Math Operations multiply 2 3 4 | `ExampleModule.MathOperations.multiply(2, 3, 4)`               |
| example function 10 20                      | `example_function(10, 20)`                                     |
| concatenate Welcome to the DSL world        | `DSLProcessor.concatenate("Welcome", "to", "the", "DSL", "world")` |

These example sentences demonstrate how the DSL processor interprets and executes different types of commands, including standalone functions, class methods, and module functions.

## Contributing

Contributions are welcome! Please see the [contributing guidelines](CONTRIBUTING.md) for more details.

## License

This project is licensed under the [MIT License](LICENSE).
