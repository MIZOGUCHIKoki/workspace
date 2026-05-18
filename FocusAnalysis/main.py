import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ==========================================
# 0. 抽出期間の設定（追加）
# ==========================================
# 集計したい期間を指定してください（YYYY-MM-DD 形式、None の場合は制限なし）
START_DATE = "2026-04-01"
END_DATE   = "2026-05-18"

# 指定のファイル名に設定
FOCUS_DATA = "focus.csv"
SLEEP_DATA = "sleep.csv"
CLASS_DATA = "class.csv"
EXCLUDE_DATA = "exclude_days.csv"

# 日本語フォント設定
plt.rcParams["font.family"] = "Hiragino Sans"
sns.set_theme(style="whitegrid", font="Hiragino Sans")

# ==========================================
# 1. データの読み込みと前処理
# ==========================================
print("\n" + "="*50)
print("🔍 ライフサイクル・データ統合 & 整合性チェック開始")
print("="*50)

# --- A. 除外スケジュールの読み込みと日付の展開 ---
try:
    df_ex = pd.read_csv(EXCLUDE_DATA)
    exclude_map = {}
    for idx, row in df_ex.iterrows():
        date_range = pd.date_range(start=row["始めの日付"], end=row["終わりの日付"], freq="D")
        for d in date_range:
            exclude_map[d.strftime("%Y-%m-%d")] = row["理由"]
    
    print("--- ①【Exclude（除外）ログ】 ---")
    print(f"■ exclude_days.csv から以下の日程を計算から完全に除外しました:")
    for d, reason in sorted(exclude_map.items()):
        print(f"  [除外日] {d} ➔ 理由: {reason}")
except Exception as e:
    print("⚠️ 除外ファイル(exclude_days.csv)のロードに失敗、または存在しません。除外なしで続行します。")
    exclude_map = {}

# 各種データの読み込み
df_tasks = pd.read_csv(FOCUS_DATA)
df_tasks["start"] = pd.to_datetime(df_tasks["start"])
df_tasks["end"] = df_tasks["start"] + pd.to_timedelta(df_tasks["secPassed"], unit="s")

df_sleep = pd.read_csv(SLEEP_DATA)
df_sleep["就寝時間"] = pd.to_datetime(df_sleep["就寝時間"])
df_sleep["起床時間"] = pd.to_datetime(df_sleep["起床時間"])

df_class_list = pd.read_csv(CLASS_DATA)
df_class_list["start_dt"] = pd.to_datetime(df_class_list["日付"] + " " + df_class_list["始めの時刻"])
df_class_list["end_dt"] = pd.to_datetime(df_class_list["日付"] + " " + df_class_list["終わりの時刻"])

# --- 期間フィルターの適用（追加） ---
if START_DATE:
    start_dt = pd.to_datetime(START_DATE)
    df_tasks = df_tasks[df_tasks["start"] >= start_dt]
    # 睡眠・授業は「起床時間」「終了時間」が期間内に入っているかも含めて判定
    df_sleep = df_sleep[df_sleep["起床時間"] >= start_dt]
    df_class_list = df_class_list[df_class_list["end_dt"] >= start_dt]

if END_DATE:
    # 終了日の 23:59:59 まで含めるため、翌日未満という条件にします
    end_dt = pd.to_datetime(END_DATE) + pd.Timedelta(days=1)
    df_tasks = df_tasks[df_tasks["start"] < end_dt]
    df_sleep = df_sleep[df_sleep["就寝時間"] < end_dt]
    df_class_list = df_class_list[df_class_list["start_dt"] < end_dt]

day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
day_labels_ja = ["月曜日", "火曜日", "水曜日", "木曜日", "金曜日", "土曜日", "日曜日"]

# ==========================================
# 2. 厳密な1分単位タイムラインの構築 & 重複追跡
# ==========================================
timeline = {}
meta_timeline = {}  # ログ追跡用の詳細な状態保持マップ
overlap_records = [] # 重複した分単位のログを格納するリスト

# --- 1. まず睡眠を展開 ---
for idx, row in df_sleep.iterrows():
    sleep_minutes = pd.date_range(start=row["就寝時間"], end=row["起床時間"], freq="min")
    for m in sleep_minutes:
        d_str = m.strftime("%Y-%m-%d")
        # 展開された分単位データでも念のため期間内かチェック
        if START_DATE and d_str < START_DATE: continue
        if END_DATE and d_str > END_DATE: continue
        if d_str in exclude_map:
            continue
        key = (d_str, m.hour, m.minute)
        timeline[key] = "0_睡眠"
        meta_timeline[key] = f"睡眠（{row['就寝時間'].strftime('%H:%M')}〜{row['起床時間'].strftime('%H:%M')}）"

