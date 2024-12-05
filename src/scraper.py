import requests
from bs4 import BeautifulSoup
import json
from typing import Dict, List, Tuple
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import logging
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ComputerProblemScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        # Expanded list of sources
        self.base_urls = [
            'https://www.techradar.com/news/computing/apple/20-common-mac-os-x-problems-solved-664676',
            'https://www.makeuseof.com/basic-troubleshooting-tips-fix-common-macos-problems/',
            'https://www.cdw.com/content/cdw/en/articles/hardware/common-computer-problems-and-solutions.html',
            'https://www.hongkiat.com/blog/pc-hardware-problems-solutions/',
            'https://www.stellarinfo.com/article/top-mac-problems-with-solutions-including-data-recovery.php',
            'https://answers.mak.ac.ug/computer-hardware/top-10-most-common-computer-problems'
        ]
        self.data_dir = Path('data')
        self.data_dir.mkdir(exist_ok=True)
        
        # Common problem indicators
        self.problem_indicators = [
            'problem', 'issue', 'error', 'trouble', 'fail', 'not working',
            'won\'t', 'cannot', 'can\'t', 'doesn\'t', 'slow', 'crash',
            'frozen', 'stuck', 'blue screen', 'black screen'
        ]

    def fetch_page(self, url: str) -> str:
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.text
        except Exception as e:
            logger.error(f'Error fetching {url}: {str(e)}')
            return ''

    def extract_content_block(self, elem) -> Tuple[str, str]:
        """Extract problem and solution from a content block"""
        problem = ''
        solution = ''
        
        # Try to find problem in header or strong text
        problem_elem = elem.find(['h2', 'h3', 'h4', 'strong', 'b'])
        if problem_elem:
            problem = problem_elem.text.strip()
        
        # Look for solution in paragraphs and lists
        solution_elems = elem.find_all(['p', 'ul', 'ol', 'div'])
        for sol_elem in solution_elems:
            if sol_elem.name == 'div' and not sol_elem.find(['p', 'ul', 'ol']):
                continue
            solution += sol_elem.text.strip() + '\n'
        
        return problem, solution.strip()

    def parse_problem_solution(self, html: str) -> List[Dict[str, str]]:
        problems_solutions = []
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            # Method 1: Look for structured content
            for section in soup.find_all(['article', 'section', 'div']):
                header = section.find(['h2', 'h3', 'h4'])
                if not header:
                    continue
                    
                header_text = header.text.lower()
                if any(ind in header_text for ind in self.problem_indicators):
                    problem, solution = self.extract_content_block(section)
                    if problem and solution:
                        problems_solutions.append({
                            'problem': problem,
                            'solution': solution,
                            'category': self.categorize_problem(problem)
                        })
            
            # Method 2: Look for numbered or bulleted lists
            for list_elem in soup.find_all(['ol', 'ul']):
                for item in list_elem.find_all('li'):
                    text = item.text.lower()
                    if any(ind in text for ind in self.problem_indicators):
                        # Try to split into problem and solution
                        parts = re.split(r'(?i)solution[s]?[:|-]|fix[:|-]|how to fix[:|-]', item.text)
                        if len(parts) > 1:
                            problem = parts[0].strip()
                            solution = parts[1].strip()
                            problems_solutions.append({
                                'problem': problem,
                                'solution': solution,
                                'category': self.categorize_problem(problem)
                            })
            
            # Method 3: Look for FAQ-style content
            for dt in soup.find_all('dt'):
                dd = dt.find_next('dd')
                if dd and any(ind in dt.text.lower() for ind in self.problem_indicators):
                    problems_solutions.append({
                        'problem': dt.text.strip(),
                        'solution': dd.text.strip(),
                        'category': self.categorize_problem(dt.text)
                    })

        except Exception as e:
            logger.error(f'Error parsing HTML: {str(e)}')
        
        return problems_solutions

    def clean_text(self, text: str) -> str:
        """Clean and format text content"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters
        text = re.sub(r'[^\w\s.,;:?!\'"()-]', '', text)
        return text.strip()

    def categorize_problem(self, problem: str) -> str:
        # Enhanced categorization with more keywords
        categories = {
            'hardware': [
                'hardware', 'device', 'screen', 'keyboard', 'mouse', 'battery',
                'power', 'printer', 'monitor', 'usb', 'fan', 'noise', 'beep',
                'port', 'adapter', 'charger', 'display', 'webcam', 'camera'
            ],
            'software': [
                'software', 'app', 'program', 'application', 'install', 'update',
                'windows', 'macos', 'os x', 'operating system', 'driver', 'virus',
                'malware', 'antivirus', 'browser', 'email', 'office'
            ],
            'network': [
                'network', 'internet', 'wifi', 'connection', 'wireless', 'ethernet',
                'ip', 'dns', 'router', 'modem', 'bluetooth', 'offline', 'online',
                'web', 'browser', 'loading', 'speed'
            ],
            'system': [
                'system', 'boot', 'startup', 'crash', 'freeze', 'slow', 'performance',
                'bios', 'blue screen', 'black screen', 'restart', 'shutdown', 'login',
                'password', 'update', 'upgrade'
            ],
            'storage': [
                'storage', 'disk', 'drive', 'space', 'memory', 'ram', 'hard drive',
                'ssd', 'hdd', 'full', 'backup', 'data', 'file', 'folder', 'save',
                'delete'
            ]
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
        unique_problems = []
        seen_problems = set()
        
        for problem in all_problems:
            clean_problem = self.clean_text(problem['problem'])
            if clean_problem not in seen_problems:
                seen_problems.add(clean_problem)
                problem['problem'] = clean_problem
                problem['solution'] = self.clean_text(problem['solution'])
                unique_problems.append(problem)

        # Save to JSON file
        output_file = self.data_dir / 'computer_problems.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(unique_problems, f, indent=2)

        logger.info(f'Saved {len(unique_problems)} unique problems to {output_file}')
        return unique_problems

if __name__ == '__main__':
    scraper = ComputerProblemScraper()
    problems = scraper.scrape_and_save()