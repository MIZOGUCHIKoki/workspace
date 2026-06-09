#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
out/result_*.csv を読み込み、学生ごと・クラスごとにグラフ化する。

出力ファイル名は クラス-学生ID.png にする。

例：
  graphs/13-25.247.png
  graphs/14-25.286.png
  graphs/15-25.301.png

使い方：
  python3 graph.py

入力：
  out/result_*.csv

出力：
  graphs/13-25.247.png
  graphs/14-25.246.png
  graphs/15-25.301.png
  graphs/summary_scores.png
  graphs/student_summary.csv
  graphs/all_results_merged.csv
"""

import argparse
import re
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import pandas as pd


def setup_japanese_font():
    """
    Matplotlibで日本語が文字化けしないようにフォントを設定する。
    macOSなら Hiragino Sans が見つかることが多い。
    """
    candidate_fonts = [
        "Hiragino Sans",
        "Hiragino Kaku Gothic ProN",
        "Yu Gothic",
        "YuGothic",
        "Meiryo",
        "Noto Sans CJK JP",
        "Noto Sans JP",
        "IPAexGothic",
        "IPAGothic",
        "TakaoGothic",
    ]

    available_fonts = {f.name for f in fm.fontManager.ttflist}

    for font_name in candidate_fonts:
        if font_name in available_fonts:
            plt.rcParams["font.family"] = font_name
            print(f"使用フォント: {font_name}")
            break
    else:
        print("日本語フォントが見つかりませんでした。文字化けする可能性があります。")

    # マイナス記号の文字化け対策
    plt.rcParams["axes.unicode_minus"] = False


def read_csv_safely(path: Path) -> pd.DataFrame:
    """UTF-8 BOM付きCSVを優先して読む。"""
    encodings = ["utf-8-sig", "utf-8", "cp932", "shift_jis"]
    last_error = None

    for enc in encodings:
        try:
            return pd.read_csv(path, encoding=enc)
        except UnicodeDecodeError as e:
            last_error = e

    raise last_error


def extract_student_id(file_name: str) -> str:
    """
    ファイル名から学生IDを取り出す。

    例：
      25.246.txt       -> 25.246
      mtdm25.246.txt   -> 25.246
      abc25.310.txt    -> 25.310
    """
    m = re.search(r"(\d{2}\.\d{3})", str(file_name))
    if m:
        return m.group(1)

    return Path(str(file_name)).stem


def extract_class_id(folder_name: str) -> str:
    """
    フォルダ名からクラス番号を取り出す。

    例：
      1-05-29-13 -> 13
      1-06-05-14 -> 14
      1-exam-15  -> 15
    """
    name = str(folder_name)

    m = re.search(r"-(\d+)$", name)
    if m:
        return m.group(1)

    return "unknown"


def folder_sort_key(folder_name: str):
    """
    フォルダ名を時系列順に並べる。

    希望順：
      exam -> 日付順

    例：
      1-exam-13
      1-05-29-13
      1-06-02-13
      1-06-05-13
    """
    name = str(folder_name)

    body = re.sub(r"^\d+-", "", name)

    # exam を最初にする
    m = re.match(r"^exam-(\d+)$", body)
    if m:
        class_id = m.group(1)
        return (0, int(class_id), 0, 0, body)

    # 日付系を exam の後にする
    m = re.match(r"^(\d{2})-(\d{2})-(\d+)$", body)
    if m:
        month, day, class_id = m.groups()
        return (1, int(month), int(day), int(class_id), body)

    return (9, body)


def load_all_results(input_dir: Path) -> pd.DataFrame:
    """out/result_*.csv をすべて結合する。"""
    csv_files = sorted(input_dir.glob("result_*.csv"))

    if not csv_files:
        raise FileNotFoundError(f"CSVファイルが見つかりません: {input_dir}/result_*.csv")

    dfs = []

    for csv_file in csv_files:
        df = read_csv_safely(csv_file)
        df["結果CSV"] = csv_file.name
        dfs.append(df)

    all_df = pd.concat(dfs, ignore_index=True)

    required_columns = [
        "フォルダ名",
        "ファイル名",
        "得点",
        "正確率_percent",
        "進捗_percent",
        "速度_CPM",
    ]

    missing = [c for c in required_columns if c not in all_df.columns]
    if missing:
        raise ValueError(f"必要な列がありません: {missing}")

    numeric_columns = [
        "元テキスト文字数",
        "入力文字数",
        "正解文字数",
        "正確率",
        "正確率_percent",
        "進捗",
        "進捗_percent",
        "速度_CPM",
        "総合スコア",
        "得点",
        "満点",
        "編集距離",
        "置換ミス数",
        "余分な文字数",
        "抜けた文字数",
    ]

    for col in numeric_columns:
        if col in all_df.columns:
            all_df[col] = pd.to_numeric(all_df[col], errors="coerce")

    # 学生IDを作る
    # 例：25.247.txt -> 25.247
    #     mtdm25.247.txt -> 25.247
    all_df["学生ID"] = all_df["ファイル名"].map(extract_student_id)

    # クラスを作る
    # 例：1-05-29-13 -> 13
    #     1-exam-14 -> 14
    all_df["クラス"] = all_df["フォルダ名"].map(extract_class_id)

    # グラフIDを作る
    # 例：13-25.247
    all_df["グラフID"] = all_df["クラス"].astype(str) + "-" + all_df["学生ID"].astype(str)

    # 並び替え用
    all_df["フォルダ順"] = all_df["フォルダ名"].map(folder_sort_key)

    all_df = all_df.sort_values(
        ["クラス", "学生ID", "フォルダ順"]
    ).reset_index(drop=True)

    return all_df

def save_student_graph(student_df: pd.DataFrame, output_dir: Path):
    """1人分の推移グラフをPNGで保存する。"""

    # 念のため、個人ごとのデータも時系列順に並べ直す
    student_df = student_df.sort_values("フォルダ順").reset_index(drop=True)

    graph_id = str(student_df["グラフID"].iloc[0])

    class_id = str(student_df["クラス"].iloc[0])
    student_id = str(student_df["学生ID"].iloc[0])

    labels = student_df["フォルダ名"].astype(str).tolist()
    x = list(range(len(labels)))

    fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

    # 上段：得点
    axes[0].plot(x, student_df["得点"], marker="o", label="得点")
    axes[0].set_title(f"{graph_id}：得点の推移")
    axes[0].set_ylabel("得点 / 50")
    axes[0].set_ylim(0, 50)
    axes[0].grid(True)
    axes[0].legend()

    # 下段：正確率・進捗・速度
    axes[1].plot(x, student_df["正確率_percent"], marker="o", label="正確率(%)")
    axes[1].plot(x, student_df["進捗_percent"], marker="o", label="進捗(%)")
    axes[1].plot(x, student_df["速度_CPM"], marker="o", label="速度(CPM)")
    axes[1].set_title(f"{graph_id}：正確率・進捗・速度の推移")
    axes[1].set_ylabel("値")
    axes[1].set_xticks(x)
    axes[1].set_xticklabels(labels, rotation=45, ha="right")
    axes[1].grid(True)
    axes[1].legend()

    fig.tight_layout()

    # ここで 13-25.247.png のように保存する
    safe_name = graph_id.replace("/", "_").replace("\\", "_")
    output_path = output_dir / f"{safe_name}.png"

    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)

    return output_path


def save_summary_graph(all_df: pd.DataFrame, output_dir: Path):
    """全員の最新得点まとめグラフを保存する。"""
    sorted_df = all_df.sort_values(["クラス", "学生ID", "フォルダ順"])

    latest_df = (
        sorted_df
        .groupby("グラフID", as_index=False)
        .tail(1)
        .sort_values(["クラス", "得点"], ascending=[True, False])
    )

    labels = latest_df["グラフID"].astype(str).tolist()
    scores = latest_df["得点"].tolist()
    x = list(range(len(labels)))

    fig, ax = plt.subplots(figsize=(16, 7))
    ax.bar(x, scores)
    ax.set_title("全員の最新得点")
    ax.set_ylabel("得点 / 50")
    ax.set_ylim(0, 50)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=90)
    ax.grid(True, axis="y")

    fig.tight_layout()

    output_path = output_dir / "summary_scores.png"
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)

    return output_path


def save_class_summary_graphs(all_df: pd.DataFrame, output_dir: Path):
    """クラスごとの最新得点まとめグラフを保存する。"""
    output_paths = []

    sorted_df = all_df.sort_values(["クラス", "学生ID", "フォルダ順"])

    latest_df = (
        sorted_df
        .groupby("グラフID", as_index=False)
        .tail(1)
    )

    for class_id, class_df in latest_df.groupby("クラス"):
        class_df = class_df.sort_values("得点", ascending=False)

        labels = class_df["グラフID"].astype(str).tolist()
        scores = class_df["得点"].tolist()
        x = list(range(len(labels)))

        fig, ax = plt.subplots(figsize=(14, 7))
        ax.bar(x, scores)
        ax.set_title(f"{class_id}組：最新得点")
        ax.set_ylabel("得点 / 50")
        ax.set_ylim(0, 50)
        ax.set_xticks(x)
        ax.set_xticklabels(labels, rotation=90)
        ax.grid(True, axis="y")

        fig.tight_layout()

        output_path = output_dir / f"summary_scores_class_{class_id}.png"
        fig.savefig(output_path, dpi=150, bbox_inches="tight")
        plt.close(fig)

        output_paths.append(output_path)

    return output_paths


def save_student_summary_csv(all_df: pd.DataFrame, output_dir: Path):
    """学生ごとの平均・最高・最新得点をCSVで保存する。"""
    sorted_df = all_df.sort_values(["クラス", "学生ID", "フォルダ順"])

    latest_df = (
        sorted_df
        .groupby("グラフID", as_index=False)
        .tail(1)
        [["グラフID", "クラス", "学生ID", "フォルダ名", "得点"]]
        .rename(columns={
            "フォルダ名": "最新フォルダ",
            "得点": "最新得点",
        })
    )

    summary_df = (
        all_df
        .groupby(["グラフID", "クラス", "学生ID"], as_index=False)
        .agg(
            回数=("得点", "count"),
            平均得点=("得点", "mean"),
            最高得点=("得点", "max"),
            最低得点=("得点", "min"),
            平均正確率_percent=("正確率_percent", "mean"),
            平均進捗_percent=("進捗_percent", "mean"),
            平均速度_CPM=("速度_CPM", "mean"),
        )
    )

    summary_df = summary_df.merge(
        latest_df,
        on=["グラフID", "クラス", "学生ID"],
        how="left",
    )

    summary_df = summary_df.sort_values(
        ["クラス", "最新得点"],
        ascending=[True, False],
    )

    output_path = output_dir / "student_summary.csv"
    summary_df.to_csv(output_path, index=False, encoding="utf-8-sig")

    return output_path


def save_class_summary_csv(all_df: pd.DataFrame, output_dir: Path):
    """クラスごとの集計CSVを保存する。"""
    class_summary_df = (
        all_df
        .groupby("クラス", as_index=False)
        .agg(
            人数=("グラフID", "nunique"),
            データ件数=("得点", "count"),
            平均得点=("得点", "mean"),
            最高得点=("得点", "max"),
            最低得点=("得点", "min"),
            平均正確率_percent=("正確率_percent", "mean"),
            平均進捗_percent=("進捗_percent", "mean"),
            平均速度_CPM=("速度_CPM", "mean"),
        )
        .sort_values("クラス")
    )

    output_path = output_dir / "class_summary.csv"
    class_summary_df.to_csv(output_path, index=False, encoding="utf-8-sig")

    return output_path


def main():
    setup_japanese_font()

    parser = argparse.ArgumentParser(
        description="out/result_*.csv を読み込み、クラス-学生IDごとのグラフを作成します。"
    )

    parser.add_argument(
        "--input-dir",
        default="out",
        help="result_*.csv が入っているディレクトリ。初期値: out",
    )

    parser.add_argument(
        "--output-dir",
        default="graphs",
        help="グラフの出力先ディレクトリ。初期値: graphs",
    )

    args = parser.parse_args()

    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    all_df = load_all_results(input_dir)

    # 結合CSV
    merged_csv = output_dir / "all_results_merged.csv"
    all_df.drop(columns=["フォルダ順"], errors="ignore").to_csv(
        merged_csv,
        index=False,
        encoding="utf-8-sig",
    )

    created_files = []

    # クラス-学生IDごとにグラフ作成
    for graph_id, student_df in all_df.groupby("グラフID"):
        output_path = save_student_graph(student_df, output_dir)
        created_files.append(output_path)
        print(f"作成: {output_path}")

    # 全体まとめ
    summary_graph = save_summary_graph(all_df, output_dir)

    # クラス別まとめグラフ
    class_summary_graphs = save_class_summary_graphs(all_df, output_dir)

    # 学生別集計CSV
    student_summary_csv = save_student_summary_csv(all_df, output_dir)

    # クラス別集計CSV
    class_summary_csv = save_class_summary_csv(all_df, output_dir)

    print()
    print(f"結合CSV: {merged_csv}")
    print(f"全体グラフ: {summary_graph}")

    for path in class_summary_graphs:
        print(f"クラス別グラフ: {path}")

    print(f"学生別集計CSV: {student_summary_csv}")
    print(f"クラス別集計CSV: {class_summary_csv}")
    print(f"完了: 学生別グラフ {len(created_files)} 件を作成しました。")


if __name__ == "__main__":
    main()