#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
import glob
import json
import os
import time

import soundfile as sf
from flask import (Flask, redirect, render_template, request,
                   send_from_directory, session)
from gtts import gTTS, lang

from chat_bot import prompts
from chat_bot.chatbot import ChatBot
from keys.keys import *
from speech_recognition.audio_transcriber import AudioTranscriber

DEVELOPMENT_ENV  = True

app = Flask(__name__)
app.secret_key = 'BAD_SECRET_KEY'

app_data = {
    "name":         "Triolingo",
    "description":  "A chatbot app to allow you to practice deep conversations when learning a new language.",
    "author":       "Team Name",
    "html_title":   "Triolingo",
    "project_name": "Triolingo",
    "slogan":       "Bringing the power of conversation to your hands"
}

chatbot = ChatBot(OPENAI_API_KEY, session)
transcriber = AudioTranscriber(DEEPGRAM_API_KEY)

cwd = os.path.dirname(os.path.realpath(__file__)) + '/'

@app.route('/')
def index():
    return render_template('index.html', app_data=app_data)

@app.route('/chat-topics')
def chat_topics():
    return render_template('chat-topics.html', app_data=app_data)

@app.route('/chat/<string:topic>')
def chat(topic):
    # Initialise language if not set
    if not "language-code" in session:
        session["language-code"] = "en-GB"
    if not "language-name" in session:
        session["language-name"] = "English"
    
    # Get random subtopic and associated prompt
    (session["prompt"], session["subtopic"]) = prompts.get_prompt(topic)

    return render_template('chat.html', app_data=app_data, language=session["language-name"], topic=session["subtopic"])

@app.route('/help')
def help():
    return render_template('help.html', app_data=app_data)

@app.route('/about')
def about():
    return render_template('about.html', app_data=app_data)

@app.route('/scripts/<path:path>')
def send_js(path):
    return send_from_directory('scripts', path)

@app.route('/images/<path:path>')
def send_img(path):
    return send_from_directory('images', path)

@app.route('/temp/<path:path>')
def send_temp(path):
    return send_from_directory('temp', path)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Save audio file from POST data
        f = request.files['audio_data']
        f.save(cwd+'temp/upload.wav')

        # Re-encode audio file ready for transcription
        data, samplerate = sf.read(cwd+'temp/upload.wav')
        sf.write(cwd+'temp/upload2.wav', data, samplerate, subtype='PCM_16')

        # Transcribe audio file
        with open(cwd+'temp/upload2.wav', 'rb') as file:
            text = asyncio.run(transcriber.transcribe_audio(file, session.get("language-code", "en-GB")))

        # Get response from ChatBot and generate speech from it
        answer = chat(text)
        tts_file = tts(answer, session["language-code"])

        response_dict = {'user': text, 'ai': answer, 'tts_file': tts_file}
        return json.dumps(response_dict)
    return "fail"

@app.route('/initial_prompt', methods=['GET', 'POST'])
def initial_prompt():
    if request.method == 'POST':
        # Start with a basic question as the initial prompt to the user, append this to the GPT-3 hidden prompt
        start_prompt = f"What is your opinion of {session['subtopic']}?"
        session["prompt"] += f"\nFriend_q: " + start_prompt

        # Translate into target language and generate speech
        translated_prompt = chatbot.translate(start_prompt, "English", session["language-name"])
        tts_file = tts(translated_prompt, session["language-code"])

        response_dict = {'ai': translated_prompt, 'tts_file': tts_file}
        return json.dumps(response_dict)
    return "fail"

@app.route('/set_language', methods=['POST'])
def set_language():
    session['language-code'] = request.form.get('lang-selected')
    session["language-name"] = lang.tts_langs()[session["language-code"][:2]]
    return redirect(request.referrer)


# Utility functions

def delete_temp_contents():
    files = glob.glob(cwd+'temp/*')
    for f in files:
        os.remove(f)

def tts(text, language):
    tts = gTTS(text, lang=language)
    delete_temp_contents()
    curr_time = str(round(time.time()))
    filename = f"tts{curr_time}.wav"
    tts.save(f"{cwd}temp/{filename}")
    return filename

def chat(text):
    if session["language-name"] != "English":
        text = chatbot.translate(text, session["language-name"], "English")
        answer = chatbot.chat(text)
        return chatbot.translate(answer, "English", session["language-name"])
    return chatbot.chat(text)

if __name__ == '__main__':
    app.run(debug=DEVELOPMENT_ENV)
