import requests
import wolframalpha
import os
import datetime
import random
import time
from api.ai import Agent
import json
# import pyttsx3
from gtts import gTTS
from playsound import playsound
import cv2
import subprocess
import pyaudio
import wikipedia
import speech_recognition as sr
import webbrowser as wb

wake_words = ["wake","john"]
greeting_phrases = ['howdy sir','whassup sir',"what's up sir",'hi sir','hello sir','hey sir']

agent = Agent(
     '<subscription-key>',
     'd7b00ed0ee08464c860a9f6e8eb7164e',
     '6fef320b63224ce6a42b443ec8428db1',
)
def chat(inp):
    response = agent.query(inp)
    result = response['result']
    fulfillment = result['fulfillment']
    response = fulfillment['speech']
    speak(response)
    
def exec_command(command):
    os.system(command)

def websearch_google():           
    r=sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        said=""

        try:
            said=r.recognize_google(audio)
            speak("Okay,i will search for{} in google".format(said))
        except Exception as e:
            speak("Some error occured    ")
    wb.open("https://www.google.com/search?q={}".format(said))   


def speak(message):
    speech = gTTS(text=message , lang='en')
    speech.save("speech.mp3")
    print(message)
    playsound("speech.mp3")

def wikisearch(get_audiowiki):
    searchstring = ""
    if "wiki" in get_audiowiki:
        searchstring = get_audiowiki.replace("wiki", "")

    elif "wikipedia" in get_audiowiki:
        searchstring = get_audiowiki.replace("wikipedia", "")
    if "search" in get_audiowiki:
        searchstring = get_audiowiki.replace("search", "")

    results = wikipedia.summary(searchstring,sentences = 2)
    speak(results)
    speak(f"According to wikipedia,{results}")

def youtube_search(item):
    url = f"https://www.youtube.com/results?search_query={item}"
    wb.open(url) 


def wishBoss():
    speak(random.choice(greeting_phrases))
    hour = int(datetime.datetime.now().hour)
    if hour>=3 and hour<6:
        speak('Good Day')
    elif hour>=6 and hour<12:
        speak('Good Morning')
    elif hour>=12 and hour<18:
        speak('Good Afternoon')
    else:
        speak('Good Evening')

client=wolframalpha.Client("U78Y2E-GR8KLU8U5U")

def wolframalpha():
    while True:
        query=get_audio("Enter what you want to know :")
        res=client.query(query)
        ans=next(res.results).text
        speak(f"THis is what i got from the web {ans}")

def createFolderIfNotExists(name):
    if not os.path.exists(name):
        os.makedirs(name)
    


def move(files, folder):
    for file in files:
        os.replace(f"{file}", f"{folder}/{file}")
        

def file_organizer():
    target_folder_path = input("""Please enter the path if the directory you want me
    to operate with (You must type this...Don't use voice command) : """ )
    
    files = os.listdir(target_folder_path)
    files.remove("file_organizer.py")

    folders_to_be_made = ["Images", "Medias", "Docs", "Others","Programs"]

    for folder in folders_to_be_made:
        createFolderIfNotExists(folder)

    imageExts = [".png",".jpg",".jpeg"]
    mediaExts = [".flv", ".mp3", ".mp4", ".wav"]
    docsExts = [".docx", ".xlsx", ".pdf", ".pptx", ".txt", ".doc"]
    othersExts = []
    programsExts = [".java",".py",".php",".html",",css",".js",".ts",".c",".cpp",".htm",".cs",".dart"]

    images = []
    medias = []
    docs = []
    others = []
    programs = []    

    for file in files:
        ext = os.path.splitext(file)[1]
        
        for extension in imageExts:
            if ext == extension:
                images.append(file)

        for extension in mediaExts:
            if ext == extension:
                medias.append(file)

        for extension in docsExts:
            if ext == extension:
                docs.append(file)
        
        for extension in programsExts:
            if ext == extension:
                programs.append(file)

        if (ext not in imageExts) and (ext not in mediaExts) and (ext not in docsExts) and (ext not in programsExts) and os.path.isfile(file):         
            others.append(file)


    move(images,"Images")    
    move(medias,"Medias")    
    move(docs,"Docs")    
    move(others,"Others")    
    move(programs, "Programs")

