import wikipediaapi
from typing import Optional, Dict


class APIHandler:
    """Dış API işlemlerini yöneten sınıf"""

    def __init__(self):
        # Wikipedia API için Türkçe wiki
        self.wiki_tr = wikipediaapi.Wikipedia(
            language='tr',
            user_agent='SmartStudyAssistant/1.0'
        )

        # İngilizce alternatif
        self.wiki_en = wikipediaapi.Wikipedia(
            language='en',
            user_agent='SmartStudyAssistant/1.0'
        )

    def get_topic_summary(self, topic_name: str, language: str = 'tr') -> Optional[Dict]:
        """Wikipedia'dan konu özetini getir"""
        wiki = self.wiki_tr if language == 'tr' else self.wiki_en

        # Daha fazla arama terimi
        search_terms = [
            topic_name,
            topic_name.replace('ı', 'i').replace('İ', 'I'),
            topic_name.lower(),
            topic_name.title(),
            # Ek terimler
            topic_name.replace(' ve ', ' '),
            topic_name.split()[0] if ' ' in topic_name else topic_name,  # İlk kelime
        ]

        # İngilizce de dene
        if language == 'tr':
            for term in search_terms.copy():
                page = wiki.page(term)
                if page.exists():
                    summary = page.summary[:500]
                    if len(page.summary) > 500:
                        summary += "..."
                    return {
                        'title': page.title,
                        'summary': summary,
                        'url': page.fullurl,
                        'exists': True
                    }

            # Türkçede bulamazsa İngilizce dene
            return self.get_topic_summary(topic_name, language='en')

        # Hiçbir şey bulunamadı
        return {
            'title': topic_name,
            'summary': f"{topic_name} için detaylı bilgi aşağıdaki kaynaklarda bulunabilir.",
            'url': None,
            'exists': False
        }


        for term in search_terms:
            page = wiki.page(term)

            if page.exists():
                # Özet ilk 500 karakter
                summary = page.summary[:500]
                if len(page.summary) > 500:
                    summary += "..."

                return {
                    'title': page.title,
                    'summary': summary,
                    'url': page.fullurl,
                    'exists': True
                }

        # Hiçbir şey bulunamadı
        return {
            'title': topic_name,
            'summary': f"{topic_name} hakkında Wikipedia'da bilgi bulunamadı.",
            'url': None,
            'exists': False
        }

    def search_related_pages(self, query: str, language: str = 'tr', limit: int = 5) -> list:
        """
        İlgili sayfaları ara

        Args:
            query: Arama sorgusu
            language: Dil
            limit: Maksimum sonuç sayısı

        Returns:
            İlgili sayfa başlıkları listesi
        """
        # Not: Wikipedia API direkt arama özelliği sınırlı
        # Bu fonksiyon basit bir implementasyon

        wiki = self.wiki_tr if language == 'tr' else self.wiki_en
        page = wiki.page(query)

        if page.exists():
            # İlgili kategorilerdeki sayfaları döndür
            categories = list(page.categories.keys())[:limit]
            return [cat.split(':')[-1] for cat in categories]

        return []

    def get_topic_categories(self, topic_name: str) -> list:
        """
        Konunun kategorilerini getir

        Args:
            topic_name: Konu adı

        Returns:
            Kategori listesi
        """
        page = self.wiki_tr.page(topic_name)

        if page.exists():
            categories = list(page.categories.keys())
            # Kategori: önekini temizle
            clean_categories = [cat.split(':')[-1] for cat in categories]
            return clean_categories[:10]  # İlk 10 kategori

        return []

    def format_summary_for_display(self, summary_data: Dict) -> str:
        """
        Özet bilgiyi HTML formatında hazırla

        Args:
            summary_data: get_topic_summary() çıktısı

        Returns:
            HTML string
        """
        if not summary_data['exists']:
            return f"""
            <div style="padding: 15px; background-color: #fff3cd; border-radius: 5px; border-left: 4px solid #ffc107;">
                <p style="margin: 0; color: #856404;">
                    ℹ️ <strong>{summary_data['title']}</strong> hakkında Wikipedia'da bilgi bulunamadı.
                </p>
            </div>
            """

        return f"""
        <div style="padding: 15px; background-color: #e7f3ff; border-radius: 5px; border-left: 4px solid #2196F3;">
            <h4 style="margin-top: 0; color: #1976D2;">
                📚 {summary_data['title']}
            </h4>
            <p style="line-height: 1.6; color: #333;">
                {summary_data['summary']}
            </p>
            <a href="{summary_data['url']}" target="_blank" style="
                color: #2196F3;
                text-decoration: none;
                font-weight: bold;
            ">
                Wikipedia'da Devamını Oku →
            </a>
        </div>
        """