import telebot
from telebot.types import VideoNote
import speech_recognition as sr
import os
from Worker import ogg_to_wav, mp4_to_wav, my_logger

from Worker import audio_to_text

PATH_VN = os.getcwd() + r"\For_vn"
PATH_VOICE = os.getcwd() + r"\Voice"
bot_token = "1925608406:AAE5vcn0bexT9YKZoTMWuzReTORbSLxUjpo"



bot = telebot.TeleBot(bot_token)

@bot.message_handler(commands=['start', 'help'])
def hello(message):
    bot.reply_to(message, "Привет! Отправь мне кружок или ГС и я переведу его в текст!")



@bot.message_handler(content_types=['voice'])
def voice(message_voice):
    bot.reply_to(message_voice, "Начинаю обработку....")
    voice = message_voice.voice
    voice_id = voice.file_id
    try:
        file_voice = bot.get_file(voice_id)
        downloaded_voice = bot.download_file(file_voice.file_path)
        with open(PATH_VOICE + "\\" + f"{str(voice_id)}" + ".ogg", "wb") as new_file:
            new_file.write(downloaded_voice)
        path_to_wav = ogg_to_wav(PATH_VOICE + "\\" + f"{str(voice_id)}" + ".ogg", voice_id, PATH_VOICE)
        bot.reply_to(message_voice, "Перевожу в текст...")
        text = audio_to_text(path_to_wav)
        my_logger(message_voice.from_user.id, voice_id, message_voice.from_user.username, text)
        print(text)
        print(type(text))
        bot.reply_to(message_voice, text)
    except Exception as error:
        print(error)


@bot.message_handler(content_types=["video_note"])
def video_note(message_vn):
    bot.reply_to(message_vn, "Начинаю обработку...")
    video_note = message_vn.video_note
    video_note_id = video_note.file_id
    try:
        file_vn = bot.get_file(video_note_id)
        downloaded_vn = bot.download_file(file_vn.file_path)
        with open(PATH_VN + "\\" + f"{str(video_note_id)}" + ".mp4", 'wb') as new_file:
            new_file.write(downloaded_vn)
        path_to_wav = mp4_to_wav(PATH_VN + "\\" + f"{str(video_note_id)}" + ".mp4", video_note_id, PATH_VOICE)
        bot.reply_to(message_vn, "Перевожу в текст...")
        text = audio_to_text(path_to_wav)
        my_logger(message_vn.from_user.id, video_note_id, message_vn.from_user.username, text)
        bot.reply_to(message_vn, text)
    except Exception as error:
        print(error)
        bot.reply_to(message_vn, "Не подходящий файл, попробуйте другой!")




bot.infinity_polling()