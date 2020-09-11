import os
import zipfile
import time
from selenium.webdriver.chrome.options import Options
from selenium import webdriver

PROXY_HOST = '45.151.101.10'  # rotating proxy or host
PROXY_PORT = 8000 # port
PROXY_USER = 'srpuA7' # username
PROXY_PASS = 'nqdBJa' # password


manifest_json = """
{
    "version": "1.0.0",
    "manifest_version": 2,
    "name": "Chrome Proxy",
    "permissions": [
        "proxy",
        "tabs",
        "unlimitedStorage",
        "storage",
        "<all_urls>",
        "webRequest",
        "webRequestBlocking"
    ],
    "background": {
        "scripts": ["background.js"]
    },
    "minimum_chrome_version":"22.0.0"
}
"""

background_js = """
var config = {
        mode: "fixed_servers",
        rules: {
        singleProxy: {
            scheme: "http",
            host: "%s",
            port: parseInt(%s)
        },
        bypassList: ["localhost"]
        }
    };

chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

function callbackFn(details) {
    return {
        authCredentials: {
            username: "%s",
            password: "%s"
        }
    };
}

chrome.webRequest.onAuthRequired.addListener(
            callbackFn,
            {urls: ["<all_urls>"]},
            ['blocking']
);
""" % (PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)


def get_chromedriver():
    # path = os.path.dirname(os.path.abspath(__file__))
    chromedriver_path = '/home/max/projects/odds-portal-scraper/chromedriver'
    chrome_options = Options()
    pluginfile = 'proxy_auth_plugin.zip'
    chrome_options.add_extension(pluginfile)
    chrome_options.add_argument("--headless")
    # chrome_options.add_argument("--window-size=640x480")
    driver = webdriver.Chrome(executable_path=chromedriver_path, options=chrome_options)
    return driver

def main():
    driver = get_chromedriver()
    driver.get('https://www.oddsportal.com/soccer/england/championship-2019-2020/brentford-fulham-Sh5sdH7o/')
    time.sleep(2)
    print('ok')
    # driver.get('https://httpbin.org/ip')

if __name__ == '__main__':
    main()