import openpyxl, math, time
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from openpyxl import Workbook
from openpyxl.utils import get_column_letter
from openpyxl.styles import Alignment
user = input('Please enter your Linkedin username\n\t ==>')
passw = input('Please enter your Linkedin password\n\t ==>')
query = input('Please enter the attribute of the Yale alumni that you are looking for\n\t ==>')
before = time.time()
driver = webdriver.Chrome("C:\Code\chromedriver\chromedriver")
linkedinurl = 'https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin'
driver.get(linkedinurl)
loginuser = driver.find_element_by_id('username')
loginuser.send_keys(user)
loginpass =  driver.find_element_by_id('password')
loginpass.send_keys(passw)
loginbutton = driver.find_element_by_class_name('login__form_action_container ')
loginbutton.click()
ldinsearch = driver.find_element_by_class_name('search-global-typeahead__input')
ldinsearch.send_keys("Yale University")
searchbutton = driver.find_element_by_class_name('search-global-typeahead__controls')
searchbutton.click()
driver.get('https://www.linkedin.com/school/yale-university/people/')
searchbox =  driver.find_element_by_id('people-search-keywords')
searchbox.send_keys("startup",Keys.ENTER)
i =0
end = 2000
top =0
t = str(top)
r = str(end)
scroller = ("window.scrollTo("+t+","+r+")")
driver.execute_script(scroller)
while(i<20):
    t = str(top)
    r = str(end)
    scroller = ("window.scrollTo("+t+","+r+")")
    time.sleep(2)
    driver.execute_script(scroller)
    top+=2000
    end+=2000
    i+=1
time.sleep(5)
elements = driver.find_elements_by_xpath("//a[contains(@href, '/in/')]")
namelist =[e.text.strip() for e in elements if e.text.strip() != '']
urls = driver.find_elements_by_tag_name("a")
urlist = [u.get_attribute("href") for u in urls if '/in/' in u.get_attribute("href")]
for u in urlist:
    if(urlist.count(u)==2):
        urlist.remove(u)
namesandurls = dict(zip(namelist,urlist))
from openpyxl import workbook
comp =[]
titles =[]
for person in urlist:
    p = driver.get(person)
    time.sleep(3)
    currpix = nxt = 0
    while(nxt<=2000):
        curp = str(currpix)
        nx = str(nxt)
        exp = ''
        driver.execute_script("window.scrollTo("+curp+","+nx+")")
        nxt+=200
        if(nxt>200):
            currpix+=200
        time.sleep(1)
        job_title = driver.find_elements_by_css_selector('#experience-section .pv-profile-section')
        if(len(job_title)!=0):
            for tit in job_title:
                exp = tit.text
                exp.replace("\n\n",'')
                exp += '\n'
            titles.append(exp)
            exp = ''
            break
        if(len(job_title)==0 and nxt ==2000):
            titles.append('')
    time.sleep(2)
wb = Workbook()
Everyone = wb.active
Everyone.title= 'Everyone'
Everyone['A1'] = 'Names'
Everyone['B1'] = 'Work Experience'
Everyone['C1'] = 'URLs'
for i in range(len(namelist)):
    adex = ('A'+str((i+2)))
    bdex = ('B'+str((i+2)))
    cdex = ('C'+str((i+2)))
    Everyone[adex] = namelist[i]
    Everyone[bdex].alignment = Alignment(wrapText=True) 
    Everyone[bdex] = titles[i]
    Everyone[cdex] = urlist[i]
sectors = ['Fintech','Biotech','Environmental','Tech']
wb.save('C:\linkedsl.xlsx')
driver.close()
after = time.time()
runtime = after - before
print('Number of Profiles assessed => ',len(namelist))
print('Program Runtime => ',runtime,' seconds.')
