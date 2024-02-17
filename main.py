from find_changed_controller import find_changed_controller_methods
from check_swagger_annotations import check_method_annotations

def main(repo_path, old_version, new_version, annotations=['@RequestMapping', '@GetMapping', '@PostMapping', '@PutMapping', '@DeleteMapping'], controller_keywords=['Controller', 'Rest', 'Api']):
    changed_methods = find_changed_controller_methods(repo_path, old_version, new_version, annotations, controller_keywords)
    non_compliant_methods = []

    for file_path, methods in changed_methods.items():
        print(f"Changed controller methods in {file_path}:")
        for method in methods:
            code = method['code']
            start_line = method['start_line']
            end_line = method['end_line']
            print(f"Method from line {start_line} to {end_line}:")
            print(code)
            is_compliant, message = check_method_annotations(code, start_line, end_line)
            if not is_compliant:
                non_compliant_methods.append((file_path, method, message)) 
                print(f"WARNING: {message}")
            else:
                print(f"OK: {message}")    
            print("-" * 40)
    
    if non_compliant_methods:
        print("Swagger注解规范：")
        print("1. 除非方法有@ApiIgnore注解，否则都需要遵守下面的规范；")    
        print("2. 方法需要有@ApiOperation注解，注解内容需要包含httpMethod和value字段；")
        print("3. 方法参数的要求是：除非是有@RequestBody注解，否则都需要有@ApiParam注解，注解内容需要包含name、value、defaultValue、required和example字段。")
        print("以下方法的Swagger注解不规范:")
        for file_path, method, message in non_compliant_methods:
            print(f"File: {file_path}")
            print(f"Method from line {method['start_line']} to {method['end_line']}:")
            print(method['code'])
            print(f"WARNING: {message}")
            print("-" * 40)
        exit(1)  # 异常退出程序

if __name__ == "__main__":
    repo_path = input("Enter the repository path: ")
    old_version = input("Enter the old version: ")
    new_version = input("Enter the new version: ")
    annotations = ['@RequestMapping', '@GetMapping', '@PostMapping', '@PutMapping', '@DeleteMapping']
    controller_keywords = ['Controller', 'Rest', 'Api']
    main(repo_path, old_version, new_version, annotations, controller_keywords)