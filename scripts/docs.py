import glob
import os
import re
import subprocess


def main(in_dpaths: list[str], out_fpath: str):
    """
    Args:
        in_dpaths: Directories for source files.
        out_fpath: Path for output .txt file
    """

    content = []

    # Get all source files using git ls-files
    for dpath in in_dpaths:
        # Get both tracked and untracked (but trackable) files
        cmd = ["git", "ls-files", "--cached", "--others", "--exclude-standard", dpath]
        result = subprocess.run(cmd, capture_output=True, text=True)
        files = result.stdout.splitlines()

        for fpath in files:
            with open(fpath, "r") as f:
                with open(fpath, "r") as f:
                    file_content = f.read()
                rel_path = os.path.relpath(fpath)
                fence = get_md_fence(fpath, file_content)
                file_content = f"# {rel_path}\n\n```{fence}\n{file_content}\n```"
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


def get_md_fence(fpath: str, content: str) -> str:
    """Determine the appropriate markdown code fence tag for a file.

    Args:
        fpath: Path to the file
        content: Content of the file

    Returns:
        The markdown code fence tag to use
    """
    # Extension based mapping
    ext_map = {
        ".py": "python",
        ".js": "javascript",
        ".ts": "typescript",
        ".sh": "bash",
        ".bash": "bash",
        ".zsh": "bash",
        ".yml": "yaml",
        ".yaml": "yaml",
        ".json": "json",
        ".md": "markdown",
        ".html": "html",
        ".css": "css",
        ".rs": "rust",
        ".go": "go",
        ".java": "java",
        ".cpp": "cpp",
        ".c": "c",
        ".sql": "sql",
    }

    # Get extension
    ext = os.path.splitext(fpath)[1].lower()

    # Check extension first
    if ext in ext_map:
        return ext_map[ext]

    # Content-based detection for special cases
    if re.search(r"^#!\s*/bin/(bash|sh|zsh)", content):
        return "bash"
    if re.search(r"^#!\s*/usr/bin/env\s+(python|bash|node)", content):
        match = re.search(r"^#!\s*/usr/bin/env\s+(\w+)", content)
        interpreter = match.group(1)
        if interpreter == "python":
            return "python"
        elif interpreter in ["bash", "sh", "zsh"]:
            return "bash"
        elif interpreter == "node":
            return "javascript"

    # Default to stripped extension (without dot) if no match
    if ext:
        return ext[1:]  # Remove the leading dot
    return "text"


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
