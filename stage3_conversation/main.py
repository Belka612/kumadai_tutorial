import numpy as np
import wave
import whisper
import io
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.recorder import record_audio

# ========================== ↓↓↓ ここから下に記述してください ↓↓↓ ==========================