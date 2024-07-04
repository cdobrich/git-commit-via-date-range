# git-commit-via-date-range

Add files to a Git repository based on specified date ranges. Tested on Linux.

This program honors all normal Git configurations, like .gitignore files and such.

## Dependencies / Requirements

pip install GitPython pytz

#### Create a local python environment

If the dependency `GitPython` and `pytz` are not available on the system, you can install them locally to an isolated Python environment.

    python3 -m venv '.venv'
    source .venv/bin/activate
    pip install GitPython pytz

## Assumptions

The input path argument (base folder) contains the Git repository you want to commit to.

## Usage

General form (when Git has prior commits to compare against):

    python git-commit-via-date-range.py /path/to/folder/with/git/repository YYYY-MM-DD <timezone>

Starting form (when the local Git repository has no prior commits):

    python git-commit-via-date-range.py /path/to/folder/with/git/repository YYYY-MM-DD <timezone> YYYY-MM-DD <timezone>

### Case 1: No starting date 

Used when the Git repository has prior commits to compare against.

    python git-commit-via-date-range.py /path/to/your/git/repository 2024-01-25 America/Los_Angeles

    Example: 
        python git-commit-via-date-range.py $HOME/images 2024-02-01 America/New_York

### Case 2: With starting date

Used when the local Git repository has no prior commits.

    python git-commit-via-date-range.py /path/to/your/git/repository 2024-01-25 America/Los_Angeles 2024-02-01 America/New_York

    Example: 
        python git-commit-via-date-range.py $HOME/images 2024-01-25 America/Los_Angeles 2024-02-01 America/New_York

### Usage with local Python Environment

    source /home/$USER/code/python/git-commit-via-date-range/.venv/bin/activate
    python /home/$USER/code/python/git-commit-via-date-range/git-commit-via-date-range.py


### Usage with local Python Environment

    source /home/$USER/code/python/git-commit-via-date-range/.venv/bin/activate
    python /home/$USER/code/python/git-commit-via-date-range/git-commit-via-date-range.py
    
# TODO

Write some unit-tests to verify things work after making further changes or features.
