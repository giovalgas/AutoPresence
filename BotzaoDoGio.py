from selenium import webdriver
import time


PATH = "C:\Program Files (x86)\chromedriver.exe"

login_url = "https://ead.redesalvatoriana.org.br/login"

driver = webdriver.Chrome(PATH)

def login():
    driver.get(login_url)
    while checkLogin() == False:
        pass

    print("[INFO] - Logado!")
    findGroups()

def checkLogin():
    if driver.title.lower() != "dashboard - rede salvatoriana":
        return False
    else:
        return True

def findGroups():
    print("[INFO] - Tentando achar as aulas!")
    group_list = driver.find_element_by_class_name("lms-discipline-list")
    groups = group_list.find_elements_by_tag_name("li")

    i = 0
    for group in groups:
        s = group.text
        i += 1

    if i == 22:
        print("[INFO] - Achei todas as 22 aulas!")
        markPresence(groups, 0)
    else:
        print("[INFO] - Não achei as aulas :(")
        exit()

def markPresence(groups, index):
    url = groups[index].get_attribute("onclick").replace("window.location.href='", "").replace("'", "") + "#/resources"

    driver.get(url)

    time.sleep(2.5)

    c_div = driver.find_element_by_class_name("ng-scope")
    c_ul = c_div.find_elements_by_class_name("lms-discipline-list-card")

    #river.maximize_window()

    for i in range(len(c_ul)):

        time.sleep(2.5)

        c_div = driver.find_element_by_class_name("ng-scope")
        c_ul = c_div.find_elements_by_class_name("lms-discipline-list-card")

        ul = c_ul[i]

        c_li = ul.find_elements_by_class_name("collection-item.lms-discipline-resource")

        for j in range(len(c_li)):

            time.sleep(2.5)

            c_div = driver.find_element_by_class_name("ng-scope")
            c_ul = c_div.find_elements_by_class_name("lms-discipline-list-card")

            #print(str(len(c_ul))+ "::" + str(i))

            ul = c_ul[i]

            c_li = ul.find_elements_by_class_name("collection-item.lms-discipline-resource")

            li = c_li[j]

            #print(str(len(c_li)) + "::" + str(j))

            #print(li.text)

            driver.execute_script("arguments[0].click();", li)

            time.sleep(0.5)

            driver.get(url)

    print("[DONE] - " + url)

    driver.get("https://ead.redesalvatoriana.org.br/dashboard")

    time.sleep (2.5)

    group_list = driver.find_element_by_class_name("lms-discipline-list")
    groups = group_list.find_elements_by_tag_name("li")

    #print(str(len(groups)) + "::"+ str(index))

    if index + 1 <= 21:
        markPresence(groups, index + 1)
    else:
        driver.execute_script("alert('Acabou!');")


login()
