# EQFast for Discord

(AIで生成されたREADMEファイルです。不備があればissueにお願いします。)

緊急地震速報（EEW）と地震速報をリアルタイムでDiscordに配信するボットです。

## 機能

- **緊急地震速報（EEW）の配信** - 地震発生時の速報情報をリアルタイムで通知
- **地震速報の配信** - 震度速報や確定震度情報を配信
- **Webhookによる送信** - Discordのウェブフックを使用した動的なメッセージ送信
- **非同期処理** - asyncioを使用した効率的なリアルタイム処理

## システム構成

```
src/eew_bot/
├── bot.py              - ボットのメインエントリーポイント
├── config.py           - 環境変数の読み込みと設定
├── models/             - データモデル
│   ├── eew.py         - 緊急地震速報データモデル
│   └── quake.py       - 地震速報データモデル
├── parsers/            - データパーサー
│   ├── eew_parser.py  - EEWデータのパース
│   └── p2p_parser.py  - 地震速報データのパース
├── services/           - 外部APIとの連携
│   ├── eew_api.py     - EEW APIとの接続
│   └── quake_api.py   - 地震速報APIとの接続
├── utils/              - ユーティリティ関数
│   ├── discord_formatter.py       - Embed形式でのメッセージ作成
│   ├── discord_raw_formatter.py   - テキスト形式でのメッセージ作成
│   ├── discord_webhook.py         - Embed送信用Webhook処理
│   ├── discord_raw_webhook.py     - テキスト送信用Webhook処理
│   ├── logger.py      - ログ設定
│   └── retry.py       - リトライロジック
└── state/              - 状態管理
    └── last_event.py  - 最新イベント情報の管理
```

## 必要な環境

- Python 3.8以上
- pip または Poetry

## インストール

```bash
# リポジトリのクローン
git clone https://github.com/ScProject-Lab/EQFast-for-discord.git
cd EQFast-for-discord

# 依存パッケージのインストール
pip install -e .
```

## セットアップ

### 環境変数の設定

プロジェクトルートに `.env` ファイルを作成し、以下の環境変数を設定してください：

```env
DISCORD_TOKEN=your_discord_token_here
RAW_DATA_WH=your_raw_data_webhook_url
EEW_API_URL=your_eew_api_url
QUAKE_API_URL=your_quake_api_url
```

### 各環境変数の説明

- **DISCORD_TOKEN** - Discordボットのトークン
- **RAW_DATA_WH** - 生データ送信用のDiscord Webhook URL
- **EEW_API_URL** - 緊急地震速報APIのエンドポイント
- **QUAKE_API_URL** - 地震速報APIのエンドポイント

## 使用方法

### ボットの起動

```bash
# eqfastコマンドで直接起動
eqfast

# または
python -m eew_bot
```

### Windowsでの起動

```bash
# bot_start.batで起動
./bot_start.bat
```

### Linuxでのサービス化

```bash
# サービスの再起動
sudo systemctl restart eqfast.service
```

## 依存ライブラリ

- **websockets** - WebSocketクライアント通信
- **python-dotenv** - 環境変数の読み込み
- **aiohttp** - 非同期HTTPクライアント

## プロジェクト構成情報

- **プロジェクト名**: eqfast
- **バージョン**: 0.1.0
- **メインモジュール**: eew_bot

## ログ

ボットの実行ログは `logs/` ディレクトリに記録されます。また、 `bot_log.txt` に日次ログも出力されます。

## ライセンス

[LICENSE](LICENSE) ファイルを参照してください。

## 開発

### テストの実行

```bash
python -m pytest scripts/test_discord.py
```

### WebSocketテストサーバー

```bash
python src/eew_bot/tests/ws_test_server.py
```

## トラブルシューティング

- ボットが起動しない場合は、環境変数が正しく設定されているか確認してください。
- WebSocketの接続エラーが発生した場合は、API URLが正しいか確認してください。
- Discordへのメッセージ送信が失敗する場合は、Webhook URLとボットの権限を確認してください。

## 問い合わせ

問題や機能リクエストは、GitHubのIssueセクションで受け付けています。
