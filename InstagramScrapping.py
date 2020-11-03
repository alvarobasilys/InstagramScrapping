from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time

class InstagramScrapping:
    def __init__(self,login,webdriver_dir):
        '''
        parameter:
            login (tuple/list) = (username,password) #You need to login to instagram
            webdriver_dir (string) = webdriver location (Make sure its Windows Edge webdriver!, if you using another webdriver, just change line 17) 
        '''
        self.login = login
        print(' Star Load Driver '.center(50,'\\'))
        self.driver = webdriver.Edge(executable_path=webdriver_dir)
        print('    Path         :',webdriver_dir)
        print(' Load Driver Success '.center(50,'\\'))

    def execute(self,userTarget,load_loop,n_link):
        '''
        parameter:
            userTarget (string) : instagram account link
            load_loop (int) : how far you going to load the Instagram feed.
            n_link (int) : how far you going to extract the data. 
        '''
        self.driver.get(userTarget)
        self.driver.find_element_by_css_selector("button.sqdOP.L3NKy.y3zKF").click()
        time.sleep(5)
        logins = self.driver.find_elements_by_css_selector("._2hvTZ.pexuQ.zyHYP")

        print(' Login Instagram '.center(50,'\\'))
        print('    Username     : ',self.login[0])
        print('    pass         : ','*'*len(self.login[0]))
        i = 0
        for login in logins:
            login.send_keys(self.login[i])
            if i == 1:
                login.send_keys(Keys.ENTER)
            i+=1
        time.sleep(5)
        self.driver.find_element_by_css_selector('.sqdOP.yWX7d.y3zKF').click()
        
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        print(' Login Finished '.center(50,'\\'))
        #Load all post...
        for x in range(0,load_loop):
            print('    Scrolling. . . .',x+1,'/',load_loop)
            # Scroll down to bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(2)

            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        self.driver.execute_script("window.scrollTo(0,0)")
        
        print(' Scroll Finished '.center(50,'\\'))

        #Extract all post links
        self.links = set()
        for x in range(0,n_link):
            print('    Extract link post. . . ',x+1,'/',n_link)

            ##Crawling, extract link data
            html = self.driver.page_source
            soup = bs(html,'html.parser')
            row = soup.find_all('div','Nnq7C weEfm')
            for r in row:
                tag_a = r.find_all('a')
                for a in tag_a:
                    self.links.add(a['href'])
            
            self.driver.find_element_by_css_selector('body').send_keys(Keys.PAGE_DOWN)
            time.sleep(0.5)
        print('    Success Extract ',len(self.links),' Links! ')

        print(' Scroll Finished '.center(50,'\\'))
        
        print(' Extract Post '.center(50,'\\'))
        
        count = 1
        self.dates = []
        self.likes = []
        self.comments = []
        self.captions = []
        for link in self.links:
            url = 'https://www.instagram.com/'+link
            self.driver.get(url)
            time.sleep(0.1)
            html = self.driver.page_source
            soup = bs(html,'html.parser')
            print('    load',link,'||',count,'/',len(self.links))

            #Extract Date
            d = soup.find('div','k_Q0X NnvRN').find('a','c-Yi7').find('time','_1o9PC Nzb55')
            self.dates.append(d['datetime'])
            print('    Date:',d['datetime'])

            #Extract like
            if len(soup.findAll('div','Nm9Fw'))==0:
                print('    Like: Undifined!')
                self.likes.append('Undifined!')
            else:
                l = soup.find('div','Nm9Fw').find('button').find('span')
                self.likes.append(l.get_text())
                print('    Like:',l.get_text())

            #Extract comment
            c = soup.find_all('div','C7I1f')
            self.comments.append(len(c))
            print('    Comment:',len(c))
            
            #Extract Caption
            if(len(soup.find_all('div','C4VMK'))!=0):
                ca = soup.find('div','C4VMK').find_all('span')[-1]
                self.captions.append(ca.get_text().encode("utf-8"))
                print('    Caption: True')
                print('            ',ca.get_text().encode("utf-8"))
            else:
                self.captions.append('No Caption')
                print('    Caption: False')
            count=count+1
            print('-'*50)
        self.driver.close()
        print(' Extract Post Finished '.center(50,'\\'))
    def toCSV(self,save_path):
        '''
        parameter:
            save_path (string) : save path 
        '''
        print(' Start Export to CSV '.center(50,'\\'))
        df = self.toDataFrame()
        df.to_csv(save_path, index = None, header=True)
        print(' Export to CSV Finish '.center(50,'\\'))
    def toDataFrame(self):
        csvDict = {
            'Link':list(self.links),
            'TimeStamp':self.dates,
            'Like':self.likes,
            'Comment':self.comments,
            'Caption':self.captions
        }
        df = pd.DataFrame(csvDict,columns = ['Link','TimeStamp','Like','Comment','Caption'])
        return df
