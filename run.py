from flask import Flask
from config import config_by_name
from database import init_db
from routes import main_bp
import os

def create_app(config_name='default'):
    """Flask uygulama fabrikası (Application Factory pattern)."""
    app = Flask(__name__)
    
    # Yapılandırmayı yükle
    app.config.from_object(config_by_name[config_name])
    
    # Veritabanını başlat ve tabloları oluştur
    init_db(app)
    
    # Blueprint'i kaydet (Rotaları aktif et)
    app.register_blueprint(main_bp)
    
    return app

# Uygulama nesnesini oluştur
app = create_app(os.getenv('FLASK_ENV', 'default'))

if __name__ == '__main__':
    # Yerel geliştirme sunucusunu başlat
    app.run(host='0.0.0.0', port=5000, debug=True)
