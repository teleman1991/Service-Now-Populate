import requests
from bs4 import BeautifulSoup
import json
from typing import Dict, List, Tuple
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import logging
import re
from urllib.parse import urljoin
import PyPDF2
from io import BytesIO

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BaseSourceScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

    def fetch_content(self, url: str) -> str:
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return response.content
        except Exception as e:
            logger.error(f'Error fetching {url}: {str(e)}')
            return None

class WebPageScraper(BaseSourceScraper):
    def __init__(self):
        super().__init__()
        self.problem_patterns = [
            r'(?i)problem[s]?[:]?\s+([^.\n]+)',
            r'(?i)issue[s]?[:]?\s+([^.\n]+)',
            r'(?i)error[s]?[:]?\s+([^.\n]+)',
            r'(?i)trouble[s]?[:]?\s+([^.\n]+)',
            r'(?i)symptom[s]?[:]?\s+([^.\n]+)'
        ]
        self.solution_patterns = [
            r'(?i)solution[s]?[:]?\s+([^.\n]+)',
            r'(?i)fix[:]?\s+([^.\n]+)',
            r'(?i)resolve[:]?\s+([^.\n]+)',
            r'(?i)how to fix[:]?\s+([^.\n]+)',
            r'(?i)troubleshoot[:]?\s+([^.\n]+)'
        ]

    def extract_problems(self, html: str) -> List[Dict[str, str]]:
        problems = []
        soup = BeautifulSoup(html, 'html.parser')
        
        # Method 1: Look for structured content
        for section in soup.find_all(['article', 'section', 'div', 'li']):
            problem_text = ''
            solution_text = ''
            
            # Look for problem indicators
            for pattern in self.problem_patterns:
                matches = re.finditer(pattern, section.text)
                for match in matches:
                    problem_text = match.group(1).strip()
                    
                    # Find corresponding solution
                    next_text = section.text[match.end():]
                    for sol_pattern in self.solution_patterns:
                        sol_match = re.search(sol_pattern, next_text)
                        if sol_match:
                            solution_text = sol_match.group(1).strip()
                            break
                    
                    if problem_text and solution_text:
                        problems.append({
                            'problem': problem_text,
                            'solution': solution_text
                        })
        
        # Method 2: Look for FAQ-style content
        for dt in soup.find_all('dt'):
            dd = dt.find_next('dd')
            if dd:
                problems.append({
                    'problem': dt.text.strip(),
                    'solution': dd.text.strip()
                })
        
        # Method 3: Look for numbered lists
        for ol in soup.find_all('ol'):
            items = ol.find_all('li')
            for item in items:
                text = item.text
                # Try to split into problem and solution
                parts = re.split(r'(?i)solution[s]?[:]|fix[:]|how to fix[:]', text)
                if len(parts) > 1:
                    problems.append({
                        'problem': parts[0].strip(),
                        'solution': parts[1].strip()
                    })
        
        return problems

class PDFScraper(BaseSourceScraper):
    def extract_problems(self, pdf_content: bytes) -> List[Dict[str, str]]:
        problems = []
        try:
            pdf_file = BytesIO(pdf_content)
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            text = ''
            for page in pdf_reader.pages:
                text += page.extract_text()
            
            # Split into sections
            sections = re.split(r'\n\n+', text)
            
            for section in sections:
                # Look for problem-solution pairs
                if re.search(r'(?i)(problem|issue|error).*?\n.*?(solution|fix|resolve)', section):
                    parts = re.split(r'(?i)(solution|fix|resolve)[s]?[:]?', section)
                    if len(parts) > 1:
                        problems.append({
                            'problem': parts[0].strip(),
                            'solution': parts[1].strip()
                        })
        
        except Exception as e:
            logger.error(f'Error parsing PDF: {str(e)}')
        
        return problems

