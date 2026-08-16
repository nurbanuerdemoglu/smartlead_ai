import os
from dotenv import load_dotenv

# .env dosyasındaki gizli anahtarları okumasını sağlar
load_dotenv()

class Config:
    # Flask için gizli anahtar
    SECRET_KEY = os.getenv('SECRET_KEY', 'gizli-anahtar-varsayilan')
    
    # Veritabanı dosya yolu
    DATABASE_URL = os.getenv('DATABASE_URL', 'instance/smartlead.db')
    
    # Groq Yapay Zeka API anahtarı
    GROQ_API_KEY = os.getenv('GROQ_API_KEY', '')
    
    # Yapay zeka servis sağlayıcısı
    AI_PROVIDER = os.getenv('AI_PROVIDER', 'groq')
    
    # Fit Society Markasına Özel Yapay Zeka Kişiliği (BUSINESS_CONTEXT)
    BUSINESS_CONTEXT = """
    Sen Fit Society'nin profesyonel ve motive edici dijital asistanısın. 
    Fit Society; fitness, yüzme havuzu, yoga/pilates stüdyoları, fizyoterapi ve klinik beslenme/diyetisyen danışmanlığını tek çatı altında toplayan bütünsel bir yaşam merkezidir[span_2](start_span)[span_2](end_span). 
    Aynı zamanda özel tasarım spor giyim ürünlerinin (Fit Society Shop) satışını yapar[span_3](start_span)[span_3](end_span). 
    Ziyaretçilere üyelik paketleri, stüdyo dersleri, fizyoterapi/beslenme danışmanlığı hakkında bilgi ver. 
    Kibar, samimi ve harekete geçirici bir dil kullan[span_4](start_span)[span_4](end_span). 
    Müşterileri deneme dersi veya detaylı bilgi için iletişim bilgilerini (isim ve telefon) bırakmaya yönlendir.
    """
    
    # CORS izinleri
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*')

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

# Ortama göre seçilecek yapılandırma sözlüğü
config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
