# Python Program (Speech to text and text to speech)
# Indepedndies
import speech_recognition as sr
import pyttsx3

import os
from dotenv import load_dotenv
load_dotenv()
OPENAI_KEY = os.getenv('OPENAI_KEY')

# allow us to talk to chatgpt using python
import openai
openai.api_key = OPENAI_KEY

#Function to convert text to speech
def SpeakText(command):
    
    #Initialize the engine
    engine = pyttsx3.init()
    # Give it the text we want it to say
    engine.say(command)
    #run the above command and say the text
    engine.runAndWait()

#installiing the recognizer
r = sr.Recognizer()

def record_text():
# loop in case of errors    
    while(1):
        try:
            # use the microphone as source of input
            with sr.Microphone() as source2:

                # prepare recognizer to receive input
                r.adjust_for_ambient_noise(source2, duration=0.2)

                print("I'm listening")

                #listen for the user's input
                audio2 = r.listen(source2)


                # Using google to recognize audio
                MyText =r.recognize_google(audio2)

                return MyText
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))

        except sr.UnknownValueError:
            print("unkown error occured")


def send_to_chatGPT(messages, model="gpt-3.5-turbo"):

    response = openai.ChatCompletion.create(

        # specify chat gpt model
        model = model,

        #the messages array (the full context of the conversation)
        messages = messages,
        
        # How long we want the messages to be (response from gpt) in characters
        max_tokens = 100,

        #Deafualts
        n=1,
        stop=None,
        temprature=0.5,
    )

    #getting the generated text by chatgpt and store it in message
    message = response.choices[0].message.content
    messages.append(response.choices[0].message) #update the messages array
    return message


messages = []
while(1): #infinite loop

    #This funcion convert the microphon audio and return the a text version from this audio in a form of string
    text = record_text()

    #append the text recieved to the as a dictionary, to keep track of the whole conversation when talk again and respond accordingly
    # "role" is to identifiy who said that text
    messages.append({"role": "user", "content": text})
    
    #send message to chatGPT, and recive the response from chatgpt and convert it to audio
    response = send_to_chatGPT(messages)
    SpeakText(response) #speak the text back to user
    print(response)