class ComprehensiveScraper:
    def __init__(self):
        self.web_scraper = WebPageScraper()
        self.pdf_scraper = PDFScraper()
        self.data_dir = Path('data')
        self.data_dir.mkdir(exist_ok=True)
        
        # Comprehensive list of sources
        self.sources = [
            # Technical support sites
            'https://www.techradar.com/how-to/computing/100-common-windows-10-problems',
            'https://www.webnots.com/11-common-computer-problems-with-solutions/',
            'https://www.hongkiat.com/blog/pc-hardware-problems-solutions/',
            
            # Support forums and knowledge bases
            'https://answers.microsoft.com/en-us/windows/forum/windows_10',
            'https://discussions.apple.com/community/mac_hardware',
            'https://support.hp.com/us-en/document/c00702723',
            'https://support.dell.com/support/articles/common-issues',
            
            # Educational resources
            'https://edu.gcfglobal.org/en/computerbasics/basic-troubleshooting-techniques/',
            'https://www.professormesser.com/free-a-plus-training/220-1001/220-1000-training-course/',
            
            # IT support documentation
            'https://www.linnmar.k12.ia.us/wp-content/uploads/2020/08/Common-Computer-Issues-and-Solutions.pdf',
            'https://www.arcsystems.co.uk/common-computer-faults-and-how-you-can-solve-them/'
        ]

    def categorize_problem(self, problem: str) -> str:
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
                'ip', 'dns', 'router', 'modem', 'bluetooth', 'offline', 'online'
            ],
            'system': [
                'system', 'boot', 'startup', 'crash', 'freeze', 'slow', 'performance',
                'bios', 'blue screen', 'black screen', 'restart', 'shutdown'
            ],
            'storage': [
                'storage', 'disk', 'drive', 'space', 'memory', 'ram', 'hard drive',
                'ssd', 'hdd', 'full', 'backup', 'data', 'file', 'folder'
            ]
        }
        
        problem_lower = problem.lower()
        for category, keywords in categories.items():
            if any(keyword in problem_lower for keyword in keywords):
                return category
        return 'other'

    def clean_text(self, text: str) -> str:
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s.,;:?!\'"()-]', '', text)
        return text.strip()

    def scrape_all_sources(self) -> List[Dict[str, str]]:
        all_problems = []
        
        with ThreadPoolExecutor(max_workers=5) as executor:
            for url in self.sources:
                try:
                    content = executor.submit(self.web_scraper.fetch_content, url).result()
                    if content:
                        if url.endswith('.pdf'):
                            problems = self.pdf_scraper.extract_problems(content)
                        else:
                            problems = self.web_scraper.extract_problems(content.decode('utf-8'))
                        
                        # Clean and categorize problems
                        for problem in problems:
                            problem['problem'] = self.clean_text(problem['problem'])
                            problem['solution'] = self.clean_text(problem['solution'])
                            problem['category'] = self.categorize_problem(problem['problem'])
                            all_problems.append(problem)
                            
                except Exception as e:
                    logger.error(f'Error processing {url}: {str(e)}')
        
        # Remove duplicates while preserving unique solutions
        unique_problems = {}
        for problem in all_problems:
            key = problem['problem'].lower()
            if key not in unique_problems:
                unique_problems[key] = problem
            else:
                # If we have a new solution, append it
                existing_sol = unique_problems[key]['solution'].lower()
                new_sol = problem['solution'].lower()
                if new_sol not in existing_sol:
                    unique_problems[key]['solution'] += f'\n\nAlternative solution:\n{problem["solution"]}'
        
        problems_list = list(unique_problems.values())
        
        # Save to JSON file
        output_file = self.data_dir / 'computer_problems_comprehensive.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(problems_list, f, indent=2)
        
        logger.info(f'Saved {len(problems_list)} unique problems to {output_file}')
        return problems_list

if __name__ == '__main__':
    scraper = ComprehensiveScraper()
    problems = scraper.scrape_all_sources()