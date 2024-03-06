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
        audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data)
    return text

def generate_srt(subtitles_file, text):
    with open(subtitles_file, 'w') as f:
        f.write("1\n00:00:00,000 --> 00:00:10,000\n")  # You need to adjust timestamps accordingly
        f.write(text)

if __name__ == "__main__":
    video_path = base_path+"vid.mp4"
    audio_path = base_path+"temp_audio.wav"
    subtitles_file = base_path+"subtitle.srt"

    extract_audio(video_path, audio_path)
    text = transcribe_audio(audio_path)
    generate_srt(subtitles_file, text)

    print("Subtitles generated successfully.")
