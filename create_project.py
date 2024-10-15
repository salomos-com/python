import os
import sys

def create_project_structure(project_name):
    # Create project directory
    os.makedirs(project_name, exist_ok=True)
    os.chdir(project_name)
    
    # Create src directory
    os.makedirs(f"src/{project_name}", exist_ok=True)
    
    # Create main project file with example class
    with open(f"src/{project_name}/{project_name}.py", "w") as f:
        f.write(f"""
class ExampleClass:
    def __init__(self, name):
        self.name = name
    
    def greet(self):
        return f"Hello, {{self.name}}!"

def main():
    example = ExampleClass("World")
    print(example.greet())

if __name__ == "__main__":
    main()
""")
    
    # Create empty __init__.py
    open(f"src/{project_name}/__init__.py", 'a').close()
    
    # Create setup.py
    with open("setup.py", "w") as f:
        f.write(f"""
from setuptools import setup, find_packages

setup(
    name="{project_name}",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={{"": "src"}},
    install_requires=[
        # Add your project dependencies here
    ],
    entry_points={{
        'console_scripts': [
            '{project_name}={project_name}.{project_name}:main',
        ],
    }},
)
""")
    
    # Create README.md
    with open("README.md", "w") as f:
        f.write(f"# {project_name.capitalize()}\n\nDescription of your project goes here.")
    
    # Create requirements.txt
    open("requirements.txt", 'a').close()
    
    # Create tests directory with updated test file
    os.makedirs("tests", exist_ok=True)
    with open("tests/test_" + project_name + ".py", "w") as f:
        f.write(f"""
import unittest
from {project_name}.{project_name} import ExampleClass

class Test{project_name.capitalize()}(unittest.TestCase):
    def test_example_class(self):
        example = ExampleClass("Test")
        self.assertEqual(example.greet(), "Hello, Test!")

if __name__ == '__main__':
    unittest.main()
""")
    
    # Create config file
    create_config_file(project_name)
    
    print(f"Project structure for {project_name} has been created.")

def create_config_file(project_name):
    config_content = f"""
[{project_name}]
debug = false
log_level = INFO

[database]
host = localhost
port = 5432
name = {project_name}_db
"""
    with open(f"config.ini", "w") as f:
        f.write(config_content)

if __name__ == "__main__":
    project_name = input("Enter the name of your project: ").strip()
    if not project_name:
        print("Error: Project name cannot be empty.")
        sys.exit(1)
    
    create_project_structure(project_name)
