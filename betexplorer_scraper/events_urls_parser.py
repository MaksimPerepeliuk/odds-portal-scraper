import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


def write_text_file(text, filename='betexplorer_scraper/urls/champ_urls_prepared.txt'):
    with open(filename, 'a') as f:
        f.write(f'{text}, ')


def make_extend_champ_urls(filename, type_champ):
    champ_urls_file = open(filename)
    champ_urls = champ_urls_file.read().split(', ')
    champ_urls_file.close()
    champ_seasons = {
        'seasons': ['2019-2020', '2018-2019', '2017-2018', '2016-2017',
                    '2015-2016', '2014-2015', '2013-2014', '2012-2013'],
        'years': ['2019', '2018', '2017', '2016', '2015', '2014', '2013']
    }
    for url in champ_urls:
        template = url.replace('2019', '{}')
        for season in champ_seasons[type_champ]:
            new_url = template.format(season)  + 'results/'
            write_text_file(new_url, 'betexplorer_scraper/urls/champ_by_years.txt')


def get_html(url):
    r = requests.get(url)
    if r.ok:
        return r.text
    print(f'{r.status_code} err on url {url}')

    
def get_events_urls(html):
    soup = BeautifulSoup(html, 'lxml')
    links = soup.select('div.box-overflow__in a.in-match')
    urls = []
    for link in links:
        url = 'https://www.betexplorer.com' + link['href']
        urls.append(url)
    return urls


def main(filename):
    champ_urls_file = open(filename)
    champ_urls = champ_urls_file.read().split(', ')
    champ_urls_file.close()
    for champ_url in tqdm(champ_urls):
        events_urls = get_events_urls(get_html(champ_url))
        for url in events_urls:
            try:
                pass
                # write_text_file(url, 'betexplorer_scraper/urls/events_urls.txt')
            except Exception as e:
                print(e)
                write_text_file(url, 'betexplorer_scraper/urls/err_urls.txt')
    # print(f'Write {len(open("betexplorer_scraper/urls/events_urls.txt").read().split(", "))} urls')


if __name__ == "__main__":
    # main('betexplorer_scraper/urls/champ_by_years.txt')
    main('betexplorer_scraper/urls/failed_champ_urls.txt')
