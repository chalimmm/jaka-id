import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import re
import json

def set_chrome_options() -> Options:
    """Sets chrome options for Selenium.
    Chrome options for headless browser is enabled.
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_prefs = {}
    chrome_options.experimental_options["prefs"] = chrome_prefs
    chrome_prefs["profile.default_content_settings"] = {"images": 2}
    return chrome_options

if __name__ == "__main__":
    driver = webdriver.Chrome(options=set_chrome_options())
    driver.get("https://academic.ui.ac.id")
    u = os.getenv("USERNAME")
    p = os.getenv("PASSWORD")
    username = driver.find_element(By.NAME, "u")
    username.send_keys(u)
    password = driver.find_element(By.NAME, "p")
    password.send_keys(p)

    login = driver.find_element(By.CSS_SELECTOR, "input[value='Login']")
    login.click()
    
    element = driver.current_url
    if element == 'https://academic.ui.ac.id/main/Authentication/Index':
        print(json.dumps({}, indent=4))
        driver.close()
    else:
        driver.get("https://academic.ui.ac.id/main/Schedule/Index")
        page_source = driver.page_source
        
        driver.close()
        
        cuts = []
                
        for m in re.finditer('<table class="box">', page_source):
            cuts.append([m.start(), m.end()])

        iter = 0
        for m in re.finditer('</table>', page_source):
            cuts[iter][1] = m.end()
            iter += 1
            if iter >= len(cuts):
                break
        
        filtered_page = ""
        for i in range(len(cuts)):
            filtered_page += page_source[cuts[i][0]:cuts[i][1]]

        regexDay = '([A-Za-z]+, [0-9]+.[0-9]+-[0-9]+.[0-9]+)'

        soup = BeautifulSoup(filtered_page, 'html.parser')
        
        courses = soup.find_all("tr")

        elements = ""
        
        for course in courses:
            selected = course.find("th")
            if selected is not None:
                if ";" in selected.text:
                    elements += selected.text
                    elements += "--------------"
            selected = course.find_all("td", nowrap="")
            if len(selected) > 0:
                for element in selected:
                    elements += element.text + "\n"
                elements += "--------------"

        listElements = elements.split("--------------")
        courses = {}
        temp = ""

        for element in listElements:
            element = element.strip()
            if ";" in element and "-" not in element[:11]:
                temp = element[:11].strip()
                temp = temp.strip('\n')
                name = element[13:-28].strip()
                name = name.strip('\n')
                courses.update({
                    temp : {
                        'Nama' : name,
                        'Kelas' : []
                    }
                })
            elif temp != "":
                tempClass = element.split('\n')
                if (len(tempClass) > 1 and ';' in tempClass[1]):
                    break
                elif len(tempClass) > 6 :
                    courses[temp]['Kelas'].append({
                        'Nama' : tempClass[1],
                        'Jadwal' : re.findall(regexDay, tempClass[4]),
                        'Ruang' : tempClass[5].strip("-"), 
                        'Dosen' : tempClass[6].strip("- ").split("- ")
                    })
                elif len(tempClass) > 5 :
                    courses[temp]['Kelas'].append({
                        'Nama' : tempClass[1],
                        'Jadwal' : re.findall(regexDay, tempClass[4]),
                        'Ruang' : tempClass[5].strip("-"), 
                        'Dosen' : ''
                    })
                elif len(tempClass) > 4 :
                    courses[temp]['Kelas'].append({
                        'Nama' : tempClass[1],
                        'Jadwal' : re.findall(regexDay, tempClass[4]),
                        'Ruang' : '', 
                        'Dosen' : ''
                    })
                elif len(tempClass) > 3 :
                    courses[temp]['Kelas'].append({
                        'Nama' : tempClass[1],
                        'Jadwal' : '',
                        'Ruang' : '', 
                        'Dosen' : ''
                    })

        print(json.dumps(courses, indent=4))
