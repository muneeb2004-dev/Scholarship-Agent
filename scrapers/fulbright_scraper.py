# scrapers/fulbright_scraper.py

from typing import List, Dict
from scrapers.base_scraper import BaseScraper

try:
    from bs4 import BeautifulSoup
except ImportError:
    BeautifulSoup = None

class FulbrightScraper(BaseScraper):
    """Scraper for Fulbright Foreign Student Program"""
    
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

            links = soup.find_all("a", href=True)

            for link in links:
                text = link.get_text(strip=True)
                href = link.get('href', '')
                text_lower = text.lower()
                
                # Skip social media & noise
                if any(skip in href.lower() for skip in self.SKIP_DOMAINS):
                    continue
                if len(text) < 15 or len(text) > 200:
                    continue
                
                if "fulbright" in text_lower or ("scholar" in text_lower and len(text) > 20):
                    normalized = text_lower.strip()
                    if normalized not in seen_titles:
                        seen_titles.add(normalized)
                        scholarships.append({
                            "title": text,
                            "country": "United States",
                            "degree": "Master's/PhD",
                            "field": "All fields",
                            "duration": "1-5 years",
                            "funding": "Full funding: tuition + monthly stipend + health insurance + airfare",
                            "eligibility": "International applicants with Bachelor's degree",
                            "documents": "GRE/TOEFL, transcripts, essays, references",
                            "deadline": "October 2025 (varies by country)",
                            "url": href if href.startswith("http") else self.url
                        })

        except Exception as e:
            print(f"Fulbright scraper error: {e}")

        if not scholarships:
            return self._get_fallback()
        return scholarships
    
    def _get_fallback(self) -> List[Dict]:
        """Return guaranteed Fulbright entry"""
        return [{
            "title": "Fulbright Foreign Student Program",
            "country": "United States",
            "degree": "Master's/PhD",
            "field": "All fields",
            "duration": "1-2 years (Master's), 3-5 years (PhD)",
            "funding": "Full scholarship: tuition + monthly stipend + health insurance + roundtrip airfare",
            "eligibility": "International students with Bachelor's degree, strong academic record, leadership potential",
            "documents": "GRE scores, TOEFL/IELTS, academic transcripts, 3 essays, 3 references, CV",
            "deadline": "October 2025 (varies by country)",
            "url": "https://foreign.fulbrightonline.org/"
        }]
