import json
import azure.cognitiveservices.speech as speech
from django import conf
from gevent import config

cred = json.load(open('auth.json'))
API_KEY = cred['API_SPEACH']
ENDPOINT = cred['END_POINT_SPEACH']
LOCATION = cred['SPEACH_LOCATION']

#media_file_path = './test.wav'
media_file_path = './test.mp3'

translation_config = speech.translation.SpeechTranslationConfig(subscription=API_KEY, endpoint=ENDPOINT)

translation_config.speech_recognition_language = 'ja-JP'
translation_config.add_target_language('en')


audio_config = speech.audio.AudioConfig(filename=media_file_path)

recognizer = speech.translation.TranslationRecognizer(translation_config=translation_config, audio_config=audio_config)

#recognizer = speech.translation.TranslationRecognitionResult(conf)

result = recognizer.recognize_once()

vars(result)
