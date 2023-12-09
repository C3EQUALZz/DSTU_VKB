import librosa
import soundfile as sf

# Загрузка аудиофайла
audio_file = 'input_audio.wav'
y, sr = librosa.load(audio_file)

# Замедление скорости аудио
y_slow = librosa.effects.time_stretch(y, 0.5)  # Указываем коэффициент замедления (в данном случае 0.5)

# Сохранение измененного аудиофайла
output_file = 'output_audio_slow.wav'
sf.write(output_file, y_slow, sr)