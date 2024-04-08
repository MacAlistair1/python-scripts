import os
import moviepy.editor as mp
import speech_recognition as sr

base_path = "/Users/nepalivlog/Documents/scripts/mp4"

def extract_audio(video_path, audio_path):
    video = mp.VideoFileClip(video_path)
    audio = video.audio
    audio.write_audiofile(audio_path)

def transcribe_audio(audio_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio_data = recognizer.record(source, duration=600)  # Set duration to 300 seconds (5 minutes)
        text = recognizer.recognize_google(audio_data)
    return text


def generate_srt(subtitles_file, text):
    with open(subtitles_file, 'w') as f:
        f.write("1\n00:00:00s,000 --> 00:00:10,000\n")  # You need to adjust timestamps accordingly
        f.write(text)

def format_timestamp(seconds):
    hours = int(seconds // 3600)
    seconds %= 3600
    minutes = int(seconds // 60)
    seconds %= 60
    milliseconds = int((seconds - int(seconds)) * 1000)
    return f"{hours:02d}:{minutes:02d}:{int(seconds):02d},{milliseconds:03d}"

if __name__ == "__main__":
    video_path = base_path+"/vid.mp4"
    audio_path = base_path+"/temp_audio.wav"
    subtitles_file = base_path+"/subtitle.srt"

    extract_audio(video_path, audio_path)
    text = transcribe_audio(audio_path)
    
    # video = mp.VideoFileClip(video_path)
    # video_duration = video.duration
    
    generate_srt(subtitles_file, text)

    print("Subtitles generated successfully.")
