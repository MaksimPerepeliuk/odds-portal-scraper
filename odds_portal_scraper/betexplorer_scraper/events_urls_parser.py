import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


def write_text_file(text, filename='betexplorer_scraper/urls/champ_urls_prepared.txt'):
    with open(filename, 'a') as f:
        f.write(f'{text}, ')


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
        try:
            events_urls = get_events_urls(get_html(champ_url))
            for url in events_urls:
                write_text_file(url, 'betexplorer_scraper/urls/events_urls.txt')
        except:
            write_text_file(champ_url, 'betexplorer_scraper/urls/failed_old_urls.txt')

    print(f'Write {len(open("betexplorer_scraper/urls/events_urls.txt").read().split(", "))} urls')


if __name__ == "__main__":
    main('betexplorer_scraper/urls/renamed_failed.txt')
