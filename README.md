# Code Parser

[中文文档](README.zh-CN.md)

A Python-based code analysis tool that leverages tree-sitter to parse and analyze Java code changes in Git repositories. This tool is particularly useful for identifying modified controller methods and validating Swagger annotations in Java Spring applications.

## Features

- **Git Diff Analysis**: Parse git diffs to identify changed files and line ranges
- **Java Code Parsing**: Use tree-sitter to parse Java source files and extract method declarations
- **Controller Method Detection**: Find modified controller methods based on annotations and file naming patterns
- **Swagger Annotation Validation**: Validate that controller methods have proper Swagger/OpenAPI annotations
- **Reusable Components**: Modular design with reusable git and parser utilities

## Main Use Cases

### 1. Finding Changed Controller Methods
Identify which controller methods were modified between two git revisions, useful for code review and impact analysis.

### 2. Swagger Annotation Compliance
Automatically validate that modified controller methods follow Swagger annotation standards:
- Methods must have `@ApiOperation` with `httpMethod` and `value` fields
- Parameters need `@ApiParam` annotation (unless annotated with `@RequestBody`)
- Required fields: `name`, `value`, `required`, and `example`

## Dependencies

### Python Libraries
- **tree-sitter**: Code parsing library (requires tree-sitter Python bindings)
- **subprocess**: For executing git commands (built-in)
- **re**: For regex pattern matching (built-in)

### External Tools
- **Git**: Required for repository operations
- **PyInstaller**: Optional, for building standalone executables

### Tree-sitter Languages
- tree-sitter-java
- tree-sitter-python

The project includes pre-compiled tree-sitter language libraries in `language/my-languages.so`.

## Installation

1. Clone the repository:
```bash
git clone https://github.com/albert-lv/code-parser.git
cd code-parser
```

2. Install Python dependencies:
```bash
pip install tree-sitter
```

3. (Optional) Build the language library if you need to update it:
```bash
python init_library.py
```

## Usage

### Basic Usage

Run the main script to check changed controller methods and their Swagger annotations:

```bash
python main.py
```

You'll be prompted to enter:
- Repository path
- Old version (commit SHA, branch, or tag)
- New version (commit SHA, branch, or tag)

### Using Individual Modules

#### Finding Changed Controller Methods

```python
from find_changed_controller import find_changed_controller_methods

repo_path = "/path/to/repo"
old_version = "commit-sha-1"
new_version = "commit-sha-2"
annotations = ['@RequestMapping', '@GetMapping', '@PostMapping', '@PutMapping', '@DeleteMapping']
controller_keywords = ['Controller', 'Rest', 'Api']

changed_methods = find_changed_controller_methods(
    repo_path, old_version, new_version, annotations, controller_keywords
)
```

#### Parsing Git Diff

```python
from parser.parse_git_diff import parse_diff

file_changes = parse_diff(repo_path, old_version, new_version)
# Returns: {file_path: [(start_line, end_line), ...], ...}
```

#### Parsing Java Files

```python
from parser.parse_single_file import parse_changed_file

methods = parse_changed_file(repo_path, file_path, revision, annotations)
# Returns: [{'start_line': int, 'end_line': int, 'code': str}, ...]
```

#### Checking Swagger Annotations

```python
from check_swagger_annotations import check_method_annotations

code = """
@ApiOperation(httpMethod = "POST", value = "Create user")
@PostMapping("/users")
public User createUser(@ApiParam(name = "user", value = "User info", required = true, example = "{}") User user) {
    return userService.create(user);
}
"""

is_compliant, message = check_method_annotations(code)
```

## Reusable Components

### Git Module (`git/`)

#### `git_diff.py`
- **Function**: `run_git_diff(repo_path, old_version, new_version)`
- **Purpose**: Execute git diff command and return unified diff output
- **Returns**: String containing diff output
- **Reusable for**: Any project needing to analyze git diffs

#### `git_show_file.py`
- **Function**: `get_single_file(repo_path, revision, file_path)`
- **Purpose**: Retrieve file content at a specific git revision
- **Returns**: String containing file content
- **Reusable for**: Any project needing to access historical file versions

### Parser Module (`parser/`)

#### `init_parser.py`
- **Function**: `init_parser(language_name)`
- **Purpose**: Initialize a tree-sitter parser for a specific language
- **Returns**: Configured Parser instance
- **Reusable for**: Any project using tree-sitter for code parsing

#### `parse_git_diff.py`
- **Function**: `parse_diff(repo_path, old_version, new_version)`
- **Purpose**: Parse git diff output to extract changed files and line ranges
- **Returns**: Dictionary mapping file paths to list of (start_line, end_line) tuples
- **Reusable for**: Projects analyzing code changes, code review tools, CI/CD pipelines

#### `parse_single_file.py`
- **Function**: `find_annotated_methods(tree, content, annotations)`
- **Purpose**: Extract methods with specific annotations from parsed AST
- **Returns**: List of method information dictionaries
- **Reusable for**: Java static analysis tools, documentation generators, code metrics tools

## Building Standalone Executable

To build a standalone executable using PyInstaller:

```bash
pyinstaller --onefile --name="CodeParser" --paths="/path/to/code-parser" main.py
```

**Important**: The executable requires `language/my-languages.so` to be present in the same directory as the executable.

## Project Structure

```
code-parser/
├── git/                          # Git operation utilities
│   ├── git_diff.py              # Git diff execution
│   └── git_show_file.py         # File retrieval at specific revision
├── parser/                       # Code parsing utilities
│   ├── init_parser.py           # Parser initialization
│   ├── parse_git_diff.py        # Diff parsing logic
│   └── parse_single_file.py     # Java file parsing
├── language/                     # Tree-sitter language libraries
│   └── my-languages.so          # Compiled language definitions
├── vendor/                       # Tree-sitter grammar submodules
│   ├── tree-sitter-java/
│   └── tree-sitter-python/
├── main.py                       # Main entry point
├── find_changed_controller.py   # Controller method finder
├── check_swagger_annotations.py # Swagger validation
└── init_library.py              # Language library builder
```

## Extension Points

### Adding New Languages

To support additional languages:

1. Add the tree-sitter grammar as a git submodule in `vendor/`
2. Update `init_library.py` to include the new language
3. Run `python init_library.py` to rebuild the language library
4. Create language-specific parsing logic similar to the Java parser

### Custom Annotation Checks

Extend `check_swagger_annotations.py` to add custom validation rules:

```python
def check_custom_annotation(code):
    parser = init_java_parser()
    tree = parser.parse(bytes(code, 'utf8'))
    # Add your custom logic here
    return is_valid, message
```

### Different Annotation Types

Modify the `annotations` list in `main.py` or when calling functions to support different annotation patterns:

```python
annotations = ['@MyCustomAnnotation', '@AnotherAnnotation']
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

Albert Lv