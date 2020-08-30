from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time
import csv
import os


def get_driver():
    chrome_options = Options()
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
        'hour': '{}'.format(info[2]),
        'odds': float(info[3])
    }


def get_hide_info(elem, driver, type_):
    ActionChains(driver).move_to_element(elem).perform()
    span = driver.find_element_by_css_selector('#tooltiptext')
    info = span.get_attribute('innerText').split('\n')
    close_info = extract_info(info[0].split(' '))
    open_info = extract_info(info[3].split(' '))
    return {
        type_+'_open_odds': open_info['odds'],
        type_+'_close_odds': close_info['odds']
    }


def get_odds_info(url):
    driver = get_driver()
    driver.get(url)
    time.sleep(0.5)
    championate_info = driver.find_elements_by_css_selector('div#breadcrumb a')
    country = championate_info[2].text
    championate = championate_info[3].text
    event_title = driver.find_element_by_css_selector(
        'div#col-content h1').text
    start_date = driver.find_element_by_css_selector('p.date').text
    final_result = driver.find_element_by_css_selector('p.result strong').text
    trs = driver.find_elements_by_css_selector('tr.lo')
    for tr in trs:
        tds = tr.find_elements_by_css_selector('td')
        book_name = tds[0].find_element_by_css_selector('a.name').text
        if book_name == 'Marathonbet.ru':
            home_win_elem = tds[1].find_element_by_css_selector('div')
            draw_elem = tds[2].find_element_by_css_selector('div')
            away_win_elem = tds[3].find_element_by_css_selector('div')
            open_close_home = get_hide_info(home_win_elem, driver, 'home')
            open_close_draw = get_hide_info(draw_elem, driver, 'draw')
            open_close_away = get_hide_info(away_win_elem, driver, 'away')
            data = {
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
            write_csv('odds_info.csv', data, data.keys())



# urls = [
#     'https://www.oddsportal.com/soccer/england/premier-league-2019-2020/liverpool-chelsea-ttobio9E/',
#     'https://www.oddsportal.com/soccer/england/premier-league-2019-2020/manchester-united-west-ham-z3p2j5OK/',
#     'https://www.oddsportal.com/soccer/england/premier-league-2019-2020/everton-bournemouth-Qiap3r8Q/'
# ]

# for url in urls:
#     get_odds_info(url)