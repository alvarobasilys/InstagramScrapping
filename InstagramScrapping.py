from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import pandas as pd
from numpy import nan
import time
from absl import app,flags,logging
from tqdm import tqdm

class InstagramScrapping:
    def __init__(self,login,webdriver_dir,targetLink,load_loop = 1,login_delay = 3.0,load_delay = 3.0,crawl_delay = 0.5):
        '''
        parameter:
            login (tuple/list) : (username,password) #You need to login to instagram
            webdriver_dir (string) : webdriver location (Make sure its Windows Edge webdriver!, if you using another webdriver, just change line 17) 
            targetLink (string) : instagram account link
            load_loop (int) : how far you going to load the Instagram feed.
            load_delay (float) : delay time of action before crawling.
            crawl_delay (float) : delay time when load instagram post.
        '''
        self.login = login
        logging.info('Load Driver. . .')
        self.driver = webdriver.Edge(executable_path=webdriver_dir)
        logging.info('    Path         :'+webdriver_dir)

        self.driver.get(targetLink)
        self.driver.find_element_by_css_selector("button.sqdOP.L3NKy.y3zKF").click()
        time.sleep(login_delay)
        logins = self.driver.find_elements_by_css_selector("._2hvTZ.pexuQ.zyHYP")
    
        logging.info('\nLogin Instagram. . .')
        logging.info('    Username     : '+str(self.login[0]))
        logging.info('    pass         : '+'*'*len(self.login[0]))
        i = 0
        for login in logins:
            login.send_keys(self.login[i])
            if i == 1:
                login.send_keys(Keys.ENTER)
            i+=1
        time.sleep(login_delay)
        self.driver.find_element_by_css_selector('.sqdOP.yWX7d.y3zKF').click() 
        
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        #Load all post...
        logging.info('\nScrolling. . .')
        for x in tqdm(range(0,load_loop)):
            
            # Scroll down to bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(load_delay)

            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        self.driver.execute_script("window.scrollTo(0,0)")

        #Extract all post links
        self.links = set()
        logging.info('\nExtract link post. . .')
        
        while True:
            ##Crawling, extract link data
            html = self.driver.page_source
            soup = bs(html,'html.parser')
            row = soup.find_all('div','Nnq7C weEfm')
            for r in row:
                tag_a = r.find_all('a')
                for a in tag_a:
                    self.links.add(a['href'])
            
            self.driver.find_element_by_css_selector('body').send_keys(Keys.PAGE_DOWN)
            time.sleep(crawl_delay)

            if last_height < self.driver.execute_script("return window.pageYOffset"):
                break
        logging.info('\nExtract Post. . .')
        
        self.dates = []
        self.post_type = []
        self.likes = []
        self.views = []
        self.comments = []
        self.captions = []
        for link in tqdm(self.links):
            url = 'https://www.instagram.com/'+link
            self.driver.get(url)
            time.sleep(crawl_delay)
            html = self.driver.page_source
            soup = bs(html,'html.parser')
            #Extract Date
            try:
                d = soup.find('time','_1o9PC Nzb55')
            
                self.dates.append(d['datetime'])
                    
                #Extract post type
                if len(soup.findAll('div','fXIG0')) == 0:
                    pt = 'Photo'
                    self.post_type.append(pt)
                else:
                    pt = 'Video'
                    self.post_type.append(pt)

                #Get View
                view_raw = soup.find_all('span','vcOH2')
                if len(view_raw) != 0:
                    v = view_raw[0].get_text()
                    viewInt = int(v[:v.find(' ')].replace(",",""))
                    self.views.append(viewInt)
                    
                    #Extract like for video
                    self.driver.find_element_by_class_name("vcOH2").click()
                    html = self.driver.page_source
                    soup = bs(html,'html.parser')

                    l = soup.find('span','vcOH2').get_text()
                    if l != 'like this':
                        likeInt = int(l[:l.find(' ')].replace(",",""))
                        self.likes.append(likeInt)

                    else:
                        self.likes.append(0)
                    
                else:
                    #Extract like for photo
                    self.views.append(nan)
                    likes_raw = soup.find_all('div','Nm9Fw')
                    
                    if len(likes_raw) != 0:
                        l = likes_raw[0].find('button').get_text()
                        if l != "like this":
                            likeInt = int(l[:l.find(' ')].replace(",",""))
                            self.likes.append(likeInt)
                        else:
                            self.likes.append(0)

                #Extract comment
                c = soup.find_all('div','C7I1f')
                self.comments.append(len(c))
                
                #Extract Caption
                if(len(soup.find_all('div','C4VMK'))!=0):
                    ca = soup.find('div','C4VMK').find_all('span')[-1]
                    self.captions.append(ca.get_text().encode("utf-8"))
                else:
                    self.captions.append(nan)
            
            except TypeError:
                self.dates.append(nan)
                self.post_type.append(nan)
                self.views.append(nan)
                self.likes.append(nan)
                self.comments.append(nan)
                self.captions.append(nan)
            
        self.driver.close()
        #print(len(self.links),len(self.dates),len(self.post_type),len(self.views),len(self.likes),len(self.comments),len(self.captions))


    def toCSV(self,save_path):
        '''
        parameter:
            save_path (string) : save path 
        '''
        logging.info('\nStart Export to CSV ...')
        df = self.toDataFrame()
        df.to_csv(save_path, index = None, header=True)
    def toDataFrame(self):
        csvDict = {
            'Link':list(self.links),
            'TimeStamp':self.dates,
            'Post Type':self.post_type,
            'View':self.views,
            'Like':self.likes,
            'Comment':self.comments,
            'Caption':self.captions
        }
        df = pd.DataFrame(csvDict,columns = ['Link','TimeStamp','Post Type','View','Like','Comment','Caption'])
        return df


FLAGS = flags.FLAGS
flags.DEFINE_list('user_info',['user','pass'],'Your instagram username "Username","Password"')
flags.DEFINE_string('webdriver','./msedgedriver.exe','Webdriver path')
flags.DEFINE_string('targetLink','https://www.instagram.com/explore/tags/playstation/','Webdriver path')
flags.DEFINE_integer('load_loop',1,'how far you going to load the Instagram feed')
flags.DEFINE_float('login_delay',3.0,'delay time of action when log in')
flags.DEFINE_float('load_delay',2.0,'delay time of action when load timeline')
flags.DEFINE_float('crawl_delay',0.5,'delay time when load instagram post')
flags.DEFINE_string('csv_path','instagram.csv','path for csv')



def main(argv):
    logging.get_absl_handler().setFormatter(None)
    logging.info('Interesting Stuff')
    scrap = InstagramScrapping(FLAGS.user_info,FLAGS.webdriver,FLAGS.targetLink,FLAGS.load_loop,FLAGS.login_delay,FLAGS.load_delay,FLAGS.crawl_delay)
    scrap.toCSV(FLAGS.csv_path)

if __name__ == '__main__':
    app.run(main)