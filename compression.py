import os, ffmpeg
import tkinter as tk
from tkinter import filedialog
#compression algo
def compress_video(video_full_path, output_file_name, target_size):
    # Reference: https://en.wikipedia.org/wiki/Bit_rate#Encoding_bit_rate
    min_audio_bitrate = 32000
    max_audio_bitrate = 256000

    probe = ffmpeg.probe(video_full_path)
    # Video duration, in s.
    duration = float(probe['format']['duration'])
    # Audio bitrate, in bps.
    audio_bitrate = float(next((s for s in probe['streams'] if s['codec_type'] == 'audio'), None)['bit_rate'])
    # Target total bitrate, in bps.
    target_total_bitrate = (target_size * 1024 * 8) / (1.073741824 * duration)

    # Target audio bitrate, in bps
    if 10 * audio_bitrate > target_total_bitrate:
        audio_bitrate = target_total_bitrate / 10
        if audio_bitrate < min_audio_bitrate < target_total_bitrate:
            audio_bitrate = min_audio_bitrate
        elif audio_bitrate > max_audio_bitrate:
            audio_bitrate = max_audio_bitrate
    # Target video bitrate, in bps.
    video_bitrate = target_total_bitrate - audio_bitrate

    i = ffmpeg.input(video_full_path)
    ffmpeg.output(i, os.devnull,
                  **{'c:v': 'libx264', 'b:v': video_bitrate, 'pass': 1, 'f': 'mp4'}
                  ).overwrite_output().run()
    ffmpeg.output(i, output_file_name,
                  **{'c:v': 'libx264', 'b:v': video_bitrate, 'pass': 2, 'c:a': 'aac', 'b:a': audio_bitrate}
                  ).overwrite_output().run()

# Compress input.mp4 to 200MB and save as output.mp4
#compress_video('H:/Montage Making/2026 on/funny vid 3/trimmed/Age Regression.mp4', 'H:/Montage Making/2026 on/funny vid 3/output1.mp4', 200 * 1000)


#make files selectable
#allow for batch compression
#allow for selected compression size
#compression code is initially taken from https://stackoverflow.com/questions/64430805/how-to-compress-video-to-target-size-by-python

##button functions

#single file

def fileSelect():
    filepath = filedialog.askopenfilename()
    print(filepath)

def folderSelect():
    filepath = filedialog.askdirectory()
    print(filepath)

root = tk.Tk()
root.title("Compressor")
root.configure(background="#070709")
root.minsize(400, 400)
root.geometry("300x300+50+50")
#single file button
fileSelect = tk.Button(root, text="Select for single file compression", command=fileSelect)
fileSelect.place(x=20,y=20)
#folder button
folderSelect = tk.Button(root, text="Select for whole folder compression", command=folderSelect)
folderSelect.place(x=360,y=20)

root.mainloop()
