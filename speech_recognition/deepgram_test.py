#!/usr/bin/env python3

from deepgram import Deepgram
import asyncio, json

# Your Deepgram API Key
DEEPGRAM_API_KEY = '84dfb83a357fb78cc94cab587f5c8f27f7d1ee2a'

# Name and extension of the file you downloaded (e.g., sample.wav)
PATH_TO_FILE = 'life-moves-pretty-fast.wav'

async def main():
  # Initialize the Deepgram SDK
  dg_client = Deepgram(DEEPGRAM_API_KEY)
  # Open the audio file
  with open(PATH_TO_FILE, 'rb') as audio:
    # Replace mimetype as appropriate
    source = {'buffer': audio, 'mimetype': 'audio/wav'}
    response = await dg_client.transcription.prerecorded(source, {'punctuate': True})
    print(json.dumps(response, indent=4))

    # get sentence
    # return response.get("results").get("channels")[0].get("alternatives")[0].get("transcript")

asyncio.run(main())
