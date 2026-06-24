# CLAUDE.md — llm-judge-summary-agent

このリポジトリは「文章を1文に要約する」要約役エージェントと、「ルーブリックで採点する審査員（LLM-as-Judge）」、そして審査員の採点を合否に変える決定的ゲート（採点係）です。
正解が一つに決まらない出力を、審査員の採点（JSON）＋決まったルールで判定します（採点は LLM・判定は決定的、に分離）。

## 確認のしかた

- `python eval/oracle.py --selftest` … 合否ゲートが正しいか（良い採点=PASS／悪い採点=FAIL）
- `python eval/oracle.py --scores PATH` … 審査員の採点JSON 1件を判定

## いじるときの約束（評価駆動 / EDD）

- 先に eval（合否ゲート）を満たすことを確認してから「完成」とする。雰囲気で done にしない。
- `eval/selftest/*.scores.json` と `eval/corpus/<ケース>/` は採点係の検証用。むやみに変えない。
- Python 標準ライブラリのみ。秘密情報・個人情報・客先コードを入れない。

## ファイルの役割

- `.claude/agents/summary-agent.md` … 要約役エージェントの定義
- `.claude/agents/judge.md` … 審査員（LLM-as-Judge）の定義
- `eval/oracle.py` … 合否ゲート（決定的）／`eval/rubric.md` … 採点基準／`design/design.md` … 設計／`README.md` … 説明
