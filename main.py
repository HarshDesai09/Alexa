import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import requests, json, sys

listener = sr.Recognizer()

engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty('voice', voices[1].id)


def engine_talk(text):
    engine.say(text)
    engine.runAndWait()


def weather(city):

    api_key = "<YOUR API KEY"

    # base_url variable to store url
    base_url = "http://api.openweathermap.org/data/2.5/weather?"

    city_name = city

    complete_url = base_url + "appid=" + api_key + "&q=" + city_name

    response = requests.get(complete_url)

    x = response.json()

    if x["cod"] != "404":

        y = x["main"]

        current_temperature = y["temp"]

        return str(current_temperature)


def user_commands():
    try:
        with sr.Microphone() as source:
            print("Start Speaking!!")
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            if 'alexa' in command:
                command = command.replace('alexa', '')
                print(command)
    except:
        pass
    return command


def run_alexa():
    command = user_commands()
    if 'play' in command:
        song = command.replace('play', '')
        # print('New Command is' +command)
        # print('The bot is telling us: Playing' +command)
        engine_talk('Playing' + song)
        pywhatkit.playonyt(song)
    elif 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        engine_talk('The current time is' + time)
    elif 'who is' in command:
        name = command.replace('who is', '')
        info = wikipedia.summary(name, 1)
        print(info)
        engine_talk(info)
    elif 'joke' in command:
        engine_talk(pyjokes.get_joke())
    elif 'weather' in command:
        engine_talk('Please tell the name of the city')
        city = user_commands()
        # weather_api = weather('Hong Kong')
        weather_api = weather(city)
        engine_talk(weather_api + 'degree fahreneit')
    elif 'stop' in command:
        sys.exit()
    else:
        engine_talk('I could not hear you properly')


while True:
    run_alexa()




