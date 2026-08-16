from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from database import lead_ekle, tum_leadler
from ai_service import yapay_zeka_yanitla

# Flask Blueprint tanımlaması
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Fit Society ana sayfa (karşılama ve chatbot arayüzü)."""
    return render_template('index.html')

@main_bp.route('/admin')
def admin():
    """Toplanan müşteri adaylarının (lead) listelendiği yönetim paneli."""
    leads = tum_leadler()
    return render_template('admin.html', leads=leads)

@main_bp.route('/api/chat', methods=['POST'])
def chat_api():
    """Chatbot ile yapay zeka tabanlı mesajlaşma uç noktası."""
    data = request.get_json() or {}
    kullanici_mesaji = data.get('message', '')
    gecmis = data.get('history', [])
    
    if not kullanici_mesaji:
        return jsonify({'response': 'Lütfen geçerli bir mesaj yazın.'}), 400
        
    # Yapay zekadan yanıt al
    yanit = yapay_zeka_yanitla(kullanici_mesaji, gecmis)
    return jsonify({'response': yanit})

@main_bp.route('/api/lead', methods=['POST'])
def lead_api():
    """Ziyaretçiden gelen iletişim bilgilerini veritabanına kaydeder."""
    data = request.get_json() or {}
    isim = data.get('isim')
    telefon = data.get('telefon')
    mesaj = data.get('mesaj', '')
    ilgi_alani = data.get('ilgi_alani', 'Genel Bilgi')
    
    if not isim or not telefon:
        return jsonify({'success': False, 'error': 'İsim ve telefon alanları zorunludur.'}), 400
        
    try:
        lead_ekle(isim, telefon, mesaj, ilgi_alani)
        return jsonify({'success': True, 'message': 'Bilgileriniz başarıyla kaydedildi. Ekibimiz en kısa sürede sizinle iletişime geçecektir.'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
