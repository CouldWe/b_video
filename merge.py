# -*- coding:utf-8 -*-
from pathlib import Path
import ffmpeg
def merge_video_audio(video_path, audio_path, output_path):
    # 检查输入文件是否存在
    if not Path(video_path).is_file():
        raise FileNotFoundError(f"Video file not found: {video_path}")
    if not Path(audio_path).is_file():
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    # 输入视频和音频文件
    video = ffmpeg.input(video_path)
    audio = ffmpeg.input(audio_path)

    # 将音频合并到视频中
    output = ffmpeg.output(video, audio, output_path, vcodec='copy', acodec='aac')

    # 覆盖已存在的文件
    output = ffmpeg.overwrite_output(output)

    # 执行命令
    try:
        ffmpeg.run(output)
    except ffmpeg.Error as e:
        print(f"An error occurred: {e.stderr.decode('utf8')}")
        raise