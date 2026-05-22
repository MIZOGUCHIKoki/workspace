#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
typing_evaluator_batch.py の動作確認テスト

使い方：
  1) typing_evaluator_batch.py とこのファイルを同じフォルダに置く
  2) 次を実行

     python3 test_typing_evaluator_batch.py

pytest が入っている場合は以下でも可：

     pytest test_typing_evaluator_batch.py

このテストで確認すること：
  - ruby付きLaTeXから本文だけを取り出せる
  - 空白・改行を無視して比較できる
  - 完全一致のとき、正確率100%、進捗100%、速度=文字数/8 になる
  - 間違いがある入力で、正確率・編集距離・ミス数が妥当に出る
  - ディレクトリ内の複数txtを一括評価してCSV出力できる
  - Shift_JIS/cp932の入力ファイルも読める
"""

import csv
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import typing_evaluator as teb


ORIGINAL_LATEX = r"""
\begin{framed}\setlength{\baselineskip}{3em}
\ruby[m]{近年}{きん|ねん}、\ruby[m]{私}{わたし}たちの\ruby[m]{生活}{せい|かつ}の\ruby[m]{中}{なか}で\ruby[m]{情報機器}{じょう|ほう|き|き}の\ruby[m]{役割}{やく|わり}はますます\ruby[m]{大}{おお}きくなっている。
\end{framed}
"""

ORIGINAL_PLAIN = "近年、私たちの生活の中で情報機器の役割はますます大きくなっている。"


class TestTypingEvaluatorBatchFunctions(unittest.TestCase):

    def test_remove_ruby_and_latex(self):
        actual = teb.normalize_text(ORIGINAL_LATEX, ignore_spaces=True)
        self.assertEqual(actual, ORIGINAL_PLAIN)

    def test_ignore_spaces_and_newlines(self):
        typed = "近年、 私たちの生活の中で\n情報機器の役割はますます大きくなっている。"
        result = teb.evaluate(ORIGINAL_LATEX, typed, minutes=8, ignore_spaces=True)

        self.assertEqual(result["元テキスト文字数"], len(ORIGINAL_PLAIN))
        self.assertEqual(result["入力文字数"], len(ORIGINAL_PLAIN))
        self.assertEqual(result["正解文字数"], len(ORIGINAL_PLAIN))
        self.assertAlmostEqual(result["正確率"], 1.0)
        self.assertAlmostEqual(result["進捗"], 1.0)
        self.assertAlmostEqual(result["速度_CPM"], len(ORIGINAL_PLAIN) / 8)
        self.assertEqual(result["編集距離"], 0)

    def test_exact_match_metrics(self):
        result = teb.evaluate(ORIGINAL_LATEX, ORIGINAL_PLAIN, minutes=8, ignore_spaces=True)

        self.assertEqual(result["元テキスト文字数"], len(ORIGINAL_PLAIN))
        self.assertEqual(result["入力文字数"], len(ORIGINAL_PLAIN))
        self.assertEqual(result["正解文字数"], len(ORIGINAL_PLAIN))
        self.assertAlmostEqual(result["正確率_percent"], 100.0)
        self.assertAlmostEqual(result["進捗_percent"], 100.0)
        self.assertAlmostEqual(result["速度_CPM"], len(ORIGINAL_PLAIN) / 8)
        self.assertGreater(result["総合スコア"], 0)
        self.assertEqual(result["置換ミス数"], 0)
        self.assertEqual(result["余分な文字数"], 0)
        self.assertEqual(result["抜けた文字数"], 0)

    def test_typo_metrics_are_reasonable(self):
        # 「近年」→「今年」に置換1件、「情報機器」→「情報機」なので抜け1件
        typed = "今年、私たちの生活の中で情報機の役割はますます大きくなっている。"
        result = teb.evaluate(ORIGINAL_LATEX, typed, minutes=8, ignore_spaces=True)

        self.assertLess(result["正確率"], 1.0)
        self.assertLess(result["正解文字数"], len(ORIGINAL_PLAIN))
        self.assertGreaterEqual(result["編集距離"], 1)
        self.assertGreaterEqual(result["置換ミス数"] + result["抜けた文字数"] + result["余分な文字数"], 1)
        self.assertAlmostEqual(result["速度_CPM"], result["正解文字数"] / 8)

    def test_read_text_safely_cp932(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "cp932.txt"
            p.write_text(ORIGINAL_PLAIN, encoding="cp932")
            self.assertEqual(teb.read_text_safely(p), ORIGINAL_PLAIN)


class TestTypingEvaluatorBatchCli(unittest.TestCase):

    def test_batch_cli_outputs_csv(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            script = Path(teb.__file__).resolve()

            original_file = tmp / "original.txt"
            input_dir = tmp / "15"
            csv_file = tmp / "result_15.csv"
            input_dir.mkdir()

            original_file.write_text(ORIGINAL_LATEX, encoding="utf-8")
            (input_dir / "25.247.txt").write_text(ORIGINAL_PLAIN, encoding="utf-8")
            (input_dir / "25.257.txt").write_text("近年、私たちの生活の中で情報機器の役割", encoding="utf-8")

            completed = subprocess.run(
                [
                    sys.executable,
                    str(script),
                    str(original_file),
                    str(input_dir),
                    "--csv",
                    str(csv_file),
                ],
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(completed.returncode, 0, msg=completed.stderr + completed.stdout)
            self.assertTrue(csv_file.exists())

            with csv_file.open("r", encoding="utf-8-sig", newline="") as f:
                rows = list(csv.DictReader(f))

            self.assertEqual(len(rows), 2)
            self.assertEqual(rows[0]["ファイル名"], "25.247.txt")
            self.assertEqual(rows[1]["ファイル名"], "25.257.txt")

            # 完全一致ファイルは100%になるはず
            exact = rows[0]
            self.assertAlmostEqual(float(exact["正確率_percent"]), 100.0)
            self.assertAlmostEqual(float(exact["進捗_percent"]), 100.0)
            self.assertAlmostEqual(float(exact["速度_CPM"]), len(ORIGINAL_PLAIN) / 8)

            # 途中までのファイルは進捗が100%未満になるはず
            partial = rows[1]
            self.assertLess(float(partial["進捗_percent"]), 100.0)
            self.assertGreater(float(partial["正確率_percent"]), 0.0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
