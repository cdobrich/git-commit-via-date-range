# git-commit-via-date-range

## Dependencies / Requirements

pip install GitPython

#### Create a local python environment

python3 -m venv '.venv'
source .venv/bin/activate
pip install GitPython

## Assumptions

The input path argument (base folder) contains the Git repository you want to commit to.

## Usage

General form:

    python git-commit-via-date-range.py /path/to/your/git/repository YYYY-MM-DD

Example:

    python git-commit-via-date-range.py /home/username/images 2022-01-31

### Usage with local Python Environment

source /home/username/code/python/git-commit-via-date-range/.venv/bin/activate
python /home/username/code/python/git-commit-via-date-range/git-commit-via-date-range.py

