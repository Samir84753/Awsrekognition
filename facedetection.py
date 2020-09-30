import boto3
import prettytable
import json
from tkinter import Tk 
from tkinter.filedialog import askopenfilename
Tk().withdraw()
photo = askopenfilename()    
# photo='rock.jpeg' 
from PIL import Image
im = Image.open(photo)
im.show()

client=boto3.client('rekognition')

#   open image
with open(photo, 'rb') as image:
    response_celeb = client.recognize_celebrities(Image={'Bytes': image.read()})
with open(photo,'rb') as image:
        response = client.detect_faces(Image={'Bytes': image.read()},Attributes=['ALL'])  
# check if image is a celebrity   
if response_celeb['CelebrityFaces']:
    for celebrity in response_celeb['CelebrityFaces']:
        print('Celebrity Status: True')
        print ('Name: ' + celebrity['Name']+'\n')
        # for url in celebrity['Urls']:
        #     print ('   ' + url)
else:
    print('Celebrity Status: False')

# image details
for person in response['FaceDetails']:
    print('Gender:',person['Gender']['Value'])
    print('Age Range:'+str(person['AgeRange']['Low'])+'-'+str(person['AgeRange']['High']))
    print('\n')
    for face in response['FaceDetails']:
        emo = prettytable.PrettyTable(["Emotions", "Confidence"])
        for emotion in face['Emotions']:
            emo.add_row([emotion['Type'],'{:.3f}'.format(emotion['Confidence'])])
    print(emo)
   
    for face in response['FaceDetails']:
        p = prettytable.PrettyTable(["Pose", "Confidence"])
        for pose in face['Pose'].items():
            p.add_row([pose[0],'{:.3f}'.format(pose[1])])
    print(p)
    for pic in response['FaceDetails']:
        a = prettytable.PrettyTable(["Quality", "Confidence"])
        for quality in face['Quality'].items():
            a.add_row([quality[0],'{:.3f}'.format(quality[1])])
    print(a)
    if person['Sunglasses']['Value']:
        print('Wearing Sunglasses ','\tConfidence:',person['Sunglasses']['Confidence'])
    if person['MouthOpen']['Value']:
        print('Mouth is open','\tConfidence:',person['MouthOpen']['Confidence'])
    if person['Eyeglasses']['Value']:
        print('Wearing Eyeglasses','\tConfidence:',person['Eyeglasses']['Confidence'])
    if person['Mustache']['Value']:
        print('Has a Moustache','\tConfidence:',person['Mustache']['Confidence'])
    if person['Beard']['Value']:
        print('Has a Beard','\tConfidence:',person['Beard']['Confidence'])
    if person['Smile']['Value']:
        print('Has a Smile','\tConfidence:',person['Smile']['Confidence'])
    if person['EyesOpen']['Value']:
        print('Eyes are open','\tConfidence:',person['EyesOpen']['Confidence'])


