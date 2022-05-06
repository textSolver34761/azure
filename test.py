import os
import io
import json
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
import requests
from PIL import Image, ImageDraw, ImageFont

cred = json.load(open('auth.json'))
API_KEY = cred['API_KEY']
ENDPOINT = cred['END_POINT']

face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(API_KEY))
img_url = 'https://upload.wikimedia.org/wikipedia/commons/9/93/Michael_Schumacher_-_Fernand_Bachmann_-_Cropped.jpg'
#img_url = 'https://upload.wikimedia.org/wikipedia/commons/0/08/Michael_Schumacher_Bernie_Ecclestone_September_1991.jpg'
#img_url = 'https://upload.wikimedia.org/wikipedia/commons/9/96/Bill_Nye%2C_Barack_Obama_and_Neil_deGrasse_Tyson_selfie_2014.jpg'
image_name = os.path.basename(img_url)
result = face_client.face.detect_with_url(img_url,detection_model='detection_03', recognition_model='recognition_04')

if not result:
    raise Exception('Pas de personne sur l\'image')
print('Il y a {0} personne(s) sur l\'image '.format(len(result)))

response_img = requests.get(img_url)
img = Image.open(io.BytesIO(response_img.content))
draw = ImageDraw.Draw(img)

for face in result:
    rect = face.face_rectangle
    left = rect.left
    top = rect.top
    right = rect.width + left
    bottom = rect.height + top
    draw.rectangle(( (left, top),(right, bottom )  ), outline='green', width=5)
img.show()