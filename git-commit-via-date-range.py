import os
import sys
import datetime
import logging
from git import Repo
import pytz

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_changed_files(repo, since_date):
    changed_files = []
    for item in repo.untracked_files:
        # Check if the file was created after the specified date
        file_path = os.path.join(repo.working_dir, item)

        try:
            file_stat = os.stat(file_path)
            create_time = datetime.datetime.fromtimestamp(file_stat.st_ctime)
            create_time = create_time.replace(tzinfo=pytz.UTC)

            if create_time >= since_date:
                changed_files.append(item)
        except (FileNotFoundError, OSError) as e:
            handle_file_error(item, e)

    return changed_files


def handle_file_error(file_path, error):
    if os.path.islink(file_path) and not os.path.exists(file_path):
        # Broken symbolic link, only report as a warning
        logger.warning(f"Broken symbolic link: {file_path}")
    else:
        logger.error(f"Error accessing file {file_path}: {error}")


def commit_changes(repo, changed_files):
    if changed_files:
        repo.index.add(changed_files)
        repo.index.commit("Auto commit changes")
        logger.info("Changes committed to Git repository.")
        logger.info("Committed files:")
        for file_path in changed_files:
            logger.info(f"- {file_path}")
    else:
        logger.info("No changes to commit.")


def parse_date_with_timezone(date_str, timezone_str):
    timezone = pytz.timezone(timezone_str)
    naive_date = datetime.datetime.fromisoformat(date_str)
    return timezone.localize(naive_date)


def main():
    if len(sys.argv) < 3 or len(sys.argv) > 6:
        print(
            "Usage: python script.py <path_to_directory> [<start_date> <start_timezone>] [<end_date> <end_timezone>]")
        print()
        print(
            "Example usage: "
            "python script.py /path/to/your/git/repository 2024-01-25 America/Los_Angeles 2024-02-01 America/New_York")
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

    if len(sys.argv) >= 5:
        start_date = parse_date_with_timezone(sys.argv[2], sys.argv[3])

    if len(sys.argv) == 6:
        end_date = parse_date_with_timezone(sys.argv[4], sys.argv[5])

    changed_files = get_changed_files(repo, start_date)
    commit_changes(repo, changed_files)


if __name__ == "__main__":
    main()
