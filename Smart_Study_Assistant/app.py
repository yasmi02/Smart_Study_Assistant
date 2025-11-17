import streamlit as st
import sys
import os
from datetime import datetime, timedelta

# Proje yolunu ekle
sys.path.insert(0, os.path.dirname(__file__))

from models.ml_model import MLModel
from models.text_processor import TextProcessor
from database.db_manager import DatabaseManager
from database.init_db import init_database
from utils.visualizer import Visualizer
from utils.api_handler import APIHandler
import pandas as pd

# Sayfa yapılandırması
st.set_page_config(
    page_title="🎓 Akıllı Öğrenme Asistanı",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Tasarım
st.markdown("""
<style>
    /* Ana Sayfa */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        background-attachment: fixed;
    }

    /* Başlıklar */
    .main-header {
        font-size: 3.5rem;
        font-weight: 900;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        animation: fadeInDown 1s ease-in-out;
    }

    .sub-header {
        font-size: 1.3rem;
        color: #6c757d;
        text-align: center;
        margin-bottom: 2rem;
        animation: fadeInUp 1.2s ease-in-out;
    }

    /* Butonlar */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: bold;
        border-radius: 15px;
        padding: 0.75rem 1.5rem;
        border: none;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        transition: all 0.3s ease;
        font-size: 1.1rem;
        text-transform: uppercase;
    }

    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }

    /* Sekmeler */
    .stTabs [data-baseweb="tab"] {
        height: 65px;
        font-size: 1.2rem;
        font-weight: 600;
        padding: 1rem 1.5rem;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }

    /* Text Area */
    .stTextArea textarea {
        border-radius: 15px;
        padding: 1.2rem;
        font-size: 1.1rem;
        min-height: 120px;
    }

    /* Checkbox */
    .stCheckbox {
        font-weight: 500;
        padding: 0.75rem 0;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
        color: white;
    }

    /* Animasyonlar */
    @keyframes fadeInDown {
        from { opacity: 0; transform: translateY(-30px); }
        to { opacity: 1; transform: translateY(0); }
    }

    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
</style>
""", unsafe_allow_html=True)

# Başlık
st.markdown('''
<div style="text-align: center; padding: 2rem 0;">
    <h1 class="main-header">🎓 Akıllı Öğrenme Asistanı</h1>
</div>
''', unsafe_allow_html=True)

# Session State Başlatma
if 'ml_model' not in st.session_state:
    with st.spinner('🧠 Sistem yükleniyor...'):
        st.session_state.ml_model = MLModel()
        st.session_state.text_processor = TextProcessor()
        st.session_state.db_manager = DatabaseManager()
        st.session_state.api_handler = APIHandler()
        st.session_state.visualizer = Visualizer()
        init_database()

# Sidebar
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 1rem 0;">
    """, unsafe_allow_html=True)


    session_id = st.text_input("👤 Kullanıcı Adı", value="misafir")

    # 🔥 STREAK SİSTEMİ
    st.markdown('<h3 style="color: white;">🔥 Öğrenme Takibi</h3>', unsafe_allow_html=True)

    history = st.session_state.db_manager.get_query_history()

    if not history.empty:
        # Tarih formatını düzelt
        history['date'] = pd.to_datetime(history['query_date']).dt.date
        unique_dates = sorted(history['date'].unique(), reverse=True)

        # Streak hesapla
        streak = 1
        today = datetime.now().date()

        if len(unique_dates) > 0:
            # Bugün arama yaptıysa
            if unique_dates[0] == today:
                for i in range(1, len(unique_dates)):
                    prev_date = unique_dates[i - 1]
                    curr_date = unique_dates[i]

                    # Ardışık mı kontrol et
                    if (prev_date - curr_date).days == 1:
                        streak += 1
                    else:
                        break
            # Dün arama yaptıysa
            elif unique_dates[0] == today - timedelta(days=1):
                streak = 1
                for i in range(1, len(unique_dates)):
                    prev_date = unique_dates[i - 1]
                    curr_date = unique_dates[i]

                    if (prev_date - curr_date).days == 1:
                        streak += 1
                    else:
                        break
            else:
                streak = 0

        # Streak barı
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 1.5rem; 
                    border-radius: 15px; 
                    text-align: center;
                    box-shadow: 0 4px 15px rgba(0,0,0,0.2);">
            <div style="font-size: 3.5rem; margin-bottom: 0.5rem;">🔥</div>
            <div style="color: white; font-size: 2.5rem; font-weight: bold; margin-bottom: 0.5rem;">
                {streak} Gün
            </div>
            <div style="color: rgba(255,255,255,0.95); font-size: 1rem;">
                Öğrenme Streak!
            </div>
        </div>
        """, unsafe_allow_html=True)

    else:
        # İlk kullanıcı
        st.markdown("""
        <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
                    padding: 1.5rem; 
                    border-radius: 15px; 
                    text-align: center;">
            <div style="font-size: 3rem;">🚀</div>
            <div style="color: white; font-size: 1.2rem; font-weight: bold; margin-top: 0.5rem;">
                Öğrenme serüvenine başla!
            </div>
            <div style="color: rgba(255,255,255,0.9); font-size: 0.9rem; margin-top: 0.5rem;">
                İlk aramayı yap ve streak'ini başlat!
            </div>
        </div>
        """, unsafe_allow_html=True)

