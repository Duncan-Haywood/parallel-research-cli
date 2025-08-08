#!/usr/bin/env python3
"""Setup script for EssayForge."""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="essayforge",
    version="3.0.0",
    author="EssayForge Team",
    author_email="",
    description="Multi-agent collaborative synthesis for research excellence",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/duncan/essayforge",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Text Processing :: General",
    ],
    python_requires=">=3.8",
    install_requires=[
        "anthropic>=0.3.0",
        "colorama>=0.4.6",
        "tqdm>=4.65.0",
        "aiohttp>=3.8.0",
        "markdown>=3.4.0",
        "python-dotenv>=1.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.3.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
        "enhanced": [
            "rich>=13.0.0",
            "pypandoc>=1.11",
            "click>=8.1.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "essayforge=main:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)