"""
Setup script for AtPoE (Admitting the Possibilities of Error)
A closed curve generation and visualization system.
"""

from setuptools import setup, find_packages

setup(
    name="atpoe",
    version="1.0.0",
    author="Closed Curve Team",
    author_email="team@atpoe.org",
    description="Admitting the Possibilities of Error - Closed curve generation and visualization system",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/team/atpoe",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Visualization",
        "Topic :: Multimedia :: Graphics",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=[
        "Pillow>=9.0.0",
        "numpy>=1.21.0",
        "matplotlib>=3.5.0",
        "streamlit>=1.20.0",
        "psutil>=5.8.0",
    ],
    entry_points={
        "console_scripts": [
            "atpoe=atpoe.cli:main",
        ],
    },
    include_package_data=True,
    keywords="curves, visualization, patterns, graphics, mathematical-art",
) 