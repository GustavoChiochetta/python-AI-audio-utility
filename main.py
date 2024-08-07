from dotenv import load_dotenv
from openai import OpenAI
import argparse

parser = argparse.ArgumentParser(description='audio translator and transcriptor using whisper.')

parser.add_argument('file_path', type=str, help='File path for the audio file')
parser.add_argument('file_name', type=str, help='File name of audio file')
parser.add_argument('openai_key', type=str, help='Your open ai key.')
parser.add_argument('--translate', action='store_true', help='Should I translate the audio?', default=True)
parser.add_argument('--transcript', action='store_true', help='Should I transcript the audio?', default=True)

args = parser.parse_args()

file_path = args.file_path
file_name = args.file_name
openai_key = args.openai_key
# should_translate = args.translate (work in progress)
# should_transcript = args.transcript (work in progress)

def write_text_to_file(text, file_name, path):
    new_file_name = f"transcription_{file_name}.txt"
    file_path = f"{path}/{new_file_name}"

    with open(file_path, "w", encoding="utf-8") as text_file:
        text_file.write(text)

def call_api(api, audio_file, file_name, model_name, save_path):
    translation = api.create(
    model=model_name, 
    file=audio_file
    )

    write_text_to_file(translation.text, file_name, save_path)

def trascribe_translate_save_audio(api, file_path, file_name, model_name):
    print(f"transcribing and translating {file_name} into text using {model_name}")

    audio_file= open(file_path, "rb")

    translations_api = api.audio.translations
    transcribe_api = api.audio.transcriptions

    call_api(translations_api, audio_file, file_name, model_name, "translations")
    call_api(transcribe_api, audio_file, file_name, model_name, "transcriptions")

    print("\nDone!")

def main():
    load_dotenv()

    api_key = openai_key


    api = OpenAI(api_key=api_key)
    
    model_name = "whisper-1"
    
    trascribe_translate_save_audio(api, file_path, file_name, model_name)

if __name__ == "__main__":
    main()