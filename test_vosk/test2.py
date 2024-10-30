from vosk import Model

try:
    model = Model(r"C:\vosk-model-small-uk-v3-nano")
    print("Модель завантажена успішно!")
except Exception as e:
    print(f"Помилка: {e}")
