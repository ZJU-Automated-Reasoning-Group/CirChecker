from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="CirChecker",
    version="0.1.0",
    description="Static analysis tool to detect ZKP vulnerabilities in Circom circuits.",
    author="rainoftime",
    author_email="rainoftime@gmail.com",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        'antlr4-python3-runtime==4.9.2',
        'colorama==0.4.6',
        'tqdm==4.67.1'
    ],
    entry_points={
        'console_scripts': [
            'circheck = circheck.cli:main',
        ],
    },
    long_description=long_description,
    long_description_content_type="text/markdown",
)
