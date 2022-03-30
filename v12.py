from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import requests
import time

import urllib.request

def tabswitch(num):
    driver.switch_to.window(driver.window_handles[num])

def rest(sec):
    time.sleep(sec)
    
def scroll(num):
    driver.execute_script("window.scrollTo(0, '"+str(num)+"');")
    
def SelectOption(name):
    tabswitch(0)
    choice_str = ""
    try:
        elem = driver.find_element_by_xpath('//select[@name = "'+str(name)+'"]')
    except:
        #print(str(name)+" exception")
        return
    else:
        for choice in elem.find_elements_by_tag_name('option'):
            if choice.get_attribute('selected'):
                choice_str = choice.text
                #print(choice_str)
                break
        tabswitch(1)
        try:
            elem = driver.find_element_by_xpath('//select/option[@value = "'+str(choice_str)+'"]')
        except:
            #print(str(name)+" exception")
            return
        else:    
            elem.click()

def CopyContent(tagname):
    tabswitch(0)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    try:
        content = soup.find('input', {'name': tagname}).get('value')
        #print(content)
    except:
        #print(str(tagname)+" exception")
        return
    else:
        #print(content)
        tabswitch(1)
        try:
            elem = driver.find_element_by_name(tagname)
        except:
            #print(str(tagname)+" exception")
            return
        else:
            if(content != '0'):
                try:
                    elem.clear()
                except:
                    #print("elem.clear() + exception")
                    return
                else:
                    elem.send_keys(content)

def CopyContent0(tagname):
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    try:
        content = soup.find('input', {'name': tagname}).get('value')
        #print(content)
    except:
        #print(str(tagname)+" exception")
        return '0'
    else:
        return content   

def CopyContent1(tagname, content):
    try:
        elem = driver.find_element_by_name(tagname)
    except:
        #print(str(tagname)+" exception")
        return
    else:
        if(content != '0'):
            try:
                elem.clear()
            except:
                #print("elem.clear() + exception")
                return
            else:
                elem.send_keys(content)
    
ctg = {}
ctg['아파트'] = '0'
ctg['단독다가구'] = '1'
ctg['빌라연립다세대'] = '2'
ctg['원룸투룸쓰리룸'] = '3'
ctg['오피스텔'] = '4'
ctg['상가점포'] = '5'
ctg['상가주택'] = '6'
ctg['상가건물'] = '7'
ctg['숙박콘도펜션'] = '8'
ctg['전원농가주택'] = '9'
ctg['토지임야'] = '10'
ctg['빌딩'] = '11'
ctg['사무실']='12'
ctg['공장/창고'] = '13'
ctg['분양권'] = '14'
ctg['기타']='15'    

driver = webdriver.Chrome("C:/Users/user/chromedriver.exe")

#구글접속
driver.get("https://google.com/")

#오일장신문검색
#//*[@id="tsf"]/div[2]/div[1]/div[1]/div[1]/div/div[2]/input
#'//*[@id="tsf"]/div[2]/div[1]/div[1]/div/div[2]/input'
elem = driver.find_element_by_xpath('/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input')

#/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input
#/html/body/div[1]/div[3]/form/div[2]/div[1]/div[1]/div/div[2]/input
#//*[@id="tsf"]/div[2]/div[1]/div[1]/div/div[2]/input

elem.send_keys('http://www.jejuall.com')
#elem.send_keys('오일장신문')
elem.send_keys(Keys.RETURN)

rest(1)

#새탭으로 오일장신문열기
elem = driver.find_elements_by_partial_link_text('jejuall.com')
#elem = driver.find_elements_by_partial_link_text('오일장신문')
elem[0].send_keys(Keys.CONTROL + "\n")


#쉬기
rest(1)
#첫번째탭으로 전환 후 오일장신문열기
tabswitch(0)
elem = driver.find_element_by_partial_link_text('jejuall.com')
elem.send_keys('\n')

#대기(로그인, 매물관리클릭, 수정버튼, 매물등록, 매물종류선택)
input('준비완료[yes]')


#복사시작!!!!
copynum = 0;
while(1):
    ####################################동시진행 탭######################################
    driver.get(driver.current_url)

    #첫번째탭의 html을 soup에 넘기기
    tabswitch(0)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

#첫번째탭 매물종류복사
    kind = soup.select('.greybox')[0].text.strip()
    #print(kind)
