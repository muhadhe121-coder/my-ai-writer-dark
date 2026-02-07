from http.server import BaseHTTPRequestHandler
import json
import os
from groq import Groq

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # Baca body request
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            # Ambil API key dari environment variable
            api_key = os.getenv('GROQ_API_KEY')
            if not api_key:
                raise ValueError("GROQ_API_KEY tidak ditemukan")
            
            # Inisialisasi Groq client
            client = Groq(api_key=api_key)
            
            # Generate artikel
            topic = data.get('topic', '')
            style = data.get('style', 'casual')
            length = data.get('length', 'medium')
            
            # Tentukan panjang kata
            word_count = {
                'short': '300-500 kata',
                'medium': '500-800 kata',
                'long': '800-1200 kata'
            }.get(length, '500-800 kata')
            
            # Buat prompt
            prompt = f"""Tulis artikel dalam Bahasa Indonesia tentang: {topic}

Gaya penulisan: {style}
Panjang: {word_count}

Buatlah artikel yang informatif, menarik, dan mudah dipahami."""
            
            # Panggil Groq API
            chat_completion = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama3-8b-8192",
                temperature=0.7,
                max_tokens=2048,
            )
            
            article = chat_completion.choices[0].message.content
            
            # Response sukses
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response = {'success': True, 'article': article}
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response = {'success': False, 'error': str(e)}
            self.wfile.write(json.dumps(response).encode())
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
# Force update
