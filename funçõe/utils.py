import pyttsx3
import logging
import datetime



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

def validar_data_hora(data_hora):
    try:
        datetime.strptime(data_hora, "%d/%m/%Y %H:%M")
        return True
    except ValueError:
        return False
    