# --- 2. 高校の授業を展開 ---
for idx, row in df_class_list.iterrows():
    class_minutes = pd.date_range(start=row["start_dt"], end=row["end_dt"], freq="min")
    for m in class_minutes:
        d_str = m.strftime("%Y-%m-%d")
        if START_DATE and d_str < START_DATE: continue
        if END_DATE and d_str > END_DATE: continue
        if d_str in exclude_map:
            continue
        key = (d_str, m.hour, m.minute)
        timeline[key] = "2_仕事関係"
        meta_timeline[key] = f"授業「{row['授業名']}」"

def categorize_target(target):
    if target in ["研究", "会議（研究）"]: return "1_研究・会議"
    elif str(target).startswith("仕事"): return "2_仕事関係"
    elif target == "授業": return "3_授業"
    elif target in ["英会話・英語", "英語"]: return "4_英語・英会話"
    else: return "5_開発・作業・他"

df_tasks["custom_category"] = df_tasks["target"].apply(categorize_target)

# --- 3. 手動Focusログを展開し、重複を検知・記録する ---
for idx, row in df_tasks.iterrows():
    task_minutes = pd.date_range(start=row["start"], end=row["end"], freq="min")
    for m in task_minutes:
        d_str = m.strftime("%Y-%m-%d")
        if START_DATE and d_str < START_DATE: continue
        if END_DATE and d_str > END_DATE: continue
        if d_str in exclude_map:
            continue
        key = (d_str, m.hour, m.minute)
        
        # すでに何らかの予定が入っていた場合は重複判定
        if key in timeline:
            prev_activity = meta_timeline.get(key, "既存のログ")
            overlap_records.append({
                "timestamp": m,
                "existing_data": prev_activity,
                "focus_data": f"Focus({row['target']})"
            })
            
        # タイムラインをFocusデータで上書き（Focus最優先）
        timeline[key] = row["custom_category"]
        meta_timeline[key] = f"Focus({row['target']})"

# --- ②【Overlap（重複）要約レポートの出力】 ---
print("\n--- ②【Overlap（重複）補正ログ】 ---")
df_ov = pd.DataFrame(overlap_records)

if not df_ov.empty:
    df_ov = df_ov.sort_values("timestamp").reset_index(drop=True)
    
    # 連続している時間帯を1本のログにまとめるためのグループ化シグナル
    df_ov["time_gap"] = df_ov["timestamp"].diff() > pd.Timedelta(minutes=1)
    df_ov["existing_change"] = df_ov["existing_data"] != df_ov["existing_data"].shift()
    df_ov["focus_change"] = df_ov["focus_data"] != df_ov["focus_data"].shift()
    
    # いずれかの変化があったら新しいグループIDを振る
    df_ov["group_id"] = (df_ov["time_gap"] | df_ov["existing_change"] | df_ov["focus_change"]).cumsum()
    
    # 詳細なログ出力を廃止し、件数だけをカウントして出力
    conflict_count = df_ov["group_id"].nunique()
    print(f"競合{conflict_count}件")
else:
    print("競合0件")

print("\n" + "="*50)
print("📊 グラフ描画プロセスの実行")
print("="*50)

# データフレーム化して可視化の準備
flat_data = []
for (d_str, hour, minute), cat in timeline.items():
    dt = pd.to_datetime(d_str)
    flat_data.append({
        "date": d_str,
        "day_of_week": dt.day_name(),
        "hour": hour,
        "detail_category": cat
    })
df_hourly = pd.DataFrame(flat_data)

# カラー・ラベル定義
detail_colors = {
    "0_睡眠": "#99aab5", "1_研究・会議": "#9966cc", "2_仕事関係": "#2ecc71",
    "3_授業": "#f1c40f", "4_英語・英会話": "#e67e22", "5_開発・作業・他": "#e74c3c"
}
category_labels_clean = {
    "0_睡眠": "睡眠", "1_研究・会議": "研究・会議", "2_仕事関係": "仕事",
    "3_授業": "授業", "4_英語・英会話": "英語", "5_開発・作業・他": "他・作業"
}

