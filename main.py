# Instagram get followers and following
#
# SeveruS 8/26/2021

from selenium import webdriver
import time
import pandas as pd
import os

def getFollowers(driver):
    liste=[]
    driver.find_element_by_partial_link_text("follower").click()
    time.sleep(2)
    fBody = driver.find_element_by_xpath("//div[@class='isgrP']")
    scroll = 0
    while scroll < 23:
        driver.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight+1000;', fBody)
        time.sleep(1)
        scroll += 1
    time.sleep(1)
    takipciler = driver.find_elements_by_css_selector(".FPmhX.notranslate._0imsa")
    sayac = 0
    for takipci in takipciler:
        sayac += 1
        #print(takipci.text)
        liste.append(takipci.text)

    return  liste

def getFollowing(driver):
    liste = []
    driver.find_element_by_partial_link_text("following").click()
    time.sleep(2)
    fBody = driver.find_element_by_xpath("//div[@class='isgrP']")
    scroll = 0
    while scroll < 23:
        driver.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight+1000;',fBody)
        time.sleep(1)
        scroll += 1
    time.sleep(1)
    takipler = driver.find_elements_by_css_selector(".FPmhX.notranslate._0imsa")
    sayac = 0
    for takip in takipler:
        sayac += 1
        #print(takip.text)
        liste.append(takip.text)

    return liste

def login(driver):
    user = ""
    userpassword = ""
    driver.get("https://www.instagram.com/")
    time.sleep(2)
    name = driver.find_element_by_name("username")
    password = driver.find_element_by_name("password")
    name.clear()
    name.send_keys(user)
    password.clear()
    password.send_keys(userpassword)
    driver.find_element_by_xpath("//form[@class='HmktE']/div[1]/div[3]/button").click()
    time.sleep(5)
    driver.get("https://www.instagram.com/"+user)
    time.sleep(2)

def unfolloowers(followers,following):
    haric = []
    for i in following:
        if not i in followers:
            haric.append(i)
            # print(i)
    return haric

def save(followers,following,vs,chl):
    wers = pd.DataFrame({'Names': followers})
    wing= pd.DataFrame({"Names":following})
    vss = pd.DataFrame({"Names": vs})
    chll = pd.DataFrame({"Names": chl})
    income_sheets = {'followers': wers, 'following': wing,'not':vss,'chance':chll}
    writer = pd.ExcelWriter('./inst.xlsx')

    for sheet_name in income_sheets.keys():
        income_sheets[sheet_name].to_excel(writer, sheet_name=sheet_name, index=False)

    writer.save()

def save1(followers,following,vs):   #first run
    wers = pd.DataFrame({'Names': followers})
    wing= pd.DataFrame({"Names":following})
    vss = pd.DataFrame({"Names": vs})
    chll = pd.DataFrame({"Names": []})
    income_sheets = {'followers': wers, 'following': wing,'not':vss,'chance':chll}
    writer = pd.ExcelWriter('./inst.xlsx')

    for sheet_name in income_sheets.keys():
        income_sheets[sheet_name].to_excel(writer, sheet_name=sheet_name, index=False)

    writer.save()

def readOldData():
    getFoll = pd.read_excel('./inst.xlsx', sheet_name='followers')
    s=[]
    for m in getFoll["Names"]:
        s.append(m)
    print(type(s))
    # a = getFoll.head()
    # b = a["Names"].to_list()
    # print(b)
    # print("b")
    return s

def chance(followers):
    today = pd.to_datetime("today")
    chlist=[]
    old = readOldData()
    print(type(old))
    if old!=0:
        gete = pd.read_excel('./inst.xlsx', sheet_name='chance')
        if len(gete)!=0:
            print(gete)
            for j in gete:
                chlist.append(j)

        for i in followers:
            if i not in old:
                dict = {"name": i,
                        "status":"New",
                       "time": today}
                chlist.append(dict)
                print(dict)
        print("----------------")
        # for i in old:
        #     if i not in followers:
        #         dict = {"name": i,
        #                 "status": "Missing",
        #                "time": today}
        #         chlist.append(dict)
        #         print(dict)
        return chlist

driver = webdriver.Chrome()
login(driver)

followers = getFollowers(driver)
print(len(followers))
driver.execute_script("window.history.go(-1)")

following=getFollowing(driver)
print(len(following))

vs=unfolloowers(followers,following)
print(len(vs))
if os.path.isfile('./inst.xlsx'):

    chl=chance(followers)
    print(len(chl))
    if len(chl)==0:
        save1(followers, following, vs)
    else:
        save(followers, following, vs, chl)

else:
    save1(followers, following, vs)



