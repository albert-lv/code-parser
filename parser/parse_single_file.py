from git.git_show_file import get_single_file
from parser.init_parser import init_parser

def get_file_content(repo_path, file_path, revision='HEAD'):
    return get_single_file(repo_path, revision, file_path)

def init_java_parser():
    return init_parser('java')

def parse_java_content(content, parser):
    return parser.parse(bytes(content, 'utf8'))

def find_annotated_methods(tree, content, annotations):
    cursor = tree.walk()
    results = []

    def get_text(node):
        return content[node.start_byte:node.end_byte]
    
    def extract_methods(node):
        if not node.children:
            return None

        if node.type == 'method_declaration':
            for child in node.children:
                if child.type == 'modifiers' and any(a in get_text(child) for a in annotations):
                    start_line = content[:node.start_byte].count('\n') + 1
                    end_line = content[:node.end_byte].count('\n') + 1
                    method_code = get_text(node).strip()
                    results.append({'start_line': start_line, 'end_line': end_line, 'code': method_code})
                    break
            
        for n in node.children:
            extract_methods(n)

    extract_methods(cursor.node)
    return results

def parse_changed_file(repo_path, file_path, revision, annotations):
    parser = init_java_parser()
    content = get_file_content(repo_path, file_path, revision)
    tree = parse_java_content(content, parser)
    methods = find_annotated_methods(tree, content, annotations)
    return methods
    

def main(repo_path, file_path, revision, annotations):
    methods = parse_changed_file(repo_path, file_path, revision, annotations)
    if methods:
        for method in methods:
            print(f"Method from line {method['start_line']} to {method['end_line']}:")
            print(method['code'])
            print("-" * 40)
    else:
        print("No methods found.")
    

if __name__ == "__main__":
    repo_path = input("Enter the repository path: ")
    file_path = input("Enter the file path: ")
    revision = input("Enter the revision: ")
    annotations = input("Enter the annotations (comma-separated): ").split(",")
    main(repo_path, file_path, revision, annotations)