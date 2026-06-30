# scrapers/chevening_scraper.py

from typing import List, Dict
from scrapers.base_scraper import BaseScraper

try:
    from bs4 import BeautifulSoup
except ImportError:
    BeautifulSoup = None

import re

class CheveningScraper(BaseScraper):
    """Scraper for Chevening Scholarships"""
    
    SKIP_DOMAINS = [
        'facebook.com', 'instagram.com', 'twitter.com', 'x.com',
        'linkedin.com', 'youtube.com', 'tiktok.com', '#', 'javascript:', 'mailto:'
    ]
    
    def scrape(self, profile: Dict) -> List[Dict]:
        scholarships = []

        try:
            response = self.session.get(self.url, timeout=40)
            soup = BeautifulSoup(response.content, "lxml")
            seen_titles = set()

            items = soup.find_all("a", href=True)
            for a in items:
                text = a.get_text(strip=True)
                href = a.get('href', '')
                
                # Skip social media & noise
                if any(skip in href.lower() for skip in self.SKIP_DOMAINS):
                    continue
                if len(text) < 15 or len(text) > 200:
                    continue
                
                if any(word in text.lower() for word in ["scholarship", "chevening", "fellowship", "award"]):
                    normalized = text.lower().strip()
                    if normalized not in seen_titles:
                        seen_titles.add(normalized)
                        scholarships.append({
                            "title": text,
                            "country": "United Kingdom",
                            "degree": "Master's",
                            "field": "All fields",
                            "duration": "1 year",
                            "funding": "Full funding: tuition + monthly stipend + travel costs + settling-in allowance",
                            "eligibility": "Open to citizens of 160+ Chevening-eligible countries, 2+ years work experience",
                            "documents": "CV, references, motivation essays, undergraduate degree",
                            "deadline": "August-November 2025 (annually)",
                            "url": href if href.startswith("http") else self.url
                        })

        except Exception as e:
            print(f"Chevening error: {e}")

        if not scholarships:
            return self._get_fallback()
        return scholarships
    
    def _get_fallback(self) -> List[Dict]:
        """Return guaranteed Chevening scholarship entry"""
        return [{
            "title": "Chevening Scholarships - UK Government's Global Scholarship Programme",
            "country": "United Kingdom",
            "degree": "Master's",
            "field": "All fields",
            "duration": "1 year",
            "funding": "Full funding: tuition fees + monthly stipend (£1,133-£1,389) + travel costs + settling-in allowance",
            "eligibility": "Citizens of 160+ eligible countries, 2+ years work experience, return to home country for 2 years",
            "documents": "Bachelor's degree, CV, references, 4 essays, IELTS 6.5+/TOEFL 79+",
            "deadline": "August-November 2025 (annually)",
            "url": "https://www.chevening.org/scholarships/"
        }]