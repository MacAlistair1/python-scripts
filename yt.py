import pytube
from pytube import Playlist

video_type = input('Youtube Video or Playlist:')
link = input('Youtube Video URL:')
# video_download.streams.first().download()


if video_type == "playlist":
	playlist = Playlist(link)
	print('Number of videos in playlist: %s' % len(playlist.video_urls))
	# Loop through all videos in the playlist and download them
	for video in playlist.videos:
	    video.streams.filter(progressive=True, file_extension='mp4').order_by(
	    'resolution').desc().first().download()

else:
	video_download = pytube.YouTube(link)
	video_download.streams.filter(progressive=True, file_extension='mp4').order_by(
	    'resolution').desc().first().download()

print('Video Downloaded', link)
