import pyttsx3
import logging
from datetime import datetime
import speech_recognition as sr



def configurar_voz():
    engine = pyttsx3.init()
    for v in engine.getProperty('voices'):
        if "portuguese" in v.name.lower() or "brazil" in v.name.lower():
            engine.setProperty('voice', v.id)
            break
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 1)
    return engine

voz_engine = configurar_voz()

def falar(texto):
    try:
        logging.info(f"Zain: {texto}")
        voz_engine.say(texto)
        voz_engine.runAndWait()
    except Exception as e:
        logging.error(f"Erro ao falar: {e}")
    print(f"Zain: {texto}")

def reconhecer_fala():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        print("Zain: Estou ouvindo...")
        audio = r.listen(source)
    try:
        texto = r.recognize_google(audio, language='pt-BR')
        print(f"Você: {texto}")
        return texto.lower()
    except sr.UnknownValueError:
        falar("Desculpe, não consegui entender o que você disse.")
    except sr.RequestError as e:
        falar(f"Erro ao reconhecer a fala: {e}")
        logging.error(f"Erro ao reconhecer a fala: {e}")
        return None

def validar_data_hora(data_hora):
    try:
        datetime.strptime(data_hora, "%d/%m/%Y %H:%M")
        return True
    except ValueError:
        return False
    


