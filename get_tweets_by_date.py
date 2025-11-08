# tweets.jsから過去の同時期のツイートを抽出する
import sys
import json
from datetime import date, timedelta, datetime

def load_tweets_from_js(file_path):
    """
    tweets.jsファイルを読み込み、JSON部分をパースしてツイートのリストを返す。
    ファイル全体をメモリに読み込む。
    """
    print(f"'{file_path}' を読み込んでいます... (サイズが大きい場合、時間がかかることがあります)")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 'window.YTD.tweets.part0 = ' のようなJS部分を取り除く
        json_str = content[content.find('=') + 1:].strip()
        
        # JSONとしてパース
        data = json.loads(json_str)
        print("読み込みと解析が完了しました。")
        return data
    except FileNotFoundError:
        print(f"エラー: ファイルが見つかりません: {file_path}", file=sys.stderr)
        return None
    except json.JSONDecodeError:
        print(f"エラー: ファイル内のJSONデータの解析に失敗しました: {file_path}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"エラー: ファイルの読み込み中に予期せぬエラーが発生しました: {e}", file=sys.stderr)
        return None

def main():
    """
    メイン処理
    """
    # スクリプトがあるディレクトリからの相対パス
    # このスクリプトはプロジェクトルートに置かれることを想定
    TWEET_DATA_PATH = "data/tweets.js"
    
    tweet_data = load_tweets_from_js(TWEET_DATA_PATH)
    if tweet_data is None:
        sys.exit(1)

    today = date.today()
    # 検索する日付の範囲 (今日を基準に前後10日間)
    date_range_start = -10
    date_range_end = 10

    print(f"\n基準日: {today.strftime('%Y-%m-%d')}")
    print(f"検索範囲: {date_range_start}日前から{date_range_end}日後までのツイートを過去年にわたって検索します。")
    print("="*20)

    found_tweets = []

    # ロードした全ツイートを処理
    for tweet_obj in tweet_data:
        tweet = tweet_obj.get('tweet')
        if not tweet:
            continue

        full_text = tweet.get('full_text', '')
        created_at_str = tweet.get('created_at')

        # RTと返信は除外
        if full_text.startswith("RT @") or full_text.startswith("@"):
            continue

        if not created_at_str:
            continue

        # Twitterの日付フォーマットをdatetimeオブジェクトに変換
        # 例: "Wed May 25 09:27:55 +0000 2022"
        tweet_date = datetime.strptime(created_at_str, "%a %b %d %H:%M:%S %z %Y")

        # 検索範囲の日付に合致するかチェック
        for i in range(date_range_start, date_range_end + 1):
            target_date = today + timedelta(days=i)
            if tweet_date.month == target_date.month and tweet_date.day == target_date.day:
                found_tweets.append(tweet)
                break
    
    if not found_tweets:
        print("該当するツイートは見つかりませんでした。")
        return

    # 見つかったツイートを日付順にソート
    found_tweets.sort(key=lambda t: datetime.strptime(t['created_at'], "%a %b %d %H:%M:%S %z %Y"))

    # 年ごとにグループ化して表示
    last_year = None
    for tweet in found_tweets:
        tweet_date = datetime.strptime(tweet['created_at'], "%a %b %d %H:%M:%S %z %Y")
        if tweet_date.year != last_year:
            print(f"\n--- {tweet_date.year} ---")
            last_year = tweet_date.year
        
        full_text = tweet['full_text']
        
        # t.coリンクを展開する
        if 'entities' in tweet and 'urls' in tweet['entities']:
            for url_entity in tweet['entities']['urls']:
                if url_entity['url'] in full_text:
                    full_text = full_text.replace(url_entity['url'], url_entity['expanded_url'])

        date_str = tweet_date.strftime('%Y-%m-%d %H:%M')
        print(f"[{date_str}] {full_text}")

if __name__ == "__main__":
    # 文字化け対策
    sys.stdout.reconfigure(encoding='utf-8')
    main()
