import os
import io
import json
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
import requests
from PIL import Image, ImageDraw, ImageFont
import cv2
import argparse

cred = json.load(open('auth.json'))
API_KEY = cred['API_KEY']
ENDPOINT = cred['END_POINT']

face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(API_KEY))

parser = argparse.ArgumentParser(description='This program shows how to use background subtraction methods provided by OpenCV. You can process both videos and images.')
parser.add_argument('--input', type=str, help='Path to a video or a sequence of image.', default='vtest.avi')
parser.add_argument('--algo', type=str, help='Background subtraction method (KNN, MOG2).', default='MOG2')
args = parser.parse_args()


#img_file = open('.\img\dwaynejohnson.jpg', 'rb')
#img_file = open('.\img\celebrity.jpg', 'rb')
#img_file = open('.\img\Joe-Biden.jpg', 'rb')
img = cv2.VideoCapture(0) #unencoded (raw) image, from the camera
if not img.isOpened():
    print('Unable to open: ' + args.input)
    exit(0)

# buf will be the encoded image
#ret,buf = cv2.imencode('.jpg', img)
buf = img.read()

# stream-ify the buffer
stream = io.BytesIO(buf)

result = face_client.face.detect_with_stream(
    stream,
    detection_model='detection_01',
    recognition_model='recognition_04',
    return_face_attributes=['age','gender','headPose','smile','facialHair','glasses','emotion','hair','makeup','occlusion','accessories','blur','exposure','noise'],
    return_face_id=True
)
if not result:
    raise Exception('Pas de personne sur l\'image')
print('Il y a {0} personne(s) sur l\'image '.format(len(result)))

img = Image.open(stream)
draw = ImageDraw.Draw(img)
font = ImageFont.truetype("arial.ttf", 10)

for face in result:
    attr = face.face_attributes
    #print(attr)
    age = attr.age
    gender = attr.gender
    hair = attr.facial_hair
    moustache = hair.moustache
    #print('Moustache ', moustache*100 , '%')
    glasses = attr.glasses
    #print('luntettes', glasses)
    makeup = attr.makeup
    #print('Maquillage' , makeup)
    rect = face.face_rectangle
    left = rect.left
    top = rect.top
    right = rect.width + left
    bottom = rect.height + top
    draw.rectangle(( (left, top),(right, bottom )  ), outline='green', width=5)
    emotion = attr.emotion
    anger = '{0:.0f}%'.format(emotion.anger * 100)
    contempt = '{0:.0f}%'.format(emotion.contempt * 100)
    disgust = '{0:.0f}%'.format(emotion.disgust * 100)
    fear = '{0:.0f}%'.format(emotion.fear * 100)
    happiness = '{0:.0f}%'.format(emotion.happiness * 100)
    neutral = '{0:.0f}%'.format(emotion.neutral * 100)
    sadness = '{0:.0f}%'.format(emotion.sadness * 100)
    surprise = '{0:.0f}%'.format(emotion.surprise * 100)
    dictionary = {
        "anger": emotion.anger * 100,
        "contempt":emotion.anger * 100 ,
        "disgust" : emotion.disgust * 100,
        "fear": emotion.fear * 100,
        "happiness": emotion.happiness * 100,
        "neutral" : emotion.neutral * 100,
        "sadness": emotion.sadness * 100,
        "surprise" : emotion.surprise * 100
    }
    hightest_Emotion = max(dictionary, key=dictionary.get)
    hightest_EmotionV = max(list(dictionary.values()))
    draw.text((right + 4, top), 'Age :' + str(int(age)), (0, 128, 0), font=font)
    draw.text((right + 4, top + 35), 'Gender :' + str(gender), (0, 128, 0), font=font)
    draw.text((right + 4, top + 65), 'Highest Emotion detected :' + hightest_Emotion + ': ' + str(hightest_EmotionV), (0, 128, 0), font=font)

img.show()