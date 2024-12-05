import json
from pathlib import Path
import logging
from comprehensive_scraper import ComprehensiveProblemScraper
from comprehensive_scraper_part2 import additional_problems
from comprehensive_scraper_part3 import more_problems
from comprehensive_scraper_part4 import final_problems
from office_problems_scraper import office_problems
from outlook_teams_problems import outlook_teams_problems

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FinalProblemScraper:
    def __init__(self):
        # Get base problems
        base_scraper = ComprehensiveProblemScraper()
        self.problems_solutions = base_scraper.problems_solutions
        
        # Add additional problems
        self.problems_solutions.extend(additional_problems)
        self.problems_solutions.extend(more_problems)
        self.problems_solutions.extend(final_problems)
        self.problems_solutions.extend(office_problems)
        self.problems_solutions.extend(outlook_teams_problems)
        
        self.data_dir = Path('data')
        self.data_dir.mkdir(exist_ok=True)
    
    def save_problems(self):
        """Save all problems to JSON file"""
        # Remove any duplicates based on problem description
        unique_problems = {}
        for problem in self.problems_solutions:
            key = problem['problem'].lower().strip()
            if key not in unique_problems:
                unique_problems[key] = problem
        
        problems_list = list(unique_problems.values())
        
        # Save to JSON file
        output_file = self.data_dir / 'computer_problems_complete.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(problems_list, f, indent=2)
        
        logger.info(f'Saved {len(problems_list)} unique problems to {output_file}')
        return problems_list

if __name__ == '__main__':
    scraper = FinalProblemScraper()
    problems = scraper.save_problems()