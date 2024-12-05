from brave_web_search import search
from urllib.parse import urlparse
import json
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ProblemSourceFinder:
    def __init__(self):
        self.search_queries = [
            'common computer problems and solutions',
            'most common PC problems fixes',
            'common Mac problems solutions',
            'computer troubleshooting guide',
            'laptop common issues solutions',
            'desktop PC problems solutions',
            'common Windows problems fixes',
            'MacOS common issues solutions',
            'computer hardware problems solutions',
            'computer software problems fixes'
        ]
        self.excluded_domains = {
            'youtube.com', 'facebook.com', 'twitter.com',
            'instagram.com', 'linkedin.com', 'pinterest.com'
        }
        self.data_dir = Path('data')
        self.data_dir.mkdir(exist_ok=True)
    
    def is_valid_url(self, url: str) -> bool:
        try:
            parsed = urlparse(url)
            domain = parsed.netloc.lower()
            
            # Check if domain should be excluded
            if any(ex_domain in domain for ex_domain in self.excluded_domains):
                return False
            
            # Check if it's a proper article URL
            if not any(word in parsed.path.lower() for word in ['problem', 'solution', 'issue', 'fix', 'guide']):
                return False
            
            return True
        except:
            return False
    
    def find_sources(self) -> list:
        all_urls = set()
        
        for query in self.search_queries:
            try:
                # Search using Brave's API
                response = search(query, max_results=20)
                
                # Extract and validate URLs
                for result in response['results']:
                    url = result.get('url', '')
                    if url and self.is_valid_url(url):
                        all_urls.add(url)
                        
            except Exception as e:
                logger.error(f'Error searching for {query}: {str(e)}')
        
        # Save URLs to file
        urls_list = list(all_urls)
        output_file = self.data_dir / 'problem_sources.json'
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump({
                'sources': urls_list,
                'total_count': len(urls_list)
            }, f, indent=2)
        
        logger.info(f'Found {len(urls_list)} unique sources')
        return urls_list

def update_scraper_sources():
    """Update the scraper's source list with newly found URLs"""
    finder = ProblemSourceFinder()
    new_sources = finder.find_sources()
    
    # Read existing scraper code
    scraper_file = Path('src/scraper.py')
    with open(scraper_file, 'r', encoding='utf-8') as f:
        scraper_code = f.read()
    
    # Find the base_urls list in the code
    base_urls_start = scraper_code.find('self.base_urls = [')
    if base_urls_start == -1:
        logger.error('Could not find base_urls in scraper code')
        return
    
    # Create new base_urls string
    new_urls_str = 'self.base_urls = [\n            ' + ',\n            '.join(f"'{url}'" for url in new_sources) + '\n        ]'
    
    # Replace old base_urls
    base_urls_end = scraper_code.find(']', base_urls_start) + 1
    new_code = scraper_code[:base_urls_start] + new_urls_str + scraper_code[base_urls_end:]
    
    # Save updated code
    with open(scraper_file, 'w', encoding='utf-8') as f:
        f.write(new_code)
    
    logger.info('Updated scraper sources')

if __name__ == '__main__':
    update_scraper_sources()