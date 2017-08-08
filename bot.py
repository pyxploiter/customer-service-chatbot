import speech_recognition as sr
import sys, os, pyttsx
import aiml, string, pyaudio
import nltk
import urllib
import json
from nltk.corpus import stopwords
from collections import Counter
from google import search

sessionId = 123

#including aiml files to integate them with python

bot = aiml.Kernel()
bot.learn("Greetings.aiml")
bot.learn("Customer.aiml")
bot.learn("learn.aiml")

#Setting up text to speech setup
engine = pyttsx.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id) 
engine.say('Hello! How can I help you?')
engine.runAndWait()

#function for machine learning
def readAiml():
   file=open("Greetings.aiml","r")
   lines = file.readlines()
   file.close()
   file=open("Greetings.aiml", "w")
   for line in lines:
      if line!="</aiml>":         
         file.write(line)
   file.close()

   file=open("Greetings.aiml","a")
   file.write("<category> \n\n<pattern>"+Upper+" </pattern> \n\n<template>" +Answer+"</template> \n\n</category> \n\n</aiml>")
   file.close()
   upper = tokens(Upper)

   for word in upper:
      if len(word)>3:
         upper1= [ word for word in upper if len(word) >= 3 ]
         for part in upper1:
            DictWrite(part)
      
#Function to store question for later learning and deducing meanings   
def write(  ):

   file=open("Smalldata.txt","a")
   file.write(messages+"\n")
   file.close()
   return

#Function to retrieve store question for later learning and deducing meanings
def read():

   file=open("Smalldata.txt","r")
   check=file.read()
   file.close()
   return check

#funcion to tokenize any string into parts
def tokens( str ):

   words=nltk.word_tokenize(str)
   return words

#function to convert speech to text 
def SpeechToText():
        r = sr.Recognizer()   #Speech recognition
        with sr.Microphone() as source:
            print("Say something!")
            audio = r.listen(source)
            message = r.recognize_google(audio)
            print("Check: "+message)
        try:
            print("User: " + r.recognize_google(audio))
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
        return message

#function to find importance of words to use them to deduce that which thing is being asked more
def Importance():
   filtered_words = [word for word in words if word not in stopwords.words('english')]
   wordfreq = []
   for w in filtered_words:
       wordfreq.append(filtered_words.count(w))
   Frequency= str(zip(filtered_words, wordfreq))
   Free=list(set([Frequency]))
   count = Counter(filtered_words)
   return count

#function to search google if user want to get links from google 
def SearchGoogle():
      
   UrlCount=0

   for url in search(message, stop=1):
       print(url)
       UrlCount +=1
       if UrlCount == 3:
          break
#function to be used by SameCheck function to return keys for dictionary that
#we built for our bot to use keywords that are stored by last questions to get the results.         

def hash_map(str):
    related_keys = []
    for tok_word in str:
        if dict.has_key(tok_word):
            related_keys.append(dict[tok_word])
    #print related_keys
    return related_keys

#function to check keywords in dictionary and fetch result from aiml
def SameCheck(int):
   count=0
   keyresponse1 = "Random"
   key = hash_map(filtered_words)
   print(key)
   for keyword1 in key:
     keywords=tokens(keyword1)
     for keyword in keywords:
        if len(keyword)>2:
           for index in range(0,int):          
              if keyword == Dict_search[index]:
                 keyresponse1 = keyword1
                 break
        else:
           keyresponse1 = "Random"
            
   text = bot.respond(keyresponse1)
   if keyresponse1 != "Random":
       
       print "Bot: " + text
       engine.say(text)
       engine.runAndWait()
      
   return text

#function to write the dictionary  key words into file for later use 
def DictWrite(str):
   file = open("Keywords.txt","a")
   file.write(Upper+"\n")
   file.close()

   file = open("Keyword_part.txt","a")
   file.write(str+"\n")
   file.close()

#function to read keywords from files and putting them to dictionary with information

def DictRead():
   file = open("Keywords.txt","r")
   dictionary = file.readlines()
   dictionary = [line.rstrip('\n') for line in open('Keywords.txt')]                                                                                                                   
   file.close()
   
   file = open("Keyword_part.txt","r")
   dictionary1 = file.readlines()
   dictionary1 = [line.rstrip('\n') for line in open('Keyword_part.txt')]
   file.close()

   mydict = {}                                                            
   for i,j in zip(dictionary1,dictionary):                                           
      mydict[i] = j                                                      
   return mydict

 #loop to run the program continuosly till user says to finish 
while True:
        message = SpeechToText()   #getting speech input
        message= message.upper()
        dict = DictRead()
        #print(dict)
        #message = raw_input("User: ")
        
        if message == "quit":
                exit()
        elif message =="I'M DONE":   
                break        
        else:
                #setting sessional ID
                bot.setPredicate("balance", "76 Rupees", sessionId)
                clients_balance= bot.getPredicate("balance", sessionId)
                bot.setPredicate("Current", "Monthly", sessionId)
                clients_balance= bot.getPredicate("current", sessionId)
                
                #Bot response
                text = bot.respond(message, sessionId)
                print("BOT: " + text)
                engine.say(text)
                engine.runAndWait()

                #tokenizing question for using it for dictionary 
                Dict_search=tokens(message)

                #writing questions to file and filtering out useless words                
                messages=str(message)
                messages=messages.translate(None, string.punctuation)
                write()
                check=read()                
                words=tokens(check)
                filtered_words = [word for word in words if word not in stopwords.words('english')]
                filtered_words = set(filtered_words)
                #print(filtered_words)

               #checking dictionary for keywords
                if text == "Let me learn this.":
                   i = len(Dict_search)
                   text = SameCheck(i)                 

                #writing into Aiml script
                if text == "Let me learn this.":
                  print("Say Human to talk to human and Search to search internet?")
                  engine.say("Say Human to talk to human and Search to search internet?")
                  engine.runAndWait()
                  option=SpeechToText()
                  option=option.upper()
                  #option=raw_input()
                  if option == "HUMAN":
                     print("Human:")
                     #Answer = raw_input()
                     Answer = SpeechToText()
                     Upper = message.upper()
                     readAiml()
                  elif option == "SEARCH":
                     print("searching.....")
                     SearchGoogle()
                     
                print("Do you want to know imortance?")
                engine.say("Do you want to know imortance?")
                engine.runAndWait()
                checkk=SpeechToText()
                checkk==checkk.upper()
                if("YES"):
                   Word_count = Importance()
                   print("Important words are: ")
                   print(Word_count)
                                                               

