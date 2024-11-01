from vosk import Model, KaldiRecognizer
import pyaudio

model = Model(r'C:\vosk-model-small-uk-v3-small') 
recognizer = KaldiRecognizer(model, 16000) # розпізнавач

cap = pyaudio.PyAudio()
stream = cap.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=2048)
stream.start_stream()

while True:
    data = stream.read(4096)
    #if len(data) == 0:
    #    break

    if recognizer.AcceptWaveform(data): 
        print(recognizer.Result())
#    else:
#        print(recognizer.PartialResult())

        