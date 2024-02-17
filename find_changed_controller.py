from parser.parse_git_diff import parse_diff
from parser.parse_single_file import parse_changed_file

def file_contains_keyword(file_path, keyword_list):
    return any(keyword in file_path for keyword in keyword_list)

def find_changed_controller_methods(repo_path, old_version, new_version, annotations, controller_keywords):
    file_changes = parse_diff(repo_path, old_version, new_version)

    changed_methods = {}

    for file_path, line_range_list in file_changes.items():
        if file_contains_keyword(file_path, controller_keywords):
            new_methods = parse_changed_file(repo_path, file_path, new_version, annotations)

            for method in new_methods:
                for line_start, line_end in line_range_list:
                    if (method['start_line'] <= line_end and
                        method['end_line'] >= line_start):
                        changed_methods.setdefault(file_path, []).append(method)
                        break
    return changed_methods

def main(repo_path, old_version, new_version, annotations, controller_keywords):
    changed_methods = find_changed_controller_methods(repo_path, old_version, new_version, annotations, controller_keywords)
    for file_path, methods in changed_methods.items():
        print(f"Changed controller methods in {file_path}:")
        for method in methods:
            print(f"  Method from line {method['start_line']} to {method['end_line']}:")
            print(method['code'])
            print("-" * 40)

if __name__ == "__main__":
    repo_path = input("Enter the repository path: ")
    old_version = input("Enter the old version: ")
    new_version = input("Enter the new version: ")
    annotations = ['@RequestMapping', '@GetMapping', '@PostMapping', '@PutMapping', '@DeleteMapping']
    controller_keywords = ['Controller', 'Rest', 'Api']
    main(repo_path, old_version, new_version, annotations, controller_keywords)

