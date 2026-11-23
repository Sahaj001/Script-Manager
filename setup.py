"""Setup configuration for the Script Command Manager (SCM) package."""
from pathlib import Path

from setuptools import find_packages, setup


def read_readme() -> str:
    readme_path = Path(__file__).parent / "README.md"
    if readme_path.exists():
        return readme_path.read_text(encoding="utf-8")
    return "Command manager using fzf"


setup(
    name="command-manager-util",
    version="1.1.0",
    description="Manage and execute shell commands from a categorized, fzf-powered menu.",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    author="Sahaj Pratap Singh",
    author_email="",
    url="https://github.com/Sahaj001/Script-Manager",
    project_urls={
        "Homepage": "https://github.com/Sahaj001/Script-Manager",
        "Source": "https://github.com/Sahaj001/Script-Manager",
        "Bug Tracker": "https://github.com/Sahaj001/Script-Manager/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Environment :: Console",
        "Topic :: Utilities",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[],
    python_requires=">=3.6",
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "scm=scm.cli:main",
        ],
    },

    license="Apache-2.0",
)

