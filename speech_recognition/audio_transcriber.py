#!/usr/bin/env python3
import asyncio

import requests


class AudioTranscriber:

    def __init__(self, api_key):
        self.url = "https://api.deepgram.com/v1/listen?punctuate=true"
        self.api_key = api_key

    async def transcribe_audio(self, audio, language_code):
        response = await self.api_request(audio, language_code)
        if response.status_code==200:
            print(response.text)
            return response.json()['results']['channels'][0]['alternatives'][0]['transcript']
        else:
            print(response.json()['error'] + ": " + response.json()['reason'])
            return ""
        
    async def api_request(self, audio, language_code):
        try:
            payload = audio
            headers = { 
                "Authorization": "Token " + self.api_key,
                "Content-Type": "audio/wave"
            }
            response = requests.request("POST", self.url + "&language=" + language_code, headers=headers, data=payload)
            return response
        except:
            print("Error: Deepgram API request failed.")
            return

if __name__ == "__main__":
    PATH_TO_FILE = 'speech_recognition/upload2.wav'
    async def main():
        transcriber = AudioTranscriber('en-GB')
        with open(PATH_TO_FILE, 'rb') as audio:
            response = await transcriber.transcribe_audio(audio)

    asyncio.run(main())
