#!/usr/bin/env python3
import requests
from deepgram import Deepgram
import asyncio, json

class AudioTranscriber:

    def __init__(self, language):
        self.language = language
        self.DEEPGRAM_API_KEY = '84dfb83a357fb78cc94cab587f5c8f27f7d1ee2a'
        self.dg_client = Deepgram(self.DEEPGRAM_API_KEY)
        self.url = "https://api.deepgram.com/v1/listen?punctuate=true"


    async def transcribe_audio(self, audio):
        response = await self.api_request(audio)
        if response.status_code==200:
            print(response.text)
            return response.json()['results']['channels'][0]['alternatives'][0]['transcript']
        else:
            print(response.json()['error'] + ": " + response.json()['reason'])
            return
        
    async def api_request(self, audio):
        source = {'buffer': audio, 'mimetype': 'audio/wav'}
        try:
            payload = audio
            headers = { 
                "Authorization": "Token " + self.DEEPGRAM_API_KEY,
                "Content-Type": "audio/wave"
            }
            response = requests.request("POST", self.url, headers=headers, data=payload)
            return response
        except:
            print("Error: Deepgram API request failed.")
            return

'''
PATH_TO_FILE = 'speech_recognition/upload2.wav'
async def main():
    transcriber = AudioTranscriber('en-GB')
    with open(PATH_TO_FILE, 'rb') as audio:
        response = await transcriber.transcribe_audio(audio)

asyncio.run(main())
'''

