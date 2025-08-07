import argparse
import os
import json
from urllib.parse import urlparse
import random
import string

from extractor.link_extractor import LinkExtractor
from extractor.article_extractor import ArticleExtractor

from utils.logger import setup_logger

logger = setup_logger("main")

def url_to_filename(url):
    parsed = urlparse(url)
    domain = parsed.netloc.replace("www.", "")
    return f"{domain}.json"

def random_filename(length=6):
    return ''.join(random.choices(string.digits, k=length)) + ".json"

def url_to_domain(url):
    parsed = urlparse(url)
    return parsed.netloc.replace("www.", "")

def save_result(data, url):
    domain = url_to_domain(url)
    folder = os.path.join("data", domain)
    os.makedirs(folder, exist_ok=True)

    filename = os.path.join(folder, random_filename())
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    logger.info(f"✅ Saved to {filename}")

def run_media_mode(url, processor):
    le = LinkExtractor(url)
    all_links = le.get_all_links()
    news_links = le.extract_news_links(all_links)

    for link in news_links:
        ae = ArticleExtractor(link, processor)
        result = ae.extract()
        if result:
            save_result([result], link)

def run_news_mode(url, processor):
    ae = ArticleExtractor(url, processor)
    result = ae.extract()
    if result:
        save_result([result], url)
    else:
        logger.error("❌ Failed to extract article.")

def main():
    parser = argparse.ArgumentParser(description="Online News Scraper")
    parser.add_argument("-m", "--media", help="Baselink media (homepage)")
    parser.add_argument("-n", "--news", help="Direct news URL")
    parser.add_argument("-p", "--processor", choices=["dragnet", "trafilatura", "newspaper"], default="trafilatura", help="Article extraction engine")

    args = parser.parse_args()

    if args.media:
        run_media_mode(args.media, args.processor)
    elif args.news:
        run_news_mode(args.news, args.processor)
    else:
        logger.error("❌ Please provide either -m (media) or -n (news) argument.")

if __name__ == "__main__":
    main()
