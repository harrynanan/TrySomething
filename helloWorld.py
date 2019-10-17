# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup as bs
import csv
import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

class ZhaoPin(object):
    def __init__(self):
        self.headers = {
            'cookie': 'x-zp-client-id=07915a73-6d69-4421-b080-6c3c5902ee89; sts_deviceid=16d14afec92a5c-0abc9dd29d06b6-38607501-1024000-16d14afec93aaa; dywez=95841923.1568010137.1.1.dywecsr=crossincode.com|dyweccn=(referral)|dywecmd=referral|dywectr=undefined|dywecct=/vip/homework/30/; __utmz=269921210.1568010137.1.1.utmcsr=crossincode.com|utmccn=(referral)|utmcmd=referral|utmcct=/vip/homework/30/; sou_experiment=unexperiment; LastCity=%E4%B8%8A%E6%B5%B7; LastCity%5Fid=538; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2216d14afec71162-005ea949b9f9c7-38607501-1024000-16d14afec72dcf%22%2C%22%24device_id%22%3A%2216d14afec71162-005ea949b9f9c7-38607501-1024000-16d14afec72dcf%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; acw_tc=2760825315680163482563694ecc959ad977f05731a4c8fe526a83d765b9ff; urlfrom=121126445; urlfrom2=121126445; adfcid=none; adfcid2=none; adfbid=0; adfbid2=0; __utmc=269921210; dywec=95841923; Hm_lvt_38ba284938d5eddca645bb5e02a02006=1568010137,1568279406; sts_sg=1; sts_chnlsid=Unknown; jobRiskWarning=true; zp_src_url=https%3A%2F%2Fwww.zhaopin.com%2F; dywea=95841923.4476522639623480300.1568010137.1568279406.1568616229.3; dyweb=95841923.1.10.1568616229; sts_sid=16d38d02946e4-0de99ceb4afb99-38607501-1024000-16d38d029479a5; __utma=269921210.825936641.1568010137.1568279406.1568616229.3; __utmt=1; __utmb=269921210.1.10.1568616229; ZP_OLD_FLAG=false; POSSPORTLOGIN=3; CANCELALL=0; Hm_lpvt_38ba284938d5eddca645bb5e02a02006=1568616234; acw_sc__v2=5d7f2f2fb7624082fab6a23fe97a742c93533767; ZL_REPORT_GLOBAL={%22sou%22:{%22actionid%22:%220dd98146-68cc-4482-9c74-9041259cab14-sou%22%2C%22funczone%22:%22smart_matching%22}%2C%22jobs%22:{%22recommandActionidShare%22:%22778bc1ef-67ba-4359-a4ce-4b3a312d4d53-job%22%2C%22funczoneShare%22:%22dtl_best_for_you%22}}; sts_evtseq=6',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
        }
        self.csvHeader = ['jobName', 'salary', 'degree', 'workExperience','JD_url', 'partTime', 'CompanyName', 'CompanyType', 'CompanySize','description']
        self.getContent = []

    def get_url(self,url):
        try:
            get_json = requests.get(url)
            if get_json.status_code == 200:
                return get_json.json()
            else:
                print('server failed')
                return False
        except Exception as e:
            print(e)
            return False
    def get_jd(self,url):
        try:
            get_web = requests.get(url,headers=self.headers)
            if get_web.status_code == 200:
                return get_web.text
            else:
                print('server failed')
                return False
        except:
            print('request Error')
            return False

    def get_info(self,job_json):
        results = job_json['data']['results']
        for info in results:
            job_info={
                'jobName':info['jobName'],
                'salary':info['salary'],
                'degree':info['eduLevel']['name'],
                'workExperience':info['workingExp']['name'],
                'JD_url':info['positionURL'],
                'partTime':info['emplType'],
                'CompanyName':info['company']['name'],
                'CompanyType':info['company']['type']['name'],
                'CompanySize':info['company']['size']['name']
            }
            path = '/Users/xmly/downloads/chromedriver'
            chrome_options = webdriver.ChromeOptions()
            # 使用headless无界面浏览器模式
            chrome_options.add_argument('--headless')  # 增加无界面选项
            chrome_options.add_argument('--disable-gpu')  # 如果不加这个选项，有时定位会出现问题
            browser = webdriver.Chrome(executable_path=path, options=chrome_options)
            browser.get(info['positionURL'])
            time.sleep(4)
            try:
                target = browser.find_element_by_class_name('describtion__detail-content').get_attribute('innerHTML')
                pre = re.compile('>(.*?)<')
                s1 = ''.join(pre.findall(target))
                job_info['description']=s1
                browser.quit()
            except Exception as e:
                job_info['description']='失败了'
                print(e)
                browser.quit()
            self.getContent.append(job_info)

        return self.getContent

    def save_csv(self):
        try:
            with open(r'/Users/xmly/desktop/ZhaoPin.csv', 'w', newline='') as f:
               f_csv = csv.DictWriter(f, self.csvHeader)
               f_csv.writeheader()
               #print(self.getcontent)
               f_csv.writerows(self.getContent)
        except:
            print('Save Error!')

if __name__ == '__main__':
    ZP = ZhaoPin()
    url = 'https://fe-api.zhaopin.com/c/i/sou?start=90&pageSize=90&cityId=538&salary=0,0&workExperience=-1&education=-1&companyType=-1&employmentType=-1&jobWelfareTag=-1&kw=python&kt=3'
    try:
        ZP.get_info(ZP.get_url(url))
        ZP.save_csv()
        print('获取成功，文件已保存')
    except Exception as e:
        print(e)
