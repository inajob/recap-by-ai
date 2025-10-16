import requests
import json
import sys
import time
import os
from dotenv import load_dotenv

# .envファイルから環境変数を読み込む
load_dotenv()

# 環境変数からWebhook URLを取得
webhook_url = os.getenv("DISCORD_WEBHOOK_URL")

# Webhook URLが設定されているか確認
if not webhook_url:
    print("エラー: .envファイルにDISCORD_WEBHOOK_URLが見つかりません。")
    print("DISCORD_WEBHOOK_URL='your_webhook_url' の形式で.envファイルを作成してください。")
    sys.exit(1)

def send(lines):
    """Discordにメッセージのリストを1つ送信します。"""
    payload = {
        'content': "\n".join(lines)
    }

    if not payload['content'].strip():
        print("コンテンツが空です。送信しません。")
        return

    print("--- Discordに送信中 ---")
    print(f"（{len(payload['content'])}文字送信中）")
    print("--------------------------")
    
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.post(webhook_url, data=json.dumps(payload), headers=headers)
        response.raise_for_status()  # 4xxまたは5xxのステータスコードで例外を発生させる
        print("Discordへの送信に成功しました。")
    except requests.exceptions.RequestException as e:
        print(f"Discordへの送信中にエラーが発生しました: {e}")

def main():
    """メイン関数：ファイルを読み込み、その内容を送信します。"""
    if len(sys.argv) < 2:
        print("使い方: python post-discord.py <ファイル名>")
        sys.exit(1)

    filename = sys.argv[1]
    content = ""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"エラー: ファイルが見つかりません {filename}")
        sys.exit(1)
    except Exception as e:
        print(f"ファイルの読み込み中にエラーが発生しました: {e}")
        sys.exit(1)
    
    # Discordの2000文字制限を考慮してコンテンツを分割
    max_chars = 2000
    chunks = [content[i:i + max_chars] for i in range(0, len(content), max_chars)]
    
    print(f"コンテンツは{len(content)}文字です。{len(chunks)}個のメッセージで送信します。")

    for i, chunk in enumerate(chunks):
        print(f"{i+1}/{len(chunks)}個目のチャンクを送信中...")
        send([chunk])
        if i < len(chunks) - 1:
            time.sleep(1)

if __name__ == "__main__":
    main()