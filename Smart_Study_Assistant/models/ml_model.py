import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Tuple
from models.text_processor import TextProcessor


class MLModel:
    """Makine öğrenmesi modeli sınıfı"""

    def __init__(self):
        self.text_processor = TextProcessor()
        self.vectorizer = TfidfVectorizer(
            max_features=100,
            ngram_range=(1, 2),  # Unigram ve bigram
            lowercase=True
        )

        # Modeli eğit
        self._train_model()

    def _train_model(self):
        """Modeli örnek verilerle eğit"""
        topics = self.text_processor.get_all_topics()
        keywords = self.text_processor.get_all_keywords()

        # Konu isimleri ve anahtar kelimeleri birleştir
        self.topic_texts = [f"{topic} {keyword}" for topic, keyword in zip(topics, keywords)]
        self.topic_names = topics

        # TF-IDF matrisi oluştur
        self.tfidf_matrix = self.vectorizer.fit_transform(self.topic_texts)

    def get_recommendations(self, query: str, top_n: int = 5) -> List[Tuple[str, float]]:
        """
        Sorguya göre en benzer konuları öner

        Args:
            query: Kullanıcının sorgusu
            top_n: Döndürülecek öneri sayısı

        Returns:
            [(konu_adı, benzerlik_skoru), ...] listesi
        """
        # Sorguyu temizle ve genişlet
        cleaned_query = self.text_processor.clean_text(query)
        expanded_query = self.text_processor.expand_query(cleaned_query)

        # Sorguyu vektörize et
        query_vector = self.vectorizer.transform([expanded_query])

        # Kosinüs benzerliği hesapla
        similarities = cosine_similarity(query_vector, self.tfidf_matrix)[0]

        # En yüksek skorları bul
        top_indices = np.argsort(similarities)[-top_n:][::-1]

        # Sonuçları hazırla
        recommendations = []
        for idx in top_indices:
            if similarities[idx] > 0.01:  # Minimum benzerlik eşiği
                recommendations.append((
                    self.topic_names[idx],
                    float(similarities[idx])
                ))

        return recommendations

    def get_similar_topics(self, topic_name: str, top_n: int = 3) -> List[Tuple[str, float]]:
        """
        Belirli bir konuya benzer konuları bul

        Args:
            topic_name: Konu adı
            top_n: Döndürülecek benzer konu sayısı

        Returns:
            [(benzer_konu, benzerlik_skoru), ...] listesi
        """
        try:
            # Konunun indeksini bul
            topic_idx = self.topic_names.index(topic_name)

            # Bu konuyla diğer konular arasındaki benzerliği hesapla
            topic_vector = self.tfidf_matrix[topic_idx]
            similarities = cosine_similarity(topic_vector, self.tfidf_matrix)[0]

            # Kendisini hariç tut ve en benzer konuları bul
            similarities[topic_idx] = -1  # Kendisini -1 yap
            top_indices = np.argsort(similarities)[-top_n:][::-1]

            similar_topics = []
            for idx in top_indices:
                if similarities[idx] > 0:
                    similar_topics.append((
                        self.topic_names[idx],
                        float(similarities[idx])
                    ))

            return similar_topics

        except ValueError:
            return []

    def analyze_query_intent(self, query: str) -> dict:
        """
        Sorgu niyetini analiz et

        Returns:
            {
                'intent': 'learning' | 'comparison' | 'question',
                'confidence': float,
                'keywords': List[str]
            }
        """
        query_lower = query.lower()

        #keywordler fln
        learning_keywords = ['öğrenmek', 'öğrenme', 'nasıl', 'başlangıç', 'temel']
        comparison_keywords = ['fark', 'karşılaştır', 'hangisi', 'vs', 'versus']
        question_keywords = ['nedir', 'ne', 'neden', 'kim', 'hangi']

        intent = 'learning'
        confidence = 0.5

        if any(keyword in query_lower for keyword in learning_keywords):
            intent = 'learning'
            confidence = 0.8
        elif any(keyword in query_lower for keyword in comparison_keywords):
            intent = 'comparison'
            confidence = 0.85
        elif any(keyword in query_lower for keyword in question_keywords):
            intent = 'question'
            confidence = 0.75

        #keyword çıkar
        words = self.text_processor.clean_text(query).split()
        keywords = [w for w in words if len(w) > 3]

        return {
            'intent': intent,
            'confidence': confidence,
            'keywords': keywords[:5]  # İlk 5 anahtar kelime
        }