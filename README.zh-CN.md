# Code Parser

[English Documentation](README.md)

一个基于 Python 的代码分析工具，利用 tree-sitter 解析和分析 Git 仓库中的 Java 代码变更。该工具特别适用于识别修改过的控制器方法并验证 Java Spring 应用程序中的 Swagger 注解。

## 功能特性

- **Git Diff 分析**：解析 git diff 以识别变更的文件和行范围
- **Java 代码解析**：使用 tree-sitter 解析 Java 源文件并提取方法声明
- **控制器方法检测**：基于注解和文件命名模式查找修改过的控制器方法
- **Swagger 注解验证**：验证控制器方法是否具有正确的 Swagger/OpenAPI 注解
- **可复用组件**：模块化设计，提供可复用的 git 和解析器工具

## 主要使用场景

### 1. 查找变更的控制器方法
识别两个 git 版本之间修改了哪些控制器方法，适用于代码审查和影响分析。

### 2. Swagger 注解合规性检查
自动验证修改过的控制器方法是否遵循 Swagger 注解标准：
- 方法必须有包含 `httpMethod` 和 `value` 字段的 `@ApiOperation` 注解
- 参数需要 `@ApiParam` 注解（除非有 `@RequestBody` 注解）
- 必需字段：`name`、`value`、`required` 和 `example`

## 依赖项

### Python 库
- **tree-sitter**：代码解析库（需要 tree-sitter Python 绑定）
- **subprocess**：用于执行 git 命令（内置）
- **re**：用于正则表达式匹配（内置）

### 外部工具
- **Git**：仓库操作必需
- **PyInstaller**：可选，用于构建独立可执行文件

### Tree-sitter 语言
- tree-sitter-java
- tree-sitter-python

项目在 `language/my-languages.so` 中包含预编译的 tree-sitter 语言库。

## 安装

1. 克隆仓库：
```bash
git clone https://github.com/albert-lv/code-parser.git
cd code-parser
```

2. 安装 Python 依赖：
```bash
pip install tree-sitter
```

3. （可选）如需更新语言库，可重新构建：
```bash
python init_library.py
```

## 使用方法

### 基本用法

运行主脚本来检查变更的控制器方法及其 Swagger 注解：

```bash
python main.py
```

系统会提示您输入：
- 仓库路径
- 旧版本（提交 SHA、分支或标签）
- 新版本（提交 SHA、分支或标签）

### 使用单独的模块

#### 查找变更的控制器方法

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

## 可复用组件

### Git 模块 (`git/`)

#### `git_diff.py`
- **函数**: `run_git_diff(repo_path, old_version, new_version)`
- **用途**: 执行 git diff 命令并返回统一的 diff 输出
- **返回**: 包含 diff 输出的字符串
- **可复用于**: 任何需要分析 git diff 的项目

#### `git_show_file.py`
- **函数**: `get_single_file(repo_path, revision, file_path)`
- **用途**: 检索特定 git 版本的文件内容
- **返回**: 包含文件内容的字符串
- **可复用于**: 任何需要访问历史文件版本的项目

### 解析器模块 (`parser/`)

#### `init_parser.py`
- **函数**: `init_parser(language_name)`
- **用途**: 为特定语言初始化 tree-sitter 解析器
- **返回**: 配置好的 Parser 实例
- **可复用于**: 任何使用 tree-sitter 进行代码解析的项目

#### `parse_git_diff.py`
- **函数**: `parse_diff(repo_path, old_version, new_version)`
- **用途**: 解析 git diff 输出以提取变更的文件和行范围
- **返回**: 将文件路径映射到 (start_line, end_line) 元组列表的字典
- **可复用于**: 代码变更分析项目、代码审查工具、CI/CD 流水线

#### `parse_single_file.py`
- **函数**: `find_annotated_methods(tree, content, annotations)`
- **用途**: 从解析的 AST 中提取具有特定注解的方法
- **返回**: 方法信息字典列表
- **可复用于**: Java 静态分析工具、文档生成器、代码度量工具

## 构建独立可执行文件

使用 PyInstaller 构建独立可执行文件：

```bash
pyinstaller --onefile --name="CodeParser" --paths="/path/to/code-parser" main.py
```

**重要提示**：可执行文件需要在同一目录下有 `language/my-languages.so` 文件。

## 项目结构

```
code-parser/
├── git/                          # Git 操作工具
│   ├── git_diff.py              # Git diff 执行
│   └── git_show_file.py         # 特定版本的文件检索
├── parser/                       # 代码解析工具
│   ├── init_parser.py           # 解析器初始化
│   ├── parse_git_diff.py        # Diff 解析逻辑
│   └── parse_single_file.py     # Java 文件解析
├── language/                     # Tree-sitter 语言库
│   └── my-languages.so          # 编译的语言定义
├── vendor/                       # Tree-sitter 语法子模块
│   ├── tree-sitter-java/
│   └── tree-sitter-python/
├── main.py                       # 主入口点
├── find_changed_controller.py   # 控制器方法查找器
├── check_swagger_annotations.py # Swagger 验证
└── init_library.py              # 语言库构建器
```

## 扩展点

### 添加新语言

支持其他语言：

1. 在 `vendor/` 中添加 tree-sitter 语法作为 git 子模块
2. 更新 `init_library.py` 以包含新语言
3. 运行 `python init_library.py` 重新构建语言库
4. 创建类似 Java 解析器的特定语言解析逻辑

### 自定义注解检查

扩展 `check_swagger_annotations.py` 以添加自定义验证规则：

```python
def check_custom_annotation(code):
    parser = init_java_parser()
    tree = parser.parse(bytes(code, 'utf8'))
    # 在此添加您的自定义逻辑
    return is_valid, message
```

### 不同的注解类型

修改 `main.py` 中的 `annotations` 列表或调用函数时传入，以支持不同的注解模式：

```python
annotations = ['@MyCustomAnnotation', '@AnotherAnnotation']
```

## 贡献

欢迎贡献！请随时提交 Pull Request。

## 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件。

## 作者

Albert Lv
