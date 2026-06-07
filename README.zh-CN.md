# Code Parser

[![CI](https://github.com/albert-lv/code-parser/actions/workflows/ci.yml/badge.svg)](https://github.com/albert-lv/code-parser/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![tree-sitter](https://img.shields.io/badge/powered%20by-tree--sitter-green.svg)](https://tree-sitter.github.io/tree-sitter/)

基于 [tree-sitter](https://tree-sitter.github.io/tree-sitter/) 的 Python 静态分析工具，用于解析 Git 仓库中的 Java 代码变更。适合需要自动识别变更的 Spring Controller 方法并校验 Swagger/OpenAPI 注解的代码审查与 CI/CD 场景。

> **Languages**: [English](README.md) | [中文](README.zh-CN.md)

## ✨ 功能

- **Git Diff 分析** — 解析 git diff，识别变更文件与行范围。
- **Java 代码解析** — 使用 tree-sitter 解析 Java 源文件并提取方法声明。
- **Controller 方法检测** — 基于 Spring 注解与文件命名规则定位变更的 Controller 方法。
- **Swagger 注解校验** — 自动校验 Controller 方法的 Swagger/OpenAPI 注解规范性。
- **可复用组件** — 模块化的 Git 与解析器工具，方便二次开发。
- **CI/CD 友好** — 发现违规时返回非零退出码，适合合并前检查。

## 🚀 快速开始

### 安装

```bash
git clone https://github.com/albert-lv/code-parser.git
cd code-parser
pip install -r requirements.txt
```

> 可选：若添加新语言，可重新编译 tree-sitter 语言库：
> ```bash
> python init_library.py
> ```

### 基本用法

运行 CLI 并按提示输入仓库信息：

```bash
python main.py
```

你需要输入：
- 仓库路径
- 旧版本（commit SHA、分支或 tag）
- 新版本（commit SHA、分支或 tag）

### 编程使用

```python
from find_changed_controller import find_changed_controller_methods

changed = find_changed_controller_methods(
    repo_path="/path/to/repo",
    old_version="main~1",
    new_version="main",
    annotations=["@RequestMapping", "@GetMapping", "@PostMapping"],
    controller_keywords=["Controller", "Rest", "Api"],
)
```

## 📋 校验规则

启用 `check_swagger_annotations.py` 时，会检查变更的 Controller 方法：

| 规则 | 要求 |
|------|------|
| `@ApiOperation` | 必须包含 `httpMethod` 和 `value` |
| `@ApiParam` | 参数必须有，除非参数已标注 `@RequestBody` |
| `@ApiParam` 字段 | 必须包含 `name`、`value`、`required` 和 `example` |

## 📚 详细文档

### 主要使用场景

#### 1. 查找变更的 Controller 方法
识别两个 git 版本之间哪些 Controller 方法被修改，适用于代码审查和影响分析。

#### 2. Swagger 注解合规检查
自动校验变更的 Controller 方法是否符合 Swagger 注解规范：
- 方法必须有 `@ApiOperation`，且包含 `httpMethod` 和 `value` 字段
- 参数必须有 `@ApiParam`（除非标注了 `@RequestBody`）
- 必填字段：`name`、`value`、`required`、`example`

### 依赖

#### Python 库
- **tree-sitter**：代码解析库（需要 Python bindings）
- **subprocess**：执行 git 命令（内置）
- **re**：正则匹配（内置）

#### 外部工具
- **Git**：仓库操作必需
- **PyInstaller**：可选，用于构建独立可执行文件

#### Tree-sitter 语言
- tree-sitter-java
- tree-sitter-python

项目已在 `language/my-languages.so` 中预编译了 tree-sitter 语言库。

### 独立模块使用

#### 查找变更的 Controller 方法

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

#### 解析 Git Diff

```python
from parser.parse_git_diff import parse_diff

file_changes = parse_diff(repo_path, old_version, new_version)
# 返回: {file_path: [(start_line, end_line), ...], ...}
```

#### 解析 Java 文件

```python
from parser.parse_single_file import parse_changed_file

methods = parse_changed_file(repo_path, file_path, revision, annotations)
# 返回: [{'start_line': int, 'end_line': int, 'code': str}, ...]
```

#### 检查 Swagger 注解

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

### 可复用组件

#### Git 模块 (`git/`)

##### `git_diff.py`
- **功能**：`run_git_diff(repo_path, old_version, new_version)`
- **用途**：执行 git diff 并返回统一 diff 输出
- **返回**：包含 diff 输出的字符串
- **适用场景**：任何需要分析 git diff 的项目

##### `git_show_file.py`
- **功能**：`get_single_file(repo_path, revision, file_path)`
- **用途**：获取特定 git 版本的文件内容
- **返回**：文件内容字符串
- **适用场景**：任何需要访问历史文件版本的项目

#### 解析器模块 (`parser/`)

##### `init_parser.py`
- **功能**：`init_parser(language_name)`
- **用途**：初始化特定语言的 tree-sitter 解析器
- **返回**：配置好的 Parser 实例
- **适用场景**：任何使用 tree-sitter 进行代码解析的项目

##### `parse_git_diff.py`
- **功能**：`parse_diff(repo_path, old_version, new_version)`
- **用途**：解析 git diff 输出，提取变更文件和行范围
- **返回**：文件路径到 (start_line, end_line) 列表的字典
- **适用场景**：代码变更分析、代码审查工具、CI/CD 流水线

##### `parse_single_file.py`
- **功能**：`find_annotated_methods(tree, content, annotations)`
- **用途**：从解析后的 AST 中提取带特定注解的方法
- **返回**：方法信息字典列表
- **适用场景**：Java 静态分析工具、文档生成器、代码指标工具

### 构建独立可执行文件

使用 PyInstaller 构建独立可执行文件：

```bash
pyinstaller --onefile --name="CodeParser" --paths="/path/to/code-parser" main.py
```

**注意**：可执行文件需要与同目录下的 `language/my-languages.so` 一起使用。

## 🏗️ 项目结构

```
code-parser/
├── git/                          # Git 操作工具
│   ├── git_diff.py              # Git diff 执行
│   └── git_show_file.py         # 特定版本文件获取
├── parser/                       # 代码解析工具
│   ├── init_parser.py           # 解析器初始化
│   ├── parse_git_diff.py        # Diff 解析逻辑
│   └── parse_single_file.py     # Java 文件解析
├── language/                     # 编译后的 tree-sitter 语言库
│   └── my-languages.so          # 编译后的语言定义
├── vendor/                       # Tree-sitter 语法子模块
│   ├── tree-sitter-java/
│   └── tree-sitter-python/
├── example/                      # 测试示例仓库
├── main.py                       # CLI 入口
├── find_changed_controller.py   # Controller 方法查找器
├── check_swagger_annotations.py # Swagger 校验
└── init_library.py              # 语言库构建脚本
```

## 🔌 扩展点

### 添加新语言支持

1. 在 `vendor/` 中添加 tree-sitter 语法作为 git submodule
2. 更新 `init_library.py` 加入新语言
3. 运行 `python init_library.py` 重新编译语言库
4. 仿照 Java 解析器编写新语言的解析逻辑

### 自定义注解检查

扩展 `check_swagger_annotations.py`：

```python
def check_custom_annotation(code):
    parser = init_java_parser()
    tree = parser.parse(bytes(code, 'utf8'))
    # 添加你的自定义逻辑
    return is_valid, message
```

### 不同的注解类型

修改 `main.py` 中的 `annotations` 列表或调用时传入：

```python
annotations = ['@MyCustomAnnotation', '@AnotherAnnotation']
```

## 🤝 贡献

欢迎提交 bug 报告、功能建议与 Pull Request。请参阅 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 📄 许可证

本项目采用 [MIT 许可证](LICENSE)。

## 🔗 相关关键词

`static-analysis` `tree-sitter` `java` `spring-boot` `swagger` `openapi` `git-diff` `code-review` `ci-cd` `controller-methods` `annotation-validation`
