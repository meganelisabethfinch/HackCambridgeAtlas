import os
import subprocess
import sys

# Install required Python libraries
subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

# Make directories
if not os.path.exists('temp'):
    os.makedirs('temp')
if not os.path.exists('keys'):
    os.makedirs('keys')

# Get keys
if not os.path.exists('keys/keys.py'):
    with open('keys/keys.py', 'w') as f:
        OPENAI_API_KEY = input("Enter OpenAI API key: ")
        DEEPGRAM_API_KEY = input("Enter Deepgram API key: ")
        f.write(f"OPENAI_API_KEY = \"{OPENAI_API_KEY}\"\nDEEPGRAM_API_KEY = \"{DEEPGRAM_API_KEY}\"\n")

print("Setup done!")
