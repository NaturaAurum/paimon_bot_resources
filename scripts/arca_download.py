from os import link
from bs4 import BeautifulSoup
import requests
import secrets
from pprint import pprint


base_url = "https://arca.live/b/genshin/"
target_url = f"{base_url}25385257"
hdrs = {'user-agent': ':Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
traveler_id = "24953655"
traveler_url = f"{base_url}{traveler_id}"

def get_content_area(bs: BeautifulSoup):
     content = bs.find('div', attrs={"class":"fr-view article-content"})
     return content

def get_character_img(link):
    resp = requests.get(link, headers=hdrs)
    bs = BeautifulSoup(resp.text, 'lxml')
    content = get_content_area(bs)
    img = content.find_all('img')[1]
    return f"{img['src'][2:]}?type=orig"

def get_traveler_img():
    resp = requests.get(traveler_url, headers=hdrs)
    bs = BeautifulSoup(resp.content, 'lxml')
    content = get_content_area(bs)
    img_tags = content.find_all('img')[1:4]
    result = []

    for img in img_tags:
        result.append(f"{img['src'][2:]}?type=orig")
    
    return result

def get_link_from_table(table):
    result = []
    trs = table.find_all('tr')
    for tr in trs:
        td = tr.find_all('td')[1]
        a_tags = td.find_all('a')
        for a in a_tags:
            link = str(a['href'])
            if link.endswith("24953655"):
                continue
            result.append(link)
    return result


def get_character_content_url_list():
    '''
    아카라이브 모음 글에서 캐릭터 url 열어서 이미지 url들을 가져온다.
    '''
    resp = requests.get(target_url, headers=hdrs)
    bs = BeautifulSoup(resp.content, 'lxml')
    content = get_content_area(bs)
    tables = content.find_all('table')
    five_star = tables[0]
    four_star = tables[1]
    five_links = get_link_from_table(five_star)
    four_links = get_link_from_table(four_star)

    five_img_links = []
    four_img_links = []

    for five_link in five_links:
        five_img_links.append(get_character_img(five_link))
    
    for four_link in four_links:
        four_img_links.append(get_character_img(four_link))

    traveler_img_links = get_traveler_img()

    result_dict = {}
    link_list = []
    link_list.extend(five_img_links)
    result_dict["five"] = link_list
    link_list = []
    link_list.extend(four_img_links)
    result_dict["four"] = link_list
    link_list = []
    link_list.extend(traveler_img_links)
    result_dict["traveler"] = link_list
    return result_dict

def download_and_save(links : dict):
    for name, link_list in links.items():
        for link in link_list:
            resp = requests.get(f'https://{link}', headers=hdrs)
            with open(f'./settings/new/{name}_{secrets.token_hex(nbytes=2)}.png', 'wb') as f:
                f.write(resp.content)


def main():
    img_link_list = get_character_content_url_list()
    #pprint(img_link_list)
    download_and_save(img_link_list)

if __name__ == '__main__':
    main()
