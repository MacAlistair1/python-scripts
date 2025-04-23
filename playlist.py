import os
import yt_dlp

# Input the playlist or video URL
video_type = input('If you want to download a playlist, type 1 and press Enter, or type 0:')
link = input('YouTube Video/Playlist URL:')
start_index = 128  # Set this to 149 to start from the 150th video

def get_video_urls_from_playlist(playlist_url):
    ydl_opts = {
        'extract_flat': True,  # Extract only URLs
        'force_generic_extractor': True,
        'quiet': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            result = ydl.extract_info(playlist_url, download=False)
            video_urls = [entry['url'] for entry in result['entries']]
            return video_urls
        except yt_dlp.utils.DownloadError as e:
            print(f"Error extracting playlist: {e}")
            return []

def download_audio(url, output_path):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'progress_hooks': [progress_hook],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([url])
        except yt_dlp.utils.DownloadError as e:
            print(f"Error downloading {url}: {e}. Skipping to the next video.")

def progress_hook(d):
    if d['status'] == 'downloading':
        print(f"Download progress: {d['_percent_str']} of {d['_total_bytes_str']} at {d['_speed_str']}")
    elif d['status'] == 'finished':
        print('Download completed, now converting...')

if video_type == "1":
    playlist_id = link.split("list=")[-1]
    playlist_feed_url = f"https://www.youtube.com/playlist?list={playlist_id}"

    video_urls = get_video_urls_from_playlist(playlist_feed_url)

    if video_urls:
        output_dir = os.path.join(os.getcwd(), 'mp3')
        os.makedirs(output_dir, exist_ok=True)

        for index, video_url in enumerate(video_urls):
            if index < start_index:
                continue  # Skip videos until reaching the start index

            print(f"Downloading video {index + 1}...")
            download_audio(video_url, output_dir)
else:
    output_dir = os.path.join(os.getcwd(), 'mp3')
    os.makedirs(output_dir, exist_ok=True)

    download_audio(link, output_dir)

print('Download Complete')
