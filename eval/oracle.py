#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
oracle.py — LLM-as-Judge 型の「判定ゲート」（決定的）。

要約のように決まった正解が無い出力は、LLM 審査員（judge.md）がルーブリックで採点する。
その採点（JSON）を、ここで決定的な合否ルールに通す。＝「採点はLLM・判定は決定的」に分離。
同じ採点なら、何度走らせても同じ合否になる（再現可能）。

合否ルール（pass）:
  hallucination == false かつ faithfulness>=4 かつ coverage>=3 かつ conciseness>=3

使い方:
  python oracle.py --scores PATH   # 採点JSON 1件を判定
  python oracle.py --selftest      # 判定ルールを検証（良い採点→PASS / 悪い採点→FAIL）

終了コード: PASS（または selftest が期待どおり）で 0、それ以外 1。
"""
import argparse
import json
import sys
from pathlib import Path

EVAL_DIR = Path(__file__).resolve().parent
REQUIRED = ["faithfulness", "coverage", "conciseness", "hallucination"]


def verdict(scores):
    reasons = []
    if scores.get("hallucination") is True:
        reasons.append("hallucination=true")
    if scores.get("faithfulness", 0) < 4:
        reasons.append(f"faithfulness {scores.get('faithfulness')}<4")
    if scores.get("coverage", 0) < 3:
        reasons.append(f"coverage {scores.get('coverage')}<3")
    if scores.get("conciseness", 0) < 3:
        reasons.append(f"conciseness {scores.get('conciseness')}<3")
    return ("PASS", "ok") if not reasons else ("FAIL", " / ".join(reasons))


def load(path):
    d = json.loads(Path(path).read_text(encoding="utf-8"))
    miss = [k for k in REQUIRED if k not in d]
    if miss:
        raise ValueError("採点JSONに不足キー: " + ",".join(miss))
    return d


def grade_one(path):
    try:
        d = load(path)
    except Exception as e:
        return ("FAIL", f"読込/検証失敗: {e}")
    return verdict(d)


def print_table(rows, title):
    print(f"\n### {title}")
    print("| 対象 | 判定 | 理由 |")
    print("|---|---|---|")
    for name, v, detail in rows:
        print(f"| {name} | {v} | {detail} |")


def selftest():
    print("# 判定ゲート自己検証 — LLM-as-Judge")
    sd = EVAL_DIR / "selftest"
    expect = {
        "good.scores.json": "PASS",
        "bad_faithfulness.scores.json": "FAIL",
        "bad_conciseness.scores.json": "FAIL",
    }
    rows, ok_all = [], True
    for fname, exp in expect.items():
        v, detail = grade_one(sd / fname)
        ok = (v == exp)
        ok_all = ok_all and ok
        rows.append((fname, v, f"期待={exp} {'OK' if ok else 'NG'} / {detail}"))
    print_table(rows, "良い採点→PASS・悪い採点→FAIL であるべき")
    print(f"\n## ゲート判定: {'PASS（合否ルールは妥当）' if ok_all else 'FAIL（ルールに欠陥）'}")
    return ok_all


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scores", help="採点JSONのパス")
    ap.add_argument("--selftest", action="store_true", help="判定ルールを検証")
    a = ap.parse_args()
    if a.selftest:
        sys.exit(0 if selftest() else 1)
    if a.scores:
        v, detail = grade_one(a.scores)
        print_table([(Path(a.scores).name, v, detail)], "採点JSONの判定")
        sys.exit(0 if v == "PASS" else 1)
    ap.print_help()
    sys.exit(2)


if __name__ == "__main__":
    main()
