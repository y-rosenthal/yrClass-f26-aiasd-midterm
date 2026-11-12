#!/usr/bin/env bash
# Build the site into docs/ (GitHub Pages serves docs/ on the main branch).
#   1. write the question pages from the exams and content/explanations/
#   2. render the Quarto book
#   3. add docs/.nojekyll, so that GitHub Pages serves the files as they are
# Usage: ./render.sh        Needs: python3, quarto
set -euo pipefail
cd "$(dirname "$0")"
if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then sed -n 2,6p "$0"; exit 0; fi
python3 tools/build_pages.py
rm -rf tools/__pycache__
quarto render
touch docs/.nojekyll
echo "Site built in docs/. Commit and push to publish."
