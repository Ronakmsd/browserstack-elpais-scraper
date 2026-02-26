# scraper.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import requests
import os
from config import OPINION_SECTION_URL, NUM_ARTICLES, IMAGE_FOLDER
from config import ARTICLE_SELECTOR, TITLE_SELECTOR, CONTENT_SELECTOR, IMAGE_SELECTOR

class ElPaisScraper:
    def __init__(self, driver):
        self.driver = driver
        self.articles_data = []
        
        # Create images folder if doesn't exist
        if not os.path.exists(IMAGE_FOLDER):
            os.makedirs(IMAGE_FOLDER)
            print(f" Created folder: {IMAGE_FOLDER}")
    
    def scrape_opinion_section(self):
        """Navigate to Opinion section and scrape articles"""
        print(f"\n{'='*80}")
        print(f"NAVIGATING TO: {OPINION_SECTION_URL}")
        print(f"{'='*80}")
        
        self.driver.get(OPINION_SECTION_URL)
        
        # Wait for page to load
        print(" Waiting for page to load...")
        time.sleep(5)
        
        # Find article elements
        try:
            print(f" Searching for articles using selector: {ARTICLE_SELECTOR}")
            articles = self.driver.find_elements(By.CSS_SELECTOR, ARTICLE_SELECTOR)
            
            print(f" Found {len(articles)} articles on page")
            print(f" Extracting first {NUM_ARTICLES} articles...\n")
            
            for i, article in enumerate(articles[:NUM_ARTICLES]):
                print(f"--- Processing Article {i+1}/{NUM_ARTICLES} ---")
                article_data = self.extract_article_data(article, i+1)
                if article_data:
                    self.articles_data.append(article_data)
                    self.print_article(article_data, i+1)
                else:
                    print(f" Failed to extract article {i+1}")
            
            print(f"\n Successfully scraped {len(self.articles_data)} articles!")
            return self.articles_data
            
        except Exception as e:
            print(f" Error scraping articles: {e}")
            return []
    
    def extract_article_data(self, article_element, article_num):
        """Extract title, content, and image from article element"""
        try:
            # Extract title
            try:
                title_element = article_element.find_element(By.CSS_SELECTOR, TITLE_SELECTOR)
                title = title_element.text.strip()
                if not title:
                    # Try alternative - get text from link inside h2
                    title = article_element.find_element(By.CSS_SELECTOR, f"{TITLE_SELECTOR} a").text.strip()
                print(f"   Title extracted: {title[:50]}...")
            except Exception as e:
                print(f"   Could not extract title: {e}")
                title = "Title not available"
            
            # Extract content/description
            try:
                content_element = article_element.find_element(By.CSS_SELECTOR, CONTENT_SELECTOR)
                content = content_element.text.strip()
                print(f"   Content extracted: {len(content)} characters")
            except Exception as e:
                print(f"   Could not extract content, trying alternative...")
                try:
                    # Try to get any paragraph
                    content = article_element.find_element(By.TAG_NAME, "p").text.strip()
                    print(f"   Content extracted (alternative): {len(content)} characters")
                except:
                    content = "Content not available"
                    print(f"   No content found")
            
            # Extract image URL
            image_url = None
            try:
                img_element = article_element.find_element(By.TAG_NAME, "img")
                image_url = img_element.get_attribute("src")
                if not image_url:
                    image_url = img_element.get_attribute("data-src")  # Lazy loading
                print(f"   Image URL found")
            except Exception as e:
                print(f"   No image found for article {article_num}")
            
            # Download image if available
            image_path = None
            if image_url:
                image_path = self.download_image(image_url, article_num)
            
            return {
                'title': title,
                'content': content,
                'image_url': image_url,
                'image_path': image_path
            }
            
        except Exception as e:
            print(f"   Error extracting article {article_num}: {e}")
            return None
    
    def download_image(self, image_url, article_num):
        """Download and save article image"""
        try:
            # Add https if missing
            if image_url.startswith('//'):
                image_url = 'https:' + image_url
            
            print(f"   Downloading image...")
            response = requests.get(image_url, timeout=10)
            
            if response.status_code == 200:
                # Determine file extension
                ext = 'jpg'
                if 'png' in image_url.lower():
                    ext = 'png'
                elif 'webp' in image_url.lower():
                    ext = 'webp'
                
                image_path = os.path.join(IMAGE_FOLDER, f"article_{article_num}.{ext}")
                
                with open(image_path, 'wb') as f:
                    f.write(response.content)
                
                print(f"   Image saved: {image_path}")
                return image_path
            else:
                print(f"   Image download failed: Status {response.status_code}")
                return None
                
        except Exception as e:
            print(f"   Failed to download image: {e}")
            return None
    
    def print_article(self, article_data, article_num):
        """Print article data in Spanish"""
        print(f"\n{'='*80}")
        print(f" ARTICLE {article_num} (SPANISH)")
        print(f"{'='*80}")
        print(f"TITLE:\n{article_data['title']}\n")
        
        content_preview = article_data['content'][:300] if len(article_data['content']) > 300 else article_data['content']
        print(f"CONTENT:\n{content_preview}...\n")
        
        if article_data['image_path']:
            print(f"IMAGE: {article_data['image_path']}")
        else:
            print(f"IMAGE: Not available")
        
        print(f"{'='*80}\n")