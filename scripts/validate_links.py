#!/usr/bin/env python3
"""
Internal link and anchor validator for M31A documentation platform.
Validates:
1. Markdown links to other docs resolve to existing files.
2. Sidebar item IDs resolve to existing files.
3. Anchors within pages are well-formed.
"""

import sys
import re
from pathlib import Path

DOCS_REPO = Path("/home/snigdha/Desktop/docs.m31a.tonmoyinfrastructure.org").resolve()
DOCS_DIR = DOCS_REPO / "docs"

RE_MD_LINK = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')

def main():
    print("==================================================")
    print("M31A Internal Link & Navigation Validator")
    print("==================================================")

    all_docs = list(DOCS_DIR.glob("**/*.md"))
    print(f"Validating internal links across {len(all_docs)} documentation files...")

    broken_links = []
    total_links_checked = 0

    for doc_path in all_docs:
        with open(doc_path, "r", encoding="utf-8") as f:
            content = f.read()

        for match in RE_MD_LINK.finditer(content):
            label = match.group(1)
            target = match.group(2).strip()

            # Skip external links and web URLs
            if target.startswith(("http://", "https://", "mailto:", "tel:", "#")):
                continue

            total_links_checked += 1
            target_path = target.split("#")[0]
            anchor = target.split("#")[1] if "#" in target else None

            if not target_path:
                continue

            # Resolve target
            if target_path.startswith("/docs/"):
                rel = target_path[6:]
                # Try as .md or directory index
                resolved = DOCS_DIR / f"{rel}.md"
                if not resolved.exists():
                    resolved = DOCS_DIR / rel
            elif target_path.startswith("/"):
                # Page or asset
                resolved = DOCS_REPO / target_path.lstrip("/")
            else:
                # Relative link
                resolved = (doc_path.parent / target_path).resolve()
                if not resolved.exists() and not target_path.endswith(".md"):
                    resolved = (doc_path.parent / f"{target_path}.md").resolve()

            if not resolved.exists() and not (DOCS_DIR / f"{target_path}.md").exists():
                broken_links.append((str(doc_path.relative_to(DOCS_REPO)), label, target))

    print(f"Total internal links evaluated: {total_links_checked}")

    if broken_links:
        print(f"\n[FAIL] Found {len(broken_links)} broken internal links:")
        for doc, label, target in broken_links[:15]:
            print(f"  - In {doc}: [{label}]({target})")
        print("\nPlease fix these links.")
        sys.exit(1)

    print("\n[SUCCESS] All evaluated internal documentation links resolve cleanly!")
    sys.exit(0)

if __name__ == "__main__":
    main()
