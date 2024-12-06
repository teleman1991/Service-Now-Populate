import requests
import json
from pathlib import Path
import csv
import logging
from typing import List, Dict
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ServiceNowUploader:
    def __init__(self, instance_url: str, username: str, password: str):
        self.instance_url = instance_url.rstrip('/')
        self.auth = (username, password)
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

    def load_problems(self) -> List[Dict]:
        """Load problems from JSON file"""
        data_file = Path('data/computer_problems_complete.json')
        if not data_file.exists():
            raise FileNotFoundError('No problem data found')
        
        with open(data_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def create_kb_article(self, problem: Dict) -> Dict:
        """Create a knowledge base article in ServiceNow"""
        endpoint = f'{self.instance_url}/api/now/table/kb_knowledge'

        article_data = {
            'short_description': problem['problem'],
            'text': f"Problem:\n{problem['problem']}\n\nSolution:\n{problem['solution']}",
            'workflow_state': 'published',
            'knowledge_base': 'IT',  # Adjust based on your ServiceNow setup
            'category': problem['category'].upper(),
            'meta': 'computer_problems'
        }

        try:
            response = requests.post(
                endpoint,
                auth=self.auth,
                headers=self.headers,
                json=article_data
            )
            response.raise_for_status()
            return response.json()['result']
        except Exception as e:
            logger.error(f'Error creating KB article: {str(e)}')
            return None

    def export_to_csv(self, problems: List[Dict], export_type: str = 'kb'):
        """Export problems to CSV for manual import via ServiceNow import tool"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'data/servicenow_import_{export_type}_{timestamp}.csv'

        if export_type == 'kb':
            fieldnames = ['short_description', 'text', 'workflow_state', 'knowledge_base', 'category', 'meta']
            rows = [
                {
                    'short_description': p['problem'],
                    'text': f"Problem:\n{p['problem']}\n\nSolution:\n{p['solution']}",
                    'workflow_state': 'published',
                    'knowledge_base': 'IT',
                    'category': p['category'].upper(),
                    'meta': 'computer_problems'
                }
                for p in problems
            ]
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

        logger.info(f'Exported {len(rows)} records to {filename}')
        return filename

    def create_incident_templates(self, problem: Dict) -> Dict:
        """Create incident templates in ServiceNow"""
        endpoint = f'{self.instance_url}/api/now/table/incident_template'

        template_data = {
            'short_description': problem['problem'],
            'description': f"Common Problem:\n{problem['problem']}\n\nRecommended Solution:\n{problem['solution']}",
            'category': 'Software' if problem['category'] == 'software' else 'Hardware',
            'subcategory': problem['category'],
            'template': 'true'
        }

        try:
            response = requests.post(
                endpoint,
                auth=self.auth,
                headers=self.headers,
                json=template_data
            )
            response.raise_for_status()
            return response.json()['result']
        except Exception as e:
            logger.error(f'Error creating incident template: {str(e)}')
            return None

    def bulk_upload(self, upload_type: str = 'kb'):
        """Bulk upload all problems to ServiceNow"""
        problems = self.load_problems()
        logger.info(f'Loaded {len(problems)} problems')

        success_count = 0
        for problem in problems:
            if upload_type == 'kb':
                result = self.create_kb_article(problem)
            else:
                result = self.create_incident_templates(problem)

            if result:
                success_count += 1

            if success_count % 10 == 0:
                logger.info(f'Successfully uploaded {success_count} records')

        logger.info(f'Upload completed. Successfully uploaded {success_count} out of {len(problems)} records')

if __name__ == '__main__':
    # Replace these with your ServiceNow instance details
    instance_url = 'https://compassdcdev.service-now.com'
    username = 'it_kb.integration'
    password = 'password'

    uploader = ServiceNowUploader(instance_url, username, password)
    uploader.bulk_upload('kb')
    # Option 1: Direct API upload to Knowledge Base
    # uploader.bulk_upload('kb')

    # Option 2: Direct API upload as Incident Templates
    # uploader.bulk_upload('incident')

    # Option 3: Export to CSV for manual import
    
