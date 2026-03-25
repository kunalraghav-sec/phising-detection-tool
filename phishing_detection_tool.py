# phishing_detection_tool.py

"""Phishing Detection Tool core logic.
Provides a callable `analyze_url` function for backend integration.
"""

import re
import requests
from urllib.parse import urlparse

# List of common phishing keywords
phishing_keywords = ['login', 'verify', 'bank', 'update', 'password', 'secure', 'account']


def check_url_structure(url):
    """Return True if URL looks suspicious based on structure."""
    # Check for IP address instead of domain name
    ip_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
    if re.search(ip_pattern, url):
        return True
    # Check for suspicious characters
    if '@' in url or '//' in url[8:]:
        return True
    return False


def check_phishing_keywords(url):
    """Return True if any phishing keyword appears in the URL."""
    for keyword in phishing_keywords:
        if keyword in url.lower():
            return True
    return False


def check_ssl(url):
    """Return True if the URL uses HTTPS and responds with status 200."""
    try:
        if url.startswith('http://'):
            return False
        response = requests.get(url, timeout=5)
        return response.status_code == 200
    except Exception:
        return False


def analyze_url(url):
    """Analyze a URL and return a dict with results.
    Returns:
        {
            "url": str,
            "is_phishing": bool,
            "reasons": list of strings,
            "confidence": float (0-1)
        }
    """
    reasons = []
    if check_url_structure(url):
        reasons.append('Suspicious URL structure')
    if check_phishing_keywords(url):
        reasons.append('Contains phishing keywords')
    if not check_ssl(url):
        reasons.append('No valid SSL certificate')
    is_phishing = len(reasons) > 0
    confidence = min(1.0, len(reasons) * 0.33)
    return {
        'url': url,
        'is_phishing': is_phishing,
        'reasons': reasons,
        'confidence': confidence
    }


def detect_phishing(url):
    """CLI helper that prints results to console."""
    result = analyze_url(url)
    if result['is_phishing']:
        print(f"⚠️ Potential phishing detected for URL: {url}")
        print('Reasons:')
        for r in result['reasons']:
            print('-', r)
    else:
        print(f"✅ URL appears safe: {url}")


if __name__ == '__main__':
    print('--- Phishing Detection Tool ---')
    user_url = input('Enter URL to check: ')
    detect_phishing(user_url)
