from selenium import webdriver
import chromedriver_autoinstaller
from selenium.webdriver.support.ui import Select
import random
from time import sleep
import csv
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

# journals = ['Public Administration Review',
#              'Public Management Review',
#              'Journal Of Public Administration Research And Theory',
#              'Public Administration',
#              'The American Review of Public Administration',
#              'Governance',
#              'VOLUNTAS: International Journal of Voluntary and Nonprofit Organizations',
#              'Science and Public Policy',
#              'Environment and Planning C: Government and Policy',
#              'International Review of Administrative Sciences',
#              'Policy Studies Journal',
#              'Administration & Society',
#              'Policy Sciences',
#              'International Journal of Public Administration',
#              'Social Policy & Administration',
#              'Local Government Studies',
#              'Review of Public Personnel Administration',
#              'Policy & Politics',
#              'International Public Management Journal',
#              'Policy and Society']



# journals = ['Policy Sciences']
journals = ['International Journal of Public Administration']
# journals = ['Social Policy & Administration']
# journals = ['Local Government Studies']
# journals = ['Review of Public Personnel Administration']
# journals = ['Policy & Politic']
# journals = ['International Public Management Journal']
# journals = ['Policy and Society']


def init_driver():
    chromedriver_path = chromedriver_autoinstaller.install()
    chrome_driver = webdriver.Chrome(executable_path=chromedriver_path)
    chrome_driver.set_page_load_timeout(100) ## for DOM to load completely
    sleep(random.uniform(1.3, 3.5))
    return chrome_driver


def scrap_data():
    scraped_data = []

    for journal in journals:
        print(journal)
        input_box = driver.find_element_by_xpath('//*[@id="value(input1)"]')
        input_box.clear()
        input_box.send_keys(journal)

        select = Select(driver.find_element_by_xpath('//*[@id="select1"]'))
        select.select_by_index(3) ## publication name

        timespan = Select(driver.find_element_by_xpath('//*[@id="timespan"]/div[2]/div/select'))
        timespan.select_by_index(6)
        start = Select(driver.find_element_by_xpath('//*[@id="timespan"]/div[3]/div/select[1]'))
        start.select_by_index(8) ##1978
        end = Select(driver.find_element_by_xpath('//*[@id="timespan"]/div[3]/div/select[2]'))
        end.select_by_index(0) ##2021

        submit_button = driver.find_element_by_xpath('//*[@id="searchCell1"]/span[1]/button')
        driver.implicitly_wait(5)
        submit_button.click()
        sleep(3)

        items_per_page = Select(driver.find_element_by_xpath('//*[@id="selectPageSize_bottom"]'))
        items_per_page.select_by_index(2) ## 50 per page
        sleep(5)


        select_page = driver.find_element_by_xpath('//*[@id="SelectPageChkId"]')
        select_page.click()

        export = driver.find_element_by_xpath('//*[@id="exportTypeName"]')
        export.click()

        excel = driver.find_element_by_xpath('//*[@id="saveToMenu"]/li[3]')
        excel.click()

        all_records = driver.find_element_by_xpath('//*[@id="numberOfRecordsAllOnPage"]')
        all_records.click()

        content = Select(driver.find_element_by_xpath('//*[@id="bib_fields"]'))
        content.select_by_index(0)## author, title and source

        submit = driver.find_element_by_xpath('//*[@id="page"]/div[11]/div[2]/form/div[3]/span/button')
        submit.click()

        pages = driver.find_element_by_xpath('//*[@id="pageCount.top"]').text
        print(pages)

        for i in range(2, int(pages)+1):
            driver.get(f'https://apps.webofknowledge.com/summary.do?product=WOS&parentProduct=WOS&search_mode=GeneralSearch&parentQid=&qid=1&SID=F6tFcvErHKPkFRUITfV&&update_back2search_link_param=yes&page={i}')

            select_page = driver.find_element_by_xpath('//*[@id="SelectPageChkId"]')
            select_page.click()

            export = driver.find_element_by_xpath('//*[@id="exportTypeName"]')
            export.click()
            #
            # all_records = driver.find_element_by_xpath('//*[@id="numberOfRecordsAllOnPage"]')
            # all_records.click()

            content = Select(driver.find_element_by_xpath('//*[@id="bib_fields"]'))
            content.select_by_index(0) ## author, title and source

            submit = driver.find_element_by_xpath('//*[@id="page"]/div[11]/div[2]/form/div[3]/span/button')
            submit.click()

    return scraped_data


def output_data(op_format, data):
    # csv
    if op_format == 'c' or op_format == 'csv':
        with open('output/out.csv', 'w') as out:
            csv_out = csv.writer(out)
            csv_out.writerow(['date', 'AOI', 'level', 'PM2', 'PM10', 'SO2', 'CO', 'NO2', 'O3_8h'])
            csv_out.writerows(data)
    else:
        print("Not yet supported XD")


if __name__ == '__main__':
    driver = init_driver()
    driver.get('https://apps.webofknowledge.com/WOS_GeneralSearch_input.do?product=WOS&search_mode=GeneralSearch&SID=E13hTlRvi9oqxOXBkT9&preferencesSaved=')
    sleep(random.uniform(3.5, 5.2))

    all_data = scrap_data()










