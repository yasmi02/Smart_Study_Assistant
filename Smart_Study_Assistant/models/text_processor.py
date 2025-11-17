import re
import json
import os
from typing import List, Dict


class TextProcessor:
    """Metin işleme ve temizleme sınıfı"""

    def __init__(self):
        self.topics_data = self._load_topics()

    def _load_topics(self) -> List[Dict]:
        """Örnek konuları yükle - önce complete'i dene"""
        # önce complete versiyonunu dene
        complete_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'sample_topics_complete.json')
        topics_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'sample_topics.json')

        #complete varsa onu kullan
        if os.path.exists(complete_path):
            try:
                with open(complete_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data['topics']
            except:
                pass

        #yoksa normal kullan
        with open(topics_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('topics', [])

    def clean_text(self, text: str) -> str:
        """Metni temizle ve normalize et"""
        # küçük harfe çevir
        text = text.lower()

        # türkçe karakterler de oldsun
        text = re.sub(r'[^\wşğüöçıİŞĞÜÖÇ\s]', '', text)

        #kelime köklerini eşleştir
        text = re.sub(r'(robot)ik\b', r'\1', text)
        text = re.sub(r'(program)lama\b', r'\1', text)
        text = re.sub(r'(öğren)me\b', r'\1', text)
        text = re.sub(r'(geliştir)me\b', r'\1', text)
        text = re.sub(r'(veri)\s+bilim\w*', r'\1', text)
        text = re.sub(r'(web)\s+geliştir\w*', r'\1', text)

        return text.strip()

    def get_all_topics(self) -> List[str]:
        """Tüm konu isimlerini döndür"""
        return [topic['name'] for topic in self.topics_data]

    def get_all_keywords(self) -> List[str]:
        """Tüm anahtar kelimeleri döndür"""
        return [topic['keywords'] for topic in self.topics_data]

    def get_topic_by_name(self, name: str) -> Dict:
        """İsme göre konu detaylarını getir"""
        for topic in self.topics_data:
            if topic['name'].lower() == name.lower():
                return topic
        return None

    def get_resources_for_topic(self, topic_name: str, difficulty: str = "beginner", learning_style: list = None) -> \
    List[str]:
        """Konu için kaynakları getir - yeni format"""
        if learning_style is None:
            learning_style = ["video"]

        topic = self.get_topic_by_name(topic_name)
        if not topic:
            return []

        resources = []

        #zorluk seviyesine göre
        if 'difficulty' in topic and difficulty in topic['difficulty']:
            resources.extend(topic['difficulty'][difficulty][:2])

        #öğrenme tarzına göre
        if 'learning_style' in topic:
            for style in learning_style:
                style_key = style.lower().replace('📹 ', '').replace('📚 ', '').replace('💻 ', '').replace('🎮 ', '')
                if style_key in topic['learning_style']:
                    resources.extend(topic['learning_style'][style_key][:1])

        #tekrarları kaldır
        return list(set(resources))[:5]

    def expand_query(self, query: str) -> str:
        """Sorguyu genişlet (sinonimler, ilgili kelimeler ekle)"""
        #eş anlamlı falan olması lazım
        synonyms = {
            'öğrenmek': 'öğrenme eğitim',
            'öğrenme': 'öğrenmek eğitim',
            'yapmak': 'geliştirme yapma',
            'yapma': 'yapmak geliştirme',
            'kod': 'programlama kod yazma',
            'programlama': 'kod yazma program',
            'uygulama': 'app yazılım program',
            'robot': 'robotik robotics otomasyon',
            'robotik': 'robot robotics otomasyon',
            'web': 'website site internet',
            'veri': 'data bilim analiz',
            'yapay': 'ai artificial zeka',
            'makine': 'machine learning öğrenme',
        }

        expanded = query
        for key, value in synonyms.items():
            if key in query.lower():
                expanded += ' ' + value

        return expanded