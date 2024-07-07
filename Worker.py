import speech_recognition as sr
from moviepy.editor import AudioFileClip
from moviepy.editor import VideoFileClip
from datetime import datetime
import moviepy as mp
import os




def audio_to_text(audio_path):
    r = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio = r.record(source)
        try:
            text_from_audio = r.recognize_vosk(audio, "ru")
        except Exception as error:
            print(error)
            return False
        text_from_audio = str(text_from_audio)
    text_from_audio = text_from_audio[13 : -3]
    return text_from_audio


def mp4_to_wav(mp4_path, name, PATH):
    path_to_wav = PATH + fr"/{name}.wav"
    Video = VideoFileClip(mp4_path)
    Video.audio.write_audiofile(path_to_wav, codec='pcm_s16le')
    return path_to_wav


def ogg_to_wav(ogg_path, name, PATH):
    Audio_ogg = AudioFileClip(ogg_path)
    Audio_wav = PATH + fr"/{name}.wav"
    Audio_ogg.write_audiofile(Audio_wav)
    return Audio_wav


def my_logger(user_id, name_of_file, user_name, text):
    way_to_home = os.getcwd()
    log_string = f"\n{user_id}    {user_name}     {name_of_file}      {datetime.now()}\n Текст: {text} \n"
    with open(way_to_home + "/log_bot.txt", "a") as file:
        file.write(log_string)