#매물종류를 id값으로 변환
    kind_id = "cc0" + ctg[kind]
    #print(kind_id)

    tabswitch(1)
    elem = driver.find_element_by_id(kind_id)
    elem.click()
    
    #거래유형
    tabswitch(0)
    typenum = -1
    typechoices = driver.find_elements_by_name('typechoice')
    for typechoice in typechoices:
        typenum += 1
        if(typechoice.get_attribute('checked')):
            break
    scroll(350)
    tabswitch(1)
    elem = driver.find_elements_by_name('typechoice')
    elem[typenum].click()
    scroll(350)
    
    #주소 초성사용
    tabswitch(0)
    typenum = -1
    typedongs = driver.find_elements_by_name('typedong')
    for typedong in typedongs:
        typenum +=1
        if(typedong.get_attribute('checked')):
            break
    tabswitch(1)
    elem = driver.find_elements_by_name('typedong')
    elem[typenum].click()
    
    SelectOption('sido')
    SelectOption('dong')
    
    ####################################복사후 전체 한번에 입력#####################################
    
    ##첫탭
    tabswitch(0)
    roadFullAddr = CopyContent0('roadFullAddr')
    subject = CopyContent0('subject')
    
    ct_month_expenses = CopyContent0('ct_month_expenses') ####################################얘야!!얘가 문제야!!
    
    sup_area_m = CopyContent0('sup_area_m')
    dedi_area_m = CopyContent0('dedi_area_m')
    
    bns_sale_price = CopyContent0('bns_sale_price')
    #CopyContent1('bns_sale_price', bns_sale_price)
    #print("bns_sale_price: " +bns_sale_price)
    bns_loan = CopyContent0('bns_loan')
    
    movin_num = CopyContent0('movin_num')
    floor = CopyContent0('floor')
    
    completion = CopyContent0('completion')
    diection = CopyContent0('diection')
    ct_deposit_money = CopyContent0('ct_deposit_money')
    rt_down_payment = CopyContent0('rt_down_payment')
    rt_year_pay = CopyContent0('rt_year_pay')
    rt_month_pay = CopyContent0('rt_month_pay')
    rt_month_expenses = CopyContent0('rt_month_expenses')
    #ct_month_expenses = CopyContent0('ct_month_expenses')
    #print("ct_month_expenses: "+ct_month_expenses)
    
    households_num = CopyContent0('households_num')
    house_num = CopyContent0('house_num')
    room_num = CopyContent0('room_num')
    parking = CopyContent0('parking')
    movie_url = CopyContent0('movie_url')
    
    ##두번째탭
    tabswitch(1)
    CopyContent1('roadFullAddr', roadFullAddr)
    CopyContent1('subject', subject)
    
    #CopyContent1('ct_month_expenses', ct_month_expenses)
    CopyContent1('sup_area_m', sup_area_m)
    CopyContent1('dedi_area_m', dedi_area_m)
    
    CopyContent1('bns_sale_price', bns_sale_price)
    #rest(1)
    CopyContent1('bns_loan', bns_loan)
    
    CopyContent1('movin_num', movin_num)
    CopyContent1('floor', floor)
    
    SelectOption('completion_gubun')
    
    CopyContent1('completion', completion)
    CopyContent1('diection', diection)
    CopyContent1('ct_deposit_money', ct_deposit_money)
    CopyContent1('rt_down_payment', rt_down_payment)
    CopyContent1('rt_year_pay', rt_year_pay)
    CopyContent1('rt_month_pay', rt_month_pay)
    CopyContent1('rt_month_expenses', rt_month_expenses)
    
    CopyContent1('ct_month_expenses', ct_month_expenses)########################################이친구 문제야!!!!!
    
    CopyContent1('households_num', households_num)
    CopyContent1('house_num', house_num)
    CopyContent1('room_num', room_num)
    CopyContent1('parking', parking)
    CopyContent1('movie_url', movie_url)
    
    #지목, 용도지역
    SelectOption('room_num')
    SelectOption('diection')
    SelectOption('buil_type')
    SelectOption('buil_use')
    
   ############################관리자 메모 복사##############################
    tabswitch(0)
    
    lastTextsWithTag = []
    lastTextsWithTag = soup.find_all('textarea')
    lastText = ""
    lastText = lastTextsWithTag[1].get_text()
    #print(lastText)
    
    #관리자메모 붙여넣기!!!!!
    tabswitch(1)
    #driver.switch_to.frame(driver.find_element_by_tag_name('iframe'))
    #driver.switch_to.frame(driver.find_element_by_tag_name('iframe'))
    
    
    elem = driver.find_element_by_name('admin_info_content')
    elem.send_keys(lastText)
    
    copynum+=1

    print (copynum)
    

    close = input('close[y/n]')
    if(close == 'y' or close == 'ㅛ'):
        
        
    
        break
