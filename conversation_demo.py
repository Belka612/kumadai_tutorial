"""
全3回の講座を踏まえた応用例です。
第1回を終えた段階でも動かせるので、ぜひ体験してみてください。
"""

import tkinter as tk
from tkinter import ttk
import sounddevice as sd
import numpy as np
import wave
import io
import whisper
import requests
import os
from dotenv import load_dotenv
import google.generativeai as genai
import pyaudio
from typing import Optional
from src.voicevox import get_speakers

# 録音設定
SAMPLE_RATE = 16000
CHANNELS = 1

# Gemini APIの初期化
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
gemini_model = genai.GenerativeModel("gemini-1.5-flash")

class VoiceChatApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.speakers = get_speakers()
        self.recording: list[np.ndarray] = []
        self.stream: Optional[sd.InputStream] = None
        self._setup_ui()
        self._update_styles()

    def _setup_ui(self) -> None:
        tk.Label(self.root, text="話者とスタイルを選んでください").pack()

        # 話者選択
        self.speaker_var = tk.StringVar()
        self.speaker_menu = ttk.Combobox(self.root, textvariable=self.speaker_var, state="readonly")
        self.speaker_menu["values"] = list(self.speakers.keys())
        self.speaker_menu.current(0)
        self.speaker_menu.pack()
        self.speaker_menu.bind("<<ComboboxSelected>>", self._update_styles)

        # スタイル選択
        self.style_var = tk.StringVar()
        self.style_menu = ttk.Combobox(self.root, textvariable=self.style_var, state="readonly")
        self.style_menu.pack()

        # 録音ボタン
        self.record_btn = tk.Button(self.root, text="録音ボタン", width=30)
        self.record_btn.pack(pady=10)
        self.record_btn.bind("<ButtonPress-1>", self._start_recording)
        self.record_btn.bind("<ButtonRelease-1>", self._stop_recording)

        # ステータスと出力欄
        self.status_label = tk.Label(self.root, text="会話内容")
        self.status_label.pack()
        self.textbox = tk.Text(self.root, height=10, width=60)
        self.textbox.pack()

    def _update_styles(self, event=None) -> None:
        speaker = self.speaker_var.get()
        styles = self.speakers[speaker]
        self.style_menu["values"] = list(styles.keys())
        self.style_menu.current(0)

    def _get_speaker_id(self) -> int:
        speaker = self.speaker_var.get()
        style = self.style_var.get()
        return self.speakers[speaker][style]

    def _start_recording(self, event=None) -> None:
        self.recording = []
        self.stream = sd.InputStream(
            samplerate=SAMPLE_RATE, channels=CHANNELS, dtype='int16', callback=self._audio_callback
        )
        self.stream.start()
        self.status_label.config(text="録音中...")

    def _stop_recording(self, event=None) -> None:
        if self.stream:
            self.stream.stop()
            self.stream.close()
        self.status_label.config(text="文字起こし中...")
        self.root.after(100, self._handle_conversation)

    def _audio_callback(self, indata, frames, time, status) -> None:
        self.recording.append(indata.copy())

    def _handle_conversation(self) -> None:
        audio_np = np.concatenate(self.recording)
        wav_bytes = self._convert_to_wav(audio_np)

        transcription = self._transcribe(wav_bytes)
        self.textbox.delete("1.0", tk.END)
        self.textbox.insert(tk.END, f"あなた: {transcription}\n")

        self.status_label.config(text="Gemini応答中...")
        response = self._get_gemini_response(transcription)
        self.textbox.insert(tk.END, f"Gemini: {response}\n")

        self.status_label.config(text="VOICEVOXで読み上げ中...")
        self._speak(response, self._get_speaker_id())

        self.status_label.config(text="完了。再録音可能です。")

    def _convert_to_wav(self, audio_np: np.ndarray) -> bytes:
        with io.BytesIO() as buf:
            with wave.open(buf, 'wb') as wf:
                wf.setnchannels(CHANNELS)
                wf.setsampwidth(2)
                wf.setframerate(SAMPLE_RATE)
                wf.writeframes(audio_np.tobytes())
            return buf.getvalue()

    def _transcribe(self, wav_bytes: bytes) -> str:
        with wave.open(io.BytesIO(wav_bytes), 'rb') as wf:
            frames = wf.readframes(wf.getnframes())
            audio_np = np.frombuffer(frames, dtype=np.int16).astype(np.float32) / 32768.0

        model = whisper.load_model("base")
        result = model.transcribe(audio_np, language="ja")
        return result["text"]

    def _get_gemini_response(self, text: str) -> str:
        prompt = f"{text}\n簡潔に答えてください。"
        response = gemini_model.generate_content(prompt)
        return response.text.strip()

    def _speak(self, text: str, speaker_id: int) -> None:
        query = requests.post("http://127.0.0.1:50021/audio_query", params={"text": text, "speaker": speaker_id})
        query.raise_for_status()
        synth = requests.post(
            "http://127.0.0.1:50021/synthesis",
            params={"speaker": speaker_id},
            headers={"Content-Type": "application/json"},
            data=query.text
        )
        synth.raise_for_status()
        self._play_audio(synth.content)

    def _play_audio(self, wav_bytes: bytes) -> None:
        with wave.open(io.BytesIO(wav_bytes), 'rb') as wf:
            audio_interface = pyaudio.PyAudio()
            stream = audio_interface.open(
                format=audio_interface.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True
            )
            data = wf.readframes(1024)
            while data:
                stream.write(data)
                data = wf.readframes(1024)
            stream.stop_stream()
            stream.close()
            audio_interface.terminate()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("簡易会話アプリ DEMO")
    app = VoiceChatApp(root)
    root.mainloop()
