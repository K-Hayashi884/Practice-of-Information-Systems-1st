# Practice-of-Information-Systems-1st
情報学研究科の情報システム論実習の前半プロジェクトです

# 環境構築
```
git clone https://github.com/K-Hayashi884/Practice-of-Information-Systems-1st
cd ./Practice-of-Information-Systems-1st
python3 -m venv .venv
source ./.venv/bin/activate
pip install -r requirements.txt
git checkout -b <好きなブランチ名>
```

# パッケージインストールしたら
`pip install`をした後には必ず`pip freeze > requirements.txt`を走らせてください。

# 参考文献
- [データベース操作](https://engineer-lifestyle-blog.com/code/python/flask-tutorial-web-app-with-database/)

# コード内容

## 1. 取得店舗をtype1, type2 の2種類に分類

type1の店　== tokubai.co.jpのリンクを踏むとチラシの画像が表示されるような店

type2の店 == tokubai.co.jpのリンクを踏むと具体的な特売商品が文字列で表示されるような店

## 2-1. type1の店での流れ

- 2.店ごとにHTMLの表記法が微妙に異なるので、`link1_to_link2(link1_list)`という関数を作成。この関数は`link1_list`に含まれる適切なチラシの階層2リンク(string)のlist(`link2_list`)を返す
- 3.`link2_list`には最新ではないチラシも含まれるため、関数`update_url_list(link2_list)`を作成。`./urls.txt`を利用。返り値`new_link2_list`には新しいチラシの階層2リンク
- 4.`get_url(new_link2_list)`で階層2のリンクを階層3のリンクに変換

## 2-2. type2の店での流れ

このタイプは、店のURLに文字列として特売情報が記録されているので、これを直接ダウンロードする処理を行う
