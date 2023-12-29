#how to get youtube videos for background / intro
from pytube import YouTube


def download_360p_mp4_videos(url: str, outpath: str = "./"):

    yt = YouTube(url)

    yt.streams.filter(file_extension="mp4").get_highest_resolution().download(outpath)


if __name__ == "__main__":

    download_360p_mp4_videos(
        "https://youtu.be/",
        "./sad",
    )