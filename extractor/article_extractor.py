from newspaper import Article
import trafilatura
import json
# from dragnet import extract_content
from cleaner.cleaner import TextCleaner

class ArticleExtractor:
    def __init__(self, url, processor="trafilatura"):
        self.url = url
        self.processor = processor
        self.cleaner = TextCleaner()

    def extract(self):
        if self.processor == "newspaper":
            return self.extract_with_newspaper()
        else:
            return self.extract_with_trafilatura()

    def extract_with_newspaper(self):
        try:
            article = Article(self.url)
            article.download()
            article.parse()
            return {
                "url": self.url,
                "processed_by": "newspaper",
                "title": self.cleaner.clean_title(article.title),
                "published_date": str(article.publish_date) if article.publish_date else "",
                "content": self.cleaner.clean_content(article.text.strip()),
                "authors": article.authors,
                "top_image": article.top_image,
                "tags": list(article.tags) if hasattr(article, "tags") else [],
                "meta_data": article.meta_data
            }
        except Exception as e:
            return {
                "url": self.url,
                "error": str(e),
            }

    def extract_with_trafilatura(self):
        try:
            downloaded = trafilatura.fetch_url(self.url)
            result = trafilatura.extract(downloaded, with_metadata=True, include_comments=False, output_format="json")
            if result:
                data = json.loads(result)
                return {
                    "url": self.url,
                    "processed_by": "trafilatura",
                    "title": self.cleaner.clean_title(data.get("title", "")),
                    "published_date": data.get("date", ""),
                    "content": self.cleaner.clean_content(data.get("text", "")),
                    "authors": data.get("author", []),
                    "top_image": data.get("image", ""),
                    "tags": data.get("tags", [])
                }
            return {
                "url": self.url,
                "title": "",
                "published_date": "",
                "content": "",
                "authors": [],
                "top_image": "",
                "tags": []
            }
        except Exception as e:
            return {
                "url": self.url,
                "error": str(e),
            }

    # def extract_with_dragnet(self):
    #     try:
    #         html = requests.get(self.url).text
    #         content = extract_content(html).strip()
    #         return {"title": "", "pub_date": "", "content": content}
    #     except:
    #         return {"title": "", "pub_date": "", "content": ""}
