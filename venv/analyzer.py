# analyzer.py
from collections import Counter
import re

class TextAnalyzer:
    def _init_(self):
        self.word_counts = {}
    
    def analyze_repeated_words(self, translated_titles):
        """Find words repeated more than twice across all titles"""
        print("\n" + "="*80)
        print(" ANALYZING REPEATED WORDS")
        print("="*80 + "\n")
        
        # Combine all titles into one text
        all_text = " ".join(translated_titles).lower()
        
        print(f"Total text to analyze: {len(all_text)} characters")
        print(f"Analyzing titles: {len(translated_titles)}\n")
        
        # Remove punctuation and split into words
        # Only keep alphabetic words (no numbers)
        words = re.findall(r'\b[a-z]+\b', all_text)
        
        print(f"Total words found: {len(words)}")
        print(f"Unique words: {len(set(words))}\n")
        
        # Count word occurrences
        word_counter = Counter(words)
        
        # Filter words that appear MORE THAN twice (>2 means 3+)
        repeated_words = {word: count for word, count in word_counter.items() 
                         if count > 2}
        
        # Sort by count (descending)
        sorted_repeated = sorted(repeated_words.items(), 
                                key=lambda x: x[1], 
                                reverse=True)
        
        # Display results
        print("─" * 80)
        print("WORDS REPEATED MORE THAN TWICE:")
        print("─" * 80)
        
        if sorted_repeated:
            for word, count in sorted_repeated:
                print(f"  '{word}' → {count} occurrences")
            print(f"\n Total unique words repeated >2 times: {len(sorted_repeated)}")
        else:
            print("  ℹ No words found that repeat more than twice.")
        
        print("="*80 + "\n")
        
        return sorted_repeated