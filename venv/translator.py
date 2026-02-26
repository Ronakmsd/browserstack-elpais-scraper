# translator.py
from googletrans import Translator
import time

class ArticleTranslator:
    def __init__(self):
        self.translator = Translator()
        self.translated_titles = []
    
    def translate_titles(self, articles_data):
        """Translate article titles from Spanish to English"""
        print("\n" + "="*80)
        print(" TRANSLATING TITLES (Spanish → English)")
        print("="*80 + "\n")
        
        for i, article in enumerate(articles_data):
            try:
                original_title = article['title']
                
                # Skip if title not available
                if original_title == "Title not available":
                    print(f"Article {i+1}: Skipping (no title)")
                    self.translated_titles.append(original_title)
                    continue
                
                print(f"Article {i+1}:")
                print(f"  Spanish:  {original_title}")
                
                # Translate title
                translation = self.translator.translate(
                    original_title, 
                    src='es', 
                    dest='en'
                )
                translated_title = translation.text
                self.translated_titles.append(translated_title)
                
                print(f"  English:  {translated_title}")
                print()
                
                # Small delay to avoid rate limiting
                time.sleep(0.5)
                
            except Exception as e:
                print(f"  ⚠ Error translating article {i+1}: {e}")
                # Keep original if translation fails
                self.translated_titles.append(article['title'])
                print()
        
        print("="*80)
        print(f" Translated {len(self.translated_titles)} titles successfully!")
        print("="*80 + "\n")
        
        return self.translated_titles