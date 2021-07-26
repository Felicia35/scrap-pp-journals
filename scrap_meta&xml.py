# Scrape Federal Register.ipynb
from selenium import webdriver
import chromedriver_autoinstaller
from selenium.common.exceptions import NoSuchElementException
import random
from time import sleep
import pandas as pd
import ssl

ssl._create_default_https_context = ssl._create_unverified_context
def init_driver():
    chromedriver_path = chromedriver_autoinstaller.install()
    chrome_driver = webdriver.Chrome(executable_path=chromedriver_path)
    chrome_driver.set_page_load_timeout(100)
    sleep(random.uniform(1.3, 3.5))
    return chrome_driver

keywords = ['Printed version:', 'Publication Date:', 'Agencies:', 'Agency:', 'CFR:', 'Dates:', 'Comments Close:', 'Document Type:', 'Document Citation:', 'Page:', 'Agency/Docket Number:', 'Document Number:']
dict_list = [] # final output with every param in one column

url_list = [] # a url for two years
year = 2022
while year > 1994:
    year_before = year - 2
    url = f"https://www.federalregister.gov/documents/search?conditions%5Bpublication_date%5D%5Bgte%5D=07%2F25%2F{year_before}&conditions%5Bpublication_date%5D%5Blte%5D=07%2F25%2F{year}&conditions%5Bterm%5D=social+equity"
    url_list.append(url)
    year -= 2

def scrap_data():

    for url in range(13, len(url_list)):
        scraped_data = []
        driver.get(url_list[url])

        file_count = driver.find_element_by_xpath('//*[@id="item-count"]').text # how many files in total in these 2 years
        page_count = int(int(file_count)/20 + 1) # how many pages in these 2 years

        for page in range(7, page_count + 1):
            for i in range(1, 21):
                dict = {}
                Agency = ''
                try:
                    link_to_paper = driver.find_element_by_xpath(f'//*[@id="main"]/div[3]/div/div/div/div/div[2]/div[2]/div/div/ul/li[{i}]/div/h5/a')
                    link_to_paper.click()
                    print(i)
                except NoSuchElementException:
                    print("error")
                    break

                ## store xml url
                strUrl = driver.current_url
                url_parts = strUrl.split('/')
                strXml = "https://www.federalregister.gov/documents/full_text/xml/" + url_parts[4] + '/' + url_parts[5] + '/' + url_parts[6] + '/' + url_parts[7] + '.xml'

                ## store name, agency and meta_dl in a list -- info
                info = []
                name = driver.find_element_by_xpath('//*[@id="metadata_content_area"]/h1').text
                info.append(name)
                try:
                    Agency = driver.find_element_by_xpath('//*[@id="p-1"]').text
                    info.append(Agency)
                except NoSuchElementException:
                    print("Agency not found in text")
                    info.append(" ")
                meta_dl = driver.find_element_by_xpath('//*[@id="main"]/div[4]/div/div/div[2]/div[1]/div[1]/div/div[2]/dl').text
                info.append(meta_dl)
                scraped_data.append(info)
                # print(info)

                # store detailed (columned:store in dict) data into a list of dict -- dict_list
                meta_list = meta_dl.split("\n")
                for term in range(len(meta_list)):
                    if meta_list[term - 2] == 'Agencies:':
                        dict[meta_list[term-2]] = (meta_list[term-1], meta_list[term])
                    if meta_list[term-1] in keywords:
                        dict[meta_list[term-1]] = meta_list[term]
                    else:
                        continue
                dict['name'] = name
                dict['Agency1'] = Agency
                dict['url'] = strXml
                dict_list.append(dict)

                # return to previous page with 20 papers
                driver.get(f'{url_list[url]}&page={page}')
                all_data = dict_list
                result = pd.DataFrame()
                for dict_idx in range(len(all_data)):
                    output = {'name': all_data[dict_idx].get('name'), 'Agency1': all_data[dict_idx].get('Agency1'),
                              'Printed version': all_data[dict_idx].get('Printed version'),
                              'Publication Date': all_data[dict_idx].get('Publication Date:'),
                              'Agencies': all_data[dict_idx].get('Agencies:'),
                              'CFR': all_data[dict_idx].get('CFR:'),
                              'Dates': all_data[dict_idx].get('Dates:'),
                              'Comments Close:': all_data[dict_idx].get('Comments Close:'),
                              'Document Type:': all_data[dict_idx].get('Document Type:'),
                              'Document Citation': all_data[dict_idx].get('Document Citation:'),
                              'Page': all_data[dict_idx].get('Page:'),
                              'Agency/Docket Number:': all_data[dict_idx].get('Agency/Docket Number:'),
                              'Document Number:': all_data[dict_idx].get('Document Number:'),
                              'url': all_data[dict_idx].get('url')
                              }
                    result = result.append(output, ignore_index=True)
                result.to_csv(f'./tables{url}/output{page}.csv', index=None, encoding='utf_8_sig')

    return dict_list


if __name__ == '__main__':
    driver = init_driver()
    sleep(1)
    all_data = scrap_data() # a list of dict


