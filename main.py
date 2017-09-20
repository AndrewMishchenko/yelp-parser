import multiprocessing
import os
import time

import xlwt
from selenium import webdriver

d_path = os.getcwd() + '/chromedriver'

domain = 'https://www.yelp.com/search?find_desc=' \
         'Movers&find_loc=San+Francisco%2C+CA&ns=1'


def page_data(href): # gets page data
    driver = webdriver.Chrome(executable_path=d_path)
    driver.get(href)
    time.sleep(3)

    try:
        url = driver.current_url
    except Exception:
        url = ''

    try:
        company_name = driver.find_element_by_css_selector(
            'h1.biz-page-title').text.strip()
    except Exception:
        company_name = ''

    try:
        website_url = driver.find_element_by_css_selector(
            'span.biz-website > a').get_attribute('href')
        website_url = website_url.split('biz_redir?url=')[1].split(
            '%3A%2F%2F')[1].split('&')[0].split('%')[0]
    except Exception:
        website_url = ''

    try:
        rating = driver.find_element_by_css_selector(
            '.i-stars').get_attribute('title').split(' ')[0]
    except Exception:
        rating = ''

    try:
        city_and_state = driver.find_element_by_css_selector(
            'address').get_attribute('innerText').strip().replace('\n', ' ')
    except Exception:
        city_and_state = ''

    try:
        phone = driver.find_element_by_css_selector(
            'span.biz-phone').text.strip().replace('\n', ' ')
    except Exception:
        phone = ''

    lock.acquire()
    with open('result.txt', 'a') as doc:
        doc.write('{}|{}|{}|{}|{}|{} \n'.format(company_name,
                                                url,
                                                website_url,
                                                rating,
                                                city_and_state,
                                                phone
                                                )
                  )
    lock.release()

    driver.close()
    return


def parse_links(): # gets all links from search result
    driver = webdriver.Chrome(executable_path=d_path)
    driver.get(domain)
    next_page = True
    while next_page:
        try:
            hrefs = [href.get_attribute('href') for href in
                     driver.find_elements_by_css_selector(
                         'h3.search-result-title a.biz-name')
                     ]
            for href in hrefs:
                with open('hrefs.txt', 'a') as doc:
                    doc.write(href + '\n')
            driver.find_element_by_css_selector('a.next').click()
            time.sleep(1)

        except Exception as err:
            print(err)
            next_page = False
            print('Done!')
    driver.close()


def get_saved_links(): # gets all saved links
    with open('hrefs.txt', 'r') as doc:
        return [href.replace('\n', '') for href in doc]


def write_xls():
    index = 0
    n = "HYPERLINK"

    # style
    font0 = xlwt.Font()
    font0.bold = True
    style = xlwt.XFStyle()
    style.font = font0

    doc_w = xlwt.Workbook()

    # write headers
    sheet = doc_w.add_sheet('sheet1')
    sheet_row = sheet.row(index)
    sheet_row.write(0, 'company_name', style)
    sheet_row.write(1, 'url', style)
    sheet_row.write(2, 'website_url', style)
    sheet_row.write(3, 'rating', style)
    sheet_row.write(4, 'city_and_state', style)
    sheet_row.write(5, 'phone', style)
    index += 1

    with open('result.txt', 'r') as doc:
        for string in doc:
            string = string.replace('\n', '').split('|')

            sheet_row = sheet.row(index)
            sheet_row.write(0, string[0])
            sheet_row.write(1, xlwt.Formula(
                n + '("{0}";"{0}")'.format(string[1])))
            sheet_row.write(2, string[2])
            sheet_row.write(3, string[3])
            sheet_row.write(4, string[4])
            sheet_row.write(5, string[5])
            doc_w.save('result.xls')
            index += 1


def init(l): # init for multiprocessing
    global lock
    lock = l


if __name__ == '__main__':
    parse_links() # save all links to companies

    hrefs = get_saved_links()

    l = multiprocessing.Lock()
    pool = multiprocessing.Pool(initializer=init, initargs=(l,))
    pool.map(page_data, hrefs)
    pool.close()
    pool.join()
    write_xls() # save into xls
