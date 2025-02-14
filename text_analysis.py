import os
import re
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize

class SentimentAnalyzer:
    def __init__(self, stop_words_dir='StopWords', master_dict_dir='MasterDictionary'):
        self.stop_words = self._load_files(stop_words_dir)
        self.positive_words, self.negative_words = self._load_dictionary(
            master_dict_dir, 
            self.stop_words
        )

    def _load_files(self, directory):
        words = set()
        for filename in os.listdir(directory):
            if filename.endswith('.txt'):
                with open(os.path.join(directory, filename), 'r', encoding='utf-8', errors='ignore') as f:
                    words.update(word.strip().lower() for word in f)
        return words

    def _load_dictionary(self, directory, stop_words):
        positive_words, negative_words = set(), set()
    
        # Check if directory exists
        if not os.path.exists(directory):
            print(f"Warning: Directory {directory} not found. Using empty dictionaries.")
            return positive_words, negative_words
    
        for filename in os.listdir(directory):
            if filename.endswith('.txt'):
                with open(os.path.join(directory, filename), 'r', encoding='utf-8', errors='ignore') as f:
                    words = {word.strip().lower() for word in f if word.strip().lower() not in stop_words}
                    if 'positive' in filename.lower():
                        positive_words.update(words)
                    elif 'negative' in filename.lower():
                        negative_words.update(words)
        return positive_words, negative_words

    def _clean_text(self, text):
        """Clean text by removing punctuation and stop words"""
        text = re.sub(r'[^\w\s]', '', text.lower())
        tokens = [
            word for word in word_tokenize(text) 
            if word not in self.stop_words and word.isalnum()
        ]
        return tokens

    def _count_syllables(self, word):
        """Count syllables with special handling"""
        vowels = 'aeiou'
        word = word.lower()
        
        if len(word) <= 3:
            return 1
        if word.endswith(('es', 'ed')):
            word = word[:-2]
        
        return max(sum(1 for i in range(len(word)-1) 
                       if word[i] in vowels and word[i+1] not in vowels), 1)

    def analyze_text(self, text):
        """Comprehensive text analysis"""
        cleaned_tokens = self._clean_text(text)
        
        # Sentiment Calculations
        positive_score = sum(1 for word in cleaned_tokens if word in self.positive_words)
        negative_score = sum(1 for word in cleaned_tokens if word in self.negative_words)
        
        total_sentiment_words = positive_score + negative_score
        total_words = len(cleaned_tokens)
        
        polarity_score = (positive_score - negative_score) / (total_sentiment_words + 0.000001)
        subjectivity_score = total_sentiment_words / (total_words + 0.000001)
        
        # Sentence and Word Analysis
        sentences = sent_tokenize(text)
        words = word_tokenize(text)
        
        avg_sentence_length = len(words) / (len(sentences) + 0.000001)
        
        complex_words = [
            word for word in cleaned_tokens 
            if self._count_syllables(word) > 2
        ]
        percentage_complex_words = len(complex_words) / (total_words + 0.000001) * 100
        
        fog_index = 0.4 * (avg_sentence_length + percentage_complex_words)
        
        # Personal Pronouns
        personal_pronouns = len(re.findall(
            r'\b(I|we|my|ours|us)(?!\s*[A-Z]{2})\b', 
            text, 
            re.IGNORECASE
        ))
        
        return {
            'positive_score': positive_score,
            'negative_score': abs(negative_score),
            'polarity_score': polarity_score,
            'subjectivity_score': subjectivity_score,
            'avg_sentence_length': avg_sentence_length,
            'percentage_of_complex_words': percentage_complex_words,
            'fog_index': fog_index,
            'complex_word_count': len(complex_words),
            'word_count': total_words,
            'syllables_per_word': sum(self._count_syllables(word) for word in cleaned_tokens) / (total_words + 0.000001),
            'personal_pronouns': personal_pronouns,
            'avg_word_length': sum(len(word) for word in cleaned_tokens) / (total_words + 0.000001)
        }

    def process_text_files(self, extracted_texts_dir):
        """Process text files and generate analysis"""
        analysis_results = []
        
        for filename in os.listdir(extracted_texts_dir):
            if filename.endswith('.txt'):
                file_path = os.path.join(extracted_texts_dir, filename)
                url_id = filename.split('.')[0]
                
                with open(file_path, 'r', encoding='utf-8') as f:
                    text = f.read()
                
                analysis = self.analyze_text(text)
                analysis['URL_ID'] = url_id
                
                analysis_results.append(analysis)
        
        return pd.DataFrame(analysis_results)

    def analyze_all_texts(self, extracted_texts_dir):
        """Process text files and generate analysis"""
        analysis_results = []
        
        for filename in os.listdir(extracted_texts_dir):
            if filename.endswith('.txt'):
                file_path = os.path.join(extracted_texts_dir, filename)
                url_id = filename.split('.')[0]
                
                with open(file_path, 'r', encoding='utf-8') as f:
                    text = f.read()
                
                analysis = self.analyze_text(text)
                analysis['URL_ID'] = url_id
                
                analysis_results.append(analysis)
        
        return pd.DataFrame(analysis_results)

# Usage
if __name__ == "__main__":
    analyzer = SentimentAnalyzer()
    results = analyzer.process_text_files('extracted_texts')
    print(results)