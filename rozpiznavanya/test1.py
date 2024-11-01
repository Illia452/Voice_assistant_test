from vosk import Model, KaldiRecognizer
import pyaudio
import numpy as np
import noisereduce as nr

model = Model(r'C:\vosk-model-small-uk-v3-small') 
recognizer = KaldiRecognizer(model, 16000) # розпізнавач

# paInt16 - 16-бітний формат зберігання, frames_per_buffer=2048 - кількість фреймів що зчитуються за один раз

cap = pyaudio.PyAudio()
stream = cap.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=2048)
stream.start_stream()



while True:
    data = stream.read(4096)

    masiv = np.frombuffer(data, dtype=np.int16) # перетворення байтів в масив

    processed_audio_noise = nr.reduce_noise(y=masiv, sr=16000) # зняття шуму з аудіо

    
    #if len(data) == 0:  # якщо не надходить звук цикл припиняється
    #    break

    if recognizer.AcceptWaveform(data): 
        print(recognizer.Result())
#    else:
#        print(recognizer.PartialResult()) # постійне прослуховування аудіо з реальним виведенням

        
        