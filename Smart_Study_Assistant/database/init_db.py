import sqlite3
import os
from datetime import datetime


# bu yer uygulama ilk kez çalıştırır ama sonra çok çalışmaz. uygulamanın ilk adımları için çok önemli.

def init_database():
    """Veritabanını başlatır ve gerekli tabloları oluşturur"""

    # veritabanı yolunu belirle
    db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'study_assistant.db')

    #bağlantı oluştur
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    #kullanıcı sorguları tablosu
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_queries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query_text TEXT NOT NULL,
            query_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            user_session TEXT
        )
    ''')

    #önerilen konular tablosu
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS recommendations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query_id INTEGER,
            recommended_topic TEXT NOT NULL,
            similarity_score REAL,
            FOREIGN KEY (query_id) REFERENCES user_queries(id)
        )
    ''')

    #istatistikler fln
    cursor.execute('''
        CREATE VIEW IF NOT EXISTS topic_statistics AS
        SELECT 
            query_text,
            COUNT(*) as search_count,
            MAX(query_date) as last_searched
        FROM user_queries
        GROUP BY query_text
        ORDER BY search_count DESC
    ''')

    conn.commit()
    conn.close()

    print("✅ Veritabanı başarıyla oluşturuldu!")


if __name__ == "__main__":
    init_database()