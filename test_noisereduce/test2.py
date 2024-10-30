import pyaudio
import noisereduce as nr
import numpy as np
from vosk import Model, KaldiRecognizer

# Параметри аудіо
RATE = 16000
BUFFER = 4096

# Завантаження моделі Vosk
model = Model(r'C:\project\vosk-model-small-uk-v3-small')
recognizer = KaldiRecognizer(model, RATE)

# Ініціалізація PyAudio
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True, frames_per_buffer=BUFFER)

def process_audio(data):
    # Перетворення даних у масив NumPy
    audio_data = np.frombuffer(data, dtype=np.int16)
    # Зменшення шуму
    reduced_noise = nr.reduce_noise(y=audio_data, sr=RATE)
    # Підсилення звуку (наприклад, множення на 1.5)
    amplified_data = np.clip(reduced_noise * 1.5, -32768, 32767)  # Зберігаємо в межах int16
    return amplified_data.astype(np.int16).tobytes()

stream.start_stream()

print("Слухаю команди...")

try:
    while True:
        data = stream.read(BUFFER)
        # Попередня обробка аудіо (зменшення шуму і підсилення)
        processed_data = process_audio(data)

        # Передача обробленого аудіо в розпізнавач
        if recognizer.AcceptWaveform(processed_data):
            print(recognizer.Result())
        
except KeyboardInterrupt:
    print("Розпізнавання зупинено.")
finally:
    stream.stop_stream()
    stream.close()
    p.terminate()
