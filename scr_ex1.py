import requests
from bs4 import BeautifulSoup

def get_wikipedia_article(keyword):
    # WikipediaのURLを生成
    url = f"https://ja.wikipedia.org/wiki/{keyword}"

    # User-Agent ヘッダーを設定
    headers = {
        'User-Agent': 'EducationalResearch; PythonTutorial/1.0; Contact: YourEmail@example.com'
    }
    
    # ページのデータを取得
    response = requests.get(url)
    
    if response.status_code != 200:
        return "記事が見つかりません"

    # HTMLを解析
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # タイトルと最初の3つのパラグラフを取得
    title = soup.find('h1', {'id': 'firstHeading'}).text
    paragraphs = soup.find_all('p', limit=3)
    intro_text = ' '.join([p.text for p in paragraphs])

    return title, intro_text

# キーワードを指定（例: "Python"）
keyword = "Python"

title, intro_text = get_wikipedia_article(keyword)

print("タイトル:", title)
print("最初の3つのパラグラフ:", intro_text)
