import pyaudio
import requests
import json
from typing import Optional

# ========================== ↓↓↓ ここから下に記述してください ↓↓↓ ==========================
def play_audio(voice: bytes) -> None:
    """
    音声バイナリをPyAudioで再生する。

    出力:
        voice (bytes): 再生するWAV形式の音声バイナリ
    """
    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16, channels=1, rate=24000, output=True)
    stream.write(voice)
    stream.stop_stream()
    stream.close()
    audio.terminate()

def VoiceVox(text: str, speaker_id: int=1) -> Optional[bytes]:
    """
    VOICEVOXで音声合成をしてWAVバイナリを返す。

    入力:
        text (str): 話させる内容
        speaker_id (int): VOICEVOX話者ID (デフォルト: 1)
    出力:
        synthesis.content (bytes): 合成音声のバイナリ 
    """
    params = {'text': text, 'speaker': speaker_id}
    query = requests.post('http://127.0.0.1:50021/audio_query', params=params)
    synthesis = requests.post(f'http://127.0.0.1:50021/synthesis', headers = {"Content-Type": "application/json"}, params=params, data = json.dumps(query.json()))
    return synthesis.content

if __name__ == '__main__':
    text = "こんにちは。僕はずんだもんなのだ。"
    voice = VoiceVox(text=text, speaker_id=1)
    play_audio(voice)