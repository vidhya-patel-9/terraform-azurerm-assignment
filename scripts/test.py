from pytube import YouTube

# Where to save
SAVE_PATH = "E:/"  # to_do

# Links of the videos to be downloaded
links = ["https://www.youtube.com/watch?v=xWOoBJUqlbI",
         "https://www.youtube.com/watch?v=xWOoBJUqlbI"]

for link in links:
    try:
        # Object creation using YouTube
        # which was imported in the beginning
        yt = YouTube(link)
    except:
        # Handle exception
        print("Connection Error")

    # Get all streams and filter for mp4 files
    mp4_streams = yt.streams.filter(file_extension='mp4').all()

    # Get the video with the highest resolution
    d_video = mp4_streams[-1]

    try:
        # Download the video
        d_video.download(output_path=SAVE_PATH)
        print('Video downloaded successfully!')
    except:
        print("Some Error!")

print('Task Completed!')