import sys
import pysrt
from pydub import AudioSegment

# 檢查命令行參數數量
if len(sys.argv) != 4:
    print("使用方式: python script.py 檔名 第一個編號 第二個編號")
    sys.exit(1)

# 從命令行參數獲取檔名和編號
filename = sys.argv[1]
start_index = int(sys.argv[2])
end_index = int(sys.argv[3])

# 檢查並移除副檔名（如果存在）
if filename.lower().endswith('.mp3'):
    filename = filename[:-4]
elif filename.lower().endswith('.srt'):
    filename = filename[:-4]

# 構建SRT和MP3文件的路徑
srt_path = f'{filename}.srt'
mp3_path = f'{filename}.mp3'

# 加載SRT和MP3文件
subs = pysrt.open(srt_path)
audio = AudioSegment.from_mp3(mp3_path)

# 檢查編號是否有效
if 1 <= start_index <= len(subs) and 1 <= end_index <= len(subs) and start_index <= end_index:
    start_sub = subs[start_index - 1]
    end_sub = subs[end_index - 1]

    start_time = (start_sub.start.hours * 3600 + start_sub.start.minutes * 60 + start_sub.start.seconds) * 1000 + start_sub.start.milliseconds
    end_time = (end_sub.end.hours * 3600 + end_sub.end.minutes * 60 + end_sub.end.seconds) * 1000 + end_sub.end.milliseconds + 500

    # 切割音頻
    segment = audio[start_time:end_time]
    output_file = f'{filename}_segment_{start_index}_to_{end_index}.mp3'
    segment.export(output_file, format='mp3')

    print(f"已輸出音頻片段至：{output_file}")
else:
    print("輸入的編號無效或超出範圍。")
