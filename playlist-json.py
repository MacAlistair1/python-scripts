import json
import yt_dlp
from datetime import datetime
import os

playlist_url = input('Enter YouTube Playlist URL: ')

def seconds_to_mmss(seconds):
    if seconds is None:
        return "00:00"
    minutes, seconds = divmod(int(seconds), 60)
    return f"{minutes:02}:{seconds:02}"

def format_upload_date(upload_date):
    if not upload_date:
        return ""
    try:
        dt = datetime.strptime(upload_date, "%Y%m%d")
        return dt.strftime("%Y-%m-%d")
    except ValueError:
        return upload_date

def format_view_count(view_count):
    if view_count >= 1_000_000_000:
        formatted = f"{view_count / 1_000_000_000:.1f}B"
    elif view_count >= 1_000_000:
        formatted = f"{view_count / 1_000_000:.1f}M"
    elif view_count >= 1_000:
        formatted = f"{view_count / 1_000:.1f}K"
    else:
        formatted = str(view_count)
    if formatted.endswith(".0K") or formatted.endswith(".0M") or formatted.endswith(".0B"):
        formatted = formatted[:-3] + formatted[-1]
    return formatted

def get_video_info_from_playlist(playlist_url, output_filename):
    ydl_opts = {
        'extract_flat': False,
        'quiet': False,
        'skip_download': True,
        'ignoreerrors': True,   # ✅ skip unavailable videos
        # 'playlist_items' : '1-10', # Limit to first 10 videos for testing
    }

    os.makedirs(os.path.dirname(output_filename), exist_ok=True)

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            result = ydl.extract_info(playlist_url, download=False)
        except Exception as e:
            print(f"❌ Playlist extraction completely failed: {e}")
            return

        if not result or 'entries' not in result:
            print("⚠️ No videos found in playlist.")
            return

        # Start JSON array
        with open(output_filename, "w", encoding="utf-8") as f:
            f.write("[\n")

        first = True
        for entry in result['entries']:
            if entry is None:
                continue  # skip unavailable videos

            try:
                video_data = {
                    'title': entry.get('title'),
                    'url': f"https://www.youtube.com/watch?v={entry.get('id')}",
                    'channel': entry.get('channel', ''),
                    'upload_date': format_upload_date(entry.get('upload_date')),
                    'view_count': format_view_count(entry.get('view_count', 0)),
                    'duration': seconds_to_mmss(entry.get('duration')),
                    'description': (entry.get('description') or '').strip()[:400],
                }

                # Append video JSON
                with open(output_filename, "a", encoding="utf-8") as f:
                    if not first:
                        f.write(",\n")
                    f.write(json.dumps(video_data, ensure_ascii=False, indent=4))
                    first = False

                print(f"✅ Saved: {video_data['title']}")

            except Exception as e:
                print(f"⚠️ Error processing video {entry.get('id')}: {e}")
                continue

        # Close JSON array
        with open(output_filename, "a", encoding="utf-8") as f:
            f.write("\n]\n")

# Run extraction
output_filename = "output/playlist_info.json"
get_video_info_from_playlist(playlist_url, output_filename)

print(f"\n🎉 Playlist info saved to '{output_filename}' (valid JSON array)")
