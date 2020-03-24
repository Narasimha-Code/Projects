import win32com.client
import speech_recognition as sr
import wikipediaapi
import json
import webbrowser
l=sr.Recognizer()
speaker=win32com.client.Dispatch("SAPI.SpVoice")
def getaudiodata():
    flag=1
    with sr.Microphone() as source:
        l.adjust_for_ambient_noise(source)
        while flag:
            audio_data=l.record(source,duration=5)
            try:
                text=l.recognize_google(audio_data)
            except:
                speaker.Speak("Cant hear anything,Please say again")
            else:
                speaker.Speak(text)
                flag=0
                return text
def countrolanalizer(text):
    text=text.replace(" ","+")
    if "talk" in text or "let's+talk" in text:
        return 1
    elif "dictionary" in text:
        return 2
    elif "quizlet" in text or "test+me" in text or "quiz" in text:
        return 3
    elif "convert+text+to+speech" in text or "text+to" in text:
        return 4
    elif "convert+speech+to+text" in text or "to+text" in text:
        return 5
    elif "voice" in text:
        return 6
    elif "Exit" in text or "stop" in text:
        return 0
    else:
        speaker.Speak("Can't understand")
        return -1
def textanalizer(text):
    data=json.load(open("D:\Python_files\Python\Project\DataBase\intents.json"))
    print(text)
    print(data.keys())
    if text in data.keys():
        return data[text]
    wiki_obj= wikipediaapi.Wikipedia('en')
    page_data= wiki_obj.page(text)
    if(page_data.exists()):
        return page_data.summary[0:300]
    text=text.replace(" ","+")
    link="https://www.bing.com/search?q="+text+"&qs=n&form=QBRE&sp=-1&pq=what&sc=8-4&sk=&cvid=C489A5BBC2864AEAAAC95A2A8926ABEC"
    webbrowser.open(link)
    return None