import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
import joblib
from scipy.sparse import hstack
import pandas as pd
from utils.logger import setup_logger

logger = setup_logger("")

class LinkExtractor:
    def __init__(self, baselink):
        self.baselink = baselink
        self.model = joblib.load('model/news_link_model.pkl')
        self.tfidf = joblib.load('model/tfidf_vectorizer.pkl')

    def get_all_links(self):
        try:
            response = requests.get(self.baselink)
            soup = BeautifulSoup(response.text, "html.parser")
            links = set()

            for a in soup.find_all("a", href=True):
                href = urljoin(self.baselink, a["href"])
                links.add(href)

            return list(links)
        except Exception as e:
            logger.error(f"Failed to get links from {self.baselink} - {e}")
            return []

    def extract_features(self, links):
        link_length = [len(link) for link in links]
        slash_count = [link.count('/') for link in links]
        digit_count = [sum(c.isdigit() for c in link) for link in links]
        alpha_count = [sum(c.isalpha() for c in link) for link in links]
        return pd.DataFrame({
            'link_length': link_length,
            'slash_count': slash_count,
            'digit_count': digit_count,
            'alpha_count': alpha_count
        })

    def extract_news_links(self, links):
        if not links:
            logger.error("No links provided for extraction.")
            return []

        logger.info(f"🔗 Extracting news links from {len(links)} total links...")

        # Feature extraction
        X_num = self.extract_features(links)
        X_text_tfidf = self.tfidf.transform(links)
        X_final = hstack([X_text_tfidf, X_num])

        # Predict
        preds = self.model.predict(X_final)

        # Group result
        news_links = [link for link, pred in zip(links, preds) if pred == 1]
        non_news_links = [link for link, pred in zip(links, preds) if pred == 0]

        if news_links:
            logger.info(f"✅ Found {len(news_links)} potential news link(s). Example:")
            for link in news_links[:5]:
                logger.info(f"   📰 {link}")
        else:
            logger.info("⚠️ No news links detected.")

        if non_news_links:
            logger.info(f"🧹 {len(non_news_links)} link(s) classified as non-news. Example:")
            for link in non_news_links[:5]:
                logger.info(f"   🚫 {link}")

        return news_links