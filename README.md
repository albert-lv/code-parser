### 如何打包？

```bash
pyinstaller --onefile --name="CodeParser" --paths="/Users/albert/CodeProjects/code-parser" main.py
```

### 如何运行？

运行目录下需要有“language/my-languages.so”动态库，否则执行时会报错。