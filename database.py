import sqlite3
import os
from flask import g
from config import Config

def get_db():
    """Veritabanına bağlanır; satırlara sütun adıyla erişim sağlar."""
    db = getattr(g, '_database', None)
    if db is None:
        # instance klasörünün var olduğundan emin olalım
        db_path = Config.DATABASE_URL
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        db = g._database = sqlite3.connect(db_path)
        db.row_factory = sqlite3.Row  # Sütun isimleriyle veri çekebilmek için
    return db

def init_db(app):
    """'leads' tablosunu oluşturur (yoksa)."""
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        # Fit Society lead tablosu (isim, telefon, mesaj ve özel ilgi alanı)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                isim TEXT NOT NULL,
                telefon TEXT NOT NULL,
                mesaj TEXT,
                ilgi_alani TEXT,
                tarih TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        db.commit()

def lead_ekle(isim, telefon, mesaj, ilgi_alani="Genel Bilgi"):
    """Yeni müşteri adayı (lead) ekler. SQL Injection'a karşı ? parametresi kullanır."""
    db = get_db()
    cursor = db.cursor()
    cursor.execute('''
        INSERT INTO leads (isim, telefon, mesaj, ilgi_alani)
        VALUES (?, ?, ?, ?)
    ''', (isim, telefon, mesaj, ilgi_alani))
    db.commit()
    return cursor.lastrowid

def tum_leadler():
    """Tüm kayıtları en yeninden eskiye doğru getirir."""
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM leads ORDER BY tarih DESC')
    rows = cursor.fetchall()
    # Sözlük listesine çevirelim
    return [dict(row) for row in rows]
