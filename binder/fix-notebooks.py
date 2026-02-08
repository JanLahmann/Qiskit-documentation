#!/usr/bin/env python3
"""Clean up IBM documentation notebooks for plain Jupyter rendering.

IBM's Qiskit notebooks are authored for a custom MDX platform.
This script fixes four issues that appear in standard Jupyter:

1. YAML frontmatter (--- title: ... ---) rendered as visible text
2. MDX cspell directives ({/* cspell:ignore ... */}) shown in output
3. JSX <Image> tags in markdown cells that don't render in Jupyter
4. Pre-rendered <Image> tags in code cell outputs (replace with HTML <img>)

Image paths are converted from absolute (/docs/images/...) to relative paths
so they resolve correctly in Jupyter's URL space.
"""

import json
import os
import re
import sys
from pathlib import Path

# --- patterns -----------------------------------------------------------

# YAML frontmatter at the start of a cell: ---\n...\n---\n
FRONTMATTER_RE = re.compile(r"\A---\n.*?^---\n*", re.DOTALL | re.MULTILINE)

# MDX comment lines: {/* cspell:ignore ... */}  (possibly with surrounding whitespace)
CSPELL_RE = re.compile(r"^\{/\*.*?\*/\}\s*\n?", re.MULTILINE)

# JSX <Image src="..." alt="..." /> — attributes in either order
IMAGE_RE = re.compile(
    r'<Image\s+'
    r'(?:src="(?P<src1>[^"]+)"\s+alt="(?P<alt1>[^"]*)"'
    r'|alt="(?P<alt2>[^"]*)"\s+src="(?P<src2>[^"]+)")'
    r'\s*/?>',
)


def _extract_image_attrs(m: re.Match) -> tuple[str, str]:
    """Extract (src, alt) from an IMAGE_RE match."""
    src = m.group("src1") or m.group("src2")
    alt = m.group("alt1") or m.group("alt2") or ""
    return src, alt


def _make_relative(abs_path: str, notebook_dir: str) -> str:
    """Convert an absolute image path like /docs/images/... to a path
    relative to the notebook's directory."""
    # Strip leading / to get repo-relative path
    repo_rel = abs_path.lstrip("/")
    return os.path.relpath(repo_rel, notebook_dir)


# --- processing ----------------------------------------------------------

def process_notebook(path: Path, root: Path) -> bool:
    """Process a single notebook. Returns True if the file was modified."""
    data = json.loads(path.read_text(encoding="utf-8"))
    changed = False

    # Directory of this notebook relative to the repo root
    nb_dir = str(path.parent.relative_to(root))

    def fix_md_image(m: re.Match) -> str:
        src, alt = _extract_image_attrs(m)
        rel = _make_relative(src, nb_dir)
        return f"![{alt}]({rel})"

    for i, cell in enumerate(data.get("cells", [])):
        # --- markdown cells: frontmatter, cspell, Image tags ---
        if cell.get("cell_type") == "markdown":
            source = "".join(cell["source"])
            original = source

            # Strip frontmatter from the first markdown cell only
            if i == 0:
                source = FRONTMATTER_RE.sub("", source)

            # Remove cspell directives
            source = CSPELL_RE.sub("", source)

            # Convert <Image> JSX to markdown with relative paths
            source = IMAGE_RE.sub(fix_md_image, source)

            # Also fix existing markdown images with absolute paths
            source = re.sub(
                r"!\[([^\]]*)\]\((/(?:docs|learning)/images/[^)]+)\)",
                lambda m: f"![{m.group(1)}]({_make_relative(m.group(2), nb_dir)})",
                source,
            )

            if source != original:
                cell["source"] = source.splitlines(keepends=True)
                changed = True

        # --- code cell outputs: pre-rendered <Image> tags ---
        for output in cell.get("outputs", []):
            text_plain = output.get("data", {}).get("text/plain", [])
            joined = "".join(text_plain) if isinstance(text_plain, list) else text_plain
            m = IMAGE_RE.search(joined)
            if m:
                src, alt = _extract_image_attrs(m)
                rel = _make_relative(src, nb_dir)
                output["data"]["text/html"] = [f'<img src="{rel}" alt="{alt}" />']
                output["data"].pop("text/plain", None)
                changed = True

    if changed:
        path.write_text(
            json.dumps(data, ensure_ascii=False, indent=1) + "\n",
            encoding="utf-8",
        )
    return changed


def main():
    root = Path(__file__).resolve().parent.parent
    notebooks = sorted(
        list((root / "docs").rglob("*.ipynb"))
        + list((root / "learning").rglob("*.ipynb"))
    )

    modified = 0
    for nb in notebooks:
        if process_notebook(nb, root):
            modified += 1

    print(f"fix-notebooks: processed {len(notebooks)} notebooks, modified {modified}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
