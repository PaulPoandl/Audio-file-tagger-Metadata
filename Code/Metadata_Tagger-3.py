import os
import re
from tkinter import Tk, filedialog
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4, MP4Cover
from mutagen.flac import FLAC

def choose_directory():
    root = Tk()
    root.withdraw()
    folder_selected = filedialog.askdirectory()
    root.destroy()
    return folder_selected

def update_metadata(file_path, artist, album, track_number):
    title = os.path.splitext(os.path.basename(file_path))[0]

    if file_path.endswith(".mp3"):
        audio = MP3(file_path)
        audio["TIT2"] = title
        audio["TPE1"] = artist
        audio["TALB"] = album
        audio["TRCK"] = str(track_number)  # Add track number
    elif file_path.endswith(".m4a"):
        audio = MP4(file_path)
        audio["\xa9nam"] = [title]
        audio["\xa9ART"] = [artist]
        audio["\xa9alb"] = [album]
        audio["----:com.apple.iTunes:track-number"] = [str(track_number).encode('utf-8')]  # Convert track number to bytes
    elif file_path.endswith(".flac"):
        audio = FLAC(file_path)
        audio["title"] = title
        audio["artist"] = artist
        audio["album"] = album
        audio["tracknumber"] = str(track_number)  # Add track number
    else:
        print(f"Unsupported file type: {file_path}")
        return

    try:
        audio.save()
        print(f"Metadata updated for: {file_path}")
    except Exception as e:
        print(f"Error updating metadata for {file_path}: {e}")

def process_folder(folder_path, artist, album):
    audio_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith((".mp3", ".m4a", ".flac"))]
    for i, file_path in enumerate(audio_files, start=1):  # Enumerate to get track number
        update_metadata(file_path, artist, album, i)
    print(f"Metadata updated for {len(audio_files)} files!")

def main():
    while True:
        directory = choose_directory()
        if not directory:
            print("No directory selected. Exiting.")
            return

        artist = input("Enter artist: ")
        album = input("Enter album: ")

        if directory and artist and album:
            process_folder(directory, artist, album)
        else:
            print("Please fill in all fields.")

        response = input("Do you want to update metadata for other files? (yes/no): ")
        if response.lower() != 'yes':
            break

if __name__ == "__main__":
    main()
