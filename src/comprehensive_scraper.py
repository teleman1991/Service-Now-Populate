import json
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ComprehensiveProblemScraper:
    def __init__(self):
        # Extended categories for better organization
        self.categories = {
            'hardware': ['input_devices', 'display', 'storage', 'power', 'printing', 'audio', 'connectivity'],
            'software': ['os', 'applications', 'browsers', 'email', 'security', 'drivers'],
            'network': ['connectivity', 'wifi', 'ethernet', 'vpn', 'sharing'],
            'system': ['performance', 'startup', 'updates', 'bsod', 'memory'],
            'security': ['malware', 'privacy', 'authentication', 'encryption'],
            'data': ['backup', 'recovery', 'synchronization', 'corruption']
        }
        
        # Comprehensive list of problems and solutions
        self.problems_solutions = [
            # HARDWARE - Input Devices
            {
                'problem': 'Keyboard keys not responding',
                'solution': '1. Check for debris under keys\n2. Update keyboard drivers\n3. Test in Safe Mode\n4. Check USB connection\n5. Verify language settings\n6. Test external keyboard',
                'category': 'hardware'
            },
            {
                'problem': 'Mouse cursor freezing',
                'solution': '1. Clean mouse sensor\n2. Check battery level\n3. Update mouse drivers\n4. Try different surface\n5. Test USB port\n6. Replace if needed',
                'category': 'hardware'
            },
            {
                'problem': 'Touchpad gestures not working',
                'solution': '1. Check touchpad settings\n2. Update touchpad drivers\n3. Enable multi-touch\n4. Reset touchpad settings\n5. Test in Safe Mode\n6. Check manufacturer settings',
                'category': 'hardware'
            },
            # HARDWARE - Display
            {
                'problem': 'Screen flickering',
                'solution': '1. Update graphics drivers\n2. Check refresh rate\n3. Test external monitor\n4. Verify cable connections\n5. Adjust power settings\n6. Check for interference',
                'category': 'hardware'
            },
            {
                'problem': 'External monitor not detected',
                'solution': '1. Check cable connections\n2. Update display drivers\n3. Try different port\n4. Press Windows+P\n5. Check monitor power\n6. Test different cable',
                'category': 'hardware'
            },
            {
                'problem': 'Screen resolution stuck',
                'solution': '1. Update graphics drivers\n2. Check display adapter\n3. Reset display settings\n4. Test in Safe Mode\n5. Check monitor capabilities\n6. Reinstall graphics drivers',
                'category': 'hardware'
            },
            # HARDWARE - Storage
            {
                'problem': 'Hard drive making clicking sounds',
                'solution': '1. Backup data immediately\n2. Check SMART status\n3. Run disk diagnostics\n4. Verify connections\n5. Test power supply\n6. Plan for replacement',
                'category': 'hardware'
            },
            {
                'problem': 'SSD performance degradation',
                'solution': '1. Check drive health\n2. Enable TRIM\n3. Update firmware\n4. Optimize drive\n5. Check temperature\n6. Verify SATA mode',
                'category': 'hardware'
            },
            {
                'problem': 'External drive not recognized',
                'solution': '1. Try different USB port\n2. Check power supply\n3. Update drivers\n4. Test on another PC\n5. Check disk management\n6. Try different cable',
                'category': 'hardware'
            },
            # HARDWARE - Power
            {
                'problem': 'Battery not charging',
                'solution': '1. Check power adapter\n2. Verify outlet works\n3. Reset power system\n4. Check battery health\n5. Update BIOS\n6. Service if needed',
                'category': 'hardware'
            },
            {
                'problem': 'Random shutdowns',
                'solution': '1. Check temperatures\n2. Test power supply\n3. Update drivers\n4. Check event logs\n5. Test RAM\n6. Clean internal components',
                'category': 'hardware'
            },
            {
                'problem': 'Power button not responding',
                'solution': '1. Check connections\n2. Reset power settings\n3. Test button mechanism\n4. Check motherboard\n5. Update BIOS\n6. Service if needed',
                'category': 'hardware'
            },
            # HARDWARE - Printing
            {
                'problem': 'Printer offline',
                'solution': '1. Check connections\n2. Verify network settings\n3. Reset print spooler\n4. Update drivers\n5. Power cycle printer\n6. Reinstall printer',
                'category': 'hardware'
            },
            {
                'problem': 'Print quality issues',
                'solution': '1. Clean print heads\n2. Check ink levels\n3. Run alignment\n4. Use quality settings\n5. Check paper type\n6. Service if needed',
                'category': 'hardware'
            },
            {
                'problem': 'Paper jams',
                'solution': '1. Clear all paper\n2. Check paper path\n3. Use correct paper\n4. Clean rollers\n5. Check alignment\n6. Service if frequent',
                'category': 'hardware'
            },
            # SOFTWARE - Operating System
            {
                'problem': 'Windows boot failure',
                'solution': '1. Use startup repair\n2. Check boot sequence\n3. Repair MBR\n4. Check disk errors\n5. Restore system\n6. Clean install if needed',
                'category': 'software'
            },
            {
                'problem': 'Blue screen errors',
                'solution': '1. Note error code\n2. Update drivers\n3. Check memory\n4. Scan system files\n5. Check updates\n6. Reset Windows',
                'category': 'software'
            },
            {
                'problem': 'System file corruption',
                'solution': '1. Run SFC scan\n2. Check disk\n3. Restore system\n4. Update Windows\n5. Repair install\n6. Clean install',
                'category': 'software'
            },
            # SOFTWARE - Applications
            {
                'problem': 'Program crashes on startup',
                'solution': '1. Run as admin\n2. Update program\n3. Check compatibility\n4. Clear app data\n5. Reinstall program\n6. Update Windows',
                'category': 'software'
            },
            {
                'problem': 'Application not responding',
                'solution': '1. Wait briefly\n2. Force close\n3. Check resources\n4. Update app\n5. Clear cache\n6. Reinstall',
                'category': 'software'
            },
            {
                'problem': 'Program installation fails',
                'solution': '1. Check requirements\n2. Run as admin\n3. Disable antivirus\n4. Clear temp files\n5. Check disk space\n6. Use compatibility mode',
                'category': 'software'
            },
            # SOFTWARE - Browsers
            {
                'problem': 'Browser crashes frequently',
                'solution': '1. Update browser\n2. Clear cache\n3. Disable extensions\n4. Check malware\n5. Reset settings\n6. Reinstall browser',
                'category': 'software'
            },
            {
                'problem': 'Slow web browsing',
                'solution': '1. Clear history\n2. Check connection\n3. Disable extensions\n4. Reset browser\n5. Update browser\n6. Check DNS settings',
                'category': 'software'
            },
            {
                'problem': 'Homepage changed without permission',
                'solution': '1. Check malware\n2. Reset settings\n3. Remove extensions\n4. Check startup items\n5. Clear registry\n6. Reinstall browser',
                'category': 'software'
            },
            # NETWORK - Connectivity
            {
                'problem': 'No internet access',
                'solution': '1. Check connections\n2. Restart modem\n3. Verify settings\n4. Test other devices\n5. Reset network\n6. Contact ISP',
                'category': 'network'
            },
            {
                'problem': 'Intermittent connection',
                'solution': '1. Check signal\n2. Update drivers\n3. Check interference\n4. Test different channel\n5. Reset equipment\n6. Contact ISP',
                'category': 'network'
            },
            {
                'problem': 'Slow network speed',
                'solution': '1. Test speeds\n2. Check usage\n3. Verify plan\n4. Update drivers\n5. Check hardware\n6. Contact ISP',
                'category': 'network'
            },
            # NETWORK - WiFi
            {
                'problem': 'WiFi not connecting',
                'solution': '1. Check password\n2. Forget network\n3. Reset adapter\n4. Update drivers\n5. Check router\n6. Reset network',
                'category': 'network'
            },
            {
                'problem': 'Weak WiFi signal',
                'solution': '1. Check distance\n2. Remove obstacles\n3. Change channel\n4. Update drivers\n5. Check antenna\n6. Add repeater',
                'category': 'network'
            },
            {
                'problem': 'WiFi keeps disconnecting',
                'solution': '1. Update drivers\n2. Check power settings\n3. Reset adapter\n4. Change channel\n5. Update firmware\n6. Replace adapter',
                'category': 'network'
            },
            # SYSTEM - Performance
            {
                'problem': 'System running slow',
                'solution': '1. Check resources\n2. Clear temp files\n3. Remove malware\n4. Update system\n5. Defrag HDD\n6. Upgrade hardware',
                'category': 'system'
            },
            {
                'problem': 'High CPU usage',
                'solution': '1. Check processes\n2. Update programs\n3. Scan malware\n4. Check cooling\n5. Reset Windows\n6. Test hardware',
                'category': 'system'
            },
            {
                'problem': 'High disk usage',
                'solution': '1. Check processes\n2. Disable services\n3. Update Windows\n4. Check drive\n5. Reset indexing\n6. Replace drive',
                'category': 'system'
            },
            # Add more problems here...
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
    scraper = ComprehensiveProblemScraper()
    problems = scraper.save_problems()