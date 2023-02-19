import os
import shutil

def move_video_files(directory):
    # Iterate over all files and directories in the given directory
    for root, dirs, files in os.walk(directory):
        # Check if any video files exist in the current directory
        video_files = [f for f in files if f.endswith((".mp4", ".avi", ".mkv"))]
        if video_files:
            # Move each video file to the parent directory
            for video_file in video_files:
                video_file_path = os.path.join(root, video_file)
                shutil.move(video_file_path, os.path.join(root, ".."))

if __name__ == "__main__":
    directory = input("Enter directory path: ")
    move_video_files(directory)
