from os import getenv
from dotenv import load_dotenv
from openai import OpenAI

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

    api_key = getenv('OPENAI_API_KEY')
    project_id = getenv('OPENAI_PROJECT_ID')
    organization_id = getenv('OPENAI_ORGANIZATION_ID')


    api = OpenAI(
    organization=organization_id,
    project=project_id,
    api_key=api_key
    )
    
    model_name = "whisper-1"
    file_path = "podcasts/cloudstrike_short.mp3"
    file_name = "cloudstrike_short"
    file_url = "https://www.hipsters.tech/incidente-incrivel-da-cloudstrike-hipsters-ponto-tech-421/"
    
    trascribe_translate_save_audio(api, file_path, file_name, model_name)

if __name__ == "__main__":
    main()