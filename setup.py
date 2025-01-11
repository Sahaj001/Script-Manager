from setuptools import setup, find_packages

setup(
    name="command-manager",
    version="0.1.0",
    description="This manages all the usesful commands at one place",
    long_description=open('README.md').read(),
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
            'scm=main:start',  # Example command
        ],
    },
    license="Apache 2.0",                    # Specify Apache 2.0 License
)
