from pytube import YouTube, Playlist
from moviepy.editor import VideoFileClip
import os, signal

def download_video(url, filepath, isVideo):
    if isVideo:
        yt = YouTube(url).streams.filter(progressive=True, file_extension='mp4').order_by('resolution').first()
    else:
        yt = YouTube(url).streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        #yt = YouTube(url).streams.filter(only_audio=True).first()

    yt.download(filepath)
    return os.path.join(filepath, yt.default_filename)

def convert_to_audio(filename, ext):
    converter = VideoFileClip(filename)
    converter.audio.write_audiofile(filename[:-4] + ext, verbose=False, logger=None)
    converter.close()

def input_links():
    print("Enter the links of videos (end by entering 'S'):")
    links = []

    links.append(input())
    while links[-1] != 'S' and links[-1] != 's':
        links.append(input())
    links.pop()

    return links

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def signal_handler(sig, frame):
    print("\nProcess terminated by user. Terminating...")
    exit(-1)

def processRequest(urls, folder, ext):
    cls()
    print(f"\nProcessing started in: {folder}\n")
    if ext == ".mp4":
        for url in urls:
            print("Done processing: ",  os.path.basename(download_video(url, folder, True)))
    else:
        for url in urls:
            path = download_video(url, folder, False)
            convert_to_audio(path, ext)
            os.remove(path)
            print(f"Done processing: {os.path.basename(path)[:-4] + ext}")

if __name__ == "__main__":
    cls()
    signal.signal(signal.SIGINT, signal_handler)
    print('''
YouTube Downloader and Converter
    (0) Paste links manually.
    (1) Download a playlist.
    ''')
    choice = input("Choice: ")
    
    print('''
Choose file format:
    (0) .mp4
    (1) .mp3
    (2) .wav
        ''')

    fileFormats = [".mp4", ".mp3", ".wav"]

    try:
        fileFormat = fileFormats[int(input("Choice: "))]
    except:
        print("\nInvalid input! Terminating...")
        exit(-1)

    if   choice == "0":
        processRequest(input_links(), "output/misc", fileFormat)
    elif choice == "1":
        playlist = Playlist(input("Enter the link to the playlist: "))
        processRequest(playlist.video_urls, os.path.join("output/", playlist.title), fileFormat)
    else:
        print("\nInvalid input! Terminating...")
        exit(-1)

    print("\nFinished! Exiting.")
    exit(0)