import os
import shutil
import subprocess
import time

# Define directories
base_dir = os.path.expanduser("~/WhisperAudio")
audio_dir = os.path.join(base_dir, "audio")
processed_dir = os.path.join(base_dir, "processed")
text_dir = os.path.join(base_dir, "text")

# Create directories if they don't exist
os.makedirs(audio_dir, exist_ok=True)
os.makedirs(processed_dir, exist_ok=True)
os.makedirs(text_dir, exist_ok=True)

def process_audio_files():
    # List all audio files in the audio directory
    audio_files = [f for f in os.listdir(audio_dir) if os.path.isfile(os.path.join(audio_dir, f))]

    # Process each audio file
    for audio_file in audio_files:
        # Define the paths
        input_path = os.path.join(audio_dir, audio_file)
        output_base = os.path.join(base_dir, os.path.splitext(audio_file)[0])
        
        # Run Whisper command
        subprocess.run(["whisper", input_path, "--model", "large", "--output_dir", base_dir])
        
        # Move the processed audio file
        shutil.move(input_path, processed_dir)
        
        # Move the text, srt, and json files to the text directory
        for ext in [".txt", ".srt", ".json"]:
            output_file = f"{output_base}{ext}"
            if os.path.exists(output_file):
                shutil.move(output_file, text_dir)

print("Monitoring folder for new files...")
while True:
    process_audio_files()
    time.sleep(10)  # Check for new files every 10 seconds
