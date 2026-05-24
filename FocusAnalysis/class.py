import urllib.request
import re
import pandas as pd
from icalendar import Calendar
from datetime import datetime, timedelta
import dateutil.rrule
import os
from dotenv import load_dotenv
load_dotenv()
# 🌟 提供されたiCloudカレンダーのURLを設定
CALENDAR_URL = os.getenv("CAL_URL")
OUTPUT_CSV = "class.csv"

# ==============================================================================
# ⚙️ 設定エリア: 条件指定を完全にキープ
# ==============================================================================
# 1. 抽出したい「日付の期間（日付A 〜 今日まで）」
today_str = pd.Timestamp.today().strftime("%Y-%m-%d")

START_DATE = "2026-04-01"  
END_DATE = "2026-05-31"    

TARGET_PERIODS = [
    {"start_date": START_DATE, "end_date": END_DATE},
]

# 2. 抽出したい「時間スロット（開始時刻 〜 終了時刻）」
# 💡 情報I(13)の考査時程枠「17:10〜18:55」を追加してあります
TARGET_SLOTS = [
    {"start_time": "17:10", "end_time": "18:40"},  # 9,10時限
    {"start_time": "19:00", "end_time": "20:30"},  # 11,12時限
    {"start_time": "17:10", "end_time": "17:55"},  # 9,10時限(考査時程)
    {"start_time": "18:10", "end_time": "18:55"},  # 11,12時限(考査時程)
    {"start_time": "17:10", "end_time": "18:55"},  # ★追加：情報I(13)考査時程(変則105分枠)
]
# ==============================================================================

def parse_web_cal_with_rrule_strict_slot(url, output_path):
    https_url = url.replace("webcal://", "https://")
    print(f"🌐 繰り返しデータ完全復元エンジン起動... (期間: {START_DATE} 〜 {END_DATE})")
    
    try:
        req = urllib.request.Request(https_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            ical_data = response.read()
    except Exception as e:
        print(f"❌ ダウンロードに失敗しました。URLまたはネットワークを確認してください。\nエラー: {e}")
        return

    cal = Calendar.from_ical(ical_data)
    lesson_records = []

    # 抽出制限の範囲を定義
    START_LIMIT = datetime.strptime(START_DATE, "%Y-%m-%d")
    END_LIMIT = datetime.strptime(END_DATE, "%Y-%m-%d").replace(hour=23, minute=59, second=59)

    for component in cal.walk():
        if component.name == "VEVENT":
            summary = str(component.get("SUMMARY", ""))
            
            # キーワードフィルタ
            if not any(k in summary for k in ["情報", "マルチメディア", "時程", "授業"]):
                continue

            dtstart = component.get("DTSTART").dt
            dtend = component.get("DTEND").dt
            
            if not isinstance(dtstart, datetime):
                continue
                
            duration = dtend - dtstart
            
            # 各イベントに属するすべての日時候補を洗い出す（単発ならその日のみ、ループなら全日程）
            dates_to_check = []
            
            if "RRULE" in component:
                try:
                    rrule_text = component["RRULE"].to_ical().decode("utf-8")
                    rule = dateutil.rrule.rrulestr(rrule_text, dtstart=dtstart)
                    
                    tz = dtstart.tzinfo
                    start_lim_tz = START_LIMIT.replace(tzinfo=tz) if tz else START_LIMIT
                    end_lim_tz = END_LIMIT.replace(tzinfo=tz) if tz else END_LIMIT
                    
                    occurrences = rule.between(start_lim_tz, end_lim_tz, inc=True)
                    for occ in occurrences:
                        dates_to_check.append(occ.replace(tzinfo=None))
                except Exception:
                    pass
            else:
                # 💡ここを強化：iCloudのバインド属性を無視して、直球でネイティブ日時を取得
                dtstart_naive = dtstart.replace(tzinfo=None) if hasattr(dtstart, 'tzinfo') else dtstart
                dates_to_check.append(dtstart_naive)

            # 洗い出した全日程に対してスロット判定をフラットに行う
            for current_start in dates_to_check:
                current_end = current_start + duration
                
                if START_LIMIT <= current_start <= END_LIMIT:
                    start_time_str = current_start.strftime("%H:%M")
                    end_time_str = current_end.strftime("%H:%M")
                    
                    in_slot = False
                    for slot in TARGET_SLOTS:
                        if start_time_str == slot["start_time"] and end_time_str == slot["end_time"]:
                            in_slot = True
                            break
                            
                    if in_slot:
                        lesson_records.append({
                            "日付": current_start.strftime("%Y-%m-%d"),
                            "始めの時刻": start_time_str,
                            "終わりの時刻": end_time_str,
                            "授業名": summary
                        })

    # --- 後処理とCSV保存 ---
    if len(lesson_records) > 0:
        df_class = pd.DataFrame(lesson_records)
        # 完全な重複（日付・時間すべて同じもの）を一掃
        df_class = df_class.drop_duplicates(subset=["日付", "始めの時刻", "終わりの時刻"])
        df_class = df_class.sort_values(by=["日付", "始めの時刻"]).reset_index(drop=True)
        
        df_class.to_csv(output_path, index=False, encoding="utf-8")
        print(f"✨ 成功: タイムゾーン同期を完了し、隠れていたループ授業と考査時程をすべて復元しました（計 {len(df_class)} 件）")
        print(f"💾 『{output_path}』に保存しました。")
        
        print("\n📋 【抽出された授業リスト（考査時程含む）】")
        print(df_class.to_string(index=False))
    else:
        print("⚠️ 指定された期間・時間スロットに合致する授業が見つかりませんでした。")

# 実行
parse_web_cal_with_rrule_strict_slot(CALENDAR_URL, OUTPUT_CSV)