from odds_portal_scraper.odds_parser import get_driver
import time

def write_text_file(text, filename='odds_portal_scraper/champ_urls_by_years.txt'):
    with open(filename, 'a') as f:
        f.write(f'{text}, ')


def make_extend_champ_urls():
    champ_urls_file = open('odds_portal_scraper/champ_urls.txt')
    champ_urls = champ_urls_file.read().split(', ')
    champ_urls_file.close()
    driver = get_driver()
    for url in champ_urls:
        driver.get(url)
        time.sleep(0.5)
        main_filter = driver.find_element_by_css_selector('div.main-menu2.main-menu-gray ul.main-filter')
        links = main_filter.find_elements_by_css_selector('li a')
        [write_text_file(url_by_year.get_attribute('href'))
            for url_by_year in links[:10]]




