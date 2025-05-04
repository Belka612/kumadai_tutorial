import sounddevice as sd
import numpy as np
import wave
import io

SAMPLE_RATE = 16000
DURATION = 5

def record_audio(duration: int=5, fs: int=SAMPLE_RATE) -> bytes:
    """
    指定時間だけ録音し、WAVバイナリとして返す

    入力:
        duration (int): 録音時間（秒）
    出力:
        bytes: 録音された音声データ（WAV形式）
    """
    print(f"{duration}秒間録音開始...")
    recording = sd.rec(int(duration*fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()
    print("録音完了")

    with io.BytesIO() as buf:
        with wave.open(buf, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(fs)
            wf.writeframes(recording.tobytes())
        return buf.getvalue()
