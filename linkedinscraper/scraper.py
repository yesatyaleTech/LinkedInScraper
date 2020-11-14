from .person import Person
from typing import List
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import time

class LinkedInScraper:

    def __init__(self, username: str, password: str, query: str, school: str, driverpath: str):
        self.username: str  = username
        self.password: str  = password
        self.query: str  = query
        self.school: str =  school
        self.browserdriver = webdriver.Chrome(driverpath)
        self.people = List[Person]
        self.login()

    def login(self):
        linkedinurl = 'https://www.linkedin.com/login'
        self.browserdriver.get(linkedinurl)
        loginuser = self.browserdriver.find_element_by_id('username')
        loginuser.send_keys(self.username)
        loginpass =  self.browserdriver.find_element_by_id('password')
        loginpass.send_keys(self.password)
        loginbutton = self.browserdriver.find_element_by_class_name('login__form_action_container ')
        loginbutton.click()
    
    def gotoschool(self):
        self.browserdriver.get('https://www.linkedin.com/school/'+self.school+'/people/')
        time.sleep(3)
    
    def search_people(self):
        searchbox = self.browserdriver.find_element_by_id('people-search-keywords')
        searchbox.send_keys(self.query,Keys.ENTER)
        time.sleep(3)

    def get_names_and_urls(self):
        i =0
        end = 2000
        top =0
        t = str(top)
        r = str(end)
        scroller = ("window.scrollTo("+t+","+r+")")
        self.browserdriver.execute_script(scroller)
        while(i<20):
            t = str(top)
            r = str(end)
            scroller = ("window.scrollTo("+t+","+r+")")
            time.sleep(2)
            self.browserdriver.execute_script(scroller)
            top+=2000
            end+=2000
            i+=1
        time.sleep(5)
        elements = self.browserdriver.find_elements_by_xpath("//a[contains(@href, '/in/')]")
        namelist =[e.text.strip() for e in elements if e.text.strip() != '']
        urls = self.browserdriver.find_elements_by_tag_name("a")
        urlist = [u.get_attribute("href") for u in urls if '/in/' in u.get_attribute("href")]
        for u in urlist:
            if(urlist.count(u)==2):
                urlist.remove(u)
        for i in range(len(urlist)):
            self.people.append(Person(namelist[i],urlist[i]))
    
    def add_additional_info(self):
        for person in self.people:
            self.browserdriver.get(person.url)
            time.sleep(3)
            currpix = nxt = 0
            while(nxt<=2000):
                curp = str(currpix)
                nx = str(nxt)
                exp = ''
                self.browserdriver.execute_script("window.scrollTo("+curp+","+nx+")")
                nxt+=200
                if(nxt>200):
                    currpix+=200
                time.sleep(1)
                job_title = self.browserdriver.find_elements_by_css_selector('#experience-section .pv-profile-section')
                if(len(job_title)!=0):
                    for tit in job_title:
                        exp = tit.text
                        exp.replace("\n\n",'')
                        exp += '\n'
                    person.add_jobhistory(exp)
                    exp = ''
                    break
                if(len(job_title)==0 and nxt ==2000):
                    person.add_jobhistory('')
            time.sleep(2)
            self.browserdriver.get(person+"detail/contact-info/")
            time.sleep(3)
            contacts = self.browserdriver.find_elements_by_tag_name('a')
            contlist = [c.get_attribute("href") for c in contacts]
            for c in contlist:
                person.add_contactinfo(c)
