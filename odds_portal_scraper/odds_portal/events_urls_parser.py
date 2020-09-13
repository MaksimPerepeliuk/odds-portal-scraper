from odds_portal_scraper.odds_parser import get_driver
import time
from tqdm import tqdm

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


def write_events_urls(url, filename):
    driver = get_driver()
    driver.get(url)
    time.sleep(0.5)
    stop_msg = driver.find_element_by_css_selector('div.cms').text
    if stop_msg == 'No data available':
        return 'no data'
    trs = driver.find_elements_by_css_selector('table#tournamentTable tr.odd')
    for tr in trs:
        tds = tr.find_elements_by_css_selector('td')
        event_url = tds[1].find_element_by_css_selector('a').get_attribute('href')
        write_text_file(event_url, filename)
    driver.quit()


def main(champ_urls, filename):
    driver = get_driver()
    for url in tqdm(champ_urls):
        template_pagination = url + '#/page/{}/'
        for i in range(1, 20):
            try:
                url_page = template_pagination.format(i)
                msg = write_events_urls(url_page, filename)
                if msg == 'no data':
                    write_text_file(url_page, 'odds_portal_scraper/no_data_urls.txt')
                    break
            except:
                print(f'fail on {url}')
                write_text_file(url, 'odds_portal_scraper/failed_urls.txt')

# def is_in(url):
#     deleted_seasons = ['2020-2019', '2019-2020', '2018-2019', '2017-2018', '2016-2017']
#     for season in deleted_seasons:
#         if season in url:
#             return False
#     return True


# def urls_filter():
#     champ_urls_file = open('odds_portal_scraper/urls/champ_urls_by_years.txt')
#     champ_urls = champ_urls_file.read().split(', ')
#     champ_urls_file.close()
#     old_urls = list(filter(is_in, champ_urls))
#     print(f'len old {len(old_urls)}')
#     for old_url in old_urls:
#         write_text_file(old_url, 'odds_portal_scraper/old_urls.txt')
        

# urls_filter()

# print('2019-2020' in 'https://www.oddsportal.com/soccer/england/championship-2019-2020/results/')

if __name__ == "__main__":
    champ_urls_file = open('odds_portal_scraper/old_urls.txt')
    champ_urls = champ_urls_file.read().split(', ')
    champ_urls_file.close()
    main(champ_urls[:50], 'odds_portal_scraper/events_urls7.txt')
    main(champ_urls)


