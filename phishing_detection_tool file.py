# phishing_detection_tool.py
# Phishing Detection Tool in Python

import re
import requests
from urllib.parse import urlparse

# List of common phishing keywords
phishing_keywords = ['login', 'verify', 'bank', 'update', 'password', 'secure', 'account']

# Function to check URL structure
def check_url_structure(url):
    # Check for IP address instead of domain name
    ip_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
    if re.search(ip_pattern, url):
        return True
    # Check for suspicious characters
    if '@' in url or '//' in url[8:]:
        return True
    return False

# Function to check for phishing keywords
def check_phishing_keywords(url):
    for keyword in phishing_keywords:
        if keyword in url.lower():
            return True
    return False

# Function to check SSL certificate
def check_ssl(url):
    try:
        if url.startswith('http://'):
            return False
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return True
    except:
        return False
    return False

# Main detection function
def detect_phishing(url):
    flags = []
    if check_url_structure(url):
        flags.append('Suspicious URL structure')
    if check_phishing_keywords(url):
        flags.append('Contains phishing keywords')
    if not check_ssl(url):
        flags.append('No valid SSL certificate')

    if flags:
        print(f'⚠️ Potential phishing detected for URL: {url}')
        print('Reasons:')
        for reason in flags:
            print('-', reason)
    else:
        print(f'✅ URL appears safe: {url}')

# User input
if __name__ == '__main__':
    print('--- Phishing Detection Tool ---')
    user_url = input('Enter URL to check: ')
    detect_phishing(user_url)
