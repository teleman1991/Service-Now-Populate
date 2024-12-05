import requests
from bs4 import BeautifulSoup
import json
from typing import Dict, List, Tuple
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ComputerProblemScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.base_urls = [
            'https://www.techradar.com/news/computing/apple/20-common-mac-os-x-problems-solved-664676',
            'https://www.makeuseof.com/basic-troubleshooting-tips-fix-common-macos-problems/',
            'https://www.cdw.com/content/cdw/en/articles/hardware/common-computer-problems-and-solutions.html'
        ]
        self.data_dir = Path('data')
        self.data_dir.mkdir(exist_ok=True)

    def fetch_page(self, url: str) -> str:
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.text
        except Exception as e:
            logger.error(f'Error fetching {url}: {str(e)}')
            return ''

    def parse_problem_solution(self, html: str) -> List[Dict[str, str]]:
        problems_solutions = []
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            # Look for common patterns in technical articles
            headers = soup.find_all(['h2', 'h3'])
            
            for header in headers:
                # Look for problem descriptions
                if any(keyword in header.text.lower() for keyword in ['problem', 'issue', 'error']):
                    problem = header.text.strip()
                    solution = ''
                    
                    # Look for solution in next sibling elements
                    next_elem = header.find_next(['p', 'ul', 'ol'])
                    while next_elem and next_elem.name not in ['h2', 'h3']:
                        solution += next_elem.text.strip() + '\n'
                        next_elem = next_elem.find_next(['p', 'ul', 'ol'])
                    
                    if problem and solution:
                        problems_solutions.append({
                            'problem': problem,
                            'solution': solution,
                            'category': self.categorize_problem(problem)
                        })
        
        except Exception as e:
            logger.error(f'Error parsing HTML: {str(e)}')
        
        return problems_solutions

    def categorize_problem(self, problem: str) -> str:
        # Simple categorization based on keywords
        categories = {
            'hardware': ['hardware', 'device', 'screen', 'keyboard', 'mouse', 'battery'],
            'software': ['software', 'app', 'program', 'application'],
            'network': ['network', 'internet', 'wifi', 'connection'],
            'system': ['system', 'boot', 'startup', 'crash', 'freeze'],
            'storage': ['storage', 'disk', 'drive', 'space', 'memory']
        }
        
        problem_lower = problem.lower()
        for category, keywords in categories.items():
            if any(keyword in problem_lower for keyword in keywords):
                return category
        return 'other'

    def scrape_and_save(self):
        all_problems = []
        
        with ThreadPoolExecutor() as executor:
            html_contents = list(executor.map(self.fetch_page, self.base_urls))
        
        for html in html_contents:
            problems = self.parse_problem_solution(html)
            all_problems.extend(problems)

        # Remove duplicates based on problem description
        unique_problems = list({
            problem['problem']: problem for problem in all_problems
        }.values())

        # Save to JSON file
        output_file = self.data_dir / 'computer_problems.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(unique_problems, f, indent=2)

        logger.info(f'Saved {len(unique_problems)} unique problems to {output_file}')
        return unique_problems

if __name__ == '__main__':
    scraper = ComputerProblemScraper()
    problems = scraper.scrape_and_save()