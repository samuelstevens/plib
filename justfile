docs: lint
    rm -rf docs/api
    uv run pdoc3 --force --output-dir docs/api --config latex_math=True plib
    uv run python scripts/docs.py --in-dpaths plib examples --out-fpath docs/llms.txt

lint: fmt
    git ls-files "*.py" --cached --others --exclude-standard | xargs uv run ruff check

fmt:
    git ls-files "*.py" --cached --others --exclude-standard | xargs uv run isort
    git ls-files "*.py" --cached --others --exclude-standard | xargs uv run ruff format --preview