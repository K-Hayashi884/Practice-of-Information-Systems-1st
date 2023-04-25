# 公式サイトからpdfリンク一覧取得
def get_urls():
  import requests
  from bs4 import BeautifulSoup

  html = requests.get('★公式サイトURL')
  soup = BeautifulSoup(html.text, 'html.parser')

  # ★以下は実際のHTML構成に合わせて実装する
  flyer_list = soup.find_all('table')
  url_list = []
  for flyer in flyer_list:
    # 日付
    date = flyer.find('div', {'class': 'sale'}).find('a').get_text(strip=True).replace(' ', '').replace('（', '(').replace('）', ')')

    # PDF
    url_info = {}
    url_info['date'] = date
    url_info['url'] = flyer.find('a', {'title': 'PDF'})['href']
    url_list.append(url_info)

  return url_list

# 未解析のチラシURLを取得
def get_new_urls(url_list):
  # urls.txt読込
  old_url_list = []
  with open('/urls.txt', 'r') as f:
    old_url_list = f.read().splitlines()

  new_url_list = []
  urls_text = []
  count = 0
  for url_info in url_list:
    urls_text.append(url_info['url'] + '\n')

    if url_info['url'] not in old_url_list:
      # 新規
      url_info['number'] = count
      new_url_list.append(url_info)
      count += 1

  # 今回のURL一覧をurls.txtに書込
  f = open('/urls.txt', 'w')
  f.writelines(urls_text)
  f.close()

  return new_url_list

# 新規のチラシPDFをDL
def dl_pdfs(new_url_list):
  import urllib.request
  import time

  pdf_list = []
  for url_info in new_url_list:
    file_name = f'./pdf/{url_info["number"]}.pdf'
    urllib.request.urlretrieve(url_info['url'], file_name)
    url_info['pdf_path'] = file_name
    # サーバーに負荷がかからないように時間をおく
    time.sleep(2)

    pdf_list.append(url_info)

  return pdf_list

# PDFをJPGに変換
def pdf_to_jpeg(path):
  import os
  from pathlib import Path
  from pdf2image import convert_from_path

  # poppler/binを環境変数PATHに追加する
  poppler_dir = '/lib/poppler/bin'
  os.environ['PATH'] += os.pathsep + str(poppler_dir)

  image_paths = []

  pdf_path = Path(path)
  # PDF -> Image に変換（150dpi）
  pages = convert_from_path(str(pdf_path), 150)

  # 画像ファイルを１ページずつ保存
  image_dir = Path('./jpg')
  for i, page in enumerate(pages):
    file_name = pdf_path.stem + '_{:02d}'.format(i + 1) + '.jpeg'
    image_path = image_dir / file_name
    # JPEGで保存
    page.save(str(image_path), 'JPEG')
    image_paths.append(image_path)

  return image_paths

### FlyerOCR ###
import shutil
import os
os.makedirs('pdf/', exist_ok=True)
os.makedirs('jpg/', exist_ok=True)

url_list = get_urls()
new_url_list = get_new_urls(url_list)
pdf_list = dl_pdfs(new_url_list)
jpg_list = pdfs_to_jpeg(pdf_list)
results = get_target_flyers(jpg_list)
slack_notice(results)

shutil.rmtree('pdf/')
shutil.rmtree('jpg/')