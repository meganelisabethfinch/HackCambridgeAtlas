#!/usr/bin/env python3

from deepgram import Deepgram
import asyncio, json

class AudioTranscriber:
    def __init__(self, language):
        self.language = language
        self.DEEPGRAM_API_KEY = '84dfb83a357fb78cc94cab587f5c8f27f7d1ee2a'
        self.dg_client = Deepgram(self.DEEPGRAM_API_KEY)

    async def transcribe_audio(self, audio):
        response = await self.api_request(audio)
        if response is None:
            print("Error: Failed to transcribe audio.")
            return
        else:
            return response.get("results").get("channels")[0].get("alternatives")[0].get("transcript")
        
    async def api_request(self, audio):
        source = {'buffer': audio, 'mimetype': 'audio/wav'}
        try:
            response = await self.dg_client.transcription.prerecorded(source, {'punctuate': True, 'language': self.language, 'alternatives': 1})
            print(json.dumps(response, indent=4))
            return response
        except:
            print("Error: Deepgram API request failed.")
            return

PATH_TO_FILE = 'speech_recognition\\life-moves-pretty-fast.wav'
async def main():
    transcriber = AudioTranscriber('en-GB')
    with open(PATH_TO_FILE, 'rb') as audio:
        response = await transcriber.transcribe_audio(audio)

asyncio.run(main())

