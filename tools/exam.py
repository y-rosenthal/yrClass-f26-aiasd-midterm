"""Read the three exam versions (exams/source/*.md) and the Version A answers (content/key-version-A.json).

QUESTIONS[v][q]  dict(stem=..., stem_md=..., options={"a": ...} | None, options_md=..., table=[(item, choice)] | None)
KEYS[v][q]       correct answer: "a".."e", or for matching "1A, 2G, 3C, 4E, 5B"
SAME[q]          for Version A question q: {"A": q, "B": its number in Version B, "C": its number in Version C}

Only Version A's key is stored. The keys for Versions B and C are worked out from it by the text of the
correct choice, so the three versions cannot disagree. check() verifies that the three versions have the
same questions and the same choices, and that only the order differs.
Run:  python tools/exam.py
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "exams" / "source"


def _clean(s):
    s = s.replace("\\_", "_").replace("\\.", ".").replace("\\*", "*").replace("\\", "")
    s = re.sub(r"\*\*(.+?)\*\*", r"\1", s)
    s = re.sub(r"`(.+?)`", r"\1", s)
    return re.sub(r"\s+", " ", s).strip()


def _load_questions(v):
    text = (SRC / f"midterm-f26-version-{v}.md").read_text()
    out, cur = {}, None
    for line in text.replace("\xa0", " ").splitlines():
        m = re.match(r"\*\*(\d+)\.\*\*\s+(.*)", line)
        if m:
            cur = int(m.group(1))
            out[cur] = dict(stem=_clean(m.group(2)), stem_md=m.group(2).strip(), options=None, options_md=None,
                            table=None)
            continue
        if cur is None:
            continue
        m = re.match(r"([a-e])\\?\.\s+(.*)", line)
        if m:
            if out[cur]["options"] is None:
                out[cur]["options"], out[cur]["options_md"] = {}, {}
            out[cur]["options"][m.group(1)] = _clean(m.group(2))
            out[cur]["options_md"][m.group(1)] = m.group(2).strip()
            continue
        if line.startswith("| ") and not line.startswith("| Item") and not line.startswith("|--"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if out[cur]["table"] is None:
                out[cur]["table"] = []
            out[cur]["table"].append((_clean(cells[0]), _clean(cells[2])))
            continue
        if (line.strip() and not line.startswith(":::") and not line.startswith("|")
                and out[cur]["options"] is None and out[cur]["table"] is None):
            out[cur]["stem"] += " " + _clean(line)
            out[cur]["stem_md"] += "\n" + line.strip()
    assert len(out) == 45, (v, len(out))
    return out


def split_label(s):
    """'1. Jailbreak' -> ('1', 'Jailbreak');  'A. A prompt ...' -> ('A', 'A prompt ...')"""
    a, b = s.split(". ", 1)
    return a, b


QUESTIONS = {v: _load_questions(v) for v in "ABC"}
KEY_A = {int(q): a for q, a in json.loads((ROOT / "content" / "key-version-A.json").read_text()).items()}

SAME = {}
for _qa, _Qa in QUESTIONS["A"].items():
    SAME[_qa] = {"A": _qa}
    for _v in "BC":
        _hits = [q for q, Q in QUESTIONS[_v].items() if Q["stem"] == _Qa["stem"]]
        assert len(_hits) == 1, (_v, _qa, _hits)
        SAME[_qa][_v] = _hits[0]

KEYS = {"A": dict(KEY_A), "B": {}, "C": {}}
for _qa, _Qa in QUESTIONS["A"].items():
    for _v in "BC":
        _q = SAME[_qa][_v]
        _Q = QUESTIONS[_v][_q]
        if _Qa["options"]:
            _right = _Qa["options"][KEY_A[_qa]]
            KEYS[_v][_q] = next(k for k, o in _Q["options"].items() if o == _right)
        else:
            _items_a = dict(split_label(i) for i, _ in _Qa["table"] if i)
            _ch_a = dict(split_label(c) for _, c in _Qa["table"])
            _pairs = {_items_a[n]: _ch_a[l] for n, l in re.findall(r"(\d)([A-G])", KEY_A[_qa])}
            _items_v = {t: n for n, t in (split_label(i) for i, _ in _Q["table"] if i)}
            _ch_v = {t: l for l, t in (split_label(c) for _, c in _Q["table"])}
            KEYS[_v][_q] = ", ".join(f"{n}{_ch_v[_pairs[t]]}"
                                    for t, n in sorted(_items_v.items(), key=lambda x: x[1]))


def check():
    """The three versions have the same 45 questions and the same choices; only the order differs."""
    problems = []
    for qa, m in SAME.items():
        Qs = {v: QUESTIONS[v][q] for v, q in m.items()}
        if Qs["A"]["options"]:
            if not (sorted(Qs["A"]["options"].values()) == sorted(Qs["B"]["options"].values())
                    == sorted(Qs["C"]["options"].values())):
                problems.append(f"A{qa}: the choices differ between versions")
        else:
            for part in (0, 1):
                sets = [sorted(split_label(r[part])[1] for r in Qs[v]["table"] if r[part]) for v in "ABC"]
                if not (sets[0] == sets[1] == sets[2]):
                    problems.append(f"A{qa}: the matching {'items' if part == 0 else 'choices'} differ")
    for v in "BC":
        if sorted(SAME[q][v] for q in SAME) != list(range(1, 46)):
            problems.append(f"Version {v} does not have each question exactly once")
    return problems


if __name__ == "__main__":
    print("problems:", check() or "none")
