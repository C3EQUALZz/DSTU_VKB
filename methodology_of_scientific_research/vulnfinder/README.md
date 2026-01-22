# VulnFinder

A command-line tool for automated vulnerability detection in source code using Large Language Models (LLM) and Retrieval-Augmented Generation (RAG) techniques. VulnFinder analyzes code snippets, identifies potential security vulnerabilities, and maps them to corresponding CVE (Common Vulnerabilities and Exposures) identifiers and CWE (Common Weakness Enumeration) categories.

## Overview

VulnFinder is a research project that demonstrates the application of modern AI techniques for static code analysis. Unlike traditional static analysis tools, VulnFinder leverages the semantic understanding capabilities of Large Language Models to detect subtle security vulnerabilities that may be missed by rule-based analyzers.

### Key Features

- 🔍 **Automated Vulnerability Detection**: Analyze source code files and projects for potential security issues
- 🎯 **CVE/CWE Mapping**: Automatically map detected vulnerabilities to known CVE identifiers and CWE categories
- 📊 **RAG-Enhanced Analysis**: Use Retrieval-Augmented Generation to provide context-aware vulnerability detection
- 🚀 **CLI Tool**: Simple command-line interface similar to tools like `mypy` and `ruff`
- 💾 **Embedded Vector Database**: Local vector storage using ChromaDB (no Docker required)
- 🔧 **Multi-Language Support**: Analyze code in multiple programming languages (Python, C/C++, Java, etc.)

## Architecture

### Clean Architecture + Domain-Driven Design (DDD)

The project follows **Clean Architecture** principles combined with **Domain-Driven Design** to ensure maintainability, testability, and separation of concerns. The architecture consists of the following layers:

#### Domain Layer (`domain/`)
Contains the core business logic and domain entities:
- **Entities**: Core domain models (Vulnerability, CVE, CWE, CodeSnippet, etc.)
- **Value Objects**: Immutable domain values
- **Domain Services**: Business logic operations
- **Repository Interfaces**: Abstract contracts for data access

#### Application Layer (`application/`)
Implements use cases and application-specific logic:
- **Use Cases**: Orchestrate domain logic for specific operations
- **DTOs**: Data transfer objects for layer communication
- **Application Services**: Coordinate between domain and infrastructure layers

#### Infrastructure Layer (`infrastructure/`)
Handles external concerns and technical implementations:
- **LLM Clients**: Integration with language model APIs/services
- **Vector Database**: ChromaDB embedded storage for CVE knowledge base
- **Code Parsers**: AST generation and code analysis tools
- **Repository Implementations**: Concrete data access implementations

#### Presentation Layer (`presentation/` or `cli/`)
User interface and interaction:
- **CLI Interface**: Command-line interface using Click
- **Output Formatters**: Format results (JSON, text, SARIF, etc.)

### Dependency Injection & IoC Container

The project uses **[dishka](https://github.com/bobronium/dishka)** for Dependency Injection and Inversion of Control. Dishka provides:

- Type-safe dependency injection
- Async/await support
- Lifecycle management
- Modular provider system

This allows for clean separation of concerns, easy testing through mocking, and flexible component configuration.

## Technology Stack

### Core Technologies

- **Python 3.11+**: Modern Python with type hints and async/await support
- **Click**: Command-line interface creation
- **dishka**: Dependency injection container
- **ChromaDB**: Embedded vector database for CVE knowledge base (no Docker required)
- **sentence-transformers**: Generate embeddings for semantic search
- **LangChain** (optional): Orchestrate LLM workflows and RAG pipelines

### LLM Integration

- **Local Models**: Support for local LLM inference (e.g., via `llama.cpp`)
- **API Integration**: Support for cloud LLM APIs (OpenAI, Anthropic, etc.)
- **Flexible Backend**: Pluggable LLM provider system

### Code Analysis

- **Tree-sitter**: Multi-language parsing and AST generation
- **Static Analysis Tools**: Integration with existing tools for validation

### Development Tools

- **Ruff**: Fast Python linter and formatter
- **mypy**: Static type checking
- **pytest**: Testing framework
- **nox**: Automated testing and linting
- **pre-commit**: Git hooks for code quality

## Project Structure

```
vulnfinder/
├── src/
│   └── vulnfinder/
│       ├── domain/              # Domain layer
│       │   ├── entities/        # Domain entities
│       │   ├── value_objects/   # Value objects
│       │   ├── services/        # Domain services
│       │   └── repositories/    # Repository interfaces
│       ├── application/         # Application layer
│       │   ├── use_cases/       # Use case implementations
│       │   ├── dto/             # Data transfer objects
│       │   └── services/        # Application services
│       ├── infrastructure/      # Infrastructure layer
│       │   ├── llm/             # LLM clients
│       │   ├── vector_db/       # Vector database (ChromaDB)
│       │   ├── parsers/         # Code parsers
│       │   └── repositories/    # Repository implementations
│       └── cli/                 # Presentation layer
│           ├── commands/        # CLI commands
│           └── formatters/      # Output formatters
├── tests/                       # Test suite
├── pyproject.toml              # Project configuration
└── README.md                   # This file
```

## Installation

```bash
# Clone the repository
git clone https://github.com/C3EQUALZz/DSTU_VKB
cd vulnfinder

# Install dependencies (using uv, pip, or poetry)
pip install -e .

# Or with development dependencies
pip install -e ".[dev]"
```

## Usage

### Basic Usage

```bash
# Analyze a single file
vulnfinder analyze path/to/file.py

# Analyze a directory
vulnfinder analyze path/to/project/ --recursive

# Output as JSON
vulnfinder analyze app.py --output json

# Specify output format (text, json, sarif)
vulnfinder analyze app.py --format json
```

### Example Output

```json
{
  "file": "app.py",
  "vulnerabilities": [
    {
      "line": 42,
      "column": 15,
      "type": "SQL Injection",
      "severity": "HIGH",
      "cwe": "CWE-89",
      "cve": "CVE-2024-XXXXX",
      "confidence": 0.92,
      "description": "User input directly concatenated into SQL query without sanitization",
      "code_snippet": "query = f'SELECT * FROM users WHERE id={user_id}'",
      "suggestion": "Use parameterized queries or ORM methods"
    }
  ]
}
```

## Research Context

This project is part of a scientific research work on "Automation of Vulnerability Detection in Source Code Using Large Language Models (LLM)". It demonstrates:

- Application of LLM for security vulnerability detection
- Integration of RAG techniques for context-aware analysis
- Comparison with traditional static analysis methods
- Evaluation metrics: precision, recall, F1-score on benchmark datasets (BigVul, DiverseVul)

## Development

### Setup Development Environment

```bash
# Install development dependencies
uv pip install -e ".[dev]"
```

### Type Checking

```bash
mypy
```

### Code Formatting

```bash
ruff format
ruff check
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the Apache Software License 2.0 - see the [LICENSE](LICENSE) file for details.

## Authors

- **Danil Kovalev** - dan.kovalev2013@gmail.com

## Acknowledgments

- Research based on recent publications in LLM-based vulnerability detection
- Inspired by tools like CodeQL, Semgrep, and other static analysis tools
- Built using modern Python ecosystem tools and best practices

## References

For a complete list of scientific sources and references used in this research, see the bibliography in the parent project directory.
