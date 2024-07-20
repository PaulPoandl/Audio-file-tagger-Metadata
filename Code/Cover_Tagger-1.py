import os
import re
import base64
from tkinter import Tk, filedialog
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4, MP4Cover
from mutagen.flac import FLAC
from mutagen.id3 import ID3, APIC

# Function to open a file dialog and return the selected file path
def choose_file():
    root = Tk()
    root.withdraw()
    file_selected = filedialog.askopenfilename()
    root.destroy()
    return file_selected

# Function to open a directory dialog and return the selected directory path
def choose_directory():
    root = Tk()
    root.withdraw()
    folder_selected = filedialog.askdirectory()
    root.destroy()
    return folder_selected

# Function to get a list of all files in a directory with the specified file extensions
def get_files(directory, file_extensions):
    return [f for f in os.listdir(directory) if f.lower().endswith(file_extensions)]

# Function to embed a cover image into an MP3 file
def embed_cover_mp3(file_path, cover_path):
    print(f"Embedding cover image {cover_path} in file {file_path}")
    audio = MP3(file_path, ID3=ID3)
    with open(cover_path, "rb") as img:
        audio.tags.add(
            APIC(
                encoding=3,
                mime='image/jpeg',
                type=3,
                desc=u'Cover',
                data=img.read()
            )
        )
    audio.save()

# Function to embed a cover image into an MP4 file
def embed_cover_mp4(file_path, cover_path):
    print(f"Embedding cover image {cover_path} in file {file_path}")
    audio = MP4(file_path)
    with open(cover_path, "rb") as img:
        audio["covr"] = [MP4Cover(img.read(), imageformat=MP4Cover.FORMAT_JPEG)]
    audio.save()

# Function to embed a cover image into a FLAC file
def embed_cover_flac(file_path, cover_path):
    print(f"Embedding cover image {cover_path} in file {file_path}")
    audio = FLAC(file_path)
    with open(cover_path, "rb") as img:
        audio.picture = [
            {
                'type': 'front cover',
                'data': img.read(),
                'mime': 'image/jpeg'
            }
        ]
    audio.save()

# Function to find a matching cover image for a music file
def find_matching_cover(music_file, cover_files):
    music_file_base = os.path.splitext(music_file)[0]

    # Check for exact match
    for cover in cover_files:
        if cover == music_file_base + os.path.splitext(cover)[1]:
            return cover

    # Check for partial match
    words = music_file_base.split()
    for i in range(1, min(len(words), 5)):
        prefix = ' '.join(words[:i])
        for cover in cover_files:
            if cover.startswith(prefix):
                return cover
    return None

