import requests
from bs4 import BeautifulSoup
import json
import time
from urllib.parse import urljoin
import csv

class ChowagokenScraper:
    def __init__(self):
        self.base_url = "https://www.chowagiken.co.jp/"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
    def get_page_content(self, url):
        """指定されたURLからページコンテンツを取得"""
        try:
            response = self.session.get(url)
            response.raise_for_status()
            response.encoding = 'utf-8'
            return response.text
        except requests.RequestException as e:
            print(f"エラー: {url} の取得に失敗しました - {e}")
            return None
    
    def scrape_main_page(self):
        """メインページから基本情報を抽出"""
        html_content = self.get_page_content(self.base_url)
        if not html_content:
            return None
            
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # 基本情報を抽出
        company_info = {
            'company_name': '株式会社調和技研',
            'main_title': '',
            'main_description': '',
            'services': [],
            'features': [],
            'clients': [],
            'images': []
        }
        
        # メインタイトルと説明文を抽出
        main_text = soup.get_text()
        lines = [line.strip() for line in main_text.split('\n') if line.strip()]
        
        # タイトル部分を抽出
        for i, line in enumerate(lines):
            if 'DX実現' in line or 'AI活用' in line:
                company_info['main_title'] = line
                if i + 1 < len(lines):
                    company_info['main_description'] = lines[i + 1]
                break
        
        # サービス情報を抽出
        service_keywords = ['コンサルティング', 'AI開発', 'AI人材育成']
        for line in lines:
            for keyword in service_keywords:
                if keyword in line and len(line) > 10:
                    company_info['services'].append(line)
                    break
        
        # 特徴を抽出
        feature_keywords = ['150件以上', '学術レベル', '独自の高品質エンジン']
        for line in lines:
            for keyword in feature_keywords:
                if keyword in line and len(line) > 15:
                    company_info['features'].append(line)
                    break
        
        # 画像URLを抽出
        images = soup.find_all('img')
        for img in images:
            src = img.get('src')
            if src:
                full_url = urljoin(self.base_url, src)
                alt_text = img.get('alt', '')
                company_info['images'].append({
                    'url': full_url,
                    'alt': alt_text
                })
        
        # クライアント情報を抽出（画像のalt属性から）
        client_images = [img for img in images if 'logo' in img.get('src', '') or '様' in img.get('alt', '')]
        for img in client_images:
            alt_text = img.get('alt', '')
            if alt_text and '様' in alt_text:
                company_info['clients'].append(alt_text)
        
        return company_info
    
    def extract_contact_info(self, soup):
        """連絡先情報を抽出"""
        contact_info = {}
        
        # お問い合わせセクションを探す
        contact_text = soup.get_text()
        if 'お問い合わせ' in contact_text:
            contact_info['contact_available'] = True
            contact_info['contact_message'] = 'お気軽にお問い合わせください'
        
        return contact_info
    
    def save_to_json(self, data, filename='chowagiken_data.json'):
        """データをJSONファイルに保存"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"データが {filename} に保存されました")
        except Exception as e:
            print(f"JSON保存エラー: {e}")
    
    def save_to_csv(self, data, filename='chowagiken_data.csv'):
        """基本データをCSVファイルに保存"""
        try:
            with open(filename, 'w', encoding='utf-8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['項目', '内容'])
                writer.writerow(['会社名', data.get('company_name', '')])
                writer.writerow(['メインタイトル', data.get('main_title', '')])
                writer.writerow(['説明', data.get('main_description', '')])
                
                # サービス
                for i, service in enumerate(data.get('services', [])):
                    writer.writerow([f'サービス{i+1}', service])
                
                # 特徴
                for i, feature in enumerate(data.get('features', [])):
                    writer.writerow([f'特徴{i+1}', feature])
                
                # クライアント
                for i, client in enumerate(data.get('clients', [])):
                    writer.writerow([f'クライアント{i+1}', client])
            
            print(f"データが {filename} に保存されました")
        except Exception as e:
            print(f"CSV保存エラー: {e}")
    
    def scrape_all(self):
        """全ての情報をスクレイピング"""
        print("調和技研のウェブサイトをスクレイピング中...")
        
        # メインページをスクレイピング
        main_data = self.scrape_main_page()
        
        if main_data:
            print("\n=== 取得データ ===")
            print(f"会社名: {main_data['company_name']}")
            print(f"メインタイトル: {main_data['main_title']}")
            print(f"説明: {main_data['main_description']}")
            
            print(f"\nサービス数: {len(main_data['services'])}")
            for i, service in enumerate(main_data['services'], 1):
                print(f"  {i}. {service}")
            
            print(f"\n特徴数: {len(main_data['features'])}")
            for i, feature in enumerate(main_data['features'], 1):
                print(f"  {i}. {feature}")
            
            print(f"\nクライアント数: {len(main_data['clients'])}")
            for i, client in enumerate(main_data['clients'], 1):
                print(f"  {i}. {client}")
            
            print(f"\n画像数: {len(main_data['images'])}")
            
            # データを保存
            self.save_to_json(main_data)
            self.save_to_csv(main_data)
            
            return main_data
        else:
            print("データの取得に失敗しました")
            return None

def main():
    """メイン実行関数"""
    scraper = ChowagokenScraper()
    
    try:
        # スクレイピング実行
        data = scraper.scrape_all()
        
        if data:
            print("\n✅ スクレイピング完了!")
            print("📁 'chowagiken_data.json' - 詳細なJSON形式")
            print("📊 'chowagiken_data.csv' - 表形式のサマリー")
        else:
            print("❌ スクレイピングに失敗しました")
            
    except KeyboardInterrupt:
        print("\n⚠️  スクレイピングが中断されました")
    except Exception as e:
        print(f"❌ エラーが発生しました: {e}")

if __name__ == "__main__":
    main()