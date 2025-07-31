#!/usr/bin/env python3
"""
AxoDen Client - Claude Code Integration
Seamless methodology recommendations for your development workflow
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="axoden-client",
    version="0.1.0",
    author="Luminescence Limited",
    author_email="contact@luminescelimited.com",
    description="AxoDen AI-powered development guidance for Claude Code users",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/YalcinkayaE/axoden-client",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.28.0",
        "click>=8.0.0",
        "rich>=13.0.0",
        "pydantic>=2.0.0",
        "python-dotenv>=1.0.0",
        "keyring>=23.0.0",  # For secure API key storage
    ],
    entry_points={
        "console_scripts": [
            "axoden=axoden_client.cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "axoden_client": ["templates/*.txt"],
    },
)