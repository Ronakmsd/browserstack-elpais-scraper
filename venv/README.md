# El País Opinion Section Scraper

Selenium-based web scraper for El País Opinion section with BrowserStack cross-browser testing integration.

## 🎯 Project Overview

This project scrapes articles from El País Spanish news website, translates titles, analyzes text patterns, and demonstrates parallel cross-browser testing using BrowserStack.

## ✨ Features

- ✅ Scrapes 5 articles from El País Opinion section (Spanish)
- ✅ Extracts titles, content, and cover images
- ✅ Translates article titles from Spanish to English (Google Translate API)
- ✅ Analyzes translated text to find repeated words (>2 occurrences)
- ✅ Cross-browser testing on BrowserStack (5 parallel threads)
- ✅ Supports Chrome, Firefox, Edge browsers on Windows

## 🛠️ Tech Stack

- *Python 3.12*
- *Selenium WebDriver* - Web scraping
- *BrowserStack* - Cloud browser testing
- *Google Translate API* - Translation
- *BeautifulSoup4* - HTML parsing
- *Requests* - Image downloading

## 📁 Project Structure
browserstack-assignment/
├── config.py              # Configuration & credentials
├── scraper.py             # Web scraping logic
├── translator.py          # Translation functionality
├── analyzer.py            # Text analysis
├── main.py                # Local testing script
├── browserstack_runner.py # BrowserStack parallel testing
├── requirements.txt       # Python dependencies
├── images/                # Downloaded article images
└── README.md
## 🚀 Setup Instructions

### 1. Clone Repository

```bash
git clone https://github.com/Ronakmsd/browserstack-elpais-scraper.git
cd browserstack-elpais-scraper
2. Create Virtual Environment
python -m venv venv

# Activate:
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
3. Install Dependencies
pip install -r requirements.txt
4. Configure BrowserStack Credentials
Edit config.py and add your BrowserStack credentials:
BS_USERNAME = "your_browserstack_username"
BS_ACCESS_KEY = "your_browserstack_access_key"
Get credentials from: https://www.browserstack.com/accounts/settings
5. Run Local Test
python main.py
This will:
Scrape 5 articles from El País Opinion section
Download images (if available)
Translate titles to English
Analyze repeated words
6. Run BrowserStack Tests
python browserstack_runner.py
This runs tests in parallel on 5 browsers via BrowserStack.
📊 Output
Console Output:
Live progress of scraping, translation, and analysis
Summary of successful/failed tests
Repeated words analysis results
Files Created:
images/ - Downloaded article cover images
BrowserStack Dashboard - Test recordings and logs
✅ Assignment Requirements Completed
[x] Visit El País website in Spanish
[x] Scrape 5 articles from Opinion section
[x] Print title & content in Spanish
[x] Download cover images (when available)
[x] Translate titles to English using Translation API
[x] Analyze repeated words (>2 occurrences)
[x] Cross-browser testing on BrowserStack (5 parallel threads)
📈 Results Summary
Scraped Articles (Examples):
"Mazón, más cerca del juzgado" → "Mazón, closer to the court"
"Mitin trumpista sobre el estado de la Unión" → "Trump rally on the state of the Union"
"Cómo alimentar a la ultraderecha" → "How to feed the far right"
Repeated Words Analysis:
"the" - 8 occurrences
"of" - 3 occurrences
BrowserStack Tests:
✅ Successfully tested on 5 parallel browser instances
✅ Chrome, Firefox, Edge on Windows
✅ All scraping, translation, and analysis tasks completed
🔗 Links
BrowserStack Dashboard: https://automate.browserstack.com/dashboard
El País Website: https://elpais.com/opinion/
👤 Author
Ronak Bhanushali
GitHub: @Ronakmsd
Email: beingronakmsd@gmail.com
📝 Assignment Context
Created as part of the BrowserStack Customer Engineer hiring process (February 2026).
🙏 Acknowledgments
BrowserStack for cloud testing platform
El País for content source
Google Translate API for translation services
## 📸 BrowserStack Execution Proof


