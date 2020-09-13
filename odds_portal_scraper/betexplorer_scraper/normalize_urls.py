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


def rename_ligues():
    rename_ligues = {
        'laliga-': 'primera-division-',
        'laliga2-': 'segunda-division-',
        'ligapro-': 'segunda-liga-',
        '1-lig-': 'tff-1-lig-',
        'proximus-league-': 'belgacom-league-',
        'tipico-bundesliga-': 'tipp3-bundesliga-',
        '2-liga-': 'erste-liga-',
        'parva-liga-': 'a-pfg-',
        '1-liga-': 'synot-liga-',
        '1st-division-': 'bet25-liga-',
        'premier-league-': 'pari-match-league-'
    }

    failed_urls_file = open('betexplorer_scraper/urls/main_failed.txt')
    failed_urls = failed_urls_file.read().split(', ')
    failed_urls_file.close()

    for new_name, old_name in rename_ligues.items():
        for failed_url in failed_urls:
            if new_name in failed_url:
                write_text_file(
                    failed_url.replace(new_name, old_name),
                    'betexplorer_scraper/urls/renamed_failed.txt')