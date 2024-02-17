import subprocess

def run_git_diff(repo_path, old_version, new_version):
    cmd = ['git', '-C', repo_path, 'diff', "-U0", "--merge-base", old_version, new_version]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    output, _ = proc.communicate()
    return output.decode('utf-8')