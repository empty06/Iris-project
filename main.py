from typing import Text
from vosk import Model, KaldiRecognizer
import os
import pyaudio
import pyttsx3
import json
import core
from nlu.classifier import classify
import webbrowser as wb

# Síntese de voz
engine = pyttsx3.init()

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[-3].id)


def speak(text):
    engine.say(text)
    engine.runAndWait()


def evaluate(text):
    # Reconhecer entidade do texto.
    entity = classify(text)
    if entity == 'time|getTime':
        speak(core.SystemInfo.get_time())
    elif entity == 'time|getDate':
        speak(core.SystemInfo.get_date())

    # Abrir programas
    elif entity == 'open|google':
        speak('Abrindo o Google')
        wb.open_new_tab('http://www.google.com')
    elif entity == 'open|youtube':
        speak('Abrindo o Youtube')
        wb.open_new_tab('"https://www.youtube.com/"')

    print('Text: {}  Entity: {}'.format(text, entity))


# Reconhecimento de fala
model = Model('model')
rec = KaldiRecognizer(model, 16000)

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1,
                rate=16000, input=True, frames_per_buffer=2048)
stream.start_stream()

# loop do reconhecimento de fala
while True:
    data = stream.read(2048)
    if len(data) == 0:
        break
    if rec.AcceptWaveform(data):
        result = rec.Result()
        result = json.loads(result)

        if result is not None:
            text = result['text']
            evaluate(text)
