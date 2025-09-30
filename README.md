# 調和技研ウェブサイトスクレイピングツール

株式会社調和技研の公式ウェブサイト（https://www.chowagiken.co.jp/）　から企業情報を自動取得するPythonスクレイピングツールです。

## 📋 概要

このツールは、調和技研のウェブサイトから以下の情報を自動で抽出・整理します：

- **企業基本情報**: 会社名、メインタイトル、説明文
- **サービス情報**: コンサルティング、AI開発、AI人材育成サービス
- **企業特徴**: 開発実績、技術力、独自エンジンなど
- **クライアント情報**: 取引先企業一覧
- **画像情報**: サイト内の全画像URL・alt属性

## 🚀 主な機能

- ✅ **自動データ抽出**: キーワードベースの高精度な情報抽出
- ✅ **複数形式出力**: JSON・CSV形式での保存
- ✅ **画像URL取得**: 相対URLの自動変換
- ✅ **クライアント自動識別**: 日本語敬語パターンの活用
- ✅ **エラーハンドリング**: ネットワークエラーや例外処理

## 📁 ファイル構成

```
scraping_easy/
├── chowagiken_scraper.py    # メインスクレイピングプログラム
├── README.md                # このファイル
├── requirements.txt         # 必要なライブラリ一覧
├── chowagiken_data.json     # 出力：詳細JSON形式（実行後生成）
└── chowagiken_data.csv      # 出力：表形式サマリー（実行後生成）
```

## 🔧 実行環境

- **Python**: 3.11.13 以上
- **OS**: Windows 10/11（その他OSでも動作）
- **必要ライブラリ**: requests, beautifulsoup4

## 📦 インストール

### 1. リポジトリのクローンまたはダウンロード

```bash
# GitHubからクローンする場合
git clone [リポジトリURL]
cd scraping_easy

# または、ファイルを直接ダウンロードして配置
```

### 2. 必要なライブラリのインストール

```bash
pip install -r requirements.txt
```

または個別インストール：

```bash
pip install requests==2.32.5 beautifulsoup4==4.14.2
```

## 🏃‍♂️ 使用方法

### 基本的な実行

```bash
python chowagiken_scraper.py
```

### 実行例

```bash
PS C:\Users\python\chowa\scraping> python chowagiken_scraper.py
調和技研のウェブサイトをスクレイピング中...

=== 取得データ ===
会社名: 株式会社調和技研
メインタイトル: 企業のDX実現に導くAI活用をトータルサポート
説明: 北大の研究室から生まれた調和技研は...

サービス数: 3
  1. コンサルティングサービス
  2. AI開発・導入支援サービス
  3. AI人材育成サービス

特徴数: 3
  1. 150件以上の開発実績に基づく豊富な知見
  2. AI分野の著名教授陣との連携と学術レベルの技術
  3. 言語系・画像系・数値系の独自の高品質エンジンを所有

クライアント数: 20
  1. 株式会社アクシスウェア様
  2. アサヒサンクリーン株式会社様
  ...

画像数: 50

データが chowagiken_data.json に保存されました
データが chowagiken_data.csv に保存されました

✅ スクレイピング完了!
📁 'chowagiken_data.json' - 詳細なJSON形式
📊 'chowagiken_data.csv' - 表形式のサマリー
```

## 📊 出力ファイル形式

### JSON形式（chowagiken_data.json）
```json
{
  "company_name": "株式会社調和技研",
  "main_title": "企業のDX実現に導くAI活用をトータルサポート",
  "main_description": "北大の研究室から生まれた調和技研は...",
  "services": [
    "コンサルティングサービス",
    "AI開発・導入支援サービス",
    "AI人材育成サービス"
  ],
  "features": [...],
  "clients": [...],
  "images": [
    {
      "url": "https://www.chowagiken.co.jp/assets/...",
      "alt": "画像の説明"
    }
  ]
}
```

### CSV形式（chowagiken_data.csv）
| 項目 | 内容 |
|------|------|
| 会社名 | 株式会社調和技研 |
| メインタイトル | 企業のDX実現に導く... |
| サービス1 | コンサルティングサービス |
| ... | ... |

## ⚙️ カスタマイズ

### キーワード変更

```python
# サービスキーワードの変更
service_keywords = ['コンサルティング', 'AI開発', 'AI人材育成', '新しいキーワード']

# 特徴キーワードの変更
feature_keywords = ['150件以上', '学術レベル', '独自の高品質エンジン']
```

### 出力形式の追加

```python
def save_to_excel(self, data, filename='chowagiken_data.xlsx'):
    # Excel形式での保存機能追加例
    pass
```

