from bs4 import BeautifulSoup
import requests
import secrets


dc_base_url = "https://gall.dcinside.com/mgallery/board/view/"
gall_name = "onshinproject"
hdrs = {'user-agent': ':Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}

def download_img(url):
    resp = requests.get(url, headers=hdrs)
    bs = BeautifulSoup(resp.text, 'lxml')
    content = bs.find('div', attrs={'class' : 'write_div'})
    imgs = content.find_all('img')
    for img in imgs:
        link = img['src']
        resp = requests.get(link, headers=hdrs)
        with open(f'./settings/new/{secrets.token_hex(nbytes=2)}.png', 'wb') as f:
            f.write(resp.content)

def main():
    five_star_url = f"{dc_base_url}?id={gall_name}&no=2347634"
    four_star_url = f"{dc_base_url}?id={gall_name}&no=2347659"

    download_img(five_star_url)
    download_img(four_star_url)
    

if __name__ == '__main__':
    main()