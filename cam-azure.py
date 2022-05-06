import base64
import os
import io
import json
from azure.cognitiveservices.vision.face import FaceClient
from cv2 import VideoCapture
from itsdangerous import base64_decode, base64_encode
from msrest.authentication import CognitiveServicesCredentials
import requests
from PIL import Image, ImageDraw, ImageFont
import cv2 as cv
import argparse
from xmlrpc.client import boolean

cred = json.load(open('auth.json'))
API_KEY = cred['API_KEY']
ENDPOINT = cred['END_POINT']

face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(API_KEY))





capture = cv.VideoCapture(0)
if not capture.isOpened():
    print('Unable to open')
    exit(0)
while True:
    bool, frame = capture.read()
    if(bool == True):
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        cv.imshow('live', frame)
        #buf = io.BytesIO(base64.encode(capture, feed))
        #img = Image.open(capture)
        decoded_vid:bytes
        decoded_vid = cv.VideoCapture(0)
        cap = cv.VideoCapture(io.BytesIO(base64.encodebytes(decoded_vid)))
        img = Image.open(capture)
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("arial.ttf", 10)
        #    buf = io.BytesIO()
        result = face_client.face.detect_with_stream(
        #capture = base64.encodebytes(capture),
        capture = io.BytesIO(base64.encodebytes(cv. capture)),
        detection_model='detection_01',
        recognition_model='recognition_04',
        return_face_attributes=['age','gender','headPose','smile','facialHair','glasses','emotion','hair','makeup','occlusion','accessories','blur','exposure','noise'],
        #return_face_id=True
        )
        if not result:
            raise Exception('Pas de personne sur l\'image')
        print('Il y a {0} personne(s) sur l\'image '.format(len(result)))

        if(cv.waitKey(20) == ord('x')):
            break
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
capture.release()
cv.destroyAllWindows()