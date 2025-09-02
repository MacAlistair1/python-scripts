import json
import yt_dlp
from datetime import timedelta, datetime

# Input the playlist URL
playlist_url = input('Enter YouTube Playlist URL: ')

def seconds_to_mmss(seconds):
    """Convert seconds to MM:SS format (trimming hours)."""
    if seconds is None:
        return "00:00"
    minutes, seconds = divmod(int(seconds), 60)
    return f"{minutes:02}:{seconds:02}"

def format_upload_date(upload_date):
    """Convert upload date from YYYYMMDD to YYYY-MM-DD."""
    if not upload_date:
        return ""
    try:
        dt = datetime.strptime(upload_date, "%Y%m%d")
        return dt.strftime("%Y-%m-%d")
    except ValueError:
        return upload_date  # fallback
    
def format_view_count(view_count):
    """Convert the view count to a more readable format (K, M, B) without the `.0` for whole numbers."""
    if view_count >= 1_000_000_000:
        formatted = f"{view_count / 1_000_000_000:.1f}B"
    elif view_count >= 1_000_000:
        formatted = f"{view_count / 1_000_000:.1f}M"
    elif view_count >= 1_000:
        formatted = f"{view_count / 1_000:.1f}K"
    else:
        formatted = str(view_count)
    
    # Remove .0 if it's a whole number (e.g., 1.0K → 1K)
    if formatted.endswith(".00"):
        formatted = formatted[:-2]
    
    return formatted

def get_video_info_from_playlist(playlist_url):
    ydl_opts = {
        'extract_flat': False,  # Get full metadata
        'quiet': False,
        'skip_download': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            result = ydl.extract_info(playlist_url, download=False)
            if 'entries' not in result:
                print("No videos found in playlist.")
                return []

            videos_info = []
            for entry in result['entries']:
                if entry is None:
                    continue

                video_data = {
                    'title': entry.get('title'),
                    'url': f"https://www.youtube.com/watch?v={entry.get('id')}",
                    'channel': entry.get('channel', ''),
                    'upload_date': format_upload_date(entry.get('upload_date')),
                    'view_count': format_view_count(entry.get('view_count', 0)),
                    'duration': seconds_to_mmss(entry.get('duration')),
                    'description': entry.get('description', '').strip()[:400],
                }
                videos_info.append(video_data)

            return videos_info

        except yt_dlp.utils.DownloadError as e:
            print(f"Error extracting playlist: {e}")
            return []

# Extract video info
videos = get_video_info_from_playlist(playlist_url)

# Save to JSON file
output_filename = "output/playlist_info.json"
with open(output_filename, "w", encoding="utf-8") as f:
    json.dump(videos, f, indent=4, ensure_ascii=False)

print(f"\n✅ Playlist info saved to '{output_filename}' with {len(videos)} videos.")
