from web_scraper import WebScraper
from text_analysis import SentimentAnalyzer
from output_generator import OutputGenerator
import config

def main():
    # Step 1: Web Scraping
    # print("Starting Web Scraping...")
    # scraper = WebScraper(config.INPUT_FILE)
    # scraper.run()
    
    # Step 2: Text Analysis
    print("Performing Text Analysis...")
    analyzer = SentimentAnalyzer(config.STOP_WORDS_DIR, config.MASTER_DICT_DIR)
    analysis_results = analyzer.analyze_all_texts(config.EXTRACTED_TEXT_DIR)
    
    # Print analysis results for debugging
    print(analysis_results[['positive_score', 'negative_score', 'polarity_score', 'subjectivity_score']])
    
    # Step 3: Generate Output
    print("Generating Output...")
    output_gen = OutputGenerator(config.INPUT_FILE, analysis_results)
    output_gen.generate_output()
    
    print("Process Completed Successfully!")

if __name__ == "__main__":
    main()