# Midterm Exam, Fall 2026: Questions Explained

NOTE - this repo was generated from a within the ../yrClass-f26-aiasd repo. See that repo for related info

# What is this folder?

AI Assisted Software Development (Prof. Y. Rosenthal).

A Quarto book for students. It has the three versions of the midterm exam as they were given, the answers for
every version, and, for Version A, every question with its answer choices: the correct answer in larger bold text,
why each choice is correct or wrong, and background on the material.

The three versions have the same questions and the same answer choices; only the order is different.
`tools/exam.py` checks this every time the pages are built, and the build stops if the versions differ.

## Files

| Path | What it is |
|---|---|
| `exams/` | The three versions as given (Word), and PDFs made from them |
| `exams/source/` | The Markdown source of each version; the pages are built from these |
| `content/key-version-A.json` | The correct answers of Version A. The answers of Versions B and C are worked out from it, by the text of the correct choice |
| `content/explanations/ANN.json` | The explanations for Version A question NN: one per choice, and the background |
| `tools/exam.py` | Reads the versions and checks that they have the same questions and choices |
| `tools/build_pages.py` | Writes `version-a-explained.qmd` (all 45 questions on one page) and `answers-all-versions.qmd` (generated: do not edit them by hand) |
| `index.qmd`, `the-exams.qmd` | The hand-written pages |
| `docs/` | The rendered site, which GitHub Pages serves |

## Build and publish

```bash
./render.sh                 # builds the site into docs/
git add -A && git commit -m "Update the site" && git push
```

GitHub Pages serves the `docs/` folder of the `main` branch.

## Taking the site down

The site is meant to be available for a limited time. To take it down:

```bash
gh api -X DELETE repos/y-rosenthal/yrClass-f26-aiasd-midterm/pages   # turns off GitHub Pages
```

The repository is public, so its files stay readable on GitHub. To remove those too, make the repository private
(`gh repo edit y-rosenthal/yrClass-f26-aiasd-midterm --visibility private --accept-visibility-change-consequences`)
or delete it. Copies that people already downloaded or forked are not removed.

The pages have `<meta name="robots" content="noindex, nofollow">`, so search engines are asked not to list them.
