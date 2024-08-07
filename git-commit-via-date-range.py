#!/user/bin/python3

import os
import sys
import datetime
import logging
import pytz
import git
from git import Repo
from tqdm import tqdm


# Custom filter class
class NoErrorFilter(logging.Filter):
    def filter(self, record):
        return record.levelno not in (logging.ERROR, logging.WARNING)


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.addFilter(NoErrorFilter())

# Attempt to import the git_lfs module
try:
    import git_lfs

    use_git_lfs_module = True
except ImportError:
    use_git_lfs_module = False


def get_changed_files(repo, since_date):
    changed_files = []
    since_date = since_date.replace(tzinfo=pytz.UTC)  # Ensure since_date is timezone-aware (UTC in this case)

    for item in tqdm(repo.untracked_files, desc="Checking files", ncols=100):
        file_path = os.path.join(repo.working_dir, item)

        try:
            file_stat = os.stat(file_path)
            create_time = datetime.datetime.fromtimestamp(file_stat.st_ctime, tz=pytz.UTC)

            if create_time >= since_date:
                changed_files.append(item)
        except (FileNotFoundError, OSError) as e:
            handle_file_error(item, e)

    logger.info("All UNTRACKED FILES processed: {}".format(len(repo.untracked_files)))
    return changed_files


def handle_file_error(file_path, error):
    if os.path.islink(file_path) and not os.path.exists(file_path):
        # Broken symbolic link, only report as a warning
        logger.warning(f"Broken symbolic link: {file_path}")
    else:
        logger.error(f"Error accessing file {file_path}: {error}")


def track_large_files(repo, large_files):
    if use_git_lfs_module:
        lfs = git_lfs.LFS(repo.working_dir)
        for large_file in large_files:
            lfs.track(large_file)
    else:
        for large_file in large_files:
            os.system(f"git lfs track '{large_file}'")
    repo.git.add('.gitattributes')  # Ensure .gitattributes is added


def commit_changes(repo, changed_files, lfs_threshold_mb=100):
    lfs_threshold_bytes = lfs_threshold_mb * 1024 * 1024
    large_files = []
    normal_files = []

    for file_path in changed_files:
        file_full_path = os.path.join(repo.working_dir, file_path)
        if os.path.getsize(file_full_path) > lfs_threshold_bytes:
            large_files.append(file_path)
        else:
            normal_files.append(file_path)

    if large_files:
        # Track large files with Git LFS
        track_large_files(repo, large_files)

    if normal_files or large_files:
        repo.index.add(normal_files + large_files)
        repo.index.commit("Auto commit changes")
        logger.info("Changes committed to Git repository.")
        logger.info("Committed files:")
        for file_path in normal_files + large_files:
            logger.info(f"- {file_path}")
    else:
        logger.info("No changes to commit.")


def parse_date_with_timezone(date_str, timezone_str):
    timezone = pytz.timezone(timezone_str)
    naive_date = datetime.datetime.fromisoformat(date_str)
    return timezone.localize(naive_date)


def print_help():
    print(
        "Usage: python script.py <path_to_directory> [<start_date> <start_timezone>] [<end_date> <end_timezone>]")
    print()
    print(
        "Example usage with no prior commits: "
        "   python script.py /path/to/your/git/repository 2024-01-25 America/Los_Angeles"
        "Example usage with no prior commits: "
        "   python script.py /path/to/your/git/repository 2024-01-25 America/Los_Angeles 2024-02-01 America/New_York")


def main():
    # parser = argparse.ArgumentParser(description="Add files to a Git repository based on specified date ranges.")
    # parser.add_argument("--date-start", help="")
    # parser.add_argument("--date-end", help="")
    # args = parser.parse_args()

    if len(sys.argv) >= 2 and (sys.argv[1] == "-h" or sys.argv[1] == "--help"):
        print_help()
        sys.exit(1)

    if len(sys.argv) < 3 or len(sys.argv) > 6:
        print_help()
        sys.exit(1)

    directory_path = sys.argv[1]

    if not os.path.exists(directory_path):
        logger.error(f"Error: Directory '{directory_path}' not found.")
        sys.exit(1)

    repo = Repo(directory_path)

    if repo.bare:
        logger.error("Error: Not a Git repository.")
        sys.exit(1)

    start_date = datetime.datetime.min
    end_date = datetime.datetime.max

    if len(sys.argv) == 4:
        start_date = parse_date_with_timezone(sys.argv[2], sys.argv[3])
    else:
        logger.error("Error: No start dates specified.")
        sys.exit(1)

    if len(sys.argv) == 6:
        end_date = parse_date_with_timezone(sys.argv[4], sys.argv[5])

    changed_files = get_changed_files(repo, start_date)
    commit_changes(repo, changed_files)


if __name__ == "__main__":
    main()
