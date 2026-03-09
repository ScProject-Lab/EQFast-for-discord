# EQFast for Discord

Discordに各種地震情報を送信できるプロジェクトです。

- 緊急地震速報
- 地震情報

が受信できます。

## 動作環境

### OS

- Windows11/10
- Linux
- MacOS

### 環境

- Python 3.14.2(でのみ動作確認済み)

- pip

## 実行方法

### 依存関係のインストール

```Bash
pip install -e .
```

### 実行

```Bash
python -m eew_bot

# Windowsの場合はこっちもok
./bot_start.bat
```

## 導入方法

サーバーのチャンネルから「チャンネルの編集」を選び、「連携サービス」を選択します。  
ウェブフックを押して、「新しいウェブフック」を埋め込み用とプレーンテキスト用に2つ作成してください。名前とチャンネルを任意のものに設定し、それぞれのウェブフックURLをコピーしてください。

プロジェクトのルートに`.env`を作成し、

```text
EMBED_WH = "埋め込み用URL"
RAW_WH = "プレーンテキスト用URL"
EEW_API_URL = "wss://ws-api.wolfx.jp/jma_eew"
QUAKE_API_URL = "wss://api.p2pquake.net/v2/ws"
```

を入力してください。(APIのURLを.envにする必要はなかったかも)  

## 構成とか

言語 : `Python`

ファイル構造

```text
EQFast-for-Discord
│  .env
│  .gitignore
│  bot_log.txt
│  bot_start.bat
│  LICENSE
│  pyproject.toml
│  README.md
│  update_bot.bat
│
├─.vscode
│      settings.json
│      tasks.json
│
├─scripts
│      test_discord.py
│      __init__.py
│
└─src
    ├─eew_bot
    │  │  bot.py
    │  │  config.py
    │  │  __main__.py
    │  │
    │  ├─models
    │  │      eew.py
    │  │      quake.py
    │  │
    │  ├─parsers
    │  │      eew_parser.py
    │  │      p2p_parser.py
    │  │
    │  ├─services
    │  │      eew_api.py
    │  │      quake_api.py
    │  │
    │  ├─state
    │  │      last_event.py
    │  │
    │  ├─tests
    │  │      ws_test_server.py
    │  │
    │  └─utils
    │          formatter.py
    │          logger.py
    │          retry.py
    │          webhook.py
    │
    └─logs
```

## ライセンス

[LICENSE](LICENSE)を参照してください  

## 問い合わせ

Issueで受け付けています。
