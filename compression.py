import os, ffmpeg
import tkinter as tk
from tkinter import filedialog

global compMode
global filePath
global folderPath
compMode = 0
filePath = ""
folderPath = ""

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

def fileSelect():
    global compMode
    global filePath
    global folderPath
    filePath = filedialog.askopenfilename()
    print(filePath)
    compMode = 0

def folderSelect():
    global compMode
    global filePath
    global folderPath
    folderPath = filedialog.askdirectory(title="Select a Folder", mustexist=True)
    print(folderPath)
    compMode = 1



##compression functions

def compression():
    global filePath
    global folderPath
    print("function clicked")
    print(compMode)
    val = entry.get()
    if val.isnumeric():
        val = int(val)
    else:
        val = 10
    if compMode == 1:
        for file in os.scandir(folderPath):
            if ".mp4" in file.name:
                out = file.path
                out = out[:-4]
                compress_video(file.path, out +"_Compressed_Ver.mp4", val * 1000)

    if compMode == 0:
        out = filePath
        out = out[:-4]
        compress_video(filePath, out +"_Compressed_Ver.mp4", val * 1000)
        



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
folderSelect.place(x=20,y=120)
#compress button
folderSelect = tk.Button(root, text="Click to compress selected file(s)", command=compression)
folderSelect.place(x=20,y=220)
#compress size entry
label = tk.Label(root, text="Enter the size you want your videos compressed to (MB)")
entry = tk.Entry(root)
label.place(x=20,y=320)
entry.place(x=20,y=345)

root.mainloop()
