from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time
import csv
import os
from multiprocessing import Pool
from functools import partial
from odds_portal_scraper.logs.loggers import app_logger
from tqdm import tqdm


def chunk(list_, size):
    result = []
    chunk = []
    for elem in list_:
        if len(chunk) == size:
            result.append(chunk)
            chunk = []
        chunk.append(elem)
    result.append(chunk)
    return result


def write_text_file(text, filename):
    with open(filename, 'a') as f:
        f.write(f'{text}, ')


def get_driver(headless=True):
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920x1080")
    chromedriver_path = './chromedriver'
    driver = webdriver.Chrome(options=chrome_options,
                              executable_path=chromedriver_path)
    return driver


def write_csv(filename, data, order):
    with open(filename, 'a') as file:
        writer = csv.DictWriter(file, fieldnames=order)
        is_empty = os.stat(filename).st_size == 0
        if is_empty:
            writer.writeheader()
        writer.writerow(data)


def extract_info(info):
    return {
        'date': '{} {}'.format(info[0], info[1][:-1]),
        'odds': float(info[3])
    }


def get_hide_info(elem, driver, type_, url):
    ActionChains(driver).move_to_element(elem).perform()
    span = driver.find_element_by_css_selector('#tooltiptext')
    info = span.get_attribute('innerText').split('\n')
    try:
        close_odds = float(info[0].split(' ')[3])
        open_odds = float(info[3].split(' ')[3])
        # app_logger.info(f'NORM INFO {info} url = {url}')
    except:
        # app_logger.exception(f'HIDE INFO ERR info = {info} split = {info[1].split(" ")} url = {url}')
        close_odds = float(info[1].split(' ')[3])
        open_odds = float(info[1].split(' ')[3])
        
    return {
        type_+'_open_odds': open_odds,
        type_+'_close_odds': close_odds
    }
       


def get_odds_info(url):
    driver = get_driver()
    driver.get(url)
    app_logger.info(f'Start parsing odds in url {url}')
    time.sleep(0.5)
    championate_info = driver.find_elements_by_css_selector('div#breadcrumb a')
    country = championate_info[2].text
    championate = championate_info[3].text
    event_title = driver.find_element_by_css_selector(
        'div#col-content h1').text
    start_date = driver.find_element_by_css_selector('p.date').text
    final_result = driver.find_element_by_css_selector('p.result strong').text
    trs = driver.find_elements_by_css_selector('tr.lo')
    data = []
    for tr in trs:
        tds = tr.find_elements_by_css_selector('td')
        book_name = tds[0].find_element_by_css_selector('a.name').text
        best_bookms = ['Pinnacle', 'Marathonbet', 'Asianodds']
        if book_name in best_bookms:
            home_win_elem = tds[1].find_element_by_css_selector('div')
            draw_elem = tds[2].find_element_by_css_selector('div')
            away_win_elem = tds[3].find_element_by_css_selector('div')
            open_close_home = get_hide_info(home_win_elem, driver, 'home', url)
            open_close_draw = get_hide_info(draw_elem, driver, 'draw', url)
            open_close_away = get_hide_info(away_win_elem, driver, 'away', url)
            odds_info = {
                'country': country,
                'championate': championate,
                'title': event_title,
                'date': start_date,
                'result': final_result,
                'book': book_name,
                **open_close_home,
                **open_close_draw,
                **open_close_away
            }
            data.append(odds_info)
    driver.quit()
    if len(data) == 0:
        raise Exception(f'RECEIVED EMPTY DATA ON URL {url}')
    return data
        
        


def run_parse(url):
    try:
        data = get_odds_info(url)
        for odds in data:
            write_csv('odds_infoTEST.csv', odds, odds.keys()) #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    except Exception:
        app_logger.exception(f'ERROR RUN PARSE ON URL {url}')
        write_text_file(url, 'odds_portal_scraper/logs/odds_failed_urls.txt')


def run_multi_parse(urls, n_proc):
    app_logger.info(f'Start multiprocess function urls - {len(urls)} num processes - {n_proc}')
    pool = Pool(n_proc)
    pool.map(run_parse, urls)
    pool.close()
    pool.join()


def main(n_proc):
    urls_file = open('odds_portal_scraper/urls/events_urls_combine1.txt')
    urls = urls_file.read().split(', ')[4830:10000]
    urls_file.close()
    urls_chunks = chunk(urls, n_proc)
    for urls_chunk in tqdm(urls_chunks):
        run_multi_parse(urls_chunk, n_proc)


if __name__ == '__main__':
    main(2)