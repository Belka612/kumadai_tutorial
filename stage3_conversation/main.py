import numpy as np
import wave
import whisper
import io
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.recorder import record_audio

# ========================== ↓↓↓ ここから下に記述してください ↓↓↓ ==========================
def transcribe_audio(wav_bytes: bytes) -> str:
    """
    WAVバイナリ音声をWhisperで文字起こしする

    入力:
        wav_bytes (bytes): WAV形式の音声データ
    出力:
        str: 文字起こし結果（日本語）
    """
    with wave.open(io.BytesIO(wav_bytes), 'rb') as wf:
        frames = wf.readframes(wf.getnframes())
        audio_np = np.frombuffer(frames, dtype=np.int16).astype(np.float32) / 32768.0

    model = whisper.load_model("base")
    result = model.transcribe(audio_np, language="ja")
    
    return result["text"]

if __name__ == '__main__':
    wav_data = record_audio()
    text = transcribe_audio(wav_data)
    print("文字起こし結果:", text)
