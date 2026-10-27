"""Re-score every system from its raw answers.

Rules (fixed before the scored runs):
- Each answer is the first [...] group in the reply (or the first line if there is none).
- Matrix puzzles: the digits must match the key, in order (unless the key says any order).
- Letter puzzles: the letters must match the key exactly.
- Chess: the first legal move found in the reply must be the key move.
- A system climbs a rung if its share of correct answers on that rung is at least the students' share,
  and it can't skip a rung. The chess puzzle is not part of the ladder or the 42-point total.

Usage:  pip install chess   then   python3 score.py          (table)
                                   python3 score.py --check  (also compare with results/scores.json)
"""
import json, os, re, sys

import chess

HERE = os.path.dirname(os.path.abspath(__file__))
TEST = json.load(open(os.path.join(HERE, "questions", "questions.json")))
KEY = json.load(open(os.path.join(HERE, "questions", "answer_key.json")))
Q = {q["id"]: q for q in TEST["questions"]}


def inner(text):
    m = re.search(r"\[([^\[\]]*)\]", text or "")
    return m.group(1) if m else (text or "").strip().split("\n")[0]


def is_correct(qid, reply):
    q, k = Q[qid], KEY[qid]
    if q["type"] == "chess":
        board = chess.Board(q["fen"])
        for tok in re.findall(r"[KQRBNOa-h0-9x+#=\-]+", (reply or "").replace("1.", " ")):
            tok = tok.strip("+#")
            for parse in (board.parse_san, lambda t: chess.Move.from_uci(t) if chess.Move.from_uci(t) in board.legal_moves else None):
                try:
                    move = parse(tok)
                except Exception:  # noqa: BLE001
                    move = None
                if move:
                    return move.uci() == k["answer_uci"]
        return False
    part = inner(reply)
    if q["type"] == "matrix":
        digits = [int(x) for x in re.findall(r"\d", part)]
        return sorted(digits) == sorted(k["answer"]) if k["any_order"] else digits == list(k["answer"])
    got = part.lower().replace(",", " ").split()
    want = [str(x).lower() for x in k["answer"]]
    if len(got) == 1 and len(want) > 1 and all(len(x) == 1 for x in want):
        got = list(got[0])
    return got == want


def page_answers(text):
    out = {}
    for line in (text or "").split("\n"):
        m = re.match(r"\s*\**\s*(R\d-\d)\s*\**\s*[:.)-]\s*(.*)", line)
        if m:
            out[m.group(1)] = m.group(2)
    return out


def replies(folder):
    """answers/<system>/: one file per question (R1-1.txt …) or one file per page (R1.txt … and C.txt)."""
    r = {}
    for f in sorted(os.listdir(folder)):
        name, text = f[:-4], open(os.path.join(folder, f), encoding="utf-8").read()
        if re.fullmatch(r"R\d-\d|C-1", name):
            r[name] = text
        elif name == "C":
            r["C-1"] = text
        else:
            r.update(page_answers(text))
    return r


def score(folder):
    rep = replies(folder)
    ok = {qid: is_correct(qid, rep.get(qid, "")) for qid in Q}
    rungs, height = {}, 0
    for rung in TEST["rungs"]:
        ids = [q["id"] for q in TEST["questions"] if q["rung"] == rung["rung"]]
        n = sum(ok[i] for i in ids)
        rungs[str(rung["rung"])] = {"correct": n, "of": len(ids), "passed": n / len(ids) >= rung["students_correct"]}
    for rung in TEST["rungs"]:
        if not rungs[str(rung["rung"])]["passed"]:
            break
        height = rung["rung"]
    return {"correct_of_42": sum(v for k, v in ok.items() if Q[k]["type"] != "chess"), "ladder_height": height, "chess_correct": ok["C-1"],
            "rungs": rungs, "per_question": ok}


if __name__ == "__main__":
    base = os.path.join(HERE, "answers")
    published = json.load(open(os.path.join(HERE, "results", "scores.json")))
    bad = 0
    print(f"{'system':16} " + " ".join(f"R{r['rung']}" for r in TEST["rungs"]) + "  /42  rung  chess")
    for name in sorted(os.listdir(base), key=lambda n: (str(published.get(n, {}).get("year", "")), n)):
        s = score(os.path.join(base, name))
        print(f"{name:16} " + " ".join(f"{s['rungs'][str(r['rung'])]['correct']:>2}" for r in TEST["rungs"]) +
              f"  {s['correct_of_42']:>3}  {s['ladder_height']:>4}  {'yes' if s['chess_correct'] else 'no':>5}")
        if "--check" in sys.argv:
            p = published[name]
            if (s["correct_of_42"], s["ladder_height"], s["chess_correct"], s["per_question"]) != (p["correct_of_42"], p["ladder_height"], p["chess_correct"], p["per_question"]):
                bad += 1; print(f"  MISMATCH with results/scores.json: {name}")
    if "--check" in sys.argv:
        print("check:", "all systems match results/scores.json" if not bad else f"{bad} mismatches")
        sys.exit(1 if bad else 0)
