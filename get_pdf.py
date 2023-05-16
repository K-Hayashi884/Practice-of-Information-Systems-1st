"""
# コード内容

## 1. 取得店舗をtype1, type2 の2種類に分類

type1の店== tokubai.co.jpのリンクを踏むとチラシの画像が表示されるような店

type2の店== tokubai.co.jpのリンクを踏むと具体的な特売商品が文字列で表示されるような店

## 2-1. type1の店での流れ

- 2.店ごとにHTMLの表記法が微妙に異なるので、`link1_to_link2(link1_list)`という関数を作成。この関数は`link1_list`に含まれる適切なチラシの階層2リンク(string)のlist(`link2_list`)を返す
- 3.`link2_list`には最新ではないチラシも含まれるため、関数`update_url_list(link2_list)`を作成。`./urls.txt`を利用。返り値`new_link2_list`には新しいチラシの階層2リンク
- 4.`get_url(new_link2_list)`で階層2のリンクを階層3のリンクに変換

## 2-2. type2の店での流れ

このタイプは、店のURLに文字列として特売情報が記録されているので、これを直接ダウンロードする処理を行う
"""

import requests
from bs4 import BeautifulSoup
import calendar
from test_asama.usecase_test import get_store_url, add_items
#ユーザエージェント変更
ua = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
headers = {'User-Agent': ua}

## 1-2.店ごとに取得する条件が異なるため、`link1_to_link2(link1)`という関数を作成。
def link1_to_link2(link1_list):
    """
    リスト`link1_list`に含まれる適切なチラシの階層2リンク(文字列)のリスト(`link2_list`)を返す
    """
    link2_list = [] #最終的には取得日に乗っているチラシのリンク(link2)一覧が格納される
    for link1 in link1_list:
        if "%E3%83%A9%E3%82%A4%E3%83%95" in link1[1]: #ライフの場合
            r = requests.get(link1[1],headers=headers)
            soup = BeautifulSoup(r.text,"html.parser")
            elements = soup.find_all(class_="image_element")
            for element in elements:
                link = element.get("href")
                l = "https://tokubai.co.jp"
                date = element.find(class_="description").string
                if date.count("月") == 1: #チラシ掲載期間が月を跨がない場合 例：/n2023年4月2〜4日まで/n -> 2023,4,2,4
                    date = date[1:-1].replace("月",",").replace("〜",",").replace("日まで",",").replace("年",",")
                    dates = date.split(",")
                    period = int(dates[3]) - int(dates[2])
                else: #チラシ掲載期間が月を跨ぐ場合　例：/n2023年4月29日〜5月2日まで/n  -> 2023,4,29,5,2
                    date = date[1:-1].replace("月",",").replace("日〜",",").replace("日まで",",").replace("年",",")
                    dates = date.split(",")
                    period = int(dates[4]) - int(dates[2]) + calendar.monthrange(2023, int(dates[1])+1)[1]
                if period < 6: #ライフでは一般的に掲載期間が6日以上のチラシは取得したくないチラシなので
                    link2_list.append((link1[0],l+link))
        elif "%E3%82%B0%E3%83%AC%E3%83%BC%E3%82%B9%E3%81%9F%E3%81%AA%E3%81%8B" in link1[1]: #グレースたなかの場合
            r = requests.get(link1[1],headers=headers)
            soup = BeautifulSoup(r.text,"html.parser")
            elements = soup.find_all(class_="image_element")
            for element in elements:
                link = element.get("href")
                l = "https://tokubai.co.jp"
                date = element.find(class_="description").string
                link2_list.append((link1[0],l+link))
    return link2_list

## 1-3.`link2_list`には最新ではないチラシも含まれるため、関数`update_urllist(link2_list)`を作成。
def update_url_list(link2_list):
    """
    `link2_list`に含まれる最新でないURLを、./type1_urls.txtを利用し削除
    昨日まで存在しなかったチラシのリンクのリストを返す
    """
    new_link2_list = []
    with open('type1_urls.txt',"r") as f: #type1_urls.txtの中には昨日使用したlink2リンクの一覧がある
        lines = f.readlines()
        old_link2_list = [line.replace("¥n","").replace("\n","") for line in lines] #改行文字削除 怖かったので\と¥を書いた
    for link2 in link2_list:
        if link2[1] in old_link2_list: #昨日使用したリンクは無視
            continue
        else: #昨日なかったリンクは欲しいのでnew_link2_listに格納
            new_link2_list.append((link2[0],link2[1]))
            
    urls_new = map(lambda x: x[1] + "\n", link2_list)
    #link2_listの内容をtype1_urls.txtに保存
    with open('type1_urls.txt', 'w', encoding='utf-8') as f:
        f.writelines(urls_new)
    return new_link2_list

## 1-4.`get_urls()`で階層2のリンクを階層3のリンクに変換
def get_url(new_link2_list):
  """
  link2をlink3(.jpg)に変換する
  """
  link3_list = []
  for new_link2 in new_link2_list:
    r = requests.get(new_link2[1],headers=headers)
    soup = BeautifulSoup(r.text,"html.parser")
    link3_url = soup.find('img',class_='leaflet').get('src').split("?")[0]
    link3_list.append((new_link2[0], link3_url)) 
  return link3_list

## 2-1. type2の店リストから特売商品のリストを取得
## url更新はしなくてもよい(内容が更新されてもURLに変化がないため)
def get_bargains(link1_list):
    """
    type2の店のlink1リストから、特売商品のリストを取得
    """
    sales_list = []
    for link1 in link1_list:
        l = link1[1]
        r = requests.get(l,headers=headers)
        soup = BeautifulSoup(r.text,"html.parser")
        if "%E3%82%B3%E3%83%AC%E3%83%A2/187995" in l: #コレモ出町柳の場合
            l = "https://tokubai.co.jp/%E3%82%B3%E3%83%AC%E3%83%A2"
            if len(soup.find_all(class_="corner_more_link_wrapper")) == 1:
                link = soup.find(class_="corner_more_link")
                l = l + link.get("href")
                r = requests.get(l,headers=headers)
                soup = BeautifulSoup(r.text,"html.parser")
            elements = soup.find_all(class_="name hoverable_link")
            sales_list.append((link1[0],[(element.contents[0][1:-1],0) for element in elements]))

        elif "%E5%A4%A7%E5%9B%BD%E5%B1%8B/14801" in l: #大黒屋北白川の場合
            elements = soup.find_all(class_="name hoverable_link")
            sales_list.append((link1[0],[(element.contents[0][1:-1],0) for element in elements]))

        elif "%E3%83%95%E3%83%AC%E3%82%B9%E3%82%B3/4244" in l: #フレスコ川端の場合
            elements = soup.find_all(class_="name hoverable_link")
            sales_list.append((link1[0],[(element.contents[0][1:-1],0) for element in elements]))

        elif "%E3%82%A4%E3%82%BA%E3%83%9F%E3%83%A4/9148" in l: #イズミヤ高野の場合
            elements = soup.find_all(class_="name hoverable_link")
            sales_list.append((link1[0],[(element.contents[0][1:-1],0) for element in elements]))
    return sales_list