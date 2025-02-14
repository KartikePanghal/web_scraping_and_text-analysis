import asyncio
import pandas as pd
from playwright.async_api import async_playwright
import os
import config

class WebScraper:
    def __init__(self, input_file):
        self.input_df = pd.read_excel(input_file)
        self.urls_df = self.input_df[['URL_ID', 'URL']]

    async def scrape_single_page(self, page, url):
        try:
            await page.goto(url, timeout=config.BROWSER_TIMEOUT)
            
            # Wait for main content to load
            await page.wait_for_selector('body', timeout=config.PAGE_LOAD_TIMEOUT)
            
            # Extract article title
            try:
                title = await page.inner_text('h1', timeout=5000)
            except:
                title = "Title Not Found"
            
            # Extract article text
            try:
                # Adjust selector based on typical article content structures
                article_text = await page.inner_text('article, .article-content, .entry-content, #main-content', timeout=5000)
            except:
                article_text = "Article Text Not Found"
            
            return title, article_text
        
        except Exception as e:
            print(f"Error scraping {url}: {e}")
            return None, None

    async def scrape_all_urls(self):
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            
            for _, row in self.urls_df.iterrows():
                url_id = row['URL_ID']
                url = row['URL']
                
                page = await browser.new_page()
                title, text = await self.scrape_single_page(page, url)
                await page.close()
                
                if text:
                    # Save extracted text
                    output_path = os.path.join(config.EXTRACTED_TEXT_DIR, f"{url_id}.txt")
                    with open(output_path, 'w', encoding='utf-8') as f:
                        f.write(f"Title: {title}\n\n{text}")
                
            await browser.close()

    def run(self):
        asyncio.run(self.scrape_all_urls())

# Usage in main script
if __name__ == "__main__":
    scraper = WebScraper(config.INPUT_FILE)
    scraper.run()