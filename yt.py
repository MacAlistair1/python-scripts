import pytube
from pytube import Playlist

video_type = input('If you want to download playlist type 1 and Enter or type 0:')
link = input('Youtube Video/Playlist URL:')


if video_type == "1":
	playlist = Playlist(link)
	print('Number of videos in playlist: %s' % len(playlist.video_urls))
	# Loop through all videos in the playlist and download them
	for video in playlist.videos:
	    video.streams.filter(adaptive=True, file_extension='mp4').order_by(
	    'resolution').desc().first().download()

else:
	video_download = pytube.YouTube(link)
	video_download.streams.filter(adaptive=True, file_extension='mp4').order_by(
	    'resolution').desc().first().download()
print('Video Downloaded')
