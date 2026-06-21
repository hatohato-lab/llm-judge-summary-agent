# 採点ルーブリック（要約）

決まった正解が無い「要約」を、次の3軸＋捏造判定で採点する。各軸 0〜5。

| 軸 | 見るところ | 5 | 3 | 0〜1 |
|---|---|---|---|---|
| faithfulness 忠実性 | source の内容だけを述べているか | 完全に忠実 | 概ね忠実だが弱点1つ | 捏造・矛盾あり |
| coverage 網羅性 | いちばん大事な点を捉えているか | 主旨を的確に | 主旨は触れるが一部欠落 | 主旨を外す |
| conciseness 簡潔性 | 1文で無駄なく言えているか | 簡潔で明快 | やや冗長 | 冗長/長すぎ |

加えて hallucination（捏造）を true / false で判定する。source に無い事実が一つでもあれば true。

## 合否ルール（oracle.py が決定的に判定）

- hallucination == false
- かつ faithfulness >= 4
- かつ coverage >= 3
- かつ conciseness >= 3

すべて満たせば PASS。一つでも外れれば FAIL。
