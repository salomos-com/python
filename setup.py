from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="salomos",
    version="0.1.4",
    author="Tom Sapletta",
    author_email="info@softreck.dev", 
    description="Salomos is a Python package that provides a domain-specific language (DSL) processor for executing commands based on sentences stored in a SQLite database.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://python.dobyemail.com",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "sqlite3",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License", 
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    entry_points={
        'console_scripts': [
            'salomos=salomos.dsl_processor:main',
        ],
    },
)
