import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from typing import List, Tuple


class Visualizer:
    """Veri görselleştirme sınıfı"""

    @staticmethod
    def create_topic_bar_chart(data: pd.DataFrame, title: str = "En Çok Aranan Konular"):
        """
        Konu arama sayılarının bar grafiği

        Args:
            data: DataFrame with 'query_text' and 'search_count' columns
            title: Grafik başlığı
        """
        if data.empty:
            fig = go.Figure()
            fig.add_annotation(
                text="Henüz veri yok",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=20)
            )
            return fig

        # İlk 10 konuyu al
        top_data = data.head(10)

        fig = px.bar(
            top_data,
            x='search_count',
            y='query_text',
            orientation='h',
            title=title,
            labels={'search_count': 'Arama Sayısı', 'query_text': 'Konu'},
            color='search_count',
            color_continuous_scale='Viridis'
        )

        fig.update_layout(
            showlegend=False,
            height=400,
            yaxis={'categoryorder': 'total ascending'}
        )

        return fig

    @staticmethod
    def create_similarity_gauge(score: float, topic_name: str):
        """
        Benzerlik skoru için gauge grafik

        Args:
            score: Benzerlik skoru (0-1 arası)
            topic_name: Konu adı
        """
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=score * 100,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': f"{topic_name}<br>Eşleşme Oranı"},
            delta={'reference': 50},
            gauge={
                'axis': {'range': [None, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 30], 'color': "lightgray"},
                    {'range': [30, 70], 'color': "gray"},
                    {'range': [70, 100], 'color': "lightgreen"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 80
                }
            }
        ))

        fig.update_layout(height=250)
        return fig

    @staticmethod
    def create_timeline_chart(data: pd.DataFrame):
        """
        Zaman çizelgesi grafiği

        Args:
            data: DataFrame with 'query_date' column
        """
        if data.empty:
            fig = go.Figure()
            fig.add_annotation(
                text="Henüz veri yok",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False
            )
            return fig

        # Tarihe göre grupla
        data['query_date'] = pd.to_datetime(data['query_date'])
        data['date_only'] = data['query_date'].dt.date

        timeline_data = data.groupby('date_only').size().reset_index(name='count')

        fig = px.line(
            timeline_data,
            x='date_only',
            y='count',
            title='Günlük Sorgu Sayısı',
            labels={'date_only': 'Tarih', 'count': 'Sorgu Sayısı'},
            markers=True
        )

        fig.update_layout(height=300)
        return fig

    @staticmethod
    def create_recommendation_cards(recommendations: List[Tuple[str, float]]):
        """
        Öneriler için HTML kartları oluştur

        Args:
            recommendations: [(konu, skor), ...] listesi

        Returns:
            HTML string
        """
        if not recommendations:
            return "<p>Öneri bulunamadı</p>"

        cards_html = ""

        for i, (topic, score) in enumerate(recommendations, 1):
            # Skor rengini belirle
            if score > 0.7:
                color = "#4CAF50"  # Yeşil
                rating = "Mükemmel Eşleşme"
            elif score > 0.4:
                color = "#FF9800"  # Turuncu
                rating = "İyi Eşleşme"
            else:
                color = "#9E9E9E"  # Gri
                rating = "Orta Eşleşme"

            percentage = int(score * 100)

            card = f"""
            <div style="
                border: 2px solid {color};
                border-radius: 10px;
                padding: 15px;
                margin: 10px 0;
                background-color: #f9f9f9;
            ">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <h3 style="margin: 0; color: {color};">#{i} {topic}</h3>
                        <p style="margin: 5px 0; color: #666;">{rating}</p>
                    </div>
                    <div style="
                        background-color: {color};
                        color: white;
                        padding: 10px 20px;
                        border-radius: 20px;
                        font-weight: bold;
                        font-size: 18px;
                    ">
                        %{percentage}
                    </div>
                </div>
            </div>
            """

            cards_html += card

        return cards_html

    @staticmethod
    def create_word_frequency_chart(queries: List[str]):
        """
        Kelime sıklığı grafiği

        Args:
            queries: Sorgu listesi
        """
        from collections import Counter
        import re

        # Tüm kelimeleri topla
        all_words = []
        for query in queries:
            words = re.findall(r'\w+', query.lower())
            all_words.extend([w for w in words if len(w) > 3])

        # En sık kullanılan 15 kelime
        word_freq = Counter(all_words).most_common(15)

        if not word_freq:
            fig = go.Figure()
            fig.add_annotation(text="Henüz veri yok", xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False)
            return fig

        words, counts = zip(*word_freq)

        fig = px.bar(
            x=list(counts),
            y=list(words),
            orientation='h',
            title='En Sık Kullanılan Kelimeler',
            labels={'x': 'Kullanım Sayısı', 'y': 'Kelime'},
            color=list(counts),
            color_continuous_scale='Blues'
        )

        fig.update_layout(showlegend=False, height=400, yaxis={'categoryorder': 'total ascending'})
        return fig