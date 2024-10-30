import pyaudio
import noisereduce as nr
import numpy as np
import soundfile as sf

# Параметри аудіо
RATE = 16000  # Частота дискретизації
BUFFER = 1024  # Розмір буфера
DURATION = 5  # Тривалість запису в секундах

# Ініціалізація PyAudio для запису аудіо
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True, frames_per_buffer=BUFFER)

print("Запис почався...")

# Запис аудіо
frames = []
for _ in range(int(RATE / BUFFER * DURATION)):
    data = stream.read(BUFFER)
    frames.append(data)

print("Запис завершено.")

# Зупинка і закриття потоку
stream.stop_stream()
stream.close()
p.terminate()

# Об'єднання фреймів в один масив
audio_data = np.frombuffer(b''.join(frames), dtype=np.int16)

# Збереження оригінального запису
sf.write("original_audio.wav", audio_data, RATE)
print("Оригінальний файл збережено як 'original_audio.wav'.")

# Зменшення шуму
reduced_noise = nr.reduce_noise(y=audio_data, sr=RATE)

# Збереження обробленого аудіо
sf.write("reduced_noise_audio.wav", reduced_noise, RATE)
print("Оброблений файл збережено як 'reduced_noise_audio.wav'.")
