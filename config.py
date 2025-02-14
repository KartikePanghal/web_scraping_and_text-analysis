import os
import nltk

# Download necessary NLTK resources
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('words')

# Directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(BASE_DIR, 'Input.xlsx')
OUTPUT_FILE = os.path.join(BASE_DIR, 'Output.xlsx')
EXTRACTED_TEXT_DIR = os.path.join(BASE_DIR, 'extracted_texts')

# Directories for stop words and master dictionary
STOP_WORDS_DIR = os.path.join(BASE_DIR, 'StopWords')
MASTER_DICT_DIR = os.path.join(BASE_DIR, 'MasterDictionary')

# Create directories if they don't exist
os.makedirs(EXTRACTED_TEXT_DIR, exist_ok=True)
os.makedirs(STOP_WORDS_DIR, exist_ok=True)
os.makedirs(MASTER_DICT_DIR, exist_ok=True)

# Playwright configuration
BROWSER_TIMEOUT = 30000  # 30 seconds
PAGE_LOAD_TIMEOUT = 20000  # 20 seconds