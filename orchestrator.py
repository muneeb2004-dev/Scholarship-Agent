# ai_engine/data_processor.py - SMART DEDUPLICATION

from typing import List, Dict
import hashlib
import re

class DataProcessor:
    """Process and clean scholarship data"""
    
    # Known scholarship families - entries with these keywords belong together
    SCHOLARSHIP_FAMILIES = {
        'daad': ['daad', 'german academic exchange'],
        'erasmus': ['erasmus', 'erasmus+', 'erasmus mundus', 'erasmus plus'],
        'fulbright': ['fulbright'],
        'chevening': ['chevening'],
        'commonwealth': ['commonwealth scholarship', 'commonwealth fellowship'],
        'hec_overseas': ['hec overseas'],
        'hec_indigenous': ['hec indigenous', 'ipdp'],
        'hec_nrpu': ['hec nrpu', 'nrpu'],
        'hec_commonwealth': ['hec commonwealth'],
        'hec_csc': ['hec chinese', 'hec csc', 'chinese government scholarship'],
        'hec_usaid': ['hec usaid'],
        'hec_turkey': ['hec turkey', 'türkiye bursları'],
        'hec_mext': ['hec japan', 'hec mext', 'mext scholarship'],
        'hec_france': ['hec france', 'campus france'],
        'hec_daad': ['hec-daad', 'hec daad'],
        'gssp': ['graduate school scholarship programme', 'gssp'],
        'epos': ['epos scholarship', 'development-related postgraduate'],
    }
    
    def process_scholarships(self, scholarships: List[Dict]) -> List[Dict]:
        """
        Process scholarships: clean, deduplicate, validate
        """
        print(f"\n🔧 DATA PROCESSING:")
        print(f"  Input: {len(scholarships)} scholarships")
        
        # Step 1: Remove invalid entries
        valid_scholarships = [s for s in scholarships if self._is_valid(s)]
        print(f"  After validation: {len(valid_scholarships)} scholarships")
        
        # Step 2: Smart deduplication 
        unique_scholarships = self._smart_deduplicate(valid_scholarships)
        print(f"  After deduplication: {len(unique_scholarships)} scholarships")
        
        # Step 3: Standardize fields
        standardized = [self._standardize(s) for s in unique_scholarships]
        print(f"  After standardization: {len(standardized)} scholarships")
        
        # Step 4: Normalize deadlines to include year
        for s in standardized:
            s['deadline'] = self._normalize_deadline(s.get('deadline', ''))
        
        return standardized
    
    def _is_valid(self, scholarship: Dict) -> bool:
        """Check if scholarship has minimum required data"""
        title = scholarship.get('title', '').strip()
        
        if not title or len(title) < 5:
            print(f"    ⚠️  Invalid: {title or 'NO TITLE'}")
            return False
        
        # Filter out non-scholarship content (nav links, social media, generic pages)
        noise_patterns = [
            r'^(home|about|contact|login|sign up|subscribe|follow us)$',
            r'^(facebook|instagram|twitter|linkedin|youtube|x\.com)$',
            r'^(cookie|privacy|terms|menu|navigation|search|share)$',
            r'^.{0,10}$',  # Too short titles
        ]
        title_lower = title.lower().strip()
        for pattern in noise_patterns:
            if re.match(pattern, title_lower, re.I):
                print(f"    ⚠️  Noise filtered: {title}")
                return False
        
        return True
    
    def _smart_deduplicate(self, scholarships: List[Dict]) -> List[Dict]:
        """Smart deduplication using multiple strategies"""
        # Step 1: Group by scholarship family
        family_groups = {}  # family_key -> list of scholarships
        ungrouped = []
        
        for sch in scholarships:
            family = self._identify_family(sch)
            if family:
                sub_key = self._get_sub_key(sch, family)
                full_key = f"{family}:{sub_key}"
                if full_key not in family_groups:
                    family_groups[full_key] = []
                family_groups[full_key].append(sch)
            else:
                ungrouped.append(sch)
        
        # Step 2: Pick best entry from each family group
        unique = []
        for key, group in family_groups.items():
            best = self._pick_best_entry(group)
            unique.append(best)
            if len(group) > 1:
                print(f"    🔄 Merged {len(group)} entries for: {best.get('title', 'Unknown')[:60]}")
        
        # Step 3: Deduplicate ungrouped by title similarity
        seen_titles = set()
        for sch in ungrouped:
            normalized = self._normalize_title(sch.get('title', ''))
            if normalized not in seen_titles:
                seen_titles.add(normalized)
                unique.append(sch)
            else:
                print(f"    🔄 Duplicate removed: {sch.get('title', 'Unknown')[:60]}")
        
        return unique
    
    def _identify_family(self, scholarship: Dict) -> str:
        """Identify which scholarship family an entry belongs to"""
        title = scholarship.get('title', '').lower()
        url = scholarship.get('url', '').lower()
        combined = f"{title} {url}"
        
        for family_key, keywords in self.SCHOLARSHIP_FAMILIES.items():
            for keyword in keywords:
                if keyword in combined:
                    return family_key
        
        return ''
    
    def _get_sub_key(self, scholarship: Dict, family: str) -> str:
        """Get a sub-key within a family to distinguish genuinely different scholarships.
        E.g., DAAD GSSP vs DAAD EPOS are different scholarships in the 'daad' family."""
        title = scholarship.get('title', '').lower()
        degree = scholarship.get('degree', '').lower()
        
        # For DAAD, distinguish by specific programme name
        if family == 'daad':
            if 'gssp' in title or 'graduate school' in title:
                return 'gssp'
            elif 'epos' in title or 'development-related' in title:
                return 'epos'
            elif 'study scholarship' in title or 'all disciplines' in title:
                return 'study'
            elif 'research grant' in title:
                return 'research'
            elif 'stibet' in title:
                return 'stibet'
            else:
                return 'general'
        
        # For HEC, distinguish by specific programme
        if family.startswith('hec_'):
            return family  # Already specific enough
        
        # For Erasmus, group everything together
        if family == 'erasmus':
            return 'main'
        
        # Default: use degree level as sub-key
        return degree or 'general'
    
    def _pick_best_entry(self, group: List[Dict]) -> Dict:
        """Pick the best/most detailed entry from a group of duplicates"""
        if len(group) == 1:
            return group[0]
        
        # Score each entry by completeness
        def completeness_score(sch):
            score = 0
            for field in ['title', 'country', 'degree', 'field', 'duration', 
                         'funding', 'eligibility', 'documents', 'deadline', 'url']:
                value = sch.get(field, '')
                if value and value not in ('N/A', 'Varies', 'Not specified', 'See website', 
                                           'Check website', 'Various', 'Rolling', 'Rolling deadlines'):
                    score += len(str(value))  # Longer = more detailed
            return score
        
        # Return the most detailed entry, merging URLs as alternate_urls
        group.sort(key=completeness_score, reverse=True)
        best = group[0].copy()
        
        # Collect all unique URLs from duplicates
        all_urls = list(set(sch.get('url', '') for sch in group if sch.get('url')))
        if len(all_urls) > 1:
            best['alternate_urls'] = all_urls
        
        return best
    
    def _normalize_title(self, title: str) -> str:
        """Normalize a title for comparison"""
        title = title.lower().strip()
        # Remove common noise words
        noise_words = ['scholarship', 'scholarships', 'program', 'programme', 
                       'the', 'and', 'for', 'in', 'at', 'to', 'of', 'on',
                       '-', '–', '—', '(', ')', ',', '.']
        for word in noise_words:
            title = title.replace(word, ' ')
        # Collapse whitespace
        title = re.sub(r'\s+', ' ', title).strip()
        # Take first 5 significant words
        words = title.split()[:5]
        return ' '.join(words)
    
    def _normalize_deadline(self, deadline: str) -> str:
        """Ensure deadline has a year. Add 2025/2026 if missing."""
        if not deadline or deadline in ('N/A', 'Not specified', 'Varies', 'Check website', 
                                         'Rolling', 'Rolling deadlines', 'Varies by program',
                                         'Varies by programme', 'Open year-round'):
            return deadline
        
        # If it already has a 4-digit year (2024-2030), keep it
        # But replace 2024 with 2025 since 2024 is past
        year_match = re.search(r'20(\d{2})', deadline)
        if year_match:
            year = int('20' + year_match.group(1))
            if year < 2025:
                deadline = deadline.replace(str(year), '2025')
            return deadline
        
        # No year found - add one
        # Determine if the month is in the future or past to choose 2025 or 2026
        from datetime import datetime
        current_month = datetime.now().month
        
        month_names = {
            'january': 1, 'february': 2, 'march': 3, 'april': 4,
            'may': 5, 'june': 6, 'july': 7, 'august': 8,
            'september': 9, 'october': 10, 'november': 11, 'december': 12,
            'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4,
            'jun': 6, 'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12
        }
        
        deadline_lower = deadline.lower()
        for month_name, month_num in month_names.items():
            if month_name in deadline_lower:
                year = 2025 if month_num >= current_month else 2026
                return f"{deadline} {year}"
        
        # Can't determine month, just append 2025
        return f"{deadline} (2025/2026)"
    
    def _standardize(self, scholarship: Dict) -> Dict:
        """Standardize scholarship fields"""
        standardized = scholarship.copy()
        
        # Standardize country names
        standardized['country'] = self._standardize_country(scholarship.get('country', ''))
        
        # Standardize degree levels
        standardized['degree'] = self._standardize_degree(scholarship.get('degree', ''))
        
        # Clean text fields
        for field in ['title', 'field', 'duration', 'funding', 'eligibility', 'documents']:
            if field in standardized:
                standardized[field] = self._clean_text(standardized[field])
        
        # Ensure URL is absolute
        url = standardized.get('url', '')
        if url and not url.startswith('http'):
            standardized['url'] = 'https://' + url
        
        return standardized
    
    def _standardize_country(self, country: str) -> str:
        """Standardize country names"""
        country_map = {
            'usa': 'United States',
            'uk': 'United Kingdom',
            'us': 'United States',
            'britain': 'United Kingdom',
            'deutschland': 'Germany',
        }
        
        country_lower = country.lower().strip()
        return country_map.get(country_lower, country.strip())
    
    def _standardize_degree(self, degree: str) -> str:
        """Standardize degree level names"""
        degree_lower = degree.lower()
        
        if 'bachelor' in degree_lower or 'undergraduate' in degree_lower:
            return "Bachelor's"
        elif 'master' in degree_lower or 'postgraduate' in degree_lower:
            return "Master's"
        elif 'phd' in degree_lower or 'doctoral' in degree_lower or 'doctorate' in degree_lower:
            return 'PhD'
        elif 'postdoc' in degree_lower:
            return 'Postdoctoral'
        
        return degree
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        if not text:
            return 'Not specified'
        
        # Remove excessive whitespace
        text = ' '.join(text.split())
        
        # Remove HTML entities if any
        text = text.replace('&nbsp;', ' ')
        text = text.replace('&amp;', '&')
        
        return text.strip()