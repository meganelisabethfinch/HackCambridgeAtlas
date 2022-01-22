#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template

DEVELOPMENT_ENV  = True

app = Flask(__name__)

app_data = {
    "name":         "Chatbot App",
    "description":  "A chatbot app to allow you to practice deep conversations when learning a new language.",
    "author":       "Team Name",
    "html_title":   "Practice Chat Session",
    "project_name": "Chatbot App",
    "slogan":       "Bringing the power of conversation to your hands",
    "keywords":     "chatbot, languages, conversation, learn"
}


@app.route('/')
def index():
    return render_template('index.html', app_data=app_data)

@app.route('/chat-topics')
def chat_topics():
    return render_template('chat-topics.html', app_data=app_data)

@app.route('/chat')
def chat():
    return render_template('chat.html', app_data=app_data)

@app.route('/help')
def help():
    return render_template('help.html', app_data=app_data)

@app.route('/about')
def about():
    return render_template('about.html', app_data=app_data)


if __name__ == '__main__':
    app.run(debug=DEVELOPMENT_ENV)