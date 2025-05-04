import requests
from typing import Dict

def get_speakers() -> Dict[str, Dict[str, int]]:
    """
    VOICEVOXの話者情報を取得し、辞書型で返す

    出力:
        dict: {話者名: {スタイル名: speaker_id}}
        例) {'ずんだもん': {'ノーマル': 3, 'あまあま': 1, ...}}
    """
    resp = requests.get("http://127.0.0.1:50021/speakers")
    resp.raise_for_status()
    speakers = resp.json()

    speaker_dict = {}
    for speaker in speakers:
        name = speaker['name']
        styles = {style['name']: style['id'] for style in speaker['styles']}
        speaker_dict[name] = styles

    return speaker_dict

if __name__ == '__main__':
    speakers = get_speakers()
    for speaker in speakers:
        print(f"話者名: {speaker}")
        for style, speaker_id in speakers[speaker].items():
            print(f"  スタイル: {style}, Speaker ID: {speaker_id}")