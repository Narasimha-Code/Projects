from tkinter import *
import tkinter.font as font
import threading
import speech_recognition as sr
import win32com.client
import json
import Operations.operations
import random
l=sr.Recognizer()
speaker=win32com.client.Dispatch("SAPI.SpVoice")
def homepage():
    global screen1
    screen1=Tk()
    myFont = font.Font(size=50)
    screen1.configure(bg="#93bfed")
    screen1.title("Speak Bot")
    screen1.geometry('1920x1080')
    robo_img=PhotoImage(file=r"D:\Python_files\Python\Project\Images\robot.png")
    dict_img=PhotoImage(file=r"D:\Python_files\Python\Project\Images\unnamed.png")
    dict_img=dict_img.subsample(3,3)
    quiz_image=PhotoImage(file=r"D:\Python_files\Python\Project\Images\quizlet_logo_large.png")
    quiz_image=quiz_image.subsample(5,5)
    texttospeach_img=PhotoImage(file=r"D:\Python_files\Python\Project\Images\TexttoSpeech.png")
    texttospeach_img=texttospeach_img.subsample(3,3)
    speachtotext_img=PhotoImage(file="D:\Python_files\Python\Project\Images\SpeechToText.png")
    speachtotext_img=speachtotext_img.subsample(3,3)
    letstalk_img=PhotoImage(file=r"D:\Python_files\Python\Project\Images\letstalklogotransparent.png")
    letstalk_img=letstalk_img.subsample(3,3)
    humatorob_img=PhotoImage(file=r"D:\Python_files\Python\Project\Images\high-five.png")
    humatorob_img=humatorob_img.subsample(3,3)
    stop_img=PhotoImage(file=r"D:\Python_files\Python\Project\Images\stop.png")
    stop_img=stop_img.subsample(5,5)
    Label(text="Speak Bot",font=myFont,pady=20,padx=800,fg="white",bg="#4c9aed").pack()
    Button(screen1,image=robo_img,bg="#93bfed",bd=0).pack()
    Button(screen1,image=letstalk_img,width=300,height=150,bg="#ddf0ce").place(x=300,y=150)
    Button(screen1,image=dict_img,width=300,height=150,bg="#ddf0ce").place(x=200,y=350)
    Button(screen1,image=quiz_image,width=300,height=150,bg="#ddf0ce").place(x=300,y=550)
    Button(screen1,image=texttospeach_img,width=300,height=150,bg="#ddf0ce").place(x=950,y=150)
    Button(screen1,image=speachtotext_img,width=300,height=150,bg="#ddf0ce").place(x=1000,y=350)
    Button(screen1,image=humatorob_img,width=300,height=150,bg="#ddf0ce").place(x=950,y=550)
    Button(screen1,image=stop_img,width=150,height=100,bg="#ddf0ce").place(x=700,y=680)
    screen1.mainloop()
def quiz_screen(qu,ans,o1,o2,o3):
    o1='1'+" "+o1
    ans='3'+" "+ans
    o3='2'+" "+o3
    o2='4'+" "+o2
    global screen2
    screen2=Toplevel(screen1)
    screen2.configure(bg="white")
    screen2.title("Quiz")
    screen2.geometry('1920x1080')
    myfont=font.Font(size=20)
    Label(screen2,text=qu,font=myfont).place(x=50,y=300)
    Label(screen2,text=o1).place(x=500,y=450)
    Label(screen2,text=o3).place(x=500,y=500)
    Label(screen2,text=ans).place(x=800,y=450)
    Label(screen2,text=o2).place(x=800,y=500)
def letstalk():
    speaker.Speak("Say a keyword or ask something")
    text=Operations.operations.getaudiodata()
    text2=Operations.operations.textanalizer(text)
    if text2==None:
        speaker.Speak("These are the results founded in web")
    else:
        speaker.Speak(text2)
    start()
def dictionary():
    speaker.Speak("Say a keyword to search")
    data=json.load(open("D:\Python_files\Python\Project\DataBase\Dictionary_data.json"))
    text=Operations.operations.getaudiodata()
    text=text.lower()
    if text in data.keys():
        speaker.Speak(data[text][0])
    else:
        speaker.Speak("Cant find please retry")
    start()
def quiz():
    data=json.load(open("D:\Python_files\Python\Project\DataBase\JEOPARDY_QUESTIONS1.json"))
    quest_no=random.randint(0,50)
    qu=data[quest_no]["question"]
    ans=data[quest_no]["answer"]
    o1=data[random.randint(0,50)]["answer"]
    o2=data[random.randint(0,50)]["answer"]
    o3=data[random.randint(0,50)]["answer"]
    t2=threading.Thread(target=quiz_screen,args=(qu,ans,o1,o2,o3))
    t2.start()
    speaker.Speak("Lets start Quiz")
    speaker.Speak(qu)
    speaker.Speak(o1)
    speaker.Speak(ans)
    speaker.Speak(o2)
    speaker.Speak(o3)
    speaker.Speak("Say your answer")
    answ=Operations.operations.getaudiodata()
    if answ=='3' or answ=='three' or answ==ans or answ=="number three" or answ=="tree":
        speaker.Speak("Correct answer")
        screen2.destroy()
        quiz()
    else:
        speaker.Speak("Wrong answer")
        screen2.destroy()
    start()
def filetospeech():
    f=open("texttospeech.txt",'r')
    text=f.read()
    speaker.Speak(text)
    start()
def speechtotext():
    speaker.Speak("Say to write")
    f=open("speechtotext.txt",'w')
    text=Operations.operations.getaudiodata()
    f.write(text)
    f.close()
    speaker.Speak("Succesfully written")
    start()
def recordvoice():
    flag=1
    speaker.Speak("Say something")
    with sr.Microphone() as source:
        l.adjust_for_ambient_noise(source)
        while flag:
            audio_data=l.record(source,duration=3)
            try:
                text=l.recognize_google(audio_data)
                with open("changedaudio.wav","wb") as f:
                    f.write(audio_data.get_wav_data())
                flag=0
            except:
                speaker.Speak("Cant hear any thing")
    speaker.Speak("Data changed and saved")
    start()
def start():
    flag=-1
    while flag==-1:
        speaker.Speak("How can I help you")
        text=Operations.operations.getaudiodata()
        flag=Operations.operations.countrolanalizer(text)
        if flag==1:
            letstalk()
        elif flag==2:
            dictionary()
        elif flag==3:
            quiz()
        elif flag==4:
            filetospeech()
        elif flag==5:
            speechtotext()
        elif flag==6:
            recordvoice()
    screen1.destroy()
Homepage_t1=threading.Thread(target=homepage)
Homepage_t1.start()
start()