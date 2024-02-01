# git-commit-via-date-range

Add files to a Git repository based on specified date ranges.

This program honors all normal Git configurations, like .gitignore files and such.

## Dependencies / Requirements

pip install GitPython pytz

#### Create a local python environment

    python3 -m venv '.venv'
    source .venv/bin/activate
    pip install GitPython

## Assumptions

The input path argument (base folder) contains the Git repository you want to commit to.

## Usage

General form:

    python git-commit-via-date-range.py /path/to/folder/with/git/repository YYYY-MM-DD <timezone>

### Case 1: No starting date 

Used when the Git repository has prior commits to compare against.

    python git-commit-via-date-range.py /path/to/your/git/repository 2022-01-01 UTC

### Case 2: With starting date

Used when the local Git repository has no prior commits.

    python git-commit-via-date-range.py /path/to/your/git/repository 2022-01-01 UTC 2022-01-31 PST

### Usage with local Python Environment

    source /home/username/code/python/git-commit-via-date-range/.venv/bin/activate
    python /home/username/code/python/git-commit-via-date-range/git-commit-via-date-range.py

