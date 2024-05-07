import pysrt

def subrip_time_to_seconds(subrip_time):
    """將SubRipTime對象轉換為總秒數"""
    return subrip_time.hours * 3600 + subrip_time.minutes * 60 + subrip_time.seconds + subrip_time.milliseconds / 1000.0

# 使用 min_duration 參數來指定最短字幕時間不可少於多少秒
def merge_short_subtitles(srt_file, min_duration=4):
    subs = pysrt.open(srt_file)
    i = 0
    while i < len(subs) - 1:
        current_sub = subs[i]
        next_sub = subs[i + 1]
        
        # 計算當前字幕的持續時間
        duration = subrip_time_to_seconds(current_sub.end) - subrip_time_to_seconds(current_sub.start)
        
        if duration < min_duration:
            # 更新當前字幕的結束時間和內容，然後刪除下一個字幕
            current_sub.end = next_sub.end
            current_sub.text += ' ' + next_sub.text
            del subs[i + 1]
        else:
            i += 1

    # 重新編號字幕
    for index, sub in enumerate(subs, start=1):
        sub.index = index

    # 儲存更改後的字幕文件
    subs.save(srt_file.replace('.srt', '_merged.srt'), encoding='utf-8')

# 調用函數
srt_file = 'working_file.srt'  # 換成你的檔案名
merge_short_subtitles(srt_file)
