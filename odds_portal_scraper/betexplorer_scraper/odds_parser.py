from odds_portal_scraper.logs.loggers import app2_logger
from odds_portal_scraper.odds_portal.odds_parser import get_driver
from odds_portal_scraper.odds_portal.odds_parser import write_csv, chunk, write_text_file
from multiprocessing import Pool
from bs4 import BeautifulSoup
from tqdm import tqdm
import time


def get_html(url):
    app2_logger.info(f'Starting get html on {url}')
    driver = get_driver(headless=True)
    try:
        driver.get(url)
        time.sleep(0.5)
        html = driver.page_source
        driver.quit()
        return html
    except Exception:
        app2_logger.exception(f'Failed on {url}')


def get_event_info(html):
    app2_logger.info(f'Starting get event info')
    try:
        soup = BeautifulSoup(html, 'lxml')
        date = soup.select('p#match-date')[0].text
        country = soup.select('ul.list-breadcrumb li')[2].select('a')[0].text
        championate = soup.select('h1.wrap-section__header__title a')[0].text
        teams = soup.select('h2.list-details__item__title')
        home_team = teams[0].select('a')[0].text
        away_team = teams[1].select('a')[0].text
        result_score = soup.select('p#js-score')[0].text
        partial_score = soup.select('h2#js-partial')[0].text
        event_info = {
            'date': date,
            'country': country,
            'championate': championate,
            'home_team': home_team,
            'away_team': away_team,
            'result_score': result_score,
            'partial_score': partial_score
        }
        return event_info
    except Exception:
        app2_logger.exception(f'Fail received event info')
        raise Exception('Err get_event_info')
        
    

def get_odds_info(html):
    event_info = get_event_info(html)
    app2_logger.info(f'Starting get odds info')
    soup = BeautifulSoup(html, 'lxml')
    trs = soup.select('div#odds-content tbody tr')
    best_bookm = ['Pinnacle', 'SBOBET', 'bet365', '1xBet']
    odds_info = []
    for tr in trs:
        tds = tr.select('td')
        bookm_name = tds[0].select('a')[0]['onclick'].split("'")[3]
        if bookm_name in best_bookm:
            data = {
                **event_info,
                'bookm': bookm_name,
                'open_hw_odds_time': tds[3]['data-opening-date'],
                'open_hw_odds': tds[3]['data-opening-odd'],
                'close_hw_odds_time': tds[3]['data-created'],
                'close_hw_odds': tds[3]['data-odd'],
                'open_draw_odds_time': tds[4]['data-opening-date'],
                'open_draw_odds': tds[4]['data-opening-odd'],
                'close_draw_odds_time': tds[4]['data-created'],
                'close_draw_odds': tds[4]['data-odd'],
                'open_aw_odds_time': tds[5]['data-opening-date'],
                'open_aw_odds': tds[5]['data-opening-odd'],
                'close_aw_odds_time': tds[5]['data-created'],
                'close_aw_odds': tds[5]['data-odd']
            }
            odds_info.append(data)
    return odds_info


def run_parse(url):
    filepath = 'odds_portal_scraper/betexplorer_scraper/betexp_odds.csv'
    try:
        html = get_html(url)
        data = get_odds_info(html)
        [write_csv(filepath, event_data, event_data.keys()) for event_data in data]
    except Exception:
        app2_logger.exception(f'Fail parser on url {url}')
        write_text_file(url, 'odds_portal_scraper/logs/betexp_failed_urls.txt')


def run_multi_parse(urls, n_proc):
    app2_logger.info(f'Start multiprocess function urls - {len(urls)} num processes - {n_proc}')
    pool = Pool(n_proc)
    pool.map(run_parse, urls)
    pool.close()
    pool.join()


def main(n_proc):
    urls_file = open('odds_portal_scraper/betexplorer_scraper/urls/events_urls.txt')
    urls = urls_file.read().split(', ')[25000:26000]
    urls_file.close()
    urls_chunks = chunk(urls, n_proc)
    for urls_chunk in tqdm(urls_chunks):
        run_multi_parse(urls_chunk, n_proc)


if __name__ == '__main__':
    main(8)