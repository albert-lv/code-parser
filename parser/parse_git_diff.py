import re
from git.git_diff import run_git_diff

def parse_diff(repo_path, old_version, new_version):
    diff_output = run_git_diff(repo_path, old_version, new_version)

    file_changes = {}
    file_pattern = re.compile(r'^\+\+\+ b/(.+)')
    hunk_pattern = re.compile(r'^@@ -(?:\d+)(?:,\d+)? \+(\d+)(?:,(\d+))? @@')

    current_file = None
    for line in diff_output.splitlines():
        file_match = file_pattern.match(line)
        if file_match:
            current_file = file_match.group(1)
            file_changes[current_file] = []

        hunk_match = hunk_pattern.match(line)
        if hunk_match:
            start_line = int(hunk_match.group(1))
            line_count = hunk_match.group(2)
            line_count = int(line_count) if line_count else 1
            end_line = start_line + line_count - 1
            file_changes[current_file].append((start_line, end_line))

    return file_changes

def print_changes(file_changes):
    for file_path, changes in file_changes.items():
        print(f"Changes in {file_path}:")
        for start_line, end_line in changes:
            print(f"  Lines {start_line} to {end_line}")

def main(repo_path, old_version, new_version):
    file_changes = parse_diff(repo_path, old_version, new_version)
    print_changes(file_changes)

if __name__ == "__main__":
    repo_path = input("Enter the repository path: ")
    old_version = input("Enter the old version: ")
    new_version = input("Enter the new version: ")
    main(repo_path, old_version, new_version)