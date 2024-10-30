import pyaudio
import noisereduce as nr
import numpy as np
import soundfile as sf
from scipy.signal import butter, lfilter

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

# Зменшення шуму за допомогою noisereduce
reduced_noise = nr.reduce_noise(y=audio_data, sr=RATE)
sf.write("reduced_noise_audio.wav", reduced_noise, RATE)  # Збереження після зменшення шуму
print("Файл після зменшення шуму збережено як 'reduced_noise_audio.wav'.")

# Альтернативна нормалізація з використанням NumPy
def normalize_audio(data):
    # Знаходимо максимальне значення амплітуди в записі
    max_amplitude = np.max(np.abs(data))
    # Масштабуємо сигнал до рівня, близького до максимуму 16-бітного діапазону
    return (data / max_amplitude) * 32767

normalized_audio = normalize_audio(reduced_noise)
sf.write("normalized_audio.wav", normalized_audio.astype(np.int16), RATE)  # Збереження після нормалізації
print("Файл після нормалізації збережено як 'normalized_audio.wav'.")

# Функція для низькочастотного фільтрування з SciPy
def butter_lowpass_filter(data, cutoff, fs, order=3):  # Порядок фільтра — 3
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    y = lfilter(b, a, data)
    return y

# Застосування низькочастотного фільтра
cutoff_freq = 3000  # Гранична частота в Герцах
filtered_audio = butter_lowpass_filter(normalized_audio, cutoff=cutoff_freq, fs=RATE)
sf.write("filtered_audio.wav", filtered_audio.astype(np.int16), RATE)  # Збереження після фільтрації
print("Фільтрований файл збережено як 'filtered_audio.wav'.")

# Додаткова нормалізація після фільтрації
final_audio = normalize_audio(filtered_audio)
sf.write("filtered_normalized_audio.wav", final_audio.astype(np.int16), RATE)
print("Оброблений і нормалізований файл збережено як 'filtered_normalized_audio.wav'.")
