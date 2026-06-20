import json
import requests
from odoo import http
from odoo.http import request

class MentalHealthChatbot(http.Controller):

    @http.route('/chatbot', type='http', auth='public', website=True)
    def chatbot_dashboard(self, **kw):
        user = request.env.user
        is_public = user == request.env.ref('base.public_user')
        
        values = {
            'user_name': 'Arifa Fitra Salima' if is_public else user.name,
            'is_public': is_public,
        }
        return request.render('mental_health_chatbot.chatbot_dashboard', values)

    @http.route('/mental/chatbot/send', type='http', auth='public', website=True, csrf=False)
    def chatbot_send(self, **kw):
        body = request.httprequest.get_data(as_text=True) or ''
        try:
            body_json = json.loads(body) if body else {}
        except Exception:
            body_json = {}

        message = None
        if isinstance(body_json, dict):
            message = body_json.get('message')
        if not message:
            message = kw.get('message')

        if not message:
            response = request.make_response(json.dumps({'reply': 'Pesan kosong.'}))
            response.headers['Content-Type'] = 'application/json'
            return response

        # Use the newest config that actually has an API key.
        config = request.env['chatbot.config'].sudo().search([
            ('api_key', '!=', False),
        ], order='id desc', limit=1)

        if not config or not config.api_key:
            # Fallback local counselor response if API key is not configured
            message_lower = message.lower()
            
            if any(word in message_lower for word in ["stres", "cemas", "panik", "anxious", "takut", "khawatir"]):
                reply = "Aku mengerti kamu sedang merasa cemas atau stres. Itu perasaan yang valid dan normal dialami oleh mahasiswa. Coba tarik napas panjang-panjang, tahan selama 4 detik, lalu keluarkan perlahan. Boleh cerita lebih detail apa yang membuatmu stres? Apakah ada tugas atau ujian yang mendekat?"
            elif any(word in message_lower for word in ["sedih", "kecewa", "menangis", "luka", "sakit hati", "depresi", "murung"]):
                reply = "Aku turut berempati mendengar kamu merasa sedih. Perasaan itu valid dan itu bagian dari menjadi manusia. Kamu tidak sendirian, dan aku di sini untuk mendengarkan. Mau cerita apa yang sedang kamu hadapi? Apakah ada kejadian khusus yang membuatmu merasa begini?"
            elif any(word in message_lower for word in ["sepi", "sendiri", "kesepian", "isolated", "terisolasi", "menyendiri"]):
                reply = "Merasa sendiri itu memang tidak menyenangkan, tapi percaya aku kamu tidak sendirian. Banyak mahasiswa yang merasakan hal sama, terutama di awal semester atau saat stress. Apa yang membuatmu merasa kesepian? Ada yang bisa aku bantu atau saran yang bisa aku berikan?"
            elif any(word in message_lower for word in ["tugas", "kuliah", "dosen", "ujian", "skripsi", "magang", "presentasi", "nilai", "ipk"]):
                reply = "Tekanan akademis memang bisa sangat berat untuk mahasiswa. Apa yang paling membuatmu overwhelmed saat ini? Apakah itu terlalu banyak tugas, deadline ketat, atau khawatir dengan hasil? Ada beberapa strategi yang bisa kita bicarain untuk mengatasinya."
            elif any(word in message_lower for word in ["tidur", "insomnia", "susah tidur", "kelelahan", "capek", "exhausted"]):
                reply = "Kurang tidur bisa membuat mood dan mental kita jeadi lebih fragile. Itu penting untuk prioritaskan kualitas tidur. Apa yang biasanya menggangu tidurmu? Apakah terlalu banyak pikiran, gadget, atau lingkungan? Aku bisa bantu cari solusi yang cocok."
            elif any(word in message_lower for word in ["teman", "hubungan", "pertemanan", "conflict", "konflik", "ribut", "putus"]):
                reply = "Masalah hubungan sosial emang salah satu stress terberat bagi mahasiswa. Aku ingin bantu kamu. Bisa cerita lebih detail apa yang terjadi? Apakah itu konflik dengan teman, keluarga, atau masalah hubungan lainnya?"
            elif any(word in message_lower for word in ["motivasi", "semangat", "malas", "prokrastinasi", "males", "energi"]):
                reply = "Kehilangan motivasi itu hal yang sering terjadi, apalagi kalau kamu sedang merasa overwhelmed. Apa yang biasanya membuatmu semangat? Kita bisa coba breakdown target jadi langkah-langkah kecil yang lebih manageable. Mau kita coba?"
            elif any(word in message_lower for word in ["keluarga", "orang tua", "ortu", "keluarga", "tekanan keluarga"]):
                reply = "Tekanan dari keluarga bisa menjadi beban tersendiri untuk mahasiswa. Aku mengerti itu challenging. Cerita dong, apa yang membuat kamu merasa tertekan dari pihak keluarga? Mungkin kita bisa cari cara yang lebih sehat untuk komunikasi."
            elif any(word in message_lower for word in ["halo", "hai", "hello", "pagi", "siang", "sore", "malam", "apa kabar", "hii", "hi"]):
                reply = "Halo! Aku TiKo AI dari Titik koma. Aku di sini untuk dengarkan cerita kamu dan bantu kamu dengan apa pun yang sedang kamu hadapi. Gimana kabarmu hari ini? Ada yang bisa aku bantu?"
            else:
                reply = "Terima kasih sudah percaya share perasaan atau masalahmu dengan aku. Aku siap mendengarkan. Bisa cerita lebih detail tentang apa yang sedang kamu rasakan atau hadapi? Aku akan coba bantu sebaik mungkin."
            
            # Save fallback message to history as well
            request.env['chatbot.history'].sudo().create({
                'user_message': message,
                'bot_response': reply,
            })
            
            response = request.make_response(json.dumps({'reply': reply}))
            response.headers['Content-Type'] = 'application/json'
            return response

        api_key = config.api_key
        model_name = config.model_name or 'gemini-2.5-flash'

        prompt = f"""Kamu adalah TiKo AI, chatbot kesehatan mental mahasiswa bernama "Titik koma." yang empati dan suportif.

KARAKTERISTIK KAMU:
- Nama: TiKo AI dari Titik koma
- Bahasa: Bahasa Indonesia, kasual namun santun (seperti teman sebaya atau konselor kampus)
- Target: Mahasiswa di Indonesia
- Tujuan: Memberikan dukungan emosional dan praktis untuk kesehatan mental

INSTRUKSI PENTING:
1. DENGARKAN DENGAN EMPATI: Validasi perasaan mahasiswa, tunjukkan bahwa kamu mengerti
2. JAWAB LANGSUNG: Fokus menjawab pertanyaan yang ditanyakan, jangan menyimpang
3. BERIKAN SARAN PRAKTIS: Jika relevan, tawarkan tips atau strategi coping yang konkret
4. GUNAKAN BAHASA SEDERHANA: Hindari istilah medis formal, gunakan kata-kata yang mudah dipahami
5. JANGAN DIAGNOSIS: Tidak boleh memberikan diagnosis medis atau mental yang formal
6. SARANKAN PROFESIONAL: Jika kondisi terasa serius atau berbahaya, rekomendasikan konselor profesional

TOPIK YANG BISA KAMU BANTU:
- Stres akademis (tugas, ujian, skripsi)
- Kecemasan dan panik
- Kesedihan atau depresi ringan
- Hubungan sosial dan teman
- Manajemen waktu dan produktivitas
- Kesepian atau isolasi
- Tekanan dari keluarga
- Burnout dan kelelahan
- Teknik relaksasi dan mindfulness
- Motivasi dan kepercayaan diri

CONTOH RESPONS YANG BAIK:
- Untuk "saya stres dengan ujian": "Stres menghadapi ujian itu normal, semua mahasiswa pernah merasa begitu. Apa yang paling membuatmu khawatir? Apakah ada materi yang sulit atau kamu hanya merasa overwhelmed dengan banyak ujian sekaligus?"
- Untuk "saya merasa sendiri": "Merasa sendiri memang berat, tapi kamu tidak sendirian. Ada banyak mahasiswa yang merasakan hal sama. Mau cerita apa yang membuatmu merasa begini?"

HINDARI:
- Menjawab di luar topik kesehatan mental mahasiswa
- Memberikan diagnosis medis
- Respons yang terlalu formal atau klinis
- Hanya mendengarkan tanpa memberi saran

Pertanyaan mahasiswa:
"{message}"

Balas dengan respons yang LANGSUNG, EMPATI, dan PRAKTIS. Fokus pada pertanyaannya dan berikan saran konkret jika memungkinkan."""

        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"

        headers = {
            'Content-Type': 'application/json'
        }

        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": prompt
                        }
                    ]
                }
            ],
            "generationConfig": {
                "temperature": config.temperature or 0.7
            }
        }

        try:
            response = requests.post(url, json=payload, headers=headers, timeout=15)
            
            if response.status_code == 200:
                res_data = response.json()
                candidates = res_data.get('candidates', [])
                reply = ""
                if candidates:
                    reply = candidates[0].get('content', {}).get('parts', [{}])[0].get('text', '')
                if not reply:
                    reply = "Maaf, saya tidak dapat memproses jawaban saat ini. Silakan coba lagi."
            elif response.status_code == 404:
                reply = response.text
            else:
                reply = f"Gagal mendapatkan respon dari AI (Status {response.status_code}). Silakan periksa konfigurasi API Key Anda."
        except Exception as e:
            reply = f"Gagal menghubungi server AI: {str(e)}"

        # Save to history
        request.env['chatbot.history'].sudo().create({
            'user_message': message,
            'bot_response': reply,
        })

        response = request.make_response(json.dumps({'reply': reply}))
        response.headers['Content-Type'] = 'application/json'
        return response