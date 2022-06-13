from requests import get
from lxml import etree
import pyperclip

def guid():
    url = 'https://www.guidgen.com/'
    html = etree.HTML(get(url).text)
    id = ''.join(html.xpath('//p/input/@value'))
    id = id[:8] + id[9:13] + id[14:18] + id[19:23] + id[24:]
    return id


if __name__ == '__main__':
    print('获取GUID中...')
    while 1:
        try:
            id = guid()
        except Exception:
            print('请检查网络')
        print('GUID\40' + id)
        pyperclip.copy('GUID\40' + id)
        if input('已将GUID复制到剪贴板中,键入1以重新获取') != '1':
            break