# Main function
def main():
    while True:
        mode = input(
                    "\n"
                    "Choose mode:\n"
                    "'single' for a single file (you need one audio file and one picture)\n"
                    "'directory' for a whole directory (You need as many pictures as audio files, the first few words in the name of the pictures have to be the same as the corresponding song)\n"
                    "'multiple' for multiple directories (You need the same as in the directory mode)\n"
                    "'batch' for applying one cover to multiple files (You need multiple audio files and one picture)\n"
                    "\n"
                    )

        if mode == 'single':
            music_file = choose_file()
            cover_file = choose_file()

            if not os.path.splitext(music_file)[1] in (".mp3", ".m4a", ".flac"):
                print("Invalid music file. Exiting.")
                continue

            if not os.path.splitext(cover_file)[1] in (".jpg", ".jpeg", ".png"):
                print("Invalid cover file. Exiting.")
                continue

            try:
                if os.path.splitext(music_file)[1] == ".mp3":
                    embed_cover_mp3(music_file, cover_file)
                elif os.path.splitext(music_file)[1] == ".m4a":
                    embed_cover_mp4(music_file, cover_file)
                elif os.path.splitext(music_file)[1] == ".flac":
                    embed_cover_flac(music_file, cover_file)
                print(f"Embedded cover for {music_file}")
            except Exception as e:
                print(f"Failed to embed cover for {music_file}: {e}")

        elif mode == 'directory':
            directory = choose_directory()
            if not directory:
                print("No directory selected. Exiting.")
                continue

            music_extensions = (".mp3", ".m4a", ".flac")
            image_extensions = (".jpg", ".jpeg", ".png")
            music_files = get_files(directory, music_extensions)
            cover_files = get_files(directory, image_extensions)

            for music_file in music_files:
                cover_file = find_matching_cover(music_file, cover_files)
                if cover_file:
                    music_path = os.path.join(directory, music_file)
                    cover_path = os.path.join(directory, cover_file)
                    try:
                        if music_file.endswith(".mp3"):
                            embed_cover_mp3(music_path, cover_path)
                        elif music_file.endswith(".m4a"):
                            embed_cover_mp4(music_path, cover_path)
                        elif music_file.endswith(".flac"):
                            embed_cover_flac(music_path, cover_path)
                        print(f"Embedded cover for {music_file}")

                        # Verify that the cover was embedded
                        if music_file.endswith(".mp3"):
                            audio = MP3(music_path)
                            if audio.tags.get("APIC"):
                                print(f"Cover successfully embedded for {music_file}")
                                os.remove(cover_path)
                                print(f"Deleted cover file {cover_file}")
                            else:
                                print(f"Cover embedding failed verification for {music_file}")
                        elif music_file.endswith(".m4a"):
                            audio = MP4(music_path)
                            if "covr" in audio:
                                print(f"Cover successfully embedded for {music_file}")
                                os.remove(cover_path)
                                print(f"Deleted cover file {cover_file}")
                            else:
                                print(f"Cover embedding failed verification for {music_file}")
                        elif music_file.endswith(".flac"):
                            audio = FLAC(music_path)
                            if audio.picture:
                                print(f"Cover successfully embedded for {music_file}")
                                os.remove(cover_path)
                                print(f"Deleted cover file {cover_file}")
                            else:
                                print(f"Cover embedding failed verification for {music_file}")
                    except Exception as e:
                        print(f"Failed to embed cover for {music_file}: {e}")

        elif mode == 'multiple':
            num_directories = input("Enter the number of directories you want to process (between 1 and 10): ")
            if not num_directories.isdigit() or int(num_directories) < 1 or int(num_directories) > 10:
                print("Invalid input. Exiting.")
                continue

            for _ in range(int(num_directories)):
                directory = choose_directory()
                if not directory:
                    print("No directory selected. Exiting.")
                    continue

                music_extensions = (".mp3", ".m4a", ".flac")
                image_extensions = (".jpg", ".jpeg", ".png")
                music_files = get_files(directory, music_extensions)
                cover_files = get_files(directory, image_extensions)

                for music_file in music_files:
                    cover_file = find_matching_cover(music_file, cover_files)
                    if cover_file:
                        music_path = os.path.join(directory, music_file)
                        cover_path = os.path.join(directory, cover_file)
                        try:
                            if music_file.endswith(".mp3"):
                                embed_cover_mp3(music_path, cover_path)
                            elif music_file.endswith(".m4a"):
                                embed_cover_mp4(music_path, cover_path)
                            elif music_file.endswith(".flac"):
                                embed_cover_flac(music_path, cover_path)
                            print(f"Embedded cover for {music_file}")

                            # Verify that the cover was embedded
                            if music_file.endswith(".mp3"):
                                audio = MP3(music_path)
                                if audio.tags.get("APIC"):
                                    print(f"Cover successfully embedded for {music_file}")
                                    os.remove(cover_path)
                                    print(f"Deleted cover file {cover_file}")
                                else:
                                    print(f"Cover embedding failed verification for {music_file}")
                            elif music_file.endswith(".m4a"):
                                audio = MP4(music_path)
                                if "covr" in audio:
                                    print(f"Cover successfully embedded for {music_file}")
                                    os.remove(cover_path)
                                    print(f"Deleted cover file {cover_file}")
                                else:
                                    print(f"Cover embedding failed verification for {music_file}")
                            elif music_file.endswith(".flac"):
                                audio = FLAC(music_path)
                                if audio.picture:
                                    print(f"Cover successfully embedded for {music_file}")
                                    os.remove(cover_path)
                                    print(f"Deleted cover file {cover_file}")
                                else:
                                    print(f"Cover embedding failed verification for {music_file}")
                        except Exception as e:
                            print(f"Failed to embed cover for {music_file}: {e}")

        elif mode == 'batch':
            music_files = []
            for i in range(5):
                music_file = choose_file()
                if not os.path.splitext(music_file)[1] in (".mp3", ".m4a", ".flac"):
                    print("Invalid music file. Exiting.")
                    continue
                music_files.append(music_file)

            cover_file = choose_file()
            if not os.path.splitext(cover_file)[1] in (".jpg", ".jpeg", ".png"):
                print("Invalid cover file. Exiting.")
                continue

            for music_file in music_files:
                try:
                    if os.path.splitext(music_file)[1] == ".mp3":
                        embed_cover_mp3(music_file, cover_file)
                    elif os.path.splitext(music_file)[1] == ".m4a":
                        embed_cover_mp4(music_file, cover_file)
                    elif os.path.splitext(music_file)[1] == ".flac":
                        embed_cover_flac(music_file, cover_file)
                    print(f"Embedded cover for {music_file}")
                except Exception as e:
                    print(f"Failed to embed cover for {music_file}: {e}")

        else:
            print("Invalid mode. Exiting.")
            continue

        user_input = input("Do you want to process more files? (yes/no): ")
        if user_input.lower() != 'yes':
            break

if __name__ == "__main__":
    main()
