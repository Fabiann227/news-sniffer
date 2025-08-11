import random
import requests
from faker import Faker

fake = Faker()

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36",
]

REFERRERS = [
    "https://www.google.com/",
    "https://www.bing.com/",
    "https://duckduckgo.com/",
    "http://www.yahoo.com" 
]

PROXIES = [
    None,  # without proxy
    # add your proxy, format: "http://user:pass@host:port" or "socks5://host:port"
]

accept_languages = [
    "en-US,en;q=0.9",
    "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7"
]

def get_random_user_agent():
    return random.choice(USER_AGENTS)

def get_random_referrer():
    return random.choice(REFERRERS)

def get_proxy():
    return random.choice(PROXIES)

def get_accept_language():
    return random.choice(accept_languages)

def get_headers():
    return {
        "User-Agent": get_random_user_agent(),
        "Referer": get_random_referrer(),
        "Accept-Language": get_accept_language(),
        "Accept-Encoding": "gzip, deflate, br",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Connection": "keep-alive",
        "X-Forwarded-For": fake.ipv4(),
        "From": fake.email()
    }

def fetch_url(url):
    proxy = get_proxy()
    proxies = {"http": proxy, "https": proxy} if proxy else None
    resp = requests.get(url, headers=get_headers(), proxies=proxies, timeout=10)
    resp.raise_for_status()
    return resp.text