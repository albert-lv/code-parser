import subprocess

def get_single_file(repo_path, revision, file_path):
    cmd = ['git', '-C', repo_path, 'show', f'{revision}:{file_path}']
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    output, _ = proc.communicate()
    return output.decode('utf-8')