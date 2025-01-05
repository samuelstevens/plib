import glob
import os


def main(in_dpaths: list[str], out_fpath: str):
    """
    Args:
        in_dpaths: Directories for source files.
        out_fpath: Path for output .txt file
    """

    content = []
    # Get all source code files from input directories using git ls-files, including unadded but trackable files. AI!
    for dpath in in_dpaths:
        for root, _, files in os.walk(dpath):
            for file in files:
                if file.endswith(".py"):
                    fpath = os.path.join(root, file)
                    with open(fpath, "r") as f:
                        rel_path = os.path.relpath(fpath)
                        file_content = f"# {rel_path}\n\n```python\n{f.read()}\n```"
                        content.append(file_content)

    # Find all .md files in docs/ except those in docs/api/
    md_files = ["README.md"]
    md_files.extend(glob.glob("docs/**/*.md", recursive=True))
    # Filter out docs/api/ files
    md_files = [f for f in md_files if "docs/api/" not in f]

    # Process markdown files
    root = os.path.commonpath([os.path.dirname(p) for p in md_files])
    for md_file in md_files:
        with open(md_file, "r") as f:
            md_content = f.read()
            content.append(with_header(md_file, md_content, root))

    # Process all modules and write to file
    with open(out_fpath, "w") as f:
        f.write("\n\n".join(content))


def with_header(md_file: str, md_content: str, root: str) -> str:
    """Add a header to markdown content if it doesn't have one.

    Args:
        md_file: Path to the markdown file
        md_content: Content of the markdown file
        root: root directory of markdown files

    Returns:
        Content with header added if needed
    """

    if not md_content.lstrip().startswith("#"):
        rel_path = os.path.relpath(md_file, root)
        return f"# {rel_path}\n\n{md_content}"
    return md_content


if __name__ == "__main__":
    import tyro

    tyro.cli(main)
