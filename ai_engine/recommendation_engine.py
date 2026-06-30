# ai_engine/recommendation_engine.py - AI-powered recommendation system

from typing import Dict, List, Optional
from datetime import datetime, timedelta
import json

class RecommendationEngine:
    """Advanced AI recommendation engine for scholarship suggestions"""
    
    def __init__(self):
        self.country_tiers = self._init_country_tiers()
        self.field_specializations = self._init_field_specializations()
    
    def _init_country_tiers(self) -> Dict:
        """Initialize country ranking based on research opportunities"""
        return {
            'tier1': ['Germany', 'Switzerland', 'Netherlands', 'United Kingdom', 'United States'],
            'tier2': ['Canada', 'Australia', 'Sweden', 'Denmark', 'Norway'],
            'tier3': ['France', 'Japan', 'South Korea', 'Singapore', 'New Zealand']
        }
    
    def _init_field_specializations(self) -> Dict:
        """Initialize field-specific recommendations"""
        return {
            'Computer Science & IT': {
                'top_countries': ['Germany', 'Netherlands', 'United States', 'Canada'],
                'avg_min_cgpa': 3.5,
                'preferred_skills': ['Python', 'Java', 'C++', 'Machine Learning']
            },
            'Engineering & Technology': {
                'top_countries': ['Germany', 'Switzerland', 'Netherlands', 'United States'],
                'avg_min_cgpa': 3.5,
                'preferred_skills': ['CAD', 'MATLAB', 'Project Management']
            },
            'Business & Management': {
                'top_countries': ['United Kingdom', 'United States', 'Canada', 'Australia'],
                'avg_min_cgpa': 3.3,
                'preferred_skills': ['Leadership', 'Finance', 'Marketing']
            },
            'Medicine & Health Sciences': {
                'top_countries': ['United Kingdom', 'United States', 'Australia', 'Canada'],
                'avg_min_cgpa': 3.6,
                'preferred_skills': ['Research', 'Clinical Skills', 'Medical Knowledge']
            },
            'Natural Sciences': {
                'top_countries': ['Germany', 'Switzerland', 'Netherlands', 'United Kingdom'],
                'avg_min_cgpa': 3.5,
                'preferred_skills': ['Research', 'Laboratory Techniques', 'Data Analysis']
            }
        }
    
    def generate_recommendations(self, profile: Dict) -> List[Dict]:
        """
        Generate AI recommendations based on user profile
        
        Returns list of recommendation objects with rationale
        """
        recommendations = []
        
        # Get field-specific recommendations
        field = profile.get('field_of_study', 'All Fields')
        specialization = self.field_specializations.get(field, {})
        
        # Recommendation 1: Best countries for field
        if specialization.get('top_countries'):
            recommendations.append({
                'type': 'country_recommendation',
                'title': f'Top Countries for {field}',
                'countries': specialization['top_countries'],
                'rationale': f'These countries have excellent programs and funding for {field}',
                'priority': 'high'
            })
        
        # Recommendation 2: CGPA-based opportunities
        cgpa_rec = self._get_cgpa_recommendations(profile, specialization)
        if cgpa_rec:
            recommendations.append(cgpa_rec)
        
        # Recommendation 3: Timeline-based recommendations
        timeline_rec = self._get_timeline_recommendations(profile)
        if timeline_rec:
            recommendations.append(timeline_rec)
        
        # Recommendation 4: Competitive advantages
        advantages_rec = self._get_competitive_advantages(profile)
        if advantages_rec:
            recommendations.append(advantages_rec)
        
        # Recommendation 5: Alternative options
        alternatives_rec = self._get_alternative_options(profile)
        if alternatives_rec:
            recommendations.append(alternatives_rec)
        
        return recommendations
    
    def _get_cgpa_recommendations(self, profile: Dict, specialization: Dict) -> Optional[Dict]:
        """Get CGPA-based recommendations"""
        cgpa = profile.get('cgpa', 0)
        min_cgpa = specialization.get('avg_min_cgpa', 3.0)
        
        if cgpa >= min_cgpa + 0.3:
            return {
                'type': 'cgpa_strength',
                'title': 'Your Strong Academic Profile',
                'message': f'Your CGPA of {cgpa} is excellent for {profile.get("field_of_study", "your field")}. You can target top-tier scholarships.',
                'priority': 'high'
            }
        elif cgpa >= min_cgpa:
            return {
                'type': 'cgpa_competitive',
                'title': 'Competitive Academic Profile',
                'message': f'Your CGPA of {cgpa} is competitive. Focus on research, projects, and personal statement to strengthen your application.',
                'priority': 'medium'
            }
        else:
            return {
                'type': 'cgpa_improvement',
                'title': 'Recommendations for CGPA',
                'message': f'Consider scholarships focused on work experience, diversity, or field-specific opportunities. Aim to improve CGPA to {min_cgpa}+',
                'priority': 'medium'
            }
    
    def _get_timeline_recommendations(self, profile: Dict) -> Optional[Dict]:
        """Get recommendations based on optimal timeline"""
        current_date = datetime.now()
        
        return {
            'type': 'timeline',
            'title': 'Application Timeline Strategy',
            'recommendations': [
                {
                    'period': 'Next 1-2 months',
                    'actions': [
                        'Research scholarships and eligibility',
                        'Gather required documents',
                        'Prepare statements of purpose'
                    ]
                },
                {
                    'period': 'Next 2-4 months',
                    'actions': [
                        'Apply to early deadline scholarships',
                        'Prepare for standardized tests (GRE/GMAT/IELTS)',
                        'Request recommendation letters'
                    ]
                },
                {
                    'period': 'Next 4-6 months',
                    'actions': [
                        'Submit most applications',
                        'Follow up on application status',
                        'Prepare for interviews'
                    ]
                }
            ],
            'priority': 'high'
        }
    
    def _get_competitive_advantages(self, profile: Dict) -> Optional[Dict]:
        """Identify competitive advantages in profile"""
        advantages = []
        
        # Check for unique characteristics
        if profile.get('work_experience_years', 0) > 3:
            advantages.append(f"Strong work experience ({profile['work_experience_years']} years)")
        
        if profile.get('cgpa', 0) >= 3.7:
            advantages.append("Excellent academic record")
        
        if profile.get('research_interests'):
            advantages.append("Defined research interests")
        
        if profile.get('language_proficiency'):
            langs = profile['language_proficiency']
            if len(langs) > 1:
                advantages.append(f"Multilingual ({', '.join(langs)})")
        
        if advantages:
            return {
                'type': 'advantages',
                'title': 'Your Competitive Advantages',
                'advantages': advantages,
                'message': 'Highlight these in your applications',
                'priority': 'high'
            }
        
        return None
    
    def _get_alternative_options(self, profile: Dict) -> Optional[Dict]:
        """Suggest alternative countries/options if primary choice is too competitive"""
        alternatives = []
        
        # Get tier of preferred country
        preferred = profile.get('country', '')
        tier = self._get_country_tier(preferred)
        
        if tier == 'tier1':
            alternatives = {
                'primary': f'{preferred} (Highly Competitive)',
                'alternatives': 'tier2',
                'message': 'Also apply to Tier 2 countries as backup options'
            }
        elif tier == 'tier2':
            alternatives = {
                'primary': f'{preferred} (Competitive)',
                'alternatives': 'tier3 or regional',
                'message': 'Broaden your search to include more countries'
            }
        
        if alternatives:
            return {
                'type': 'alternatives',
                'title': 'Balanced Application Strategy',
                'data': alternatives,
                'priority': 'medium'
            }
        
        return None
    
    def _get_country_tier(self, country: str) -> str:
        """Get tier of a country"""
        for tier, countries in self.country_tiers.items():
            if country in countries:
                return tier
        return 'other'
    
    def get_personalized_scholarships(self, profile: Dict, scholarships: List[Dict]) -> List[Dict]:
        """
        Rank scholarships based on personalized fit
        
        Takes into account profile strengths and opportunities
        """
        scored_scholarships = []
        
        for scholarship in scholarships:
            base_score = scholarship.get('match_score', 0)
            
            # Bonus for work experience match
            if profile.get('work_experience_years', 0) > 0 and 'experience' in scholarship.get('eligibility', '').lower():
                base_score += 5
            
            # Bonus for research interest alignment
            interests = profile.get('research_interests', [])
            if interests and any(interest.lower() in scholarship.get('title', '').lower() for interest in interests):
                base_score += 10
            
            scholarship['personalized_score'] = min(base_score, 100)
            scored_scholarships.append(scholarship)
        
        # Sort by personalized score
        scored_scholarships.sort(key=lambda x: x['personalized_score'], reverse=True)
        
        return scored_scholarships
