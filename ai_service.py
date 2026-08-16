import os
from groq import Groq
from config import Config

def yapay_zeka_yanitla(kullanici_mesaji, gecmis_sohbet=None):
    """Groq API kullanarak Fit Society bağlamına uygun yanıt üretir."""
    api_key = Config.GROQ_API_KEY
    
    # API anahtarı girilmemişse yedek bir yanıt döndür
    if not api_key:
        return "Fit Society'ye hoş geldiniz! Size yardımcı olabilmemiz için lütfen adınızı ve telefon numaranızı bırakın, ekibimiz sizinle iletişime geçsin."
    
    try:
        client = Groq(api_key=api_key)
        
        # Mesaj geçmişini hazırla
        messages = [
            {"role": "system", "content": Config.BUSINESS_CONTEXT}
        ]
        
        # Varsa önceki sohbetleri ekle
        if gecmis_sohbet:
            messages.extend(gecmis_sohbet)
            
        # Son kullanıcı mesajını ekle
        messages.append({"role": "user", "content": kullanici_mesaji})
        
        # Groq model çağrısı (llama serisi)
        chat_completion = client.chat.completions.create(
            messages=messages,
            model="llama-3.3-70b-versatile",
            temperature=0.7,
            max_tokens=500
        )
        
        return chat_completion.choices[0].message.content
        
    except Exception as e:
        print(f"Yapay zeka servis hatası: {e}")
        return "Şu anda sistemde geçici bir yoğunluk var. Lütfen doğrudan telefon numaranızı bırakın, size hemen dönüş yapalım!"
