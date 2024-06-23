import os
import shutil
import subprocess
import time
import logging

# Set up logging
logging.basicConfig(filename=os.path.expanduser("~/WhisperAudio/whisper_automation.log"),
                    level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

# Define directories
base_dir = os.path.expanduser("~/WhisperAudio")
audio_dir = os.path.join(base_dir, "audio")
processed_dir = os.path.join(base_dir, "processed")
text_dir = os.path.join(base_dir, "text")

# Create directories if they don't exist
os.makedirs(audio_dir, exist_ok=True)
os.makedirs(processed_dir, exist_ok=True)
os.makedirs(text_dir, exist_ok=True)

processed_files = set()

def process_audio_files():
    try:
        # List all audio files in the audio directory
        audio_files = [f for f in os.listdir(audio_dir) if os.path.isfile(os.path.join(audio_dir, f))]

        # Process each audio file
        for audio_file in audio_files:
            if audio_file not in processed_files:
                logging.info(f"Processing file: {audio_file}")

                # Define the paths
                input_path = os.path.join(audio_dir, audio_file)
                output_base = os.path.join(base_dir, os.path.splitext(audio_file)[0])

                # Run Whisper command
                result = subprocess.run(["whisper", input_path, "--model", "large", "--output_dir", base_dir])
                
                if result.returncode != 0:
                    logging.error(f"Error processing file {audio_file} with Whisper.")
                    continue

                # Move the processed audio file
                shutil.move(input_path, processed_dir)
                processed_files.add(audio_file)

                # Move the text, srt, and json files to the text directory
                for ext in [".txt", ".srt", ".json"]:
                    output_file = f"{output_base}{ext}"
                    if os.path.exists(output_file):
                        shutil.move(output_file, text_dir)
                logging.info(f"File processed and moved: {audio_file}")
    except Exception as e:
        logging.error(f"An error occurred: {e}")

print("Monitoring folder for new files...")
logging.info("Started monitoring folder for new files.")
while True:
    process_audio_files()
    time.sleep(10)  # Check for new files every 10 seconds
