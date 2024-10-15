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

## Usage Examples

The package also includes example modules and functions to illustrate usage:

- `ExampleModule` (`example_module.py`): Contains a greeting function and sample math operations
- `example_function` (`example_function.py`): A standalone example function

Refer to these examples for basic usage patterns of the Salomos package classes and functions.

## Contributing

Contributions are welcome! Please see the [contributing guidelines](CONTRIBUTING.md) for more details.

## License

This project is licensed under the [MIT License](LICENSE).
