"""AI integration features for WhatsApp Bot"""

import json
import sqlite3
from datetime import datetime
from typing import List, Dict, Optional
import os

try:
    import openai
    from transformers import pipeline
    from cryptography.fernet import Fernet
    from dotenv import load_dotenv
    
    # Load environment variables
    load_dotenv()
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False
    print(
        "AI features not available. Install requirements: pip install -r requirements.txt"
    )


class AIMessageAssistant:
    """AI-powered message generation and optimization"""

    def __init__(self):
        self.openai_client = None
        self.sentiment_analyzer = None
        self.translator = None

        if AI_AVAILABLE and os.getenv("OPENAI_API_KEY"):
            openai.api_key = os.getenv("OPENAI_API_KEY")
            self.openai_client = openai.OpenAI()

        if AI_AVAILABLE:
            try:
                self.sentiment_analyzer = pipeline("sentiment-analysis")
                self.translator = pipeline(
                    "translation", model="Helsinki-NLP/opus-mt-en-mul"
                )
            except Exception as e:
                print(f"Could not load AI models: {e}")

    async def generate_message_suggestions(
        self, context: str, tone: str = "professional"
    ) -> List[str]:
        """Generate AI-powered message suggestions"""
        if not self.openai_client:
            return [
                "AI features not configured. Please set OPENAI_API_KEY in .env file."
            ]

        try:
            prompt = f"""
            Generate 3 WhatsApp message suggestions with a {tone} tone for this context: {context}
            Keep messages concise, engaging, and appropriate for WhatsApp.
            Return as JSON array of strings.
            """

            response = await self.openai_client.chat.completions.acreate(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=200,
            )

            suggestions = json.loads(response.choices[0].message.content)
            return suggestions if isinstance(suggestions, list) else [suggestions]

        except Exception as e:
            return [f"Error generating suggestions: {str(e)}"]

    def analyze_sentiment(self, message: str) -> Dict:
        """Analyze message sentiment"""
        if not self.sentiment_analyzer:
            return {"label": "NEUTRAL", "score": 0.5}

        try:
            result = self.sentiment_analyzer(message)[0]
            return {
                "label": result["label"],
                "score": result["score"],
                "recommendation": self._get_tone_recommendation(result),
            }
        except Exception as e:
            return {"error": str(e)}

    def _get_tone_recommendation(self, sentiment_result: Dict) -> str:
        """Get tone recommendations based on sentiment"""
        if sentiment_result["label"] == "NEGATIVE" and sentiment_result["score"] > 0.8:
            return "Consider using a more positive or neutral tone"
        elif sentiment_result["label"] == "POSITIVE":
            return "Great! Your message has a positive tone"
        else:
            return "Message tone is neutral"


class SmartScheduler:
    """AI-optimized scheduling system"""

    def __init__(self):
        self.db_path = "whatsapp_bot.db"
        self.init_database()

    def init_database(self):
        """Initialize SQLite database for analytics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS message_analytics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            phone_number TEXT,
            send_time TIMESTAMP,
            delivered BOOLEAN,
            read BOOLEAN,
            response_time INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        )

        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS optimal_times (
            phone_number TEXT PRIMARY KEY,
            best_hour INTEGER,
            best_day_of_week INTEGER,
            timezone TEXT,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        )

        conn.commit()
        conn.close()

    def get_optimal_send_time(self, phone_number: str) -> Dict:
        """Get AI-recommended optimal send time for a contact"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Get historical data for this contact
        cursor.execute(
            """
        SELECT AVG(CASE WHEN delivered = 1 THEN 1.0 ELSE 0.0 END) as delivery_rate,
               AVG(response_time) as avg_response_time,
               strftime('%H', send_time) as hour
        FROM message_analytics 
        WHERE phone_number = ? 
        GROUP BY strftime('%H', send_time)
        ORDER BY delivery_rate DESC, avg_response_time ASC
        LIMIT 1
        """,
            (phone_number,),
        )

        result = cursor.fetchone()
        conn.close()

        if result and result[0] is not None:
            return {
                "optimal_hour": int(result[2]),
                "delivery_rate": result[0],
                "avg_response_time": result[1],
                "confidence": "high" if result[0] > 0.8 else "medium",
            }
        else:
            # Default optimal times based on general WhatsApp usage patterns
            now = datetime.now()
            default_hours = [10, 14, 19]  # 10 AM, 2 PM, 7 PM
            return {
                "optimal_hour": min(default_hours, key=lambda x: abs(x - now.hour)),
                "delivery_rate": 0.75,
                "avg_response_time": 300,
                "confidence": "low",
            }

    def log_message_analytics(
        self,
        phone_number: str,
        send_time: datetime,
        delivered: bool = True,
        read: bool = False,
        response_time: Optional[int] = None,
    ):
        """Log message analytics for AI learning"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
        INSERT INTO message_analytics (phone_number, send_time, delivered, read, response_time)
        VALUES (?, ?, ?, ?, ?)
        """,
            (phone_number, send_time, delivered, read, response_time),
        )

        conn.commit()
        conn.close()


