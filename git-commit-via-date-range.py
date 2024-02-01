import os
import sys
import datetime
from git import Repo


def get_changed_files(repo, since_date):
    changed_files = []
    for item in repo.index.diff(None):
        if item.change_type in ['A', 'M', 'R', 'D']:
            # Check if the change occurred after the specified date
            commit_date = repo.git.log('-n', '1', '--format=%aI', item.a_path)
            commit_date = datetime.datetime.fromisoformat(commit_date)
            if commit_date >= since_date:
                changed_files.append(item.a_path)

    return changed_files


def commit_changes(repo, changed_files):
    if changed_files:
        repo.index.add(changed_files)
        repo.index.commit("Auto commit changes")
        print(f"Changes committed to Git repository.")
    else:
        print("No changes to commit.")


def main():
    if len(sys.argv) != 3:
        print("Usage: python script.py <path_to_directory> <date_in_ISO_format>")
        sys.exit(1)

    directory_path = sys.argv[1]
    input_date = datetime.datetime.fromisoformat(sys.argv[2])

    if not os.path.exists(directory_path):
        print(f"Error: Directory '{directory_path}' not found.")
        sys.exit(1)

    repo = Repo(directory_path)

    if repo.bare:
        print("Error: Not a Git repository.")
        sys.exit(1)

    changed_files = get_changed_files(repo, input_date)
    commit_changes(repo, changed_files)


if __name__ == "__main__":
    main()
