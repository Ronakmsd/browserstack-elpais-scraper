# main.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import sys

from scraper import ElPaisScraper
from translator import ArticleTranslator
from analyzer import TextAnalyzer

def setup_local_driver():
    """Setup Chrome driver for local testing"""
    print("\n Setting up Chrome driver for LOCAL testing...\n")
    
    chrome_options = Options()
    chrome_options.add_argument('--start-maximized')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument('--disable-notifications')
    chrome_options.add_argument('--lang=es')  # Set language to Spanish
    
    # Add user agent
    chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        print(" Chrome driver initialized successfully!\n")
        return driver
    except Exception as e:
        print(f" Error setting up Chrome driver: {e}")
        print("\nMake sure ChromeDriver is installed and in PATH")
        print("Download from: https://chromedriver.chromium.org/downloads")
        sys.exit(1)

def main():
    """Main execution function"""
    print("\n" + "="*80)
    print(" EL PAÍS OPINION SECTION SCRAPER")
    print("="*80)
    
    driver = None
    
    try:
        # Step 1: Setup driver
        driver = setup_local_driver()
        
        # Step 2: Scrape articles
        print(" STEP 1: SCRAPING ARTICLES FROM EL PAÍS")
        scraper = ElPaisScraper(driver)
        articles_data = scraper.scrape_opinion_section()
        
        if not articles_data:
            print("\n No articles scraped. Exiting.")
            return
        
        # Step 3: Translate titles
        print("\n STEP 2: TRANSLATING ARTICLE TITLES")
        translator = ArticleTranslator()
        translated_titles = translator.translate_titles(articles_data)
        
        # Step 4: Analyze repeated words
        print("\n STEP 3: ANALYZING REPEATED WORDS")
        analyzer = TextAnalyzer()
        repeated_words = analyzer.analyze_repeated_words(translated_titles)
        
        # Final summary
        print("\n" + "="*80)
        print(" ALL TASKS COMPLETED SUCCESSFULLY!")
        print("="*80)
        print(f"\n Summary:")
        print(f"  • Articles scraped: {len(articles_data)}")
        print(f"  • Titles translated: {len(translated_titles)}")
        print(f"  • Images downloaded: {sum(1 for a in articles_data if a['image_path'])}")
        print(f"  • Repeated words found: {len(repeated_words)}")
        print("\n" + "="*80 + "\n")
        
    except KeyboardInterrupt:
        print("\n\n Process interrupted by user.")
    except Exception as e:
        print(f"\n An error occurred: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Close browser
        if driver:
            print("\n Closing browser...")
            driver.quit()
            print(" Browser closed.\n")

if __name__ == "__main__":
    main()