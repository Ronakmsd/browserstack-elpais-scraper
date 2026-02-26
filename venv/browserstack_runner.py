# browserstack_runner.py
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import threading
import time
import sys

from config import BS_USERNAME, BS_ACCESS_KEY
from scraper import ElPaisScraper
from translator import ArticleTranslator
from analyzer import TextAnalyzer

def get_browserstack_driver(browser_name, os_name, test_id):
    """Create BrowserStack driver with proper configuration"""
    
    print(f"[Thread {test_id}] Setting up {browser_name} on {os_name}...")
    
    # BrowserStack hub URL with credentials
    hub_url = f"https://{BS_USERNAME}:{BS_ACCESS_KEY}@hub-cloud.browserstack.com/wd/hub"
    
    # Browser capabilities
    options = Options()
    options.set_capability('browserName', browser_name)
    options.set_capability('bstack:options', {
        'os': os_name,
        'osVersion': '10',
        'browserVersion': 'latest',
        'projectName': 'El Pais Scraper',
        'buildName': 'Opinion Section Analysis',
        'sessionName': f'{browser_name} on {os_name} - Thread {test_id}',
        'local': 'false',
        'seleniumVersion': '4.0.0'
    })
    
    # Create driver
    driver = webdriver.Remote(
        command_executor=hub_url,
        options=options
    )
    
    return driver

def run_single_test(browser_name, os_name, test_id, results_dict, lock):
    """Run test on a single browser"""
    
    driver = None
    
    try:
        print(f"\n{'='*80}")
        print(f"[Thread {test_id}] STARTING TEST")
        print(f"Browser: {browser_name} | OS: {os_name}")
        print(f"{'='*80}\n")
        
        # Get driver
        driver = get_browserstack_driver(browser_name, os_name, test_id)
        print(f"[Thread {test_id}] ✓ Connected to BrowserStack")
        
        # Set timeouts
        driver.set_page_load_timeout(30)
        driver.implicitly_wait(10)
        
        # Run scraping
        print(f"[Thread {test_id}] Starting scraping...")
        scraper = ElPaisScraper(driver)
        articles = scraper.scrape_opinion_section()
        
        # Store results
        with lock:
            results_dict[test_id] = {
                'browser': browser_name,
                'os': os_name,
                'status': 'SUCCESS',
                'articles_count': len(articles),
                'articles': articles
            }
        
        print(f"[Thread {test_id}] ✅ SUCCESS - {len(articles)} articles scraped\n")
        
    except Exception as e:
        print(f"[Thread {test_id}] ❌ FAILED - {str(e)[:150]}\n")
        with lock:
            results_dict[test_id] = {
                'browser': browser_name,
                'os': os_name,
                'status': 'FAILED',
                'error': str(e)[:200]
            }
    
    finally:
        if driver:
            try:
                driver.quit()
                print(f"[Thread {test_id}] Browser closed")
            except:
                pass

def main():
    """Main execution function"""
    
    print("\n" + "="*80)
    print("🌐 BROWSERSTACK PARALLEL TESTING")
    print("="*80 + "\n")
    
    # Test configurations - 5 browsers
    test_configs = [
        ('Chrome', 'Windows'),
        ('Chrome', 'Windows'),  # Same browser, different session
        ('Firefox', 'Windows'),
        ('Edge', 'Windows'),
        ('Chrome', 'Windows')   # Third Chrome instance
    ]
    
    print(f"Running {len(test_configs)} parallel tests...\n")
    
    # Results storage
    results = {}
    lock = threading.Lock()
    threads = []
    
    # Start all threads
    for i, (browser, os) in enumerate(test_configs, 1):
        thread = threading.Thread(
            target=run_single_test,
            args=(browser, os, i, results, lock)
        )
        threads.append(thread)
        thread.start()
        time.sleep(2)  # Small delay between starts
    
    # Wait for completion
    print("⏳ Waiting for all tests to complete...\n")
    for thread in threads:
        thread.join()
    
    # Print summary
    print("\n" + "="*80)
    print("📊 TEST SUMMARY")
    print("="*80 + "\n")
    
    successful = sum(1 for r in results.values() if r['status'] == 'SUCCESS')
    failed = len(results) - successful
    
    print(f"Total: {len(results)} | ✅ Success: {successful} | ❌ Failed: {failed}\n")
    
    for test_id in sorted(results.keys()):
        r = results[test_id]
        icon = "✅" if r['status'] == 'SUCCESS' else "❌"
        print(f"{icon} Test {test_id}: {r['browser']} on {r['os']}")
        if r['status'] == 'SUCCESS':
            print(f"   Articles: {r['articles_count']}")
        else:
            print(f"   Error: {r.get('error', 'Unknown')[:100]}")
        print()
    
    # Run translation & analysis if we have successful results
    successful_with_articles = [r for r in results.values() 
                               if r['status'] == 'SUCCESS' and r.get('articles_count', 0) > 0]
    
    if successful_with_articles:
        print("\n" + "="*80)
        print("🌐 TRANSLATION & ANALYSIS")
        print("="*80 + "\n")
        
        articles = successful_with_articles[0]['articles']
        
        # Translate
        translator = ArticleTranslator()
        translated_titles = translator.translate_titles(articles)
        
        # Analyze
        analyzer = TextAnalyzer()
        repeated_words = analyzer.analyze_repeated_words(translated_titles)
        
        print("\n" + "="*80)
        print("✅ ALL TASKS COMPLETED SUCCESSFULLY!")
        print("="*80)
        print(f"✅ Tested on {successful} browsers")
        print(f"✅ Analyzed {len(articles)} articles")
        print("="*80 + "\n")
    else:
        print("\n⚠️ No successful tests. Check credentials and BrowserStack account.")

if __name__ == "__main__":
    main()