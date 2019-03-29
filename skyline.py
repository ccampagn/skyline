import time
import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import smtplib
import configparser
import sys

config = configparser.RawConfigParser()#load config parser
configFilePath = r'C:\Users\ccampagn\Documents\Python\skyline\config.ini'#file path of config file
config.read(configFilePath)#read config file

try:#try/except block
    browser = config.get('file', 'browser')#get browser from file
    website = config.get('file', 'website')#get website from file
    textfile = config.get('file', 'textfile')#get textfile from file
    fromaddr = config.get('file', 'from')#get fromaddress from file
    toaddrs = config.get('file', 'to')#get toaddress from file
    username = config.get('file', 'username')#get username from file
    password = config.get('file', 'password')#get password from file
    mailserver = config.get('file', 'mailserver')#get mailserver from file
except configparser.NoOptionError :#except with no options error
    print('could not read configuration file')#Error message if can't read 
    sys.exit(1)  #exit program on error

try:#try/except block
     browser = webdriver.Firefox(executable_path=browser)#load webdriver
     browser.get(website)#go to the website
     time.sleep(5)#sleep to give website time to load 
except Exception as e:
    file_obj = open(textfile,"a") #open text file
    file_obj.write(str(datetime.datetime.now())+str(e)+" browser\n") #write to text file about browser error
    file_obj.close()#close text file
    sys.exit(1) #exit program
try:#try/except block
    content = browser.find_element_by_class_name("ui-dialog-buttonset")#get content
    content.click()#click on content
    time.sleep(5)#sleep to give website time to load 
except Exception as e:
    file_obj = open(textfile,"a") #open text file
    file_obj.write(str(datetime.datetime.now())+str(e)+" popup\n") #error for closing text file
    file_obj.close()#close text file
    sys.exit(1) #exit program
try:#try/except block
    restype = browser.find_element_by_id('selResType')#get element for backcountry site
    restype.send_keys('Backcountry camping')#set type to backcountry camping
    time.sleep(5)#sleep to give website time to load 
except Exception as e:
    file_obj = open(textfile,"a") #open text file
    file_obj.write(str(datetime.datetime.now())+str(e)+" restype\n") #write error to textfile for restype
    file_obj.close()#close text file
    sys.exit(1) #exit program
try:#try/except block
    resmonth = browser.find_element_by_id('selArrMth')#get element to select date
    resmonth.send_keys(Keys.ENTER)#press enter keys
    time.sleep(5)#sleep to give website time to load 
    for _ in range(datetime.datetime.now().month,8):#loop thru to get right month
        resmonth.send_keys(Keys.DOWN)#press down key 
        time.sleep(5)#sleep to give website time to load
    resmonth.send_keys(Keys.ENTER)#press enter key
    time.sleep(5)#sleep to give website time to load 
    resday = browser.find_element_by_id('selArrDay')#get element to select date
    resday.send_keys(Keys.ENTER)#press enter key
    time.sleep(5)#sleep to give website time to load 
    for _ in range(15):#loop thru to get right date
        resday.send_keys(Keys.DOWN)#press down keys
        time.sleep(5)#sleep to give website time to load 
    resday.send_keys(Keys.ENTER)#press enter key
    time.sleep(5)#sleep to give website time to load 
except Exception as e:
    file_obj = open(textfile,"a") #open text file
    file_obj.write(str(datetime.datetime.now())+str(e)+" select month day\n") #write to text file for error with month day
    file_obj.close()#close the text file
    sys.exit(1) #exit program
try:#try/except block
    restentpad = browser.find_element_by_id('selPartySize')#get element for party size
    restentpad.send_keys('1')#set party size
    time.sleep(5)#sleep to give website time to load 
    restentpad = browser.find_element_by_id('selTentPads')#get element for tents pads
    restentpad.send_keys('1')#tents pads needed
    time.sleep(5)#sleep to give website time to load 
    content = browser.find_element_by_id('selItineraryResource')#get element for what available
    content = content.find_elements_by_class_name('avail')
except Exception as e:
    file_obj = open(textfile,"a") #open text file
    file_obj.write(str(datetime.datetime.now())+str(e)+" select party tent\n") #write error to text file for party tent
    file_obj.close()#close the text file
    sys.exit(1) #exit program
try:#try/except block
    match=False#set match to false
    msg =""
    for x in content:#loop thru the content that was return 
        text=x.text.split(' - ')[1]
        if text=="Snowbowl" or text=="Curator" or text=="Tekarra" or text=="Signal" or text=="Watchtower" :#check if any available is number 30
            msg=msg +text+" "#msg to sent as text               
            match=True#set match to true
    if match:
        server = smtplib.SMTP(mailserver)#setup mailserver
        server.ehlo()#letting other server know
        server.starttls()#start szecure connection
        server.login(username,password)#login with username and password for config file
        server.sendmail(fromaddr, toaddrs, msg)#sent email
        server.quit()#exit server 
        file_obj = open(textfile,"a") #open text file
        file_obj.write(str(datetime.datetime.now())+" "+msg+" - Available\n") #write it is available
        file_obj.close()#close text file
    else:
        file_obj = open(textfile,"a") #open text file
        file_obj.write(str(datetime.datetime.now())+" - None\n") #write available is none
        file_obj.close()#close text file
except Exception as e:
    file_obj = open(textfile,"a") #open text file
    file_obj.write(str(datetime.datetime.now())+str(e)+" txt\n") #write error for text file part
    file_obj.close()#close text file
    sys.exit(1) #exit program
