import logging
import os
import requests
from goose3 import Goose
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict

# Ensure the logs directory exists
LOG_DIRECTORY = "logs"
os.makedirs(LOG_DIRECTORY, exist_ok=True)

# Configure logging
LOG_FILE = os.path.join(LOG_DIRECTORY, "app.log")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Initialize FastAPI application
app = FastAPI()

# Define request model
class URLRequest(BaseModel):
    url: str

# Define response model
class ArticleInfo(BaseModel):
    title: str
    content: str
    meta_description: str
    meta_keywords: List[str]
    authors: List[str]
    publish_date: str
    links: List[str]
    domain: str

def fetch_webpage(url: str) -> str:
    """Fetch the content of the webpage."""
    logger.info(f"Fetching webpage for URL: {url}")
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to fetch webpage: {e}")
        raise HTTPException(status_code=response.status_code, detail=f"Failed to retrieve the webpage. Error: {str(e)}")

def extract_with_goose(html: str) -> Dict:
    """Extract article information using Goose3."""
    logger.info("Extracting content with Goose3")
    g = Goose()
    try:
        article = g.extract(raw_html=html)
        return {
            'title': article.title or "No title found",
            'content': article.cleaned_text or "No content found",
            'meta_description': article.meta_description or "No meta description found",
            'meta_keywords': article.meta_keywords if article.meta_keywords else [],
            'authors': article.authors if article.authors else ["No author found"],
            'publish_date': article.publish_date or "No publish date found",
            'links': article.links if article.links else [],
            'domain': article.domain or "No domain found"
        }
    except Exception as e:
        logger.error(f"Goose3 extraction failed: {e}")
        raise HTTPException(status_code=500, detail=f"Goose3 extraction failed. Error: {str(e)}")

def extract_article_info(url: str) -> Dict:
    """Extract article information from a URL."""
    html = fetch_webpage(url)
    article_info = extract_with_goose(html)
    logger.info("Extraction process completed successfully.")
    return article_info

@app.post("/api/extract-article")
async def extract_article(request: URLRequest):
    """Extract article information from a given URL."""
    logger.info(f"Received request to extract article from URL: {request.url}")
    article_info = extract_article_info(request.url)
    return article_info
