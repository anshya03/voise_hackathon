"""
Database management for Prescription Conflict Checker
Handles user authentication and session management using SQLite
"""

import sqlite3
import bcrypt
import os
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import uuid

class DatabaseManager:
    def __init__(self, db_path: str = "prescription_checker.db"):
        """Initialize database manager"""
        self.db_path = db_path
        self.init_database()

    def init_database(self):
        """Create database tables if they don't exist"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Users table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_login TIMESTAMP,
                    is_active BOOLEAN DEFAULT 1
                )
            ''')
            
            # Sessions table for login management
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS sessions (
                    id TEXT PRIMARY KEY,
                    user_id INTEGER NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    expires_at TIMESTAMP NOT NULL,
                    is_active BOOLEAN DEFAULT 1,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            
            # Analysis history table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS analysis_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    doctor_a_medicines TEXT NOT NULL,
                    doctor_b_medicines TEXT NOT NULL,
                    interactions_found INTEGER NOT NULL,
                    risk_level TEXT NOT NULL,
                    analysis_result TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            
            conn.commit()
            
            # Create demo user if it doesn't exist
            self.create_demo_user()

    def create_demo_user(self):
        """Create demo user for testing"""
        try:
            demo_user = self.get_user_by_email('demo@example.com')
            if not demo_user:
                self.create_user('Demo User', 'demo@example.com', 'demo123')
                print("Demo user created: demo@example.com / demo123")
        except Exception as e:
            print(f"Error creating demo user: {e}")

    def hash_password(self, password: str) -> str:
        """Hash password using bcrypt"""
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')

    def verify_password(self, password: str, hashed: str) -> bool:
        """Verify password against hash"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

    def create_user(self, name: str, email: str, password: str) -> Dict[str, Any]:
        """Create new user"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Check if user already exists
                cursor.execute('SELECT id FROM users WHERE email = ?', (email,))
                if cursor.fetchone():
                    raise ValueError('User with this email already exists')
                
                # Hash password
                password_hash = self.hash_password(password)
                
                # Insert user
                cursor.execute('''
                    INSERT INTO users (name, email, password_hash)
                    VALUES (?, ?, ?)
                ''', (name, email, password_hash))
                
                user_id = cursor.lastrowid
                conn.commit()
                
                return {
                    'id': user_id,
                    'name': name,
                    'email': email,
                    'created_at': datetime.now().isoformat()
                }
        except Exception as e:
            raise Exception(f"Error creating user: {str(e)}")

    def authenticate_user(self, email: str, password: str) -> Optional[Dict[str, Any]]:
        """Authenticate user and return user data if successful"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT id, name, email, password_hash, last_login
                    FROM users 
                    WHERE email = ? AND is_active = 1
                ''', (email,))
                
                user = cursor.fetchone()
                
                if user and self.verify_password(password, user[3]):
                    # Update last login
                    cursor.execute('''
                        UPDATE users 
                        SET last_login = CURRENT_TIMESTAMP 
                        WHERE id = ?
                    ''', (user[0],))
                    conn.commit()
                    
                    return {
                        'id': user[0],
                        'name': user[1],
                        'email': user[2],
                        'last_login': user[4]
                    }
                
                return None
        except Exception as e:
            print(f"Error authenticating user: {e}")
            return None

    def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Get user by email"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT id, name, email, created_at, last_login
                    FROM users 
                    WHERE email = ? AND is_active = 1
                ''', (email,))
                
                user = cursor.fetchone()
                
                if user:
                    return {
                        'id': user[0],
                        'name': user[1],
                        'email': user[2],
                        'created_at': user[3],
                        'last_login': user[4]
                    }
                
                return None
        except Exception as e:
            print(f"Error getting user: {e}")
            return None

    def create_session(self, user_id: int) -> str:
        """Create user session and return session ID"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                session_id = str(uuid.uuid4())
                expires_at = datetime.now() + timedelta(days=7)  # Session expires in 7 days
                
                cursor.execute('''
                    INSERT INTO sessions (id, user_id, expires_at)
                    VALUES (?, ?, ?)
                ''', (session_id, user_id, expires_at))
                
                conn.commit()
                
                return session_id
        except Exception as e:
            print(f"Error creating session: {e}")
            return None

    def get_session_user(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get user from session ID"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT u.id, u.name, u.email, s.expires_at
                    FROM users u
                    JOIN sessions s ON u.id = s.user_id
                    WHERE s.id = ? AND s.is_active = 1 AND s.expires_at > CURRENT_TIMESTAMP
                ''', (session_id,))
                
                result = cursor.fetchone()
                
                if result:
                    return {
                        'id': result[0],
                        'name': result[1],
                        'email': result[2],
                        'session_expires': result[3]
                    }
                
                return None
        except Exception as e:
            print(f"Error getting session user: {e}")
            return None

    def invalidate_session(self, session_id: str):
        """Invalidate user session (logout)"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    UPDATE sessions 
                    SET is_active = 0 
                    WHERE id = ?
                ''', (session_id,))
                
                conn.commit()
        except Exception as e:
            print(f"Error invalidating session: {e}")

    def save_analysis_result(self, user_id: int, doctor_a_medicines: list, doctor_b_medicines: list, 
                           interactions_count: int, risk_level: str, full_result: dict):
        """Save analysis result to history"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                import json
                
                cursor.execute('''
                    INSERT INTO analysis_history 
                    (user_id, doctor_a_medicines, doctor_b_medicines, interactions_found, risk_level, analysis_result)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    user_id,
                    json.dumps(doctor_a_medicines),
                    json.dumps(doctor_b_medicines),
                    interactions_count,
                    risk_level,
                    json.dumps(full_result)
                ))
                
                conn.commit()
        except Exception as e:
            print(f"Error saving analysis result: {e}")

    def get_user_analysis_history(self, user_id: int, limit: int = 10) -> list:
        """Get user's analysis history"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT doctor_a_medicines, doctor_b_medicines, interactions_found, 
                           risk_level, created_at, analysis_result
                    FROM analysis_history
                    WHERE user_id = ?
                    ORDER BY created_at DESC
                    LIMIT ?
                ''', (user_id, limit))
                
                results = cursor.fetchall()
                
                import json
                history = []
                for result in results:
                    history.append({
                        'doctor_a_medicines': json.loads(result[0]),
                        'doctor_b_medicines': json.loads(result[1]),
                        'interactions_found': result[2],
                        'risk_level': result[3],
                        'date': result[4],
                        'full_result': json.loads(result[5])
                    })
                
                return history
        except Exception as e:
            print(f"Error getting analysis history: {e}")
            return []

    def cleanup_expired_sessions(self):
        """Clean up expired sessions"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    UPDATE sessions 
                    SET is_active = 0 
                    WHERE expires_at < CURRENT_TIMESTAMP
                ''')
                
                conn.commit()
        except Exception as e:
            print(f"Error cleaning up sessions: {e}")

    def get_user_stats(self, user_id: int) -> Dict[str, Any]:
        """Get user statistics"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Total analyses
                cursor.execute('''
                    SELECT COUNT(*) FROM analysis_history WHERE user_id = ?
                ''', (user_id,))
                total_analyses = cursor.fetchone()[0]
                
                # High risk analyses
                cursor.execute('''
                    SELECT COUNT(*) FROM analysis_history 
                    WHERE user_id = ? AND risk_level = 'HIGH'
                ''', (user_id,))
                high_risk_count = cursor.fetchone()[0]
                
                # Recent activity (last 30 days)
                cursor.execute('''
                    SELECT COUNT(*) FROM analysis_history 
                    WHERE user_id = ? AND created_at > datetime('now', '-30 days')
                ''', (user_id,))
                recent_analyses = cursor.fetchone()[0]
                
                return {
                    'total_analyses': total_analyses,
                    'high_risk_analyses': high_risk_count,
                    'recent_analyses': recent_analyses
                }
        except Exception as e:
            print(f"Error getting user stats: {e}")
            return {'total_analyses': 0, 'high_risk_analyses': 0, 'recent_analyses': 0}

# Example usage
if __name__ == "__main__":
    db = DatabaseManager()
    
    print("🔧 Database initialized successfully!")
    print("📊 Demo user available: demo@example.com / demo123")
    
    # Test creating a user
    try:
        user = db.create_user("Test User", "test@example.com", "password123")
        print(f"✅ Created test user: {user}")
    except Exception as e:
        print(f"ℹ️  Test user might already exist: {e}")
    
    # Test authentication
    auth_result = db.authenticate_user("demo@example.com", "demo123")
    if auth_result:
        print(f"✅ Authentication successful: {auth_result}")
    else:
        print("❌ Authentication failed")