# scrapers/commonwealth_scraper.py

from typing import List, Dict
from scrapers.base_scraper import BaseScraper

try:
    from bs4 import BeautifulSoup
except ImportError:
    BeautifulSoup = None

import re

class CommonwealthScraper(BaseScraper):
    """Scraper for Commonwealth Scholarships"""
    
    def scrape(self, profile: Dict) -> List[Dict]:
        scholarships = []

        try:
            response = self.session.get(self.url, timeout=40)
            soup = BeautifulSoup(response.content, "lxml")
            seen_titles = set()

            posts = soup.find_all("article")

            for p in posts:
                title_elem = p.find(["h2", "h3"])
                if not title_elem:
                    continue

                title = title_elem.get_text(strip=True)
                
                if len(title) < 15:
                    continue

                if "scholar" in title.lower() or "commonwealth" in title.lower():
                    normalized = title.lower().strip()
                    if normalized not in seen_titles:
                        seen_titles.add(normalized)
                        a = p.find("a", href=True)
                        link = a["href"] if a else self.url

                        scholarships.append({
                            "title": title,
                            "country": "United Kingdom",
                            "degree": "Master's/PhD",
                            "field": "All fields",
                            "duration": "1–3 years",
                            "funding": "Full scholarship: tuition + monthly stipend (£1,347) + airfare + thesis grant",
                            "eligibility": "Commonwealth citizens from eligible countries",
                            "documents": "References, research proposal, academic transcripts",
                            "deadline": "October-December 2025 (annually)",
                            "url": link
                        })

        except Exception as e:
            print(f"Commonwealth error: {e}")

        if not scholarships:
            return self._get_fallback()
        return scholarships
    
    def _get_fallback(self) -> List[Dict]:
        """Return guaranteed Commonwealth scholarship entry"""
        return [{
            "title": "Commonwealth Scholarships and Fellowships (CSC UK)",
            "country": "United Kingdom",
            "degree": "Master's/PhD",
            "field": "All fields",
            "duration": "Master's: 1 year, PhD: up to 3 years",
            "funding": "Full scholarship: tuition + £1,347/month stipend + airfare + thesis grant + arrival allowance",
            "eligibility": "Citizens of Commonwealth countries, strong academic record, commitment to development",
            "documents": "Academic transcripts, references, research proposal (PhD), development impact statement",
            "deadline": "October-December 2025 (annually)",
            "url": "https://cscuk.fcdo.gov.uk/scholarships/"
        }]
