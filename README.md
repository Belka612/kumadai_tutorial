# 熊大チュートリアル：Gemini × VOICEVOX 音声対話アプリ  

このリポジトリは、熊本大学情報融合学環の1年生を対象に、Pythonを用いてどのようなことができるのかを体験的に学ぶためのチュートリアル教材です。  
大規模言語モデル（Gemini API）や音声合成（VOICEVOX）といった技術に軽く触れながら、それらを組み合わせた簡単な音声対話の流れを体験できる内容になっています。  

※この教材は、筆者個人の自主的な活動に基づくものであり、熊本大学の公式な教材・活動とは関係ありません。  

---

## 初期設定  

1. 仮想環境の作成・有効化（例：Anaconda）  

```bash
conda create -n gemini_env python=3.10
conda activate gemini_env
```

2. `.env` ファイルをプロジェクトルートに作成し、以下のように記述してください：  
```bash
GOOGLE_API_KEY=YOUR_API_KEY
```

3. ライブラリをインストール  
```bash
pip install -r requirements.txt
```

---  

## チュートリアル概要（全3回）  

### 第1回：Gemini API を使ってみよう  
- Gemini APIの基本的な使い方  
- テキスト入力 → 応答生成  
- `.env` でAPIキーを安全に管理  

### 第2回：VOICEVOXでしゃべらせよう  
- VOICEVOXローカルエンジンのREST API利用  
- テキスト → 音声合成 → WAV再生  

### 第3回：音声で会話しよう  
- 録音 → Whisperで文字起こし  
- Geminiに送って応答取得  
- VOICEVOXで音声化して応答  

---  

## 📁 フォルダ構成  

kumadai_tutorial/  
├─ .env # APIキーなどの環境変数（ユーザーが作成）  
├─ requirements.txt # 使用ライブラリとバージョン指定  
├─ README.md # このファイル  
├─ config/  
│└─ settings.py # .env読み込み・APIキー管理  
├─ stage1_gemini_api/  
│└─ main.py # Gemini API 単体利用  
├─ stage2_voicevox/  
│└─ main.py # VOICEVOX 単体利用  
├─ stage3_conversation/  
│└─ main.py # 録音 → 文字起こし → Gemini → VOICEVOX 応答  
├─ conversation_demo.py # 応用例
--- 

## 詳細な手順・解説
チュートリアルの詳しい進め方や補足情報は、以下の Notion にまとめています。    
必要に応じてこちらも参照してください：  
[Notion解説ページ](https://www.notion.so/1e66ffd29278804c9a86f34bb5b08c41?pvs=4)  

### 注意
VOICEVOXエンジンはローカルで起動しておく必要があります。  
Gemini APIキーは無料枠でも動作可能ですが、使用量に注意してください。  

### 補足
ご自身の用途に合わせて話者やモデルの設定を変更することも可能です。  