#!/usr/bin/env python
# -*- coding: utf-8 -*-
import speech_recognition as sr
from os import path
import pyttsx3
from datetime import datetime
import wikipedia
import language_check
import nltk
import random
import string
from textblob import TextBlob
from nltk.chat.util import Chat, reflections
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from PyNews import Business_news

def file_availibilty(file):
    if path.exists(file):
        print(" Audio .wav file exist at location: " + file)
        file_availibilty_flag = True
        return file_availibilty_flag
    else:
        file_availibilty_flag = False
        return file_availibilty_flag

def transcribe_audio_file(file):
    # transcribe audio file
    # use the audio file as the audio source
    #print('Speech recognisation for file : ', file)
    audio_file_wav = sr.AudioFile(file)
    with audio_file_wav as source:
        r.dynamic_energy_threshold = True
        r.adjust_for_ambient_noise(source,duration=0.5)
        audio = r.record(source)  # read the entire audio file
        print("Transcription : " + str(r.recognize_google(audio)))#,show_all=True)))
    try:
        audio_file_text = r.recognize_google(audio)  # ,show_all=True)
        system_speech_msg(audio_file_text)
        return audio_file_text
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

def SpeechToText():
    print("Say something!")
    #word = "Hey I am Listening , please say something!"
    #system_speech_msg(word)
    with mic as source:
        r.dynamic_energy_threshold = True
        r.adjust_for_ambient_noise(source)#,duration=0.5)
        audio = r.listen(source)#,timeout=20,phrase_time_limit=15)
        message = r.recognize_google(audio)
    try:
        print("User: " + r.recognize_google(audio))
    except sr.WaitTimeoutError as e:
        print("Timeout; {0}".format(e))
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
    return message

def system_speech_msg(input_context):
    engine = pyttsx3.init()
    engine.say(input_context)
    engine.setProperty('rate', 25)
    engine.setProperty('volume', 0.9)
    engine.runAndWait()

def gratiude_wish():
    if now_UTC_hr >= 4 and now_UTC_hr < 12:
        print("It's time to say, Good Morning")
        gratiude = 'Good Morning'
        system_speech_msg(gratiude)
    elif now_UTC_hr >= 12 and now_UTC_hr < 17:
        print("It's time to say, Good Afternoon")
        gratiude = 'Good Afternoon'
        system_speech_msg(gratiude)
    elif now_UTC_hr >= 17 and now_UTC_hr <= 21:
        print("It's time to say, Good Evening")
        gratiude = 'Good Evening'
        system_speech_msg(gratiude)
    elif now_UTC_hr > 21:
        print("It's time to sleep, Good Night")
        gratiude = 'Good Night'
        system_speech_msg(gratiude)

# WordNet is a semantically-oriented dictionary of English included in NLTK.
def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]

def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

def greeting(sentence):
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)

def news(sentence):
    for word in sentence.split():
        if word.lower() in news_INPUTS:
            yield random.choice(news_RESPONSES)


def response(user_response):
    robo_response=''
    sent_tokens.append(user_response)
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
    tfidf = TfidfVec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx=vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    if(req_tfidf==0):
        robo_response=robo_response + " I am sorry! I don't understand you"
        return robo_response
    else:
        robo_response = robo_response+sent_tokens[idx]
        return robo_response

if __name__ == "__main__":
    r = sr.Recognizer()
    mic = sr.Microphone()
    language = 'en'
    now_UTC_hr = datetime.utcnow().hour  # Get the UTC time
    AUDIO_FILE = "C:/Users/khushal/Documents/Python Scripts/male.wav"
    AUDIO_FILE_WITHOUT_NOISE = "C:/Users/khushal/Documents/Python Scripts/h_orig.wav"
    AUDIO_FILE_WITH_NOISE = "C:/Users/khushal/Documents/Python Scripts/h_noise.wav"
    file_availibilty_flag = file_availibilty(AUDIO_FILE)
    if file_availibilty_flag:
        audio_file_to_text = transcribe_audio_file(AUDIO_FILE_WITHOUT_NOISE)
        print(audio_file_to_text)
    else:
        word = "Audio file isn't present at local server"
        system_speech_msg(word)
    list_of_mic = sr.Microphone.list_microphone_names()
    print(list_of_mic)

    tool = language_check.LanguageTool('en-US')
    #text = u'A sentence with a error in the Hitchhiker’s Guide tot he Galaxy'

    Chatbot_wiki = wikipedia.page("Chatbot")
    raw = Chatbot_wiki.content.lower()

    sent_tokens = nltk.sent_tokenize(raw)  # converts to list of sentences
    #print(sent_tokens[:2])
    word_tokens = nltk.word_tokenize(raw)  # converts to list of words
    #print(word_tokens[:5])
    lemmer = nltk.stem.WordNetLemmatizer()
    remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
    GREETING_INPUTS = ("hello", "hi", "greetings", "sup", "what's up", "hey")
    news_INPUTS = ("news","headlines","cricket news","sports news","Business news")
    news_RESPONSES = ("Today's news are","Today's headlines are")
    GREETING_RESPONSES = ["hi", "hey", "*nods*", "hi there", "hello", "I am glad! You are talking to me"]
    gratiude_wish()
    flag = True
    while (flag == True):
        user_response = input()
        #user_response = SpeechToText()
        matches = tool.check(user_response)
        user_response = language_check.correct(user_response, matches)
        print(user_response)
        user_response = user_response.lower()
        if (user_response != 'bye'):
            if (user_response == 'thanks' or user_response == 'thank you'):
                flag = False
                print("\n ROBO: You are welcome..")
                word = "You are welcome."
                system_speech_msg(word)
            else:
                if (greeting(user_response) != None):
                    print("\n ROBO: " + greeting(user_response))
                    word = greeting(user_response)
                    system_speech_msg(word)

                elif (news(user_response) != None):
                    word = "Please wait,Let me collect today's headlines "
                    system_speech_msg(word)
                    word = news(user_response)
                    system_speech_msg(word)
                    business_headlines_list, india_Business_news_list, international_Business_news_list = Business_news('business')
                    system_speech_msg(business_headlines_list)

                else:
                    print("\n ROBO: ", end="")
                    print(response(user_response))
                    sent_tokens.remove(user_response)
                    word = response(user_response)
                    system_speech_msg(word)

        elif (user_response == 'bye'):
            flag = False
            print("\n  ROBO: Bye! take care..")
            word = "Bye! take care.."
            system_speech_msg(word)
            if now_UTC_hr > 21:
                print("It's time to sleep, Good Night")
                gratiude = 'Good Night'
                system_speech_msg(gratiude)



##############################################
