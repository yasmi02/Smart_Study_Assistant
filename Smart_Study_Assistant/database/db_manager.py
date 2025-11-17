import sqlite3
import os
import pandas as pd
from datetime import datetime


class DatabaseManager:
    """Veritabanı işlemlerini yöneten sınıf"""

    def __init__(self):
        self.db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'study_assistant.db')
        self._ensure_db_exists()

    def _ensure_db_exists(self):
        """Veritabanının var olduğundan emin ol"""
        if not os.path.exists(self.db_path):
            from database.init_db import init_database
            init_database()

    def get_connection(self):
        """Veritabanı bağlantısı döndür"""
        return sqlite3.connect(self.db_path)

    def save_query(self, query_text, session_id="default"):
        """Kullanıcı sorgusunu kaydet"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO user_queries (query_text, user_session)
            VALUES (?, ?)
        ''', (query_text, session_id))

        query_id = cursor.lastrowid
        conn.commit()
        conn.close()

        return query_id

    def save_recommendations(self, query_id, recommendations):
        """Önerileri kaydet"""
        conn = self.get_connection()
        cursor = conn.cursor()

        for topic, score in recommendations:
            cursor.execute('''
                INSERT INTO recommendations (query_id, recommended_topic, similarity_score)
                VALUES (?, ?, ?)
            ''', (query_id, topic, float(score)))

        conn.commit()
        conn.close()

    def get_query_history(self, limit=50):
        """Sorgu geçmişini getir"""
        conn = self.get_connection()

        query = '''
            SELECT 
                id,
                query_text,
                query_date,
                user_session
            FROM user_queries
            ORDER BY query_date DESC
            LIMIT ?
        '''

        df = pd.read_sql_query(query, conn, params=(limit,))
        conn.close()

        return df

    def get_topic_statistics(self):
        """Konu istatistiklerini getir"""
        conn = self.get_connection()

        query = '''
            SELECT 
                query_text,
                search_count,
                last_searched
            FROM topic_statistics
            LIMIT 20
        '''

        df = pd.read_sql_query(query, conn)
        conn.close()

        return df

    def get_recommendations_for_query(self, query_id):
        """Belirli bir sorgu için önerileri getir"""
        conn = self.get_connection()

        query = '''
            SELECT 
                recommended_topic,
                similarity_score
            FROM recommendations
            WHERE query_id = ?
            ORDER BY similarity_score DESC
        '''

        df = pd.read_sql_query(query, conn, params=(query_id,))
        conn.close()

        return df

    def export_history_to_csv(self, filename="query_history.csv"):
        """Geçmişi graph olarak dışa aktar"""
        df = self.get_query_history(limit=1000)
        export_path = os.path.join(os.path.dirname(__file__), '..', 'data', filename)
        df.to_csv(export_path, index=False, encoding='utf-8')
        return export_path