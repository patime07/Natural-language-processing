from selenium import webdriver
import wikipedia
import time
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType
import regex as re
wd = webdriver.Chrome('chromedriver',options=chrome_options)
#setting language to darija
wikipedia.set_lang('ary')
wait = WebDriverWait(wd,1)
#get the link to the list of all article links webpage
wd.get('''https://ary.wikipedia.org/wiki/%D8%AE%D8%A7%D8%B5:%D9%83%D9%84_
       %D8%A7%D9%84%D8%B5%D9%81%D8%AD%D8%A7%D8%AA?from=&to=&namespace=0''')
i = 1
file = 1
article = 1
first = True
file_path = '/content/gdrive/MyDrive/wikipedia-darija/corpus_'+str(file)+'.txt'
#retrieve the first 5000 articles
while (articles <= 5000): 
  try:
    #get the path to the next link in the list
    path = '//*[@id="mw-content-text"]/div[3]/ul/li[' + str(i) +']/a'
    link = wd.find_element('xpath', path)
    #get the title of the article
    title = link.get_attribute('title')
    #retrieve the text of the article
    article = wikipedia.page(title)
    text = article.content 
    text = re.sub(r'==.*?==+', ' ', text)
    text = text.replace('\n', ' ')
    text += '\n'
    #store the article in a text file
    with open(file_path, 'a') as f: 
      f.write(text)
    article += 1
    i += 1
  except: 
    i += 1 
    pass
  try:
    #if all articles on this webpage were clicked, click on the next button
    if (i == 346): 
      if first == True: 
        nxt = wd.find_element('xpath','//*[@id="mw-content-text"]/div[4]/a').get_attribute('href')
        first = False
      else: 
        nxt = wd.find_element('xpath','//*[@id="mw-content-text"]/div[4]/a[2]').get_attribute('href')
      wd.get(nxt)
      i = 1
      file += 1
      file_path = '/content/gdrive/MyDrive/wikipedia-darija/corpus_'+str(file)+'.txt' 
  except:
    i += 1
    pass
