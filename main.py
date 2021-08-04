from typing import Text
from vosk import Model, KaldiRecognizer
import os
import pyaudio
import pyttsx3
import json
import core

# Síntese de voz
engine = pyttsx3.init()

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[-3].id)


def speak(text):
    engine.say(text)
    engine.runAndWait()


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

            print(text)
# Horas:
            if text == 'que horas são' or text == 'me diga as horas':
                speak(core.SystemInfo.get_time())

# Dando bom dia, boa tarde ou boa noite!
            if text == 'bom dia':
                speak('Bom dia!')

            if text == 'boa tarde':
                speak('Boa tarde!')

            if text == 'boa noite':
                speak('Boa noite!')
