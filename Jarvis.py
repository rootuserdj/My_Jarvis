from errno import EILSEQ
import speech_recognition as sr
import wikipedia
import pyttsx3
import webbrowser
import datetime
import random
import os






###################################################################################
# Speak Function
###################################################################################
def speak(sound):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice' , voices[1].id)
    rate = engine.getProperty('rate')
    engine.setProperty('rate', 150)
    engine.say(sound)
    engine.runAndWait()




#######################################################################################
# Wish
#######################################################################################
def wish():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour<12:
        speak("good morning sir")
    elif hour>= 12 and hour<18:
        speak("good evening sir")
    else:
        pass

 




#######################################################################################
# Take input funstion
#######################################################################################
def takecom():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listning....")
        r.adjust_for_ambient_noise(source, duration=0.4)
        audio = r.listen(source)
    try:
        print("Recognising.") 
        text = r.recognize_google(audio,language='en-in')
        print(text)
    except Exception:                #For Error handling
        exit()
        speak("error...")
        print("Network connection error") 
        return "none"
    return text





########################################################################################
# Main Function
########################################################################################
if __name__ == "__main__":
    wish()
    while True:
        query = takecom().lower()

        if "wikipedia" in query:
            speak("searching details....Wait")
            query.replace("wikipedia","")
            results = wikipedia.summary(query,sentences=2)
            print(results)
            speak(results)
        elif 'open youtube' in query or "open video online" in query:
            webbrowser.open("www.youtube.com")
            speak("opening youtube")
        elif 'open github' in query:
            webbrowser.open("https://www.github.com")
            speak("opening github")  
        elif 'open facebook' in query:
            webbrowser.open("https://www.facebook.com")
            speak("opening facebook")      
        elif 'open instagram' in query:
            webbrowser.open("https://www.instagram.com")
            speak("opening instagram")    
        elif 'open google' in query:
            webbrowser.open("https://www.google.com")
            speak("opening google")
            
        elif 'open yahoo' in query:
            webbrowser.open("https://www.yahoo.com")
            speak("opening yahoo")
            
        elif 'open gmail' in query:
            webbrowser.open("https://mail.google.com")
            speak("opening google mail") 
            
        elif 'open snapdeal' in query:
            webbrowser.open("https://www.snapdeal.com") 
            speak("opening snapdeal")  
             
        elif 'open amazon' in query or 'shop online' in query:
            webbrowser.open("https://www.amazon.com")
            speak("opening amazon")
        elif 'open flipkart' in query:
            webbrowser.open("https://www.flipkart.com")
            speak("opening flipkart")   
        elif 'open ebay' in query:
            webbrowser.open("https://www.ebay.com")
            speak("opening ebay")
        elif 'music from pc' in query or "music" in query:
            speak("ok i am playing music")
            music_dir = './music'
            musics = os.listdir(music_dir)
            os.startfile(os.path.join(music_dir,musics[0]))
        elif 'video from pc' in query or "video" in query:
            speak("ok i am playing videos")
            video_dir = './video'
            videos = os.listdir(music_dir)
            os.startfile(os.path.join(video_dir,videos[0]))  
        elif 'good bye' in query:
            speak("good bye")
            exit()
        elif "shutdown" in query:
            speak("shutting down")
            os.system('shutdown -s') 
        elif "what\'s up" in query or 'how are you' in query:
            stMsgs = ['Just doing my thing!', 'I am fine!', 'Nice!', 'I am nice and full of energy','i am okey ! How are you']
            ans_q = random.choice(stMsgs)
            speak(ans_q)  
            ans_take_from_user_how_are_you = takecom()
            if 'fine' in ans_take_from_user_how_are_you or 'happy' in ans_take_from_user_how_are_you or 'okey' in ans_take_from_user_how_are_you:
                speak('okey..')  
            elif 'not' in ans_take_from_user_how_are_you or 'sad' in ans_take_from_user_how_are_you or 'upset' in ans_take_from_user_how_are_you:
                speak('oh sorry..')  
        elif 'who make you' in query or 'who created you' in query or 'who develop you' in query:
            ans_m = " For your information Dhananjay sah Created me ! I give Lot of Thanks to Him "
            print(ans_m)
            speak(ans_m)
        elif "who are you" in query or "about you" in query or "your details" in query:
            about = "I am Jarvis an A I based computer program but i can help you lot like a your close friend ! i promise you ! Simple try me to give simple command ! like playing music or video from your directory i also play video and song from web or online ! i can also entain you i so think you Understand me ! ok Lets Start "
            print(about)
            speak(about)
        elif "hello" in query or "hello Jarvis" in query:
            hel = "Hello Dhananjay Sir ! How May i Help you.."
            print(hel)
            speak(hel)
        elif "your name" in query or "sweat name" in query:
            na_me = "Thanks for Asking my name my self ! Jarvis"  
            print(na_me)
            speak(na_me)
        elif "you feeling" in query:
            print("feeling Very sweet after meeting with you")
            speak("feeling Very sweet after meeting with you") 
        elif query == 'none':
            continue 
        elif 'exit' in query or 'abort' in query or 'stop' in query or 'bye' in query or 'quit' in query :
            ex_exit = 'I feeling very sweet after meeting with you but you are going! i am very sad'
            speak(ex_exit)
            exit()
        elif "time" in query or "what is the time" in query or "what is the time now" in query or "time now" in query:
            now = datetime.datetime.now()
            current_time = now.strftime("%H:%M")
            print("the time is "+current_time+" sir")
            speak("the time is "+current_time+" sir")
        elif "play my favourite song" in query or "play favourite songs" in query or "favourite song" in query:
            webbrowser.open("https://youtu.be/79eF1VY9mW8")
            speak("playing your favourite song")
        else:
            temp = query.replace(' ','+')
            g_url="https://www.google.com/search?q="    
            res_g = 'sorry! i cant understand but i search from internet to give your answer ! okay'
            print(res_g)
            speak(res_g)
            webbrowser.open(g_url+temp) 