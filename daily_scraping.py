from test_asama.usecase_test import get_store_url, add_items, clear_item
from get_pdf import link1_to_link2, update_url_list, get_url, get_bargains
from ocr_tanaka import ocr_all_stores
def main():
  """
  (店名,URL,(if type1 then 0 else 1))というタプルのリストを受け取る
  これを受け取った後、type1の店リストとtype2の店リストの2つに振り分け、それぞれ店名と一緒に.jpgと特売情報リストを返す
  """
  clear_item()
  input_list = get_store_url()
  type1_link1_list = []
  type2_link1_list = []
  for t in input_list:
      if t[2] == 0:
          type1_link1_list.append((t[0],t[1]))
      else:
          type2_link1_list.append((t[0],t[1]))
  link2_list = link1_to_link2(type1_link1_list)
  new_link2_list = update_url_list(link2_list)
  type1_link3_list = get_url(new_link2_list)
  ocr_all_stores(type1_link3_list)
  type2_string_list = get_bargains(type2_link1_list)
  for l in type2_string_list:
      add_items(l[0],l[1])
  print(type1_link3_list)

if __name__ == "__main__":
    main()