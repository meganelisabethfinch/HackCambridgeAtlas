#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from ssl import OPENSSL_VERSION
from flask import Flask, render_template, send_from_directory, request, session, redirect
from chat_bot.chatbot import ChatBot
from speech_recognition.audio_transcriber import AudioTranscriber
import asyncio
import soundfile as sf
from keys.keys import *
from gtts import gTTS, lang
import glob
import os
import time

DEVELOPMENT_ENV  = True

app = Flask(__name__)
app.secret_key = 'BAD_SECRET_KEY'

app_data = {
    "name":         "Triolingo",
    "description":  "A chatbot app to allow you to practice deep conversations when learning a new language.",
    "author":       "Team Name",
    "html_title":   "Practice Chat Session",
    "project_name": "Triolingo",
    "slogan":       "Bringing the power of conversation to your hands",
    "language":     "English",
    "language_code": "en-GB"
}



transcriber = AudioTranscriber("en-GB")

@app.route('/')
def index():
    return render_template('index.html', app_data=app_data)

@app.route('/chat-topics')
def chat_topics():
    return render_template('chat-topics.html', app_data=app_data)

@app.route('/chat/<string:topic>')
def chat(topic):
    if not "language-code" in session:
        session["language-code"] = "en-GB"
    global chatbot
    chatbot = ChatBot(OPENAI_API_KEY, topic)
    app_data["topic"] = topic
    return render_template('chat.html', app_data=app_data)

@app.route('/help')
def help():
    return render_template('help.html', app_data=app_data)

@app.route('/about')
def about():
    return render_template('about.html', app_data=app_data)

@app.route('/scripts/<path:path>')
def send_js(path):
    return send_from_directory('scripts', path)

@app.route('/temp/<path:path>')
def send_temp(path):
    return send_from_directory('temp', path)

def delete_temp_contents():
    files = glob.glob('temp/*')
    for f in files:
        os.remove(f)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        f = request.files['audio_data']
        f.save('temp/upload.wav')
        data, samplerate = sf.read('temp/upload.wav')
        sf.write('temp/upload2.wav', data, samplerate, subtype='PCM_16')

        with open('temp/upload2.wav', 'rb') as file:
            print(file)
            text = asyncio.run(transcriber.transcribe_audio(file))
        print(text)
        language = lang.tts_langs()[session["language-code"][:2]]
        translated_t = chatbot.translate(text, language, "English")
        answer = chatbot.chat(translated_t)
        translated_a = chatbot.translate(answer, "English", language)
        tts = gTTS(translated_a, lang=session["language-code"][:2])
        delete_temp_contents()
        curr_time = str(round(time.time()))
        tts.save("temp/tts"+curr_time+".wav")
        response_dict = {'user': text, 'ai': translated_a, 'time': curr_time}
        return json.dumps(response_dict)
    return "fail"

@app.route('/initial_prompt', methods=['GET', 'POST'])
def initial_prompt():
    if request.method == 'POST':
        prompt = "What is your opinion of "+app_data["topic"]+"?"
        chatbot.prompt += f"\nFriend_q: " + prompt
        language = lang.tts_langs()[session["language-code"][:2]]
        translated_p = chatbot.translate(prompt, "English", language)
        response_dict = {'ai': translated_p}
        return json.dumps(response_dict)
    return "fail"

@app.route('/set_language', methods=['POST'])
def set_language():
    session['language-code'] = request.form.get('lang-selected')
    global transcriber
    transcriber = AudioTranscriber(session.get("language-code", "en-GB"))
    return redirect(request.referrer)

if __name__ == '__main__':
    app.run(debug=DEVELOPMENT_ENV)
