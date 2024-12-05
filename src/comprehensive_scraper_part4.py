# Final set of problems and solutions

final_problems = [
    # OFFICE APPLICATIONS
    {
        'problem': 'Excel not responding',
        'solution': '1. Disable add-ins\n2. Clear Excel temp\n3. Repair Office\n4. Check file size\n5. Save as new file\n6. Reinstall Office',
        'category': 'software'
    },
    {
        'problem': 'Word document corruption',
        'solution': '1. Use auto-recover\n2. Open in safe mode\n3. Repair document\n4. Convert format\n5. Extract content\n6. Restore backup',
        'category': 'software'
    },
    {
        'problem': 'PowerPoint not playing media',
        'solution': '1. Update codecs\n2. Check format\n3. Embed media\n4. Convert files\n5. Update Office\n6. Repair installation',
        'category': 'software'
    },
    # DATABASE
    {
        'problem': 'Database connection lost',
        'solution': '1. Check network\n2. Verify credentials\n3. Test connection\n4. Reset services\n5. Check firewall\n6. Contact DBA',
        'category': 'software'
    },
    {
        'problem': 'SQL Server performance issues',
        'solution': '1. Check queries\n2. Update statistics\n3. Check indexes\n4. Monitor resources\n5. Clear cache\n6. Optimize database',
        'category': 'software'
    },
    {
        'problem': 'Database backup failing',
        'solution': '1. Check space\n2. Verify permissions\n3. Test backup path\n4. Check logs\n5. Manual backup\n6. Contact support',
        'category': 'data'
    },
    # LINUX SPECIFIC
    {
        'problem': 'Linux boot failure',
        'solution': '1. Check GRUB\n2. Update kernel\n3. Check fstab\n4. Boot recovery\n5. Check logs\n6. Repair boot',
        'category': 'system'
    },
    {
        'problem': 'Package manager broken',
        'solution': '1. Update repos\n2. Clear cache\n3. Fix dependencies\n4. Force update\n5. Check sources\n6. Repair database',
        'category': 'software'
    },
    {
        'problem': 'X server not starting',
        'solution': '1. Check logs\n2. Update drivers\n3. Check config\n4. Reset X\n5. Check GPU\n6. Reinstall desktop',
        'category': 'system'
    },
    # ENTERPRISE
    {
        'problem': 'Active Directory sync issues',
        'solution': '1. Check connectivity\n2. Verify credentials\n3. Test ports\n4. Check services\n5. Reset sync\n6. Contact admin',
        'category': 'network'
    },
    {
        'problem': 'Group Policy not applying',
        'solution': '1. gpupdate /force\n2. Check WMI\n3. Verify links\n4. Test connectivity\n5. Check logs\n6. Reset policy',
        'category': 'system'
    },
    {
        'problem': 'Certificate errors',
        'solution': '1. Check expiry\n2. Verify trust\n3. Update chain\n4. Clear cache\n5. Reissue cert\n6. Contact CA',
        'category': 'security'
    },
    # VIRTUALIZATION
    {
        'problem': 'Hyper-V creation failed',
        'solution': '1. Check resources\n2. Verify permissions\n3. Update Hyper-V\n4. Check logs\n5. Reset service\n6. Rebuild VM',
        'category': 'system'
    },
    {
        'problem': 'VMware tools issues',
        'solution': '1. Reinstall tools\n2. Update VM\n3. Check compatibility\n4. Reset services\n5. Update host\n6. Rebuild tools',
        'category': 'software'
    },
    {
        'problem': 'Virtual network down',
        'solution': '1. Check switches\n2. Reset network\n3. Update drivers\n4. Verify settings\n5. Test connectivity\n6. Rebuild network',
        'category': 'network'
    },
    # HARDWARE FAILURES
    {
        'problem': 'Memory test failures',
        'solution': '1. Run memtest86\n2. Test individual sticks\n3. Check slots\n4. Clean contacts\n5. Update BIOS\n6. Replace RAM',
        'category': 'hardware'
    },
    {
        'problem': 'CPU overheating',
        'solution': '1. Clean heatsink\n2. Replace paste\n3. Check fan\n4. Monitor temps\n5. Check load\n6. Replace cooler',
        'category': 'hardware'
    },
    {
        'problem': 'Motherboard not posting',
        'solution': '1. Check power\n2. Clear CMOS\n3. Test components\n4. Check beep codes\n5. Flash BIOS\n6. Replace board',
        'category': 'hardware'
    },
    # MOBILE DEVICE MANAGEMENT
    {
        'problem': 'MDM enrollment failing',
        'solution': '1. Check connectivity\n2. Verify credentials\n3. Reset enrollment\n4. Update MDM\n5. Check compatibility\n6. Contact support',
        'category': 'system'
    },
    {
        'problem': 'Device policy conflicts',
        'solution': '1. Review policies\n2. Check precedence\n3. Update policy\n4. Reset device\n5. Clear cache\n6. Reapply policy',
        'category': 'security'
    },
    {
        'problem': 'Mobile app deployment failed',
        'solution': '1. Check package\n2. Verify signing\n3. Test deployment\n4. Check space\n5. Update MDM\n6. Manual install',
        'category': 'software'
    },
    # CLOUD SERVICES
    {
        'problem': 'Azure AD sync issues',
        'solution': '1. Check connector\n2. Verify credentials\n3. Test connection\n4. Update client\n5. Reset sync\n6. Contact support',
        'category': 'network'
    },
    {
        'problem': 'AWS instance unavailable',
        'solution': '1. Check status\n2. Verify network\n3. Check security\n4. Test connection\n5. Restart instance\n6. Contact AWS',
        'category': 'network'
    },
    {
        'problem': 'Cloud storage quota exceeded',
        'solution': '1. Check usage\n2. Clear cache\n3. Remove old files\n4. Upgrade plan\n5. Archive data\n6. Contact admin',
        'category': 'storage'
    }
]