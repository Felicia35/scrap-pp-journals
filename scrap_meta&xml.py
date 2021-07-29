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
url_list = [] # a url for two years
year = 2022
while year > 1994:
    year_before = year - 2
    url = f"https://www.federalregister.gov/documents/search?conditions%5Bpublication_date%5D%5Bgte%5D=07%2F25%2F{year_before}&conditions%5Bpublication_date%5D%5Blte%5D=07%2F25%2F{year}&conditions%5Bterm%5D=social+equity"
    url_list.append(url)
    year -= 2

def scrap_data():
    for url in range(0, len(url_list)):
        driver.get(url_list[url])

        file_count = driver.find_element_by_xpath('//*[@id="item-count"]').text # how many files in total in these 2 years
        page_count = int(int(file_count)/20 + 1) # how many pages in these 2 years

        for page in range(1, page_count + 1):
            driver.get(f'{url_list[url]}&page={page}')
            dict_list = []  # final output with every param in one column
            for i in range(1, 21):
                dict = {}
                Agency1 = ''
                Dated = ''
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

                ## try to find name, Agency1 and Dated in text
                try:
                    name = driver.find_element_by_xpath('//*[@id="metadata_content_area"]/h1').text
                    Agency1 = driver.find_element_by_id('p-1').text
                    # Agency1 = driver.find_element_by_css_selector('#p-1').text
                    Dated = driver.find_element_by_css_selector('p.signature-date').text
                except NoSuchElementException:
                    print("Dated not found in text")

                try:
                    # store detailed (columned:store in dict) data into a list of dict -- dict_list
                    meta_dl = driver.find_element_by_xpath('//*[@id="main"]/div[4]/div/div/div[2]/div[1]/div[1]/div/div[2]/dl').text
                    meta_list = meta_dl.split("\n")
                    for term in range(len(meta_list)):
                        if meta_list[term - 2] == 'Agencies:' and (meta_list[term] not in keywords):
                            dict['Agency:'] = (meta_list[term-1], meta_list[term])
                        if meta_list[term-1] in keywords:
                            dict[meta_list[term-1]] = meta_list[term]
                        else:
                            continue
                    dict['name'] = name
                    dict['Agency1'] = Agency1
                    dict['url'] = strXml
                    dict['Dated'] = Dated
                    dict_list.append(dict)

                    # return to previous page with 20 papers
                    driver.get(f'{url_list[url]}&page={page}')
                except:
                    continue

            all_data = dict_list
            result = pd.DataFrame()
            for dict_idx in range(len(all_data)):
                output = {'name': all_data[dict_idx].get('name'),
                          'Agencies': all_data[dict_idx].get('Agency:'),
                          'Dated': all_data[dict_idx].get('Dated'),
                          'Agency1': all_data[dict_idx].get('Agency1'),
                          'Printed version': all_data[dict_idx].get('Printed version'),
                          'Publication Date': all_data[dict_idx].get('Publication Date:'),
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
            result.to_csv(f'./tables/year{url}page{page}.csv', index=None, encoding='utf_8_sig')

    return dict_list


if __name__ == '__main__':
    driver = init_driver()
    sleep(1)
    all_data = scrap_data() # a list of dict





########################## merge ###############################
# import pandas as pd
# import glob
# import os


# csv_files = glob.glob(os.path.join('./tables', "*.csv"))
# li = []
# for file in csv_files:
#     tmp = pd.read_csv(file, index_col=None, header=None)
#     li.append(tmp)

# result = pd.concat(li, axis=0, ignore_index=True)
# result = result.drop_duplicates()
# result = result.reset_index(drop=True)
# result.to_csv(r'./result.csv', encoding='utf_8_sig')

########################## download xml ###############################
# import pandas as pd
# import requests

# input = pd.read_csv('result.csv')

# url_list = input['url']
# url_list = list(url_list)

# for idx in range(127,len(url_list)):
#     print(idx+1)
#     print(url_list[idx])
#     response = requests.get(url_list[idx])
#     with open(f'./xmls/{idx+1}.xml', 'wb') as file:
#         file.write(response.content)
