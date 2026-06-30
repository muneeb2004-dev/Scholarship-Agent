# scrapers/online_scholarships_scraper.py - RELIABLE ONLINE SCRAPER

from typing import List, Dict
from scrapers.base_scraper import BaseScraper
import feedparser
import requests
import re

class OnlineScholarshipsScraper(BaseScraper):
    """Scraper for online scholarship databases using APIs and RSS feeds"""

    def scrape(self, profile: Dict) -> List[Dict]:
        """Scrape from multiple online sources"""
        scholarships = []
        
        # Try Scholars4Dev RSS
        scholarships.extend(self._scrape_scholars4dev())
        
        # Try Opportunities Corners RSS
        scholarships.extend(self._scrape_opportunities())
        
        # Try Youth Opportunities RSS
        scholarships.extend(self._scrape_youth_opportunities())
        
        print(f"    ✓ Online Scholarships: {len(scholarships)} scholarships")
        return scholarships if scholarships else self._get_fallback_scholarships()

    def _scrape_scholars4dev(self) -> List[Dict]:
        """Parse Scholars4Dev RSS feed"""
        scholarships = []
        try:
            feed = feedparser.parse("https://www.scholars4dev.com/feed/")
            
            for entry in feed.entries[:20]:  # Limit to 20 latest
                try:
                    scholarship = {
                        'title': entry.get('title', 'Unknown'),
                        'url': entry.get('link', ''),
                        'country': 'Multiple',
                        'degree': 'Various',
                        'field': 'All fields',
                        'funding': 'Partial/Full',
                        'deadline': entry.get('published', 'Rolling'),
                        'eligibility': 'Check website',
                        'documents': 'See official website',
                        'description': entry.get('summary', '')[:200]
                    }
                    
                    # Extract country from description if possible
                    if entry.get('summary'):
                        desc = entry['summary'].lower()
                        if 'germany' in desc or 'daad' in desc:
                            scholarship['country'] = 'Germany'
                        elif 'uk' in desc or 'britain' in desc or 'chevening' in desc:
                            scholarship['country'] = 'United Kingdom'
                        elif 'canada' in desc:
                            scholarship['country'] = 'Canada'
                        elif 'australia' in desc:
                            scholarship['country'] = 'Australia'
                        elif 'usa' in desc or 'united states' in desc or 'fulbright' in desc:
                            scholarship['country'] = 'United States'
                    
                    scholarships.append(scholarship)
                except Exception as e:
                    continue
                    
        except Exception as e:
            print(f"      Scholars4Dev error: {e}")
        
        return scholarships

    def _scrape_opportunities(self) -> List[Dict]:
        """Parse Opportunities Corners RSS feed"""
        scholarships = []
        try:
            feed = feedparser.parse("https://opportunitiescorners.com/feed/")
            
            for entry in feed.entries[:20]:
                try:
                    scholarship = {
                        'title': entry.get('title', 'Unknown'),
                        'url': entry.get('link', ''),
                        'country': 'Multiple',
                        'degree': 'Various',
                        'field': 'All fields',
                        'funding': 'Varies',
                        'deadline': entry.get('published', 'Rolling'),
                        'eligibility': 'Check website',
                        'documents': 'See official website',
                        'description': entry.get('summary', '')[:200]
                    }
                    
                    scholarships.append(scholarship)
                except:
                    continue
                    
        except Exception as e:
            print(f"      Opportunities Corners error: {e}")
        
        return scholarships

    def _scrape_youth_opportunities(self) -> List[Dict]:
        """Parse Youth Opportunities RSS feed"""
        scholarships = []
        try:
            feed = feedparser.parse("https://www.youthopportunities.com/feed/")
            
            for entry in feed.entries[:20]:
                try:
                    scholarship = {
                        'title': entry.get('title', 'Unknown'),
                        'url': entry.get('link', ''),
                        'country': 'Global',
                        'degree': 'Various',
                        'field': 'Multiple',
                        'funding': 'Varies',
                        'deadline': entry.get('published', 'Rolling'),
                        'eligibility': 'Check website',
                        'documents': 'See official website',
                        'description': entry.get('summary', '')[:200]
                    }
                    
                    scholarships.append(scholarship)
                except:
                    continue
                    
        except Exception as e:
            print(f"      Youth Opportunities error: {e}")
        
        return scholarships

    def _get_fallback_scholarships(self) -> List[Dict]:
        """Fallback scholarships when scraping fails"""
        return [
            {
                'title': 'DAAD Scholarships - Germany',
                'country': 'Germany',
                'degree': "Master's",
                'field': 'All fields',
                'funding': 'Full scholarship: €934-1,200/month + health insurance + travel',
                'deadline': 'October 2025 (annually)',
                'url': 'https://www2.daad.de/deutschland/stipendium/datenbank/en/21148-scholarship-database/',
                'eligibility': "Bachelor's degree required, English/German language proficiency",
                'documents': 'Academic records, language certificate, motivation letter, CV'
            },
            {
                'title': 'Fulbright Foreign Student Program - USA',
                'country': 'United States',
                'degree': "Master's/PhD",
                'field': 'All fields',
                'funding': 'Full scholarship: tuition + living stipend + health insurance + airfare',
                'deadline': 'October 2025 (annually)',
                'url': 'https://foreign.fulbrightonline.org/',
                'eligibility': "Bachelor's degree, TOEFL/IELTS, work experience preferred",
                'documents': 'Academic transcripts, English language test scores, CV, study plan'
            },
            {
                'title': 'Chevening Scholarships - UK',
                'country': 'United Kingdom',
                'degree': "Master's",
                'field': 'All fields',
                'funding': 'Full scholarship: tuition + monthly stipend + travel costs',
                'deadline': 'November 2025 (annually)',
                'url': 'https://www.chevening.org/',
                'eligibility': "Bachelor's degree, 2+ years work experience, return to home country",
                'documents': 'Academic records, employment records, references, essays'
            },
            {
                'title': 'Erasmus Mundus Joint Masters - Europe',
                'country': 'Europe (multiple countries)',
                'degree': "Master's",
                'field': 'All fields',
                'funding': 'Full scholarship: tuition + €1,400/month + travel + insurance',
                'deadline': 'January 2026 (varies by programme)',
                'url': 'https://www.eacea.ec.europa.eu/scholarships/erasmus-mundus-catalogue_en',
                'eligibility': "Bachelor's degree, language proficiency (English/programme language)",
                'documents': 'Transcripts, language certificate, motivation letter, CV, references'
            }
        ]
