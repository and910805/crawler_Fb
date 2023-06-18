
from selenium import webdriver
import time
from bs4 import BeautifulSoup
import bs4
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pygsheets

index_url='https://www.facebook.com/groups/1260448967306807/?hoisted_section_header_type=recently_seen&multi_permalinks=3832053180146360'

class Connect:
    def __init__(self):
        self.browser = webdriver.Chrome()
        self.contents=""
        self.posttime=""
        self.comment=""
        self.comment_number=0    
        self.good_number=""
        
    def connect_pygsheets(self):
        self.gc = pygsheets.authorize(service_file='./auth.json')
        self.spreadsheet = self.gc.open_by_key('1Ymi5GT_nydUbPc--vuFh9tXSEPKnEMKjOPJzJrfTqSw') 
        self.worksheet = self.spreadsheet.sheet1
        
      
        print('資料已儲存到 Google Sheets 中。')
    def runsrc(self):
        self.browser.get(index_url)
        time.sleep(3)
     
  

    def content(self):
        soup= BeautifulSoup(self.browser.page_source,"lxml")
        
        posts= soup.find_all("div", {"class": "x9f619 x1n2onr6 x1ja2u2z x2bj2ny x1qpq9i9 xdney7k xu5ydu1 xt3gfkd xh8yej3 x6ikm8r x10wlt62 xquyuld"})
        post_number=1
        for tmp in posts[1:]:
            self.comment_number = int(tmp.find("span", {"class": "x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen xo1l8bm xi81zsa"}).text.replace("則留言",""))
            if self.comment_number > 50:#只抓大於50的貼文
                
                self.posttime = tmp.find(class_='x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x1heor9g xt0b8zv xo1l8bm').text
                
                try:
                    button = self.browser.find_element("xpath","//div[@class='x1iorvi4 x1pi30zi x1l90r2v x1swvt13']//div[@role='button' and contains(text(), '查看更多')]")
                    button.click()
                except:
                    print("內文不夠長，不用展開")
                    pass
                # post_element = self.browser.find_element('xpath', "//div[@class='x1jx94hy x12nagc']")
                while True:
                    try:
                        button=self.browser.find_element("xpath","//div[@class='x78zum5 x1iyjqo2 x21xpn4 x1n2onr6']//div[@class='x1i10hfl xjbqb8w xjqpnuy xa49m3k xqeqjp1 x2hbi6w x13fuv20 xu3j5b3 x1q0q8m5 x26u7qi x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xdl72j9 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r x2lwn1j xeuugli xexx8yu x18d9i69 xkhd6sd x1n2onr6 x16tdsg8 x1hl2dhg xggy1nq x1ja2u2z x1t137rt x1o1ewxj x3x9cwd x1e5q0jg x13rtm0m x3nfvp2 x1q0g3np x87ps6o x1a2a7pz x6s0dn4 xi81zsa x1iyjqo2 xs83m0k xsyo7zv xt0b8zv']")
                        button.click()
                        time.sleep(1)
                    except:
                        print("留言都打開了")
                        break
            
                self.good_number=tmp.find(class_="xrbpyxo x6ikm8r x10wlt62 xlyipyv x1exxlbk").text
                
                print("按讚數: "+self.good_number)
                print("發文時間: "+self.posttime)#時間
                print("留言數量: "+str(self.comment_number))
                #要重新抓取頁面，不然留言找不到
                soup=BeautifulSoup(self.browser.page_source,"lxml")
                posts= soup.find_all("div", {"class": "x9f619 x1n2onr6 x1ja2u2z x2bj2ny x1qpq9i9 xdney7k xu5ydu1 xt3gfkd xh8yej3 x6ikm8r x10wlt62 xquyuld"})
                tmp_number=1
                for tmp2 in posts[1:]:#要找尋剛剛是抓哪一篇文章
                    if(tmp_number==post_number):
                        usercontents = tmp.find_all('div',{'class':'xdj266r x11i5rnm xat24cr x1mh8g0r x1vvkbs x126k92a'})
                    
                        self.contents += usercontents[0].get_text(separator='\n').strip()
                        print("內文: "+ self.contents)
                        comments_div = tmp2.find_all(class_="xdj266r x11i5rnm xat24cr x1mh8g0r x1vvkbs")
                        comments_people = tmp2.find_all(class_="x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x4zkp8e x676frb x1nxh6w3 x1sibtaa x1s688f xzsf02u")
                        a=5
                        self.worksheet.update_value((2, 1), self.contents)  
                        self.worksheet.update_value((2, 2), self.posttime)  
                        self.worksheet.update_value((2, 3), self.good_number)
                        self.worksheet.update_value((2, 4), self.comment_number)
                        for div, people in zip(comments_div[1:], comments_people):
                            try:
                                div_text = div.get_text(separator='\n').strip()
                                people_text = people.get_text().strip()
                                self.comment="發言者("+people_text+"): 留言內容: "+div_text+"\n"
                                print(self.comment)
                                time.sleep(0.5)
                                
                                self.worksheet.update_value((2, a), self.comment)
                                a+=1
                                
                            except:
                                break
                                
                            
                        
                        
                    else:
                        tmp_number+=1
                break
            else:
                post_number+=1
            
if __name__ == '__main__':
    connect=Connect()
    connect.connect_pygsheets()
    connect.runsrc()
    connect.content()