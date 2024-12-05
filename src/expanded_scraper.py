import requests
from bs4 import BeautifulSoup
import json
from typing import Dict, List
from pathlib import Path
import logging
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ExpandedProblemScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        # Expanded list of problems and solutions
        self.problems_solutions = [
            # System Performance Issues
            {
                'problem': 'Computer is running slow',
                'solution': '1. Check for and remove malware\n2. Clear temporary files and browser cache\n3. Uninstall unused programs\n4. Disable startup programs\n5. Add more RAM if needed\n6. Consider upgrading to an SSD',
                'category': 'system'
            },
            {
                'problem': 'System freezes or becomes unresponsive',
                'solution': '1. Wait for system to respond\n2. Use Task Manager to identify high-resource processes\n3. Update system drivers\n4. Check for overheating\n5. Test RAM integrity\n6. Scan for malware',
                'category': 'system'
            },
            # Startup Issues
            {
                'problem': 'Computer won\'t boot',
                'solution': '1. Check power connections\n2. Listen for beep codes\n3. Test with minimal hardware\n4. Check RAM seating\n5. Test power supply\n6. Reset CMOS',
                'category': 'hardware'
            },
            {
                'problem': 'Operating system fails to load',
                'solution': '1. Boot in Safe Mode\n2. Run startup repair\n3. Check disk for errors\n4. Restore from backup\n5. Repair/reinstall bootloader\n6. Check for corrupt system files',
                'category': 'system'
            },
            # Blue Screen Errors
            {
                'problem': 'BSOD: MEMORY_MANAGEMENT',
                'solution': '1. Run Windows Memory Diagnostic\n2. Update drivers\n3. Check for memory conflicts\n4. Test RAM modules individually\n5. Scan for malware\n6. Check for Windows updates',
                'category': 'system'
            },
            {
                'problem': 'BSOD: DRIVER_IRQL_NOT_LESS_OR_EQUAL',
                'solution': '1. Update device drivers\n2. Remove incompatible drivers\n3. Check for hardware conflicts\n4. Scan for malware\n5. Run system file checker\n6. Reset Windows if necessary',
                'category': 'system'
            },
            # Network Issues
            {
                'problem': 'No internet connection',
                'solution': '1. Check physical connections\n2. Restart modem and router\n3. Verify WiFi is enabled\n4. Run network troubleshooter\n5. Reset network adapter\n6. Update network drivers',
                'category': 'network'
            },
            {
                'problem': 'Slow internet speed',
                'solution': '1. Test speed at router\n2. Check for background downloads\n3. Scan for malware\n4. Update network drivers\n5. Reset network settings\n6. Contact ISP if persistent',
                'category': 'network'
            },
            # Hardware Issues
            {
                'problem': 'Printer not responding',
                'solution': '1. Check connections\n2. Clear print queue\n3. Restart print spooler\n4. Update printer drivers\n5. Remove and re-add printer\n6. Check network settings',
                'category': 'hardware'
            },
            {
                'problem': 'USB device not recognized',
                'solution': '1. Try different USB port\n2. Update USB drivers\n3. Check Device Manager\n4. Test device on another computer\n5. Disable USB selective suspend\n6. Check power management settings',
                'category': 'hardware'
            },
            # Storage Issues
            {
                'problem': 'Hard drive making clicking sounds',
                'solution': '1. Back up data immediately\n2. Run disk diagnostics\n3. Check drive connections\n4. Monitor SMART status\n5. Plan for drive replacement\n6. Consider data recovery options',
                'category': 'storage'
            },
            {
                'problem': 'System running out of space',
                'solution': '1. Run Disk Cleanup\n2. Empty Recycle Bin\n3. Uninstall large programs\n4. Move files to external storage\n5. Enable Storage Sense\n6. Use disk analysis tools',
                'category': 'storage'
            },
            # Software Issues
            {
                'problem': 'Program won\'t install',
                'solution': '1. Check system requirements\n2. Run as administrator\n3. Disable antivirus temporarily\n4. Clear temp files\n5. Check disk space\n6. Use compatibility mode',
                'category': 'software'
            },
            {
                'problem': 'Application crashes frequently',
                'solution': '1. Update the application\n2. Check for conflicts\n3. Verify system requirements\n4. Run in compatibility mode\n5. Reinstall the application\n6. Update Windows',
                'category': 'software'
            },
            # Display Issues
            {
                'problem': 'Screen flickering',
                'solution': '1. Update display drivers\n2. Check refresh rate\n3. Test monitor on another PC\n4. Check cable connections\n5. Disable visual effects\n6. Test different resolution',
                'category': 'hardware'
            },
            {
                'problem': 'Blank or black screen',
                'solution': '1. Check monitor power\n2. Test with external monitor\n3. Update graphics drivers\n4. Check for loose cables\n5. Reset display adapter\n6. Check startup settings',
                'category': 'hardware'
            },
            # Audio Issues
            {
                'problem': 'No sound output',
                'solution': '1. Check volume settings\n2. Test different outputs\n3. Update audio drivers\n4. Run audio troubleshooter\n5. Check audio services\n6. Test speakers/headphones',
                'category': 'hardware'
            },
            {
                'problem': 'Microphone not working',
                'solution': '1. Check privacy settings\n2. Test in Sound settings\n3. Update audio drivers\n4. Check app permissions\n5. Test different ports\n6. Verify default device',
                'category': 'hardware'
            },
            # Security Issues
            {
                'problem': 'Antivirus not updating',
                'solution': '1. Check internet connection\n2. Verify subscription status\n3. Temporarily disable firewall\n4. Run as administrator\n5. Repair installation\n6. Reinstall if necessary',
                'category': 'software'
            },
            {
                'problem': 'Suspicious pop-ups appearing',
                'solution': '1. Run full antivirus scan\n2. Check browser extensions\n3. Clear browser data\n4. Check startup programs\n5. Reset browser settings\n6. Use anti-malware tools',
                'category': 'software'
            },
            # Mac-Specific Issues
            {
                'problem': 'Mac kernel panic',
                'solution': '1. Check for software updates\n2. Disconnect peripherals\n3. Reset SMC\n4. Reset NVRAM/PRAM\n5. Test in Safe Mode\n6. Check system logs',
                'category': 'system'
            },
            {
                'problem': 'Mac spinning beachball',
                'solution': '1. Force quit frozen apps\n2. Check Activity Monitor\n3. Free up disk space\n4. Reset SMC\n5. Check RAM usage\n6. Repair disk permissions',
                'category': 'system'
            },
            # Keyboard/Mouse Issues
            {
                'problem': 'Keyboard keys not responding',
                'solution': '1. Check for debris\n2. Update keyboard drivers\n3. Test in Safe Mode\n4. Check language settings\n5. Try different USB port\n6. Test external keyboard',
                'category': 'hardware'
            },
            {
                'problem': 'Mouse cursor jumping',
                'solution': '1. Clean mouse sensor\n2. Update mouse drivers\n3. Check surface quality\n4. Test different USB port\n5. Adjust sensitivity\n6. Try different mouse',
                'category': 'hardware'
            },
            # Power Issues
            {
                'problem': 'Battery not charging',
                'solution': '1. Check power adapter\n2. Verify outlet works\n3. Reset power management\n4. Check battery health\n5. Update power drivers\n6. Service if under warranty',
                'category': 'hardware'
            },
            {
                'problem': 'Random shutdowns',
                'solution': '1. Check for overheating\n2. Test power supply\n3. Update system drivers\n4. Check event logs\n5. Test RAM integrity\n6. Monitor temperatures',
                'category': 'hardware'
            }
        ]
        
        self.data_dir = Path('data')
        self.data_dir.mkdir(exist_ok=True)
    
    def save_problems(self):
        """Save problems to JSON file"""
        output_file = self.data_dir / 'computer_problems.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.problems_solutions, f, indent=2)
        
        logger.info(f'Saved {len(self.problems_solutions)} problems to {output_file}')
        return self.problems_solutions

if __name__ == '__main__':
    scraper = ExpandedProblemScraper()
    problems = scraper.save_problems()