class SecurityManager:
    """Enhanced security features for 2025"""

    def __init__(self):
        self.encryption_key = os.getenv("ENCRYPTION_KEY")
        if self.encryption_key:
            self.fernet = Fernet(self.encryption_key.encode())
        else:
            # Generate a new key if none provided
            key = Fernet.generate_key()
            self.fernet = Fernet(key)
            print(f"Generated new encryption key: {key.decode()}")
            print("Add this to your .env file as ENCRYPTION_KEY")

    def encrypt_contact(self, phone_number: str) -> str:
        """Encrypt sensitive contact information"""
        try:
            encrypted = self.fernet.encrypt(phone_number.encode())
            return encrypted.decode()
        except Exception as e:
            print(f"Encryption error: {e}")
            return phone_number

    def decrypt_contact(self, encrypted_phone: str) -> str:
        """Decrypt contact information"""
        try:
            decrypted = self.fernet.decrypt(encrypted_phone.encode())
            return decrypted.decode()
        except Exception as e:
            print(f"Decryption error: {e}")
            return encrypted_phone

    def validate_secure_input(self, input_data: str) -> bool:
        """Validate input for security threats"""
        dangerous_patterns = [
            "script",
            "javascript:",
            "onload=",
            "onerror=",
            "../",
            "..\\",
            "/etc/passwd",
            "cmd.exe",
        ]

        input_lower = input_data.lower()
        for pattern in dangerous_patterns:
            if pattern in input_lower:
                return False
        return True


class ModernAnalytics:
    """Advanced analytics and reporting"""

    def __init__(self):
        self.db_path = "whatsapp_bot.db"

    def generate_delivery_report(self) -> Dict:
        """Generate comprehensive delivery analytics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Overall statistics
        cursor.execute(
            """
        SELECT 
            COUNT(*) as total_messages,
            AVG(CASE WHEN delivered = 1 THEN 1.0 ELSE 0.0 END) as delivery_rate,
            AVG(CASE WHEN read = 1 THEN 1.0 ELSE 0.0 END) as read_rate,
            AVG(response_time) as avg_response_time
        FROM message_analytics
        WHERE send_time > datetime('now', '-30 days')
        """
        )

        stats = cursor.fetchone()

        # Peak hours analysis
        cursor.execute(
            """
        SELECT 
            strftime('%H', send_time) as hour,
            COUNT(*) as message_count,
            AVG(CASE WHEN delivered = 1 THEN 1.0 ELSE 0.0 END) as success_rate
        FROM message_analytics
        WHERE send_time > datetime('now', '-30 days')
        GROUP BY strftime('%H', send_time)
        ORDER BY success_rate DESC
        """
        )

        peak_hours = cursor.fetchall()
        conn.close()

        return {
            "period": "Last 30 days",
            "total_messages": stats[0] or 0,
            "delivery_rate": round((stats[1] or 0) * 100, 2),
            "read_rate": round((stats[2] or 0) * 100, 2),
            "avg_response_time": round(stats[3] or 0, 2),
            "best_hours": [
                {"hour": h[0], "success_rate": round(h[2] * 100, 2)}
                for h in peak_hours[:3]
            ]
            if peak_hours
            else [],
        }


# Global instances - only create if AI dependencies are available
if AI_AVAILABLE:
    ai_assistant = AIMessageAssistant()
    smart_scheduler = SmartScheduler()
    security_manager = SecurityManager()
    analytics = ModernAnalytics()
else:
    ai_assistant = None
    smart_scheduler = None
    security_manager = None
    analytics = None
