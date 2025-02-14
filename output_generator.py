import pandas as pd
import config

class OutputGenerator:
    def __init__(self, input_file, analysis_results):
        # Read original input file to get URL and other details
        self.input_df = pd.read_excel(input_file)
        self.analysis_df = analysis_results

    def generate_output(self):
        # Merge input data with analysis results
        output_df = pd.merge(
            self.input_df, 
            self.analysis_df, 
            on='URL_ID', 
            how='left'
        )

        # Reorder columns to match exact output structure
        output_columns = [
            'URL_ID', 'URL', 
            'positive_score', 'negative_score', 
            'polarity_score', 'subjectivity_score',
            'avg_sentence_length', 'percentage_of_complex_words', 
            'fog_index', 'avg_word_length', 
            'complex_word_count', 'word_count', 
            'syllables_per_word', 'personal_pronouns'
        ]

        # Ensure all columns exist
        for col in output_columns:
            if col not in output_df.columns:
                output_df[col] = None

        # Final output dataframe
        final_output = output_df[output_columns]
        
        # Save to Excel
        final_output.to_excel(config.OUTPUT_FILE, index=False)
        print(f"Output saved to {config.OUTPUT_FILE}")

# Usage in main script
if __name__ == "__main__":

    from text_analysis import SentimentAnalyzer
    
    analyzer = SentimentAnalyzer(config.STOP_WORDS_DIR, config.MASTER_DICT_DIR)
    analysis_results = analyzer.analyze_all_texts(config.EXTRACTED_TEXT_DIR)
    
    output_gen = OutputGenerator(config.INPUT_FILE, analysis_results)
    output_gen.generate_output()