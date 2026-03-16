from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
README_PATH = Path(__file__).parent / "lexora-web-editor" / "README.md"
if README_PATH.exists():
    long_description = README_PATH.read_text(encoding="utf-8")
else:
    long_description = "Lexora - A simple English-like programming language"

setup(
    name="lexora-lang",
    version="1.0.0",
    author="Lexora Team",
    author_email="team@lexora.dev",
    description="A revolutionary English-like programming language with web-based editor",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/lexora",
    packages=find_packages(where="lexora-web-editor/src"),
    package_dir={"": "lexora-web-editor/src"},
    include_package_data=True,
    package_data={
        'lexora': ['*.py'],
        'templates': ['*.html'],
        'static': ['**/*'],
    },
    py_modules=["app"],
    install_requires=[
        "Flask>=2.2.2",
        "Werkzeug>=2.2.2",
    ],
    entry_points={
        "console_scripts": [
            "lexora=lexora.lexora:main",
            "lexora-editor=app:run_server",  # Web editor command
        ],
    },
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Languages",
        "Topic :: Education",
        "Topic :: Text Editors :: Integrated Development Environments (IDE)",
    ],
    keywords=["programming language", "education", "english", "beginner-friendly", "IDE"],
)
