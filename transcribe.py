import os
from moviepy.editor import VideoFileClip
import speech_recognition as sr

# Define the directory containing `.mov` files
input_directory = "/Users/dev/Movies/Transcribe"

# Check if the directory exists
if not os.path.exists(input_directory):
    print(f"Directory {input_directory} does not exist.")
    exit()

# Create an output directory for transcriptions
output_directory = os.path.join(input_directory, "Transcriptions")
os.makedirs(output_directory, exist_ok=True)

# Initialize the speech recognizer
recognizer = sr.Recognizer()

# Iterate through all `.mov` files in the directory
for filename in os.listdir(input_directory):
    if filename.endswith(".mov"):
        filepath = os.path.join(input_directory, filename)
        print(f"Processing: {filename}")

        try:
            # Extract audio from the video
            video = VideoFileClip(filepath)
            audio_path = os.path.join(output_directory, f"{os.path.splitext(filename)[0]}.wav")
            video.audio.write_audiofile(audio_path)

            # Transcribe the audio
            audio_file = sr.AudioFile(audio_path)
            with audio_file as source:
                audio_data = recognizer.record(source)

            # Recognize the speech
            try:
                transcription = recognizer.recognize_google(audio_data)
                print(f"Transcription for {filename}:")
                print(transcription)

                # Save the transcription to a text file
                transcription_path = os.path.join(output_directory, f"{os.path.splitext(filename)[0]}.txt")
                with open(transcription_path, "w") as f:
                    f.write(transcription)

                print(f"Saved transcription to {transcription_path}\n")

            except sr.UnknownValueError:
                print(f"Could not understand the audio in {filename}.")
            except sr.RequestError as e:
                print(f"Error with the transcription API for {filename}: {e}")

        except Exception as e:
            print(f"Error processing {filename}: {e}")

print("Transcription complete!")