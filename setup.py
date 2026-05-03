"""
Setup configuration for the S-Command-Manager (SCM) package.

This script uses setuptools to manage the installation, packaging, and 
distribution of SCM. It defines the 'scm' entry point, allowing the 
logic to be executed as a standalone CLI tool.

Key Features:
    - Defines a console script entry point 'scm' mapping to main:start.
    - Configured for local 'editable' installation for development.

Author: Sahaj Pratap Singh
License: Apache License 2.0
"""
from setuptools import setup

def read_file():
    """Read the README file."""
    try:
        with open("README.md", "r", encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return "Command manager using fzf"

setup(
    name="command-manager-util",
    version="1.0.0",
    description="Manages useful commands in one place using fzf",
    long_description=read_file(),
    long_description_content_type="text/markdown",
    author="Sahaj Pratap Singh",
    url="https://github.com/Sahaj001/Script-Manager",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    install_requires=[],
    python_requires='>=3.6',
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'scm=main:main', 
        ],
    },
    license="Apache 2.0",
)
