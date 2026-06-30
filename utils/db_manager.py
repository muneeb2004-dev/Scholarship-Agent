# utils/db_manager.py - Database management for Flask app

import sqlite3
import json
from datetime import datetime
from typing import Dict, List, Optional
import uuid
import os
import tempfile

class DatabaseManager:
    """Manages SQLite database for storing searches and statistics"""
    
    def __init__(self, db_path: str = None):
        if db_path is None:
            db_path = os.environ.get('DATABASE_PATH')

        if db_path is None:
            db_path = os.path.join(tempfile.gettempdir(), 'scholarships.db') if os.environ.get('VERCEL') else 'data/scholarships.db'

        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path) if os.path.dirname(db_path) else 'data', exist_ok=True)
    
    def init_db(self):
        """Initialize database tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Searches table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS searches (
                id TEXT PRIMARY KEY,
                profile TEXT NOT NULL,
                scholarships TEXT NOT NULL,
                count INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # User searches history
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS search_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                search_id TEXT NOT NULL,
                user_profile TEXT NOT NULL,
                result_count INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (search_id) REFERENCES searches(id)
            )
        ''')
        
        # Saved scholarships
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS saved_scholarships (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                scholarship_id TEXT UNIQUE NOT NULL,
                title TEXT NOT NULL,
                data TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # User interactions/events
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_type TEXT NOT NULL,
                event_data TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Statistics cache
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS statistics (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_search(self, profile: Dict, scholarships: List[Dict]) -> str:
        """Save a search and its results"""
        search_id = str(uuid.uuid4())
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO searches (id, profile, scholarships, count, created_at, updated_at)
                VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
            ''', (
                search_id,
                json.dumps(profile),
                json.dumps(scholarships),
                len(scholarships)
            ))
            
            # Log to history
            cursor.execute('''
                INSERT INTO search_history (search_id, user_profile, result_count, created_at)
                VALUES (?, ?, ?, CURRENT_TIMESTAMP)
            ''', (search_id, json.dumps(profile), len(scholarships)))
            
            conn.commit()
            return search_id
        
        finally:
            conn.close()
    
    def get_search(self, search_id: str) -> Optional[Dict]:
        """Retrieve a specific search"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT profile, scholarships, created_at 
                FROM searches WHERE id = ?
            ''', (search_id,))
            
            row = cursor.fetchone()
            
            if row:
                return {
                    'profile': json.loads(row[0]),
                    'scholarships': json.loads(row[1]),
                    'created_at': row[2]
                }
            
            return None
        
        finally:
            conn.close()
    
    def get_search_history(self, limit: int = 10) -> List[Dict]:
        """Get recent search history"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT search_id, user_profile, result_count, created_at
                FROM search_history
                ORDER BY created_at DESC
                LIMIT ?
            ''', (limit,))
            
            rows = cursor.fetchall()
            
            return [
                {
                    'search_id': row[0],
                    'profile': json.loads(row[1]),
                    'result_count': row[2],
                    'created_at': row[3]
                }
                for row in rows
            ]
        
        finally:
            conn.close()
    
    def save_scholarship(self, scholarship: Dict) -> bool:
        """Save a scholarship for later reference"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT OR IGNORE INTO saved_scholarships (scholarship_id, title, data, created_at)
                VALUES (?, ?, ?, CURRENT_TIMESTAMP)
            ''', (
                scholarship.get('id', str(uuid.uuid4())),
                scholarship.get('title', 'Untitled'),
                json.dumps(scholarship)
            ))
            
            conn.commit()
            return True
        
        except Exception as e:
            print(f"Error saving scholarship: {e}")
            return False
        
        finally:
            conn.close()
    
    def get_saved_scholarships(self) -> List[Dict]:
        """Get all saved scholarships"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT data FROM saved_scholarships
                ORDER BY created_at DESC
            ''')
            
            rows = cursor.fetchall()
            
            return [json.loads(row[0]) for row in rows]
        
        finally:
            conn.close()
    
    def log_event(self, event_type: str, event_data: Dict) -> bool:
        """Log a user event for analytics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO user_events (event_type, event_data, created_at)
                VALUES (?, ?, CURRENT_TIMESTAMP)
            ''', (event_type, json.dumps(event_data)))
            
            conn.commit()
            return True
        
        finally:
            conn.close()
    
    def get_statistics(self) -> Dict:
        """Get application statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Total searches
            cursor.execute('SELECT COUNT(*) FROM searches')
            total_searches = cursor.fetchone()[0]
            
            # Total scholarships found
            cursor.execute('SELECT SUM(count) FROM searches')
            total_scholarships = cursor.fetchone()[0] or 0
            
            # Average scholarships per search
            avg_scholarships = total_scholarships / max(total_searches, 1)
            
            # Most recent search
            cursor.execute('''
                SELECT created_at FROM searches 
                ORDER BY created_at DESC LIMIT 1
            ''')
            last_search = cursor.fetchone()
            
            # Most searched countries
            cursor.execute('''
                SELECT 
                    json_extract(profile, '$.country') as country,
                    COUNT(*) as count
                FROM searches
                GROUP BY country
                ORDER BY count DESC
                LIMIT 5
            ''')
            top_countries = [{'country': row[0], 'count': row[1]} for row in cursor.fetchall()]
            
            # Most searched fields
            cursor.execute('''
                SELECT 
                    json_extract(profile, '$.field_of_study') as field,
                    COUNT(*) as count
                FROM searches
                GROUP BY field
                ORDER BY count DESC
                LIMIT 5
            ''')
            top_fields = [{'field': row[0], 'count': row[1]} for row in cursor.fetchall()]
            
            return {
                'total_searches': total_searches,
                'total_scholarships_found': total_scholarships,
                'average_per_search': round(avg_scholarships, 2),
                'last_search': last_search[0] if last_search else None,
                'top_countries': top_countries,
                'top_fields': top_fields
            }
        
        finally:
            conn.close()
    
    def cleanup_old_searches(self, days: int = 30) -> int:
        """Delete searches older than specified days"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                DELETE FROM searches 
                WHERE created_at < datetime('now', '-' || ? || ' days')
            ''', (days,))
            
            deleted = cursor.rowcount
            conn.commit()
            return deleted
        
        finally:
            conn.close()