# Ana Sekmeler
tab1, tab2, tab3, tab4 = st.tabs(["🔍 Yeni Öğrenme", "📚 Geçmiş", "📊 İstatistikler", "🎯 Konu Keşfi"])

# TAB 1: Yeni Öğrenme
with tab1:
    st.header("🔍 Ne Öğrenmek İstiyorsunuz?")

    col1, col2 = st.columns([3, 1])

    with col1:
        user_query = st.text_area(
            "Öğrenmek istediğiniz konuyu yazın ve 'öneri al' butonuna tıklayın:",
            placeholder="Örnek: Python programlama öğrenmek istiyorum",
            height=120
        )

    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        search_button = st.button("🚀 Öneri Al", use_container_width=True)

        st.markdown("<br>", unsafe_allow_html=True)


        # Checkbox'lar
        show_wikipedia = st.checkbox("📚 Wikipedia", value=True)
        show_resources = st.checkbox("🔗 Kaynaklar", value=True)

    if search_button and user_query:
        with st.spinner('🔍 Öneriler hazırlanıyor...'):
            # Önerileri al
            recommendations = st.session_state.ml_model.get_recommendations(user_query, top_n=5)

            if recommendations:
                # Veritabanına kaydet
                query_id = st.session_state.db_manager.save_query(user_query, session_id)
                st.session_state.db_manager.save_recommendations(query_id, recommendations)

                st.success(f"✅ {len(recommendations)} öneri bulundu!")
                st.markdown("---")

                # Önerileri göster
                for i, (topic, score) in enumerate(recommendations, 1):
                    # Renk belirle
                    if score > 0.7:
                        color = "#11998e"
                        emoji = "🟢"
                    elif score > 0.4:
                        color = "#f093fb"
                        emoji = "🟡"
                    else:
                        color = "#4facfe"
                        emoji = "⚪"

                    percentage = int(score * 100)

                    # Kart
                    st.markdown(f"""
                    <div style="background: white; border-radius: 15px; padding: 1.5rem; margin: 1rem 0; border-left: 5px solid {color};">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <h3 style="margin: 0; color: {color};">#{i} {topic}</h3>
                            <div style="background: {color}; color: white; padding: 0.5rem 1rem; border-radius: 20px; font-weight: bold;">
                                {emoji} {percentage}%
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    # Wikipedia
                    if show_wikipedia:
                        wiki_data = st.session_state.api_handler.get_topic_summary(topic)
                        if wiki_data['exists']:
                            with st.expander("📚 Wikipedia Bilgisi"):
                                st.write(wiki_data['summary'])
                                if wiki_data['url']:
                                    st.markdown(f"[Devamını Oku]({wiki_data['url']})")

                    # Kaynaklar
                    if show_resources:
                        topic_data = st.session_state.text_processor.get_topic_by_name(topic)
                        if topic_data and 'difficulty' in topic_data:
                            with st.expander("🔗 Öğrenme Kaynakları"):
                                # Zorluk seviyesine göre
                                diff_map = {
                                    "🌱 Başlangıç": "beginner",
                                    "🚀 Orta": "intermediate",
                                    "⚡ İleri": "advanced"
                                }


                                col1, col2, col3 = st.columns(3)

                                with col1:
                                    st.markdown("**🌱 Başlangıç**")
                                    if 'beginner' in topic_data['difficulty']:
                                        for idx, link in enumerate(topic_data['difficulty']['beginner'][:2], 1):
                                            st.markdown(f"[Kaynak {idx}]({link})")

                                with col2:
                                    st.markdown("**🚀 Orta**")
                                    if 'intermediate' in topic_data['difficulty']:
                                        for idx, link in enumerate(topic_data['difficulty']['intermediate'][:2], 1):
                                            st.markdown(f"[Kaynak {idx}]({link})")

                                with col3:
                                    st.markdown("**⚡ İleri**")
                                    if 'advanced' in topic_data['difficulty']:
                                        for idx, link in enumerate(topic_data['difficulty']['advanced'][:2], 1):
                                            st.markdown(f"[Kaynak {idx}]({link})")

                    st.markdown("<br>", unsafe_allow_html=True)
            else:
                st.warning("⚠️ Öneri bulunamadı. Farklı kelimeler deneyin.")

    elif search_button:
        st.error("❌ Lütfen bir şeyler yazın!")

# TAB 2: Geçmiş
with tab2:
    st.header("📚 Sorgu Geçmişi")

    history_df = st.session_state.db_manager.get_query_history(limit=100)

    if not history_df.empty:
        st.dataframe(
            history_df,
            use_container_width=True,
            column_config={
                "query_text": "Sorgu",
                "query_date": "Tarih",
                "user_session": "Kullanıcı"
            }
        )
    else:
        st.info("Henüz sorgu yok!")

# TAB 3: İstatistikler
with tab3:
    st.header("📊 İstatistikler")

    topics_stats = st.session_state.db_manager.get_topic_statistics()

    if not topics_stats.empty:
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📊 En Çok Aranan")
            fig1 = st.session_state.visualizer.create_topic_bar_chart(topics_stats)
            st.plotly_chart(fig1, use_container_width=True)

        with col2:
            st.subheader("📅 Zaman Çizelgesi")
            history_df = st.session_state.db_manager.get_query_history(limit=1000)
            fig2 = st.session_state.visualizer.create_timeline_chart(history_df)
            st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("İstatistik için sorgu yapın!")

# TAB 4: Konu Keşfi
with tab4:
    st.header("🎯 Konu Keşfi")
    st.write("Konu üzerine tıklayarak detayları görün.")

    all_topics = st.session_state.text_processor.get_all_topics()

    # Her konu için expander
    for topic in all_topics:
        with st.expander(f"📘 {topic}"):
            topic_data = st.session_state.text_processor.get_topic_by_name(topic)

            if topic_data and 'difficulty' in topic_data:
                st.markdown("#### 📚 Öğrenme Kaynakları")

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.markdown("**🌱 Başlangıç**")
                    if 'beginner' in topic_data['difficulty']:
                        for i, link in enumerate(topic_data['difficulty']['beginner'][:3], 1):
                            st.markdown(f"{i}. [Link]({link})")

                with col2:
                    st.markdown("**🚀 Orta**")
                    if 'intermediate' in topic_data['difficulty']:
                        for i, link in enumerate(topic_data['difficulty']['intermediate'][:3], 1):
                            st.markdown(f"{i}. [Link]({link})")

                with col3:
                    st.markdown("**⚡ İleri**")
                    if 'advanced' in topic_data['difficulty']:
                        for i, link in enumerate(topic_data['difficulty']['advanced'][:3], 1):
                            st.markdown(f"{i}. [Link]({link})")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 20px;'>
    <h3 style='color: white;'>🎓 Akıllı Öğrenme Asistanı</h3>
    <p style='color: white;'>Yasemin ADATEPE | © 2025</p>
</div>
""", unsafe_allow_html=True)