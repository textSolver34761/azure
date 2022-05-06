import azure.cognitiveservices.speech as speechsdk
import json

cred = json.load(open('auth.json'))
API_KEY = cred['API_SPEACH']
ENDPOINT = cred['END_POINT_SPEACH']
LOCATION = cred['SPEACH_LOCATION']

speech_config = speechsdk.SpeechConfig(subscription=API_KEY, region=LOCATION)
audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)

# The language of the voice that speaks.
#speech_config.speech_synthesis_voice_name='fr-FR-DeniseNeural'
#speech_config.speech_synthesis_voice_name='fr-FR-HenriNeural'
speech_config.speech_synthesis_voice_name='fr-CH-ArianeNeural'

speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

# Get text from the console and synthesize to the default speaker.
print("Enter some text that you want to speak >")
text = input()

speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()

if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
    print("Speech synthesized for text [{}]".format(text))
elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
    cancellation_details = speech_synthesis_result.cancellation_details
    print("Speech synthesis canceled: {}".format(cancellation_details.reason))
    if cancellation_details.reason == speechsdk.CancellationReason.Error:
        if cancellation_details.error_details:
            print("Error details: {}".format(cancellation_details.error_details))
            print("Did you set the speech resource key and region values?")