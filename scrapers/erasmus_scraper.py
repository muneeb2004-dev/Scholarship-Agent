# scrapers/erasmus_scraper.py

from typing import List, Dict
from scrapers.base_scraper import BaseScraper

try:
    from bs4 import BeautifulSoup
except ImportError:
    BeautifulSoup = None

import re

class ErasmusScraper(BaseScraper):
    """Scraper for Erasmus+ study abroad opportunities"""
    
    # URLs/domains to skip (social media, non-scholarship pages)
    SKIP_DOMAINS = [
        'facebook.com', 'instagram.com', 'twitter.com', 'x.com',
        'linkedin.com', 'youtube.com', 'tiktok.com', 'pinterest.com',
        'flickr.com', '#', 'javascript:', 'mailto:'
    ]
    
    def scrape(self, profile: Dict) -> List[Dict]:
        scholarships = []

        try:
            response = self.session.get(self.url, timeout=45)
            soup = BeautifulSoup(response.content, "lxml")

            listings = soup.find_all("a", href=True)
            seen_titles = set()

            for a in listings:
                href = a.get('href', '')
                text = a.get_text(strip=True)
                text_lower = text.lower()
                
                # Skip social media and noise links
                if any(skip in href.lower() for skip in self.SKIP_DOMAINS):
                    continue
                
                # Skip very short or very long titles
                if len(text) < 15 or len(text) > 200:
                    continue
                
                # Skip navigation/UI elements
                if text_lower in ('home', 'about', 'contact', 'login', 'menu', 'search', 
                                   'subscribe', 'share', 'follow us', 'cookie policy',
                                   'privacy policy', 'terms', 'sitemap'):
                    continue

                # Must be scholarship-related
                if any(k in text_lower for k in ["erasmus", "scholarship", "mobility", "study abroad"]):
                    # Normalize title to avoid duplicates
                    normalized = re.sub(r'\s+', ' ', text).strip()
                    if normalized.lower() not in seen_titles:
                        seen_titles.add(normalized.lower())
                        scholarships.append({
                            "title": normalized,
                            "country": "Europe (multiple countries)",
                            "degree": "Bachelor's/Master's",
                            "field": "All fields",
                            "duration": "3–12 months",
                            "funding": "Monthly stipend + travel support",
                            "eligibility": "Students enrolled in partner universities",
                            "documents": "Transcript, learning agreement",
                            "deadline": "Rolling deadlines (check programme)",
                            "url": href if href.startswith("http") else self.url
                        })

        except Exception as e:
            print(f"Erasmus error: {e}")

        # If scraping found nothing useful, return a curated fallback
        if not scholarships:
            return self._get_fallback()
        
        return scholarships
    
    def _get_fallback(self) -> List[Dict]:
        """Return a curated Erasmus+ scholarship entry"""
        return [{
            "title": "Erasmus Mundus Joint Master Degrees",
            "country": "Europe (multiple countries)",
            "degree": "Master's",
            "field": "All fields (varies by programme)",
            "duration": "12-24 months",
            "funding": "Full scholarship: up to €1,400/month + travel + tuition waiver + insurance",
            "eligibility": "Bachelor's degree holders from any country, language proficiency required",
            "documents": "Academic transcripts, language certificates, CV, motivation letter, references",
            "deadline": "October 2025 - January 2026 (varies by programme)",
            "url": "https://www.eacea.ec.europa.eu/scholarships/erasmus-mundus-catalogue_en"
        }]
