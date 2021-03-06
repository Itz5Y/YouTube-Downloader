import tkinter as tk
from tkinter import messagebox
from pytube import YouTube
from pytube import Playlist
import os

#window
window = tk.Tk()
window.geometry('640x480')
window.resizable(True,True)
window.title('YouTube Video Downloader')
input_frame = tk.Frame(window, width=640, height=50)
input_frame.pack()

#label
label = tk.Label(input_frame,text='Enter URL')
label.place(rely=0.2, relx=0.5, anchor='center')

#input
input_url = tk.StringVar()
input_entry = tk.Entry(input_frame, textvariable=input_url, width=60)
input_entry.place(rely=0.75, relx=0.5, anchor='center')

#button
def btn_click():
    url = input_url.get()
    try:
        check_playlist(url)
    except:
        messagebox.askokcancel('Error', 'Invalid input!')
        return
btn = tk.Button(input_frame, text='Download', command = btn_click)
btn.place(rely=0.75, relx=0.9, anchor='center')


def download_video(url):
    yt = YouTube(url, on_progress_callback=progress)
    try:
        stream = yt.streams.filter(progressive=False, res='720p').first()
    except:
        try:
            stream = yt.streams.filter(progressive=False, res='360p').first()
        except:
            stream = yt.streams.filter(progressive=False, res='240p').first()
    print("=========\nTitle:        " + yt.title + "\nResolution:   " + stream.resolution + "\n=========")
    stream.download('YT downloads')
    print('\nThe video is saved in ' + os.getcwd() + '\YT downloads')


def progress(stream, chunk, remains):
    total = stream.filesize
    percent = (total - remains) / total * 100
    print('Download progress = [' + '▉' * int(percent / 5),
          ' ' * (20 - int(percent / 5)) + '] ' + '{:05.2f}%'.format(percent), end='\r')

def download_playlist(url):
    p = Playlist(url)
    print('Playlist url = ' + str(p))
    for urls in p.video_urls:
        print('\nDownloading ' + urls)
        download_video(urls)


def check_playlist(url):
    if 'playlist?list=' in str(url):
        download_playlist(url)
    else:
        download_video(url)


window.mainloop()
