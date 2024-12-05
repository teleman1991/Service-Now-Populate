import requests
from bs4 import BeautifulSoup
import json
from typing import Dict, List
from pathlib import Path
import logging
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PreciseProblemScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        # Manually curated list of reliable problems and solutions
        self.problems_solutions = [
            {
                'problem': 'Computer is running slow',
                'solution': '1. Check for and remove malware\n2. Clear temporary files and browser cache\n3. Uninstall unused programs\n4. Disable startup programs\n5. Add more RAM if needed\n6. Consider upgrading to an SSD',
                'category': 'system'
            },
            {
                'problem': 'Blue Screen of Death (BSOD)',
                'solution': '1. Record the error message\n2. Update device drivers\n3. Check for Windows updates\n4. Scan for malware\n5. Check hard drive for errors\n6. Test RAM integrity\n7. Roll back recent changes if problem started recently',
                'category': 'system'
            },
            {
                'problem': 'Computer won\'t start',
                'solution': '1. Check power connections\n2. Listen for beep codes\n3. Remove and reseat RAM\n4. Test power supply\n5. Check monitor connection\n6. Try booting without non-essential peripherals\n7. Reset CMOS if necessary',
                'category': 'hardware'
            },
            {
                'problem': 'No internet connection',
                'solution': '1. Check physical connections\n2. Restart modem and router\n3. Verify WiFi is enabled\n4. Run Windows network troubleshooter\n5. Check IP configuration\n6. Reset network adapter\n7. Update network adapter drivers',
                'category': 'network'
            },
            {
                'problem': 'Printer not working',
                'solution': '1. Check physical connections\n2. Ensure printer is online\n3. Clear print queue\n4. Restart print spooler service\n5. Update or reinstall printer drivers\n6. Set printer as default\n7. Check for paper jams',
                'category': 'hardware'
            },
            {
                'problem': 'System running out of disk space',
                'solution': '1. Run Disk Cleanup\n2. Empty Recycle Bin\n3. Uninstall unnecessary programs\n4. Move files to external storage\n5. Enable Storage Sense\n6. Clean temporary files\n7. Use disk space analysis tools to find large files',
                'category': 'storage'
            },
            {
                'problem': 'Applications freezing or crashing',
                'solution': '1. Force quit the frozen application\n2. Update the application\n3. Check system requirements\n4. Scan for malware\n5. Update Windows\n6. Check for conflicting programs\n7. Reinstall the application if necessary',
                'category': 'software'
            },
            {
                'problem': 'Unable to open files',
                'solution': '1. Verify file extension\n2. Install required software\n3. Update associated program\n4. Check file permissions\n5. Scan file for viruses\n6. Repair file associations\n7. Try alternative software',
                'category': 'software'
            },
            {
                'problem': 'Computer making strange noises',
                'solution': '1. Clean dust from fans\n2. Check fan operation\n3. Ensure proper ventilation\n4. Monitor system temperatures\n5. Check hard drive health\n6. Tighten loose components\n7. Replace failing fans if necessary',
                'category': 'hardware'
            },
            {
                'problem': 'System overheating',
                'solution': '1. Clean dust and debris\n2. Ensure proper ventilation\n3. Check fan operation\n4. Replace thermal paste\n5. Reduce CPU load\n6. Monitor temperatures\n7. Consider additional cooling',
                'category': 'hardware'
            }
        ]
        
        # Define reliable sources for web scraping
        self.sources = [
            'https://support.microsoft.com/en-us/windows',
            'https://support.apple.com/mac',
            'https://www.dell.com/support/home',
            'https://support.hp.com/us-en'
        ]
        
        self.data_dir = Path('data')
        self.data_dir.mkdir(exist_ok=True)
    
    def scrape_additional_problems(self) -> List[Dict[str, str]]:
        """Scrape additional problems from reliable sources"""
        additional_problems = []
        
        for url in self.sources:
            try:
                response = requests.get(url, headers=self.headers)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Look for well-structured support articles
                articles = soup.find_all(['article', 'section'])
                for article in articles:
                    title = article.find(['h1', 'h2', 'h3'])
                    content = article.find_all(['p', 'ul', 'ol'])
                    
                    if title and content:
                        problem = title.text.strip()
                        solution = '\n'.join(c.text.strip() for c in content)
                        
                        if self.is_valid_problem_solution(problem, solution):
                            additional_problems.append({
                                'problem': problem,
                                'solution': solution,
                                'category': self.categorize_problem(problem)
                            })
            
            except Exception as e:
                logger.error(f'Error scraping {url}: {str(e)}')
        
        return additional_problems
    
    def is_valid_problem_solution(self, problem: str, solution: str) -> bool:
        """Validate if the problem-solution pair is meaningful"""
        if len(problem) < 10 or len(solution) < 20:
            return False
        
        # Check if problem describes an actual issue
        if not any(word in problem.lower() for word in ['error', 'issue', 'problem', 'not', 'fail', 'slow', 'crash']):
            return False
        
        # Check if solution contains actual steps
        if not any(word in solution.lower() for word in ['check', 'update', 'install', 'verify', 'restart', 'run']):
            return False
        
        return True
    
    def categorize_problem(self, problem: str) -> str:
        """Categorize the problem based on keywords"""
        categories = {
            'hardware': ['hardware', 'printer', 'screen', 'keyboard', 'mouse', 'power', 'noise', 'fan'],
            'software': ['software', 'program', 'app', 'windows', 'mac', 'application', 'install'],
            'network': ['network', 'internet', 'wifi', 'connection', 'ethernet', 'wireless'],
            'system': ['system', 'boot', 'slow', 'crash', 'freeze', 'blue screen'],
            'storage': ['storage', 'disk', 'space', 'drive', 'full', 'memory']
        }
        
        problem_lower = problem.lower()
        for category, keywords in categories.items():
            if any(keyword in problem_lower for keyword in keywords):
                return category
        return 'other'
    
    def save_problems(self):
        """Save all problems to a JSON file"""
        # Combine curated and scraped problems
        all_problems = self.problems_solutions.copy()
        
        # Add scraped problems if they don't duplicate existing ones
        seen_problems = {p['problem'].lower() for p in all_problems}
        
        for problem in self.scrape_additional_problems():
            if problem['problem'].lower() not in seen_problems:
                all_problems.append(problem)
                seen_problems.add(problem['problem'].lower())
        
        # Save to JSON file
        output_file = self.data_dir / 'computer_problems.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(all_problems, f, indent=2)
        
        logger.info(f'Saved {len(all_problems)} problems to {output_file}')
        return all_problems

if __name__ == '__main__':
    scraper = PreciseProblemScraper()
    problems = scraper.save_problems()