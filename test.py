import time, requests, json, re, os, opencc, urllib.request
from bs4 import BeautifulSoup
from collections import Counter
from urllib.request import urlopen

w_url='https://www.wenku8.net'
def test1():
    scale = 50
    print("执行开始".center(scale // 2, "-"))  # .center() 控制输出的样式，宽度为 25//2，即 22，汉字居中，两侧填充 -
    start = time.perf_counter()  # 调用一次 perf_counter()，从计算机系统里随机选一个时间点A，计算其距离当前时间点B1有多少秒。当第二次调用该函数时，默认从第一次调用的时间点A算起，距离当前时间点B2有多少秒。两个函数取差，即实现从时间点B1到B2的计时功能。

    for i in range(scale + 1):
        a = '*' * i  # i 个长度的 * 符号
        b = '.' * (scale - i)  # scale-i） 个长度的 . 符号。符号 * 和 . 总长度为50
        c = (i / scale) * 100  # 显示当前进度，百分之多少
        dur = time.perf_counter() - start  # 计时，计算进度条走到某一百分比的用时
        print("\r{:^3.0f}% [{}->{}] {:.2f}s".format(c, a, b, dur),end='')# \r用来在每次输出完成后，将光标移至行首，这样保证进度条始终在同一行输出，即在一行不断刷新的效果；{:^3.0f}，输出格式为居中，占3位，小数点后0位，浮点型数，对应输出的数为c；{}，对应输出的数为a；{}，对应输出的数为b；{:.2f}，输出有两位小数的浮点数，对应输出的数为dur；end=''，用来保证不换行，不加这句默认换行。
        time.sleep(0.1)  # 在输出下一个百分之几的进度前，停止0.1秒
    print("\n" + "执行结果".center(scale // 2, '-'))
    '''
def progress(now):
    global x
    global xx
    global start
    c = (now / xx) *100  # 显示当前进度，百分之多少
    a = '*' * int(c/2)  # i 个长度的 * 符号
    b = '.' * (50-int(c/2))  # scale-i） 个长度的 . 符号。符号 * 和 . 总长度为50
    dur = time.perf_counter() - start  # 计时，计算进度条走到某一百分比的用时
    print("\r{:^3.0f}%_{:.2f}s_[{}->{}]".format(c, dur, a, b), end='')
    '''
def get_data(url):
    data = json.loads(requests.get(url).text)
    if data['Response'] == 'True':
        return data
    else:
        return None
def get_web_page(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                             'AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/66.0.3359.181 Safari/537.36'}
    resp = requests.get(url, headers=headers)
    resp.encoding='gbk' #更改編碼器為GBK
    if resp.status_code == 200: #網頁是否存在
        return resp.text
    else:
        print('Invalid url:', resp.url)
        return None
def get_novel(dom):
    soup = BeautifulSoup(dom, 'lxml')
    novels=[]
    title=soup.find('div',id='title').text  #標題
    author=soup.find('div',id='info').text.split('：')[-1]  #作者
    name=[cc(rereplace(title)),cc(rereplace(author))]
    chapter_title = soup.find_all('td', 'vcss')
    for c in chapter_title:
        chapter_title_text=c.text   #章節
        chapter=c.parent.find_next_sibling('tr').a['href'].split('.')[0]    #章節第一節超連結
        #chapter = c.parent.find_next_sibling('tr').find('a', {'href': re.compile('\d+')})['href'].split('.')[0]
        novels.append({'chapter_title':chapter_title_text,'chapter':chapter})
    return name, novels
def rereplace(text):
    tt=re.sub('[/:*??"<>|\\\]+', '', text)
    return tt
def cc(c):  #簡轉繁
    cc=opencc.OpenCC('s2t')
    cn=cc.convert(c)
    return cn

def download(now_num, obj, p_name):
    download_add='http://dl.wenku8.com/packtxt.php?aid='+str(now_num)+'&vid='+str(obj['chapter'])#+'&charset=utf-8'
    urllib.request.urlretrieve(download_add,p_name+rereplace(str(obj['chapter_title']))+'.txt')
def when(n,title):
    global start
    dur = time.perf_counter() - start  # 计时，计算进度条走到某一百分比的用时
    print("\r第{}個 {} 已花費{:.2f}s".format(n, title, dur), end='')
if __name__ == '__main__':
    if not os.path.isdir('novels'):  # n資料夾是否存在
        os.mkdir('novels')
    os.chdir('novels')
    scale = 50
    print("执行开始".center(scale // 2, "-"))
    start = time.perf_counter()

    for n in range(977,978):
        try:
            url='https://www.wenku8.net/novel/'+str(int(n/1000))+'/'+str(n)+'/index.htm'
            resp = get_web_page(url)
            name,novels = get_novel(resp)   #標題 作者 與章節+超連結
            n_name='_'.join(name)
            if not os.path.isdir(n_name):   #n資料夾是否存在
                os.mkdir(n_name)    #創建資料夾
            add =  n_name +'/'   #下載地址os.getcwd() +'/' +
            for d in novels:
                download(n, d, add) #開載
            when(n,name[0])
        except Exception as e:
            Error_log = []
            Error_log.append(e)
            print(e)
    #[\*?？"<>!][／/:, -]
    print('\n'+"执行结果".center(scale // 2, '-'))