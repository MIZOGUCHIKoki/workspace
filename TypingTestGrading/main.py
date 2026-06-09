#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
タイピング一括評価プログラム（8分固定・50点満点対応）

使い方：
  python3 typing_evaluator_batch.py original.txt 15 --csv result.csv
  python3 typing_evaluator_batch.py original.txt 15 --pattern "*.txt" --csv result.csv
  python3 typing_evaluator_batch.py original.txt 15 --recursive --csv result.csv
  python3 typing_evaluator_batch.py original.txt 15 --keep-spaces --csv result.csv

original.txt : 元テキスト。LaTeXの \ruby[m]{近年}{きん|ねん} を含むままでOK。
input_dir    : 生徒の入力txtが入っているディレクトリ。
"""

import argparse
import csv
import re
import unicodedata
from pathlib import Path


# 50点満点
FULL_SCORE = 50


def remove_ruby_and_latex(text: str) -> str:
    """LaTeXのrubyと簡単な環境指定を取り除き、本文だけにする。"""
    # \ruby[m]{近年}{きん|ねん} -> 近年
    pattern = r'\\ruby(?:\[[^\]]*\])?\{([^{}]*)\}\{([^{}]*)\}'
    while re.search(pattern, text):
        text = re.sub(pattern, r'\1', text)

    # よく使う環境・設定を削除
    text = re.sub(r'\\begin\{framed\}', '', text)
    text = re.sub(r'\\end\{framed\}', '', text)
    text = re.sub(r'\\setlength\{[^{}]*\}\{[^{}]*\}', '', text)

    # 残ったLaTeXコマンドを軽く除去
    text = re.sub(r'\\[a-zA-Z]+(?:\[[^\]]*\])?', '', text)
    text = text.replace('{', '').replace('}', '')

    return text


def normalize_text(text: str, ignore_spaces: bool = True) -> str:
    """比較しやすいように文字を整える。"""
    text = remove_ruby_and_latex(text)
    text = unicodedata.normalize('NFKC', text)

    if ignore_spaces:
        # 改行・半角空白・全角空白・タブを無視
        text = re.sub(r'[\s\u3000]+', '', text)

    return text


def levenshtein_alignment(original: str, typed: str):
    """編集距離と比較詳細を返す。文字単位で比較する。"""
    n, m = len(original), len(typed)
    dp = [[0] * (m + 1) for _ in range(n + 1)]

    for i in range(n + 1):
        dp[i][0] = i
    for j in range(m + 1):
        dp[0][j] = j

    for i in range(1, n + 1):
        oi = original[i - 1]
        for j in range(1, m + 1):
            cost = 0 if oi == typed[j - 1] else 1
            dp[i][j] = min(
                dp[i - 1][j] + 1,       # delete
                dp[i][j - 1] + 1,       # insert
                dp[i - 1][j - 1] + cost # match/replace
            )

    i, j = n, m
    operations = []

    while i > 0 or j > 0:
        if i > 0 and j > 0:
            cost = 0 if original[i - 1] == typed[j - 1] else 1
            if dp[i][j] == dp[i - 1][j - 1] + cost:
                if cost == 0:
                    operations.append(('match', original[i - 1], typed[j - 1], i, j))
                else:
                    operations.append(('replace', original[i - 1], typed[j - 1], i, j))
                i -= 1
                j -= 1
                continue

        if i > 0 and dp[i][j] == dp[i - 1][j] + 1:
            operations.append(('delete', original[i - 1], '', i, j))
            i -= 1
        else:
            operations.append(('insert', '', typed[j - 1], i, j))
            j -= 1

    operations.reverse()
    return dp[n][m], operations


def evaluate(
    original_text: str,
    typed_text: str,
    minutes: float = 8,
    ignore_spaces: bool = True,
    full_score: float = FULL_SCORE
):
    original = normalize_text(original_text, ignore_spaces=ignore_spaces)
    typed = normalize_text(typed_text, ignore_spaces=ignore_spaces)

    distance, operations = levenshtein_alignment(original, typed)

    original_chars = len(original)
    typed_chars = len(typed)

    correct_chars = sum(1 for op, _, _, _, _ in operations if op == 'match')
    replace_count = sum(1 for op, _, _, _, _ in operations if op == 'replace')
    insert_count = sum(1 for op, _, _, _, _ in operations if op == 'insert')
    delete_count = sum(1 for op, _, _, _, _ in operations if op == 'delete')

    # 正確率：入力した文字のうち、正しかった割合
    accuracy = correct_chars / typed_chars if typed_chars else 0

    # 進捗：元テキスト全体に対してどこまで入力したか
    progress = min(typed_chars / original_chars, 1) if original_chars else 0

    # 速度：正解文字数 ÷ 分
    speed_cpm = correct_chars / minutes if minutes else 0

    # 総合スコア
    score = speed_cpm * accuracy * (0.5 + 0.5 * progress)

    # 理論上の最大スコア
    # 全文を正確に打った場合：
    # speed_cpm = original_chars / minutes
    # accuracy = 1
    # progress = 1
    # score = original_chars / minutes
    max_score = original_chars / minutes if minutes and original_chars else 0

    # 50点満点などに換算
    if max_score > 0:
        point = min(score / max_score, 1.0) * full_score
    else:
        point = 0

    return {
        '元テキスト文字数': original_chars,
        '入力文字数': typed_chars,
        '正解文字数': correct_chars,
        '正確率': accuracy,
        '正確率_percent': accuracy * 100,
        '進捗': progress,
        '進捗_percent': progress * 100,
        '速度_CPM': speed_cpm,
        '総合スコア': score,
        '得点': point,
        '満点': full_score,
        '編集距離': distance,
        '置換ミス数': replace_count,
        '余分な文字数': insert_count,
        '抜けた文字数': delete_count,
    }


def read_text_safely(path: Path) -> str:
    """UTF-8優先。失敗したらShift_JIS系も試す。"""
    encodings = ['utf-8', 'utf-8-sig', 'cp932', 'shift_jis']
    last_error = None

    for enc in encodings:
        try:
            return path.read_text(encoding=enc)
        except UnicodeDecodeError as e:
            last_error = e

    raise last_error


def collect_files(input_dir: Path, pattern: str = '*.txt', recursive: bool = False):
    if recursive:
        files = sorted(input_dir.rglob(pattern))
    else:
        files = sorted(input_dir.glob(pattern))

    return [p for p in files if p.is_file()]


def main():
    parser = argparse.ArgumentParser(
        description='ディレクトリ内の入力txtを一括でタイピング評価してCSV出力します。'
    )

    parser.add_argument(
        'original_file',
        help='元テキストファイル。ruby付きLaTeXでも可。'
    )

    parser.add_argument(
        'input_dir',
        help='生徒の入力txtが入っているディレクトリ。例: 15'
    )

    parser.add_argument(
        '--csv',
        default='typing_results.csv',
        help='出力CSV名。初期値: typing_results.csv'
    )

    parser.add_argument(
        '--minutes',
        type=float,
        default=8,
        help='制限時間。初期値は8分。'
    )

    parser.add_argument(
        '--full-score',
        type=float,
        default=FULL_SCORE,
        help='満点。初期値は50点。'
    )

    parser.add_argument(
        '--pattern',
        default='*.txt',
        help='対象ファイルのパターン。初期値: *.txt'
    )

    parser.add_argument(
        '--recursive',
        action='store_true',
        help='サブディレクトリ内も対象にする。'
    )

    parser.add_argument(
        '--keep-spaces',
        action='store_true',
        help='空白・改行も評価対象にする。'
    )

    args = parser.parse_args()

    original_path = Path(args.original_file)
    input_dir = Path(args.input_dir)
    csv_path = Path(args.csv)

    if not original_path.is_file():
        raise FileNotFoundError(f'元テキストファイルが見つかりません: {original_path}')

    if not input_dir.is_dir():
        raise NotADirectoryError(f'入力ディレクトリが見つかりません: {input_dir}')

    original_text = read_text_safely(original_path)
    files = collect_files(input_dir, pattern=args.pattern, recursive=args.recursive)

    if not files:
        print(f'対象ファイルがありません: {input_dir} / pattern={args.pattern}')
        return

    fieldnames = [
        'ファイル名',
        '相対パス',
        '元テキスト文字数',
        '入力文字数',
        '正解文字数',
        '正確率',
        '正確率_percent',
        '進捗',
        '進捗_percent',
        '速度_CPM',
        '総合スコア',
        '得点',
        '満点',
        '編集距離',
        '置換ミス数',
        '余分な文字数',
        '抜けた文字数',
    ]

    rows = []

    for file_path in files:
        try:
            typed_text = read_text_safely(file_path)

            result = evaluate(
                original_text,
                typed_text,
                minutes=args.minutes,
                ignore_spaces=not args.keep_spaces,
                full_score=args.full_score,
            )

            row = {
                'ファイル名': file_path.name,
                '相対パス': str(file_path.relative_to(input_dir)),
                **result,
            }

            rows.append(row)

            print(
                f'OK: {file_path.name} / '
                f'正確率 {result["正確率_percent"]:.2f}% / '
                f'進捗 {result["進捗_percent"]:.2f}% / '
                f'速度 {result["速度_CPM"]:.2f} / '
                f'得点 {result["得点"]:.2f}/{result["満点"]:.0f}'
            )

        except Exception as e:
            # 失敗したファイルもCSVに残す
            row = {name: '' for name in fieldnames}
            row['ファイル名'] = file_path.name
            row['相対パス'] = str(file_path.relative_to(input_dir))
            row['総合スコア'] = f'ERROR: {e}'
            rows.append(row)

            print(f'ERROR: {file_path.name} / {e}')

    with csv_path.open('w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print()
    print(f'完了: {len(rows)}件をCSVに出力しました -> {csv_path}')


if __name__ == '__main__':
    main()