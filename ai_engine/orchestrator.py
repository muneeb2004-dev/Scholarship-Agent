# ai_engine/orchestrator.py - WITH DEBUG LOGGING AND ADVANCED FEATURES

from typing import Dict, List, Optional
from scrapers.scraper_factory import ScraperFactory
from ai_engine.matcher import ProfileMatcher
from ai_engine.data_processor import DataProcessor
import concurrent.futures
from datetime import datetime, timedelta
import re

# Import recommendation engine if available, otherwise define placeholder
try:
    from ai_engine.recommendation_engine import RecommendationEngine
except ImportError:
    class RecommendationEngine:
        """Placeholder for recommendation engine"""
        def generate_recommendations(self, profile: Dict) -> List[Dict]:
            return []

class AIOrchestrator:
    """Main AI orchestration engine for scholarship search"""
    
    def __init__(self):
        self.matcher = ProfileMatcher()
        self.processor = DataProcessor()
        self.recommendation_engine = RecommendationEngine()
    
    def search_scholarships(self, profile: Dict, progress_callback=None) -> List[Dict]:
        """
        Main orchestration method for scholarship search
        
        Args:
            profile: User profile dictionary
            progress_callback: Optional callback for progress updates
        
        Returns:
            List of matched and ranked scholarships
        """
        print("\n" + "="*60)
        print("🚀 STARTING SCHOLARSHIP SEARCH")
        print("="*60)
        print(f"Profile: {profile}")
        print()
        
        # Step 1: Select appropriate scrapers
        scrapers = ScraperFactory.get_scrapers_by_country(profile.get('country', 'Any Country'))
        
        print(f"\n📋 Selected {len(scrapers)} scrapers:")
        for idx, scraper in enumerate(scrapers, 1):
            print(f"  {idx}. {scraper.name}")
        print()
        
        if progress_callback:
            progress_callback("Initializing scrapers...", 0.1)
        
        # Step 2: Execute parallel scraping
        all_scholarships = self._parallel_scrape(scrapers, profile, progress_callback)
        
        print(f"\n📊 RAW RESULTS: {len(all_scholarships)} scholarships scraped")
        
        if progress_callback:
            progress_callback(f"Found {len(all_scholarships)} scholarships", 0.6)
        
        # Step 3: Process and deduplicate
        processed = self.processor.process_scholarships(all_scholarships)
        
        print(f"✅ AFTER PROCESSING: {len(processed)} scholarships (after deduplication)")
        
        if progress_callback:
            progress_callback("Processing results...", 0.8)
        
        # Step 4: Match and rank
        matched = self.matcher.match_and_rank(processed, profile)
        
        print(f"🎯 FINAL MATCHES: {len(matched)} scholarships (after profile matching)")
        print()
        
        if matched:
            print("Top 5 Results:")
            for idx, sch in enumerate(matched[:5], 1):
                print(f"  {idx}. {sch.get('title', 'Unknown')} - {sch.get('match_score', 0):.0f}% match")
        else:
            print("⚠️  WARNING: No scholarships matched the profile!")
        
        print("\n" + "="*60)
        print("✅ SEARCH COMPLETE")
        print("="*60 + "\n")
        
        if progress_callback:
            progress_callback("Complete!", 1.0)
        
        return matched
    
    def _parallel_scrape(self, scrapers: List, profile: Dict, progress_callback=None) -> List[Dict]:
        """Execute scraping in parallel for faster results"""
        all_scholarships = []
        
        # Use ThreadPoolExecutor for parallel scraping
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            # Submit all scraping tasks
            future_to_scraper = {
                executor.submit(scraper.get_scholarships, profile): scraper 
                for scraper in scrapers
            }
            
            # Collect results as they complete
            completed = 0
            for future in concurrent.futures.as_completed(future_to_scraper):
                scraper = future_to_scraper[future]
                try:
                    scholarships = future.result(timeout=40)
                    all_scholarships.extend(scholarships)
                    
                    completed += 1
                    result_msg = f"  ✓ {scraper.name}: {len(scholarships)} scholarships"
                    print(result_msg)
                    
                    if progress_callback:
                        progress_pct = 0.1 + (completed / len(scrapers)) * 0.5
                        progress_callback(result_msg, progress_pct)
                        
                except Exception as e:
                    print(f"  ✗ {scraper.name}: FAILED - {str(e)}")
        
        return all_scholarships
    
    def filter_scholarships(self, scholarships: List[Dict], filters: Dict) -> List[Dict]:
        """
        Filter scholarships by advanced criteria
        
        Args:
            scholarships: List of scholarships to filter
            filters: Dictionary with filter criteria:
                - min_funding: minimum funding amount
                - max_deadline_days: deadline within N days
                - keywords: search keywords
                - degree_level: filter by degree
                - country: filter by country
        
        Returns:
            Filtered list of scholarships
        """
        filtered = scholarships
        
        # Filter by minimum funding
        min_funding = filters.get('min_funding')
        if min_funding:
            filtered = [s for s in filtered if self._parse_funding(s.get('funding', '')) >= min_funding]
        
        # Filter by deadline (within N days)
        max_deadline_days = filters.get('max_deadline_days')
        if max_deadline_days:
            filtered = [s for s in filtered if self._is_deadline_soon(s.get('deadline', ''), max_deadline_days)]
        
        # Filter by keywords
        keywords = filters.get('keywords', [])
        if keywords:
            filtered = [s for s in filtered if self._matches_keywords(s, keywords)]
        
        # Filter by degree level
        degree = filters.get('degree_level')
        if degree:
            filtered = [s for s in filtered if degree.lower() in s.get('degree', '').lower()]
        
        # Filter by country
        country = filters.get('country')
        if country:
            filtered = [s for s in filtered if country.lower() in s.get('country', '').lower()]
        
        return filtered
    
    def get_ai_recommendations(self, profile: Dict) -> List[Dict]:
        """
        Get AI-powered recommendations based on profile
        
        Args:
            profile: User profile with extended info
                - degree_level: desired degree
                - field_of_study: field of interest
                - nationality: user nationality
                - cgpa: academic performance
                - country: preferred country
                - work_experience_years: professional experience
                - research_interests: list of research topics
                - language_proficiency: languages spoken
        
        Returns:
            List of recommendations with rationale
        """
        return self.recommendation_engine.generate_recommendations(profile)
    
    def get_scholarship_details(self, scholarship_id: str) -> Optional[Dict]:
        """Fetch detailed information about a specific scholarship"""
        # This would normally query a database or make an API call
        # For now, returns a template
        return {
            'id': scholarship_id,
            'details': 'Implementation depends on your data source',
            'last_updated': datetime.now().isoformat()
        }
    
    def _parse_funding(self, funding_str: str) -> float:
        """Extract numeric funding amount from string"""
        try:
            numbers = re.findall(r'\d+(?:,\d{3})*(?:\.\d+)?', funding_str)
            if numbers:
                return float(numbers[0].replace(',', ''))
        except:
            pass
        return 0.0
    
    def _is_deadline_soon(self, deadline_str: str, days: int) -> bool:
        """Check if deadline is within specified number of days"""
        try:
            # Simple date parsing - may need enhancement based on actual format
            deadline = datetime.strptime(deadline_str, '%Y-%m-%d')
            days_left = (deadline - datetime.now()).days
            return 0 <= days_left <= days
        except:
            return True  # Include if date parsing fails
    
    def _matches_keywords(self, scholarship: Dict, keywords: List[str]) -> bool:
        """Check if scholarship matches any keywords"""
        text = f"{scholarship.get('title', '')} {scholarship.get('description', '')} {scholarship.get('field', '')}".lower()
        return any(kw.lower() in text for kw in keywords)