import pytube
from pytube import Playlist
import progressbar as progress

video_type = input(
    'If you want to download playlist type 1 and Enter or type 0:')
link = input('Youtube Video/Playlist URL:')

global filesize


def progress(streams, chunk: bytes, bytes_remaining: int):
    contentsize = filesize
    size = contentsize - bytes_remaining

    print('\r' + '[Download progress]:[%s%s]%.2f%%;' % (
        '█' * int(size*20/contentsize), ' '*(20-int(size*20/contentsize)), float(size/contentsize*100)), end='')


if video_type == "1":
    playlist = Playlist(link, )
    print('Number of videos in playlist: %s' % len(playlist.video_urls))
    # Loop through all videos in the playlist and download them
    for video in playlist.videos:
        video.register_on_progress_callback(progress)
        stream = video.streams.filter(progressive=True, file_extension='mp4').order_by(
            'resolution').desc().first()
        filesize = stream.filesize
        stream.download()

else:
    video_download = pytube.YouTube(
        link, on_progress_callback=progress)
    stream = video_download.streams.filter(progressive=True, file_extension='mp4').order_by(
        'resolution').desc().first()
    filesize = stream.filesize
    stream.download()
print('Video Downloaded')
