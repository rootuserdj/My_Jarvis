from statistics import quantiles
import pyttsx3
import speech_recognition as sr
import openai
from dotenv import load_dotenv
import pyfirmata
import datetime
import face_recognition
import cv2
import numpy as np
import os


###################################################################################
# Ardino function
####################################################################################
board = pyfirmata.Arduino('COM3')
board.digital[7].mode = pyfirmata.OUTPUT
board.digital[7].write(1)
board.digital[8].mode = pyfirmata.OUTPUT
board.digital[8].write(1)
board.digital[9].mode = pyfirmata.OUTPUT
board.digital[9].write(1)


###################################################################################
# Speak Function
###################################################################################
def speak(name):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice' , voices[1].id)
    rate = engine.getProperty('rate')
    engine.setProperty('rate', 150)
    engine.say(name)
    engine.runAndWait()


#######################################################################################
# Take listen funstion
#######################################################################################
def takecom():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listning....")
       # r.adjust_for_ambient_noise(source, duration=0.5)
        audio = r.listen(source)
    try:
        print("Recognising.") 
        text = r.recognize_google(audio,language='en-in')
        print(text)
    except Exception:                #For Error handling
        return "none"
    return text

#################################################################################################
# Open ai code
###################################################################################################
apikey = "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"

openai.api_key = apikey

load_dotenv()
completion = openai.Completion()

chat_log_template = '''You : Hello, who are you?
Jarvis : I am doing great. How can I help you today?
'''

def Reply(question, chat_log=None):
    if chat_log is None:
        chat_log = chat_log_template
    prompt = f'{chat_log}You : {question}\nJarvis :'
    response = completion.create(
        prompt=prompt, engine="davinci", stop=['\nYou'], temperature=0.9,
        top_p=1, frequency_penalty=0, presence_penalty=0.6, best_of=1,
        max_tokens=150)
    answer = response.choices[0].text.strip()
    return answer



#######################################################################################
# Wish
#######################################################################################
def wish(name):

    try:
        speak("flash turning  off")
        board.digital[7].write(1)
        hour = int(datetime.datetime.now().hour)
        if hour >= 0 and hour<12:
            print(f"good morning {name} sir")
            speak(f"good morning {name} sir")
            main()
        else:
            print(f"good evening {name} sir")
            speak(f"good evening {name} sir")
            main()

    except:
        speak("i can't recognize your face ! beacuse i can't see your face clearly ! please turn on led or flashlight !")
        main()


###################################################################################
# Face Encoding
###################################################################################
def faceEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList



########################################################################################
# Images Matching 
########################################################################################
def matching():
    path = 'images'
    images = []
    personNames = []
    myList = os.listdir(path)
    for cu_img in myList:
        current_Img = cv2.imread(f'{path}/{cu_img}')
        images.append(current_Img)
        personNames.append(os.path.splitext(cu_img)[0])

    encodeListKnown = faceEncodings(images)

    cap = cv2.VideoCapture(0)
    speak("turnig on flash for face recognition ")

    while True:
       
        board.digital[7].write(0)

        ret, frame = cap.read()
        faces = cv2.resize(frame,(0,0), None, fx=0.25, fy=0.25)

        faces = cv2.cvtColor(faces, cv2.COLOR_BGR2RGB)

        facesCurrentFrame = face_recognition.face_locations(faces)
        encodesCurrentFrame = face_recognition.face_encodings(faces, facesCurrentFrame)

        for encodeFace, faceLoc in zip(encodesCurrentFrame, facesCurrentFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            # print(faceDis)
            matchIndex = np.argmin(faceDis)
            if matches[matchIndex]:
                name = personNames[matchIndex].upper()
             # print(name)
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(frame, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(frame, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                wish(name)
        if cv2.waitKey(1) == 13:
            break

    cap.release()
    cv2.destroyAllWindows()



def main():
    
    
    
    board.digital[7].write(1)
    while True:
        query = takecom().lower()
        if "turn on the light" == query:
            print("okey sir !")
            speak("okey sir !")
            board.digital[7].write(0)
        elif "turn off the light" == query:
            print("okey sir")           
            speak("okey sir!")
            board.digital[7].write(1)
        elif "who created you" == query:
            print("thanks for dhananjay sah for created me")
            speak("thanks for dhananjay sah for created me ")
        elif "turn on the fan" == query:
            speak("okey sir")
            board.digital[9].write(0)
        elif "turn off the fan" == query:
            speak("okey sir")
            board.digital[9].write(1)
        elif "turn on the room light" == query:
            speak("okey sir")
            board.digital[8].write(0)
        elif "turn off the room light" == query:
            speak("okey sir")
            board.digital[8].write(1)
        elif "bye" in query or "good bye" in query or "good bye jarvis" in query:
            speak("good bye sir ")
            break

        else:
            sound = Reply(query).lower()
            speak(sound)

matching()