def weather():
    api_key = "37398a81e248fdede1955c07d51ecb69"
    speak("Enter the name of the city : ")
    city = get_audio()
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    results = requests.request(method="POST",url=url)
    jsondata = results.json()
    weather_description = jsondata["weather"][0]["description"]
    temp = round(float(jsondata["main"]["temp"]) - 273,ndigits=2) 
    temp_min = round(float(jsondata["main"]["temp_min"]) - 273,ndigits=2)  
    temp_max = round(float(jsondata["main"]["temp_max"]) - 273,ndigits=2)  
    pressure = jsondata["main"]["pressure"]
    humidity = jsondata["main"]["humidity"]
    wind_speed = jsondata["wind"]["speed"]

    speak(f"{weather_description}")
    time.sleep(0.6)

    weather_data = f"""
    temperature {temp}  degree celsius
    maximum temperature {temp_max}  degree celsius      
    minimum temperature {temp_min}  degree celsius
    Pressure {pressure}    millibars
    Humidity {humidity}
    wind speed {wind_speed}  knots
    """

    speak(weather_data)

def get_audio():
    r = sr.Recognizer()
    
    while(1):     
          
        # Exception handling to handle 
        # exceptions at the runtime 
        try: 
              
            # use the microphone as source for input. 
            with sr.Microphone() as source2: 
                  
                # wait for a second to let the recognizer 
                # adjust the energy threshold based on 
                # the surrounding noise level  
                r.adjust_for_ambient_noise(source2, duration=0.2) 
                  
                #listens for the user's input  
                audio2 = r.listen(source2) 
                  
                # Using ggogle to recognize audio 
                MyText = r.recognize_google(audio2) 
                return MyText 
                print("User : ",MyText)
                  
        except sr.RequestError as e: 
            speak("Could not request results; {0}".format(e)) 
              
        except sr.UnknownValueError: 
            speak("unknown error occured") 


def get_intent(inp):
    response = agent.query(inp)
    result = response['result']
    intent = result['metadata']['intentName']
    return intent
    

def work():
    while True:
                try:

                    # inp = get_audio()
                    inp = input("User : ")
                    intent = get_intent(inp)
                    if "TellToSearch" in intent:
                        response = agent.query(inp)
                        result = response['result']    
                        searchstring = result['parameters']['searched_item']
                        results = wikipedia.summary(searchstring,sentences = 2)
                        speak(results)
                        # speak(f"{results}")
                    if "go to" in inp:
                        query = inp.replace("go to", "")
                        speak(f"Okay! Going to {query}")
                        wb.open(query)
                        speak("Done!")

                    elif "youtube" in inp:
                        speak("Okay! Fetching Results")
                        query = inp.replace("youtube", "")
                        wb.open(f'https://www.youtube.com/results?search_query={query}')
                        speak("Checkout Youtube Results!")

                    elif "wikipedia" in inp:
                        wikisearch(inp)

                    elif 'the time' in inp:
                        strTime = datetime.datetime.now().strftime("%H:%M")
                        t = time.strptime(strTime, "%H:%M")
                        timevalue_12hour = time.strftime( "%I:%M %p", t )   
                        speak(f"Sir, the time is {timevalue_12hour}") 

                    elif "change your voice" in inp:
                        s=1
                        speak("Okay...  changing my voice ")
                        voices = engine.getProperty('voices')
                        if s==1:
                            engine.setProperty('voice', voices[1].id)
                            s=0
                        else:
                            engine.setProperty('voice', voices[0].id)
                        speak("Okay...  i have changed my voice  ")
    
                    elif "wiki" in inp:
                        wikisearch(inp)                
                    elif "open vscode" in inp:
                        speak("Opening Visual Studio Code ...")
                        exec_command("code")
                    elif ("organize" in inp) and (("folder" in inp) or ("directory" in inp)):
                        file_organizer()

                    elif "current" in inp and "weather" in inp:
                        weather()
                    elif 'click' in inp and "photo" in inp:
                        stream = cv2.VideoCapture(0)
                        grabbed, frame = stream.read()
                        if grabbed:
                            cv2.imshow('pic', frame)
                            cv2.imwrite('pic.jpg',frame)
                        stream.release()

                    elif 'record' in inp and "video" in inp:
                        try:
                            cap = cv2.VideoCapture(0)
                            out = cv2.VideoWriter('output.avi', -1, 20.0, (640,480))
                            while(cap.isOpened()):
                                ret, frame = cap.read()
                                if ret:
                                    
                                    out.write(frame)

                                    cv2.imshow('frame',frame)
                                    if cv2.waitKey(1) & 0xFF == ord('q'):
                                        break
                                else:
                                    break
                            cap.release()
                            out.release()
                            cv2.destroyAllWindows()

                        except Exception as e:
                            speak("video completed")    
                            
                                
                    elif "bye" in inp:
                        speak("okay      bye   see you soon")
                        exit(0)                  
                    else:    
                        chat(inp)
                        
                except Exception as e :
                    # speak("Sorry sir     can't understand  ")
                    continue
    
if __name__ == "__main__":
    while True:
            # wake = get_audio()
            # if "john" in wake:
                wishBoss()
                work()
           
           