# ==========================================
# 3. プロット
# ==========================================
fig, axes = plt.subplots(7, 2, figsize=(18, 15), gridspec_kw={'width_ratios': [3, 1]})
total_days_per_dayofweek = df_hourly.groupby("day_of_week")["date"].nunique().to_dict()

for i, day in enumerate(day_order):
    df_day = df_hourly[df_hourly["day_of_week"] == day]
    day_count = total_days_per_dayofweek.get(day, 1)
    
    if not df_day.empty:
        df_pivot = df_day.pivot_table(index="hour", columns="detail_category", aggfunc="size", fill_value=0) / day_count
        df_pivot = df_pivot.reindex(range(0, 24), fill_value=0)
        
        row_sums = df_pivot.sum(axis=1)
        for hour_idx in range(24):
            if row_sums.iloc[hour_idx] > 60:
                df_pivot.iloc[hour_idx] = (df_pivot.iloc[hour_idx] / row_sums.iloc[hour_idx]) * 60
        
        current_colors = [detail_colors[c] for c in df_pivot.columns if c in detail_colors]
        df_pivot.plot(kind="bar", stacked=True, ax=axes[i, 0], color=current_colors, edgecolor="black", linewidth=0.3, legend=False)
        
        for col_idx, col_name in enumerate(df_pivot.columns):
            for hour_idx in range(24):
                val = df_pivot.loc[hour_idx, col_name]
                if val >= 8:
                    bottom_val = df_pivot.iloc[hour_idx, :col_idx].sum()
                    text_y = bottom_val + (val / 2)
                    label_text = f"{int(round(val))}分"
                    text_color = "white" if col_name == "0_睡眠" else "black"
                    axes[i, 0].text(hour_idx, text_y, label_text, ha="center", va="center", 
                                    fontsize=8, weight="bold", color=text_color)

        df_total = df_pivot.sum(axis=0)
        total_colors = [detail_colors[c] for c in df_total.index]
        
        y_positions = np.arange(len(df_total))
        axes[i, 1].barh(y_positions, df_total.values, color=total_colors, edgecolor="black", linewidth=0.5)
        axes[i, 1].set_yticks(y_positions)
        axes[i, 1].set_yticklabels([category_labels_clean[c] for c in df_total.index], fontsize=9)
        axes[i, 1].invert_yaxis()
        
        for y_idx, total_min in enumerate(df_total.values):
            if total_min > 0:
                h = int(total_min // 60)
                m = int(total_min % 60)
                time_str = f" {h}h{m}m" if h > 0 else f" {m}m"
                axes[i, 1].text(total_min, y_idx, time_str, va="center", fontsize=9, weight="bold")

    axes[i, 0].set_ylabel(day_labels_ja[i], rotation=0, labelpad=45, va="center", fontsize=11, weight="bold")
    axes[i, 0].set_ylim(0, 60)
    axes[i, 0].set_yticks([0, 30, 60])
    axes[i, 0].grid(axis="x", linestyle="--", alpha=0.5)
    axes[i, 1].grid(axis="x", linestyle="--", alpha=0.4)
    axes[i, 1].set_xlim(0, 60 * 10)
    sns.despine(ax=axes[i, 1], left=True, bottom=True)

# グラフタイトル等に期間を自動反映させる（オプション的な改善）
date_range_str = f" ({START_DATE} 〜 {END_DATE})" if START_DATE and END_DATE else ""
axes[0, 0].set_title(f"【時間帯別】1時間あたりの平均活動配分{date_range_str}", fontsize=13, weight="bold", pad=15)
axes[0, 1].set_title("【1日合計】各項目の平均総時間", fontsize=13, weight="bold", pad=15)
axes[6, 0].set_xlabel("時間帯", fontsize=11)
axes[6, 0].set_xticklabels([f"{h}時" for h in range(0, 24)], rotation=0)
axes[6, 1].set_xlabel("総時間", fontsize=11)

legend_elements = [plt.Rectangle((0,0),1,1, color=detail_colors[c]) for c in detail_colors]
legend_labels = [category_labels_clean[c] for c in detail_colors]
fig.legend(legend_elements, legend_labels, loc="upper center", bbox_to_anchor=(0.5, 0.97), ncol=6, fontsize=11)

plt.tight_layout()
plt.subplots_adjust(top=0.92, hspace=0.4, wspace=0.25)
plt.show()