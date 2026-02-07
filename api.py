from flask import Blueprint, request, jsonify
from groq import Groq
import os

api = Blueprint('api', __name__)

# Initialize Groq
api_key = os.environ.get('GROQ_API_KEY')
client = Groq(api_key=api_key) if api_key else None

@api.route('/chat', methods=['POST'])
def chat():
    if not client:
        return jsonify({'status': 'error', 'error': 'GROQ_API_KEY tidak tersetting'}), 500
    
    try:
        data = request.json
        topic = data.get('topic', '')
        style = data.get('style', 'formal')
        length = data.get('length', 'medium')
        
        if not topic or len(topic.strip()) < 5:
            return jsonify({'status': 'error', 'error': 'Topik terlalu pendek'}), 400
        
        length_config = {'short': '300-500 kata', 'medium': '500-800 kata', 'long': '800-1200 kata'}
        style_config = {
            'formal': 'profesional dan akademis',
            'casual': 'santai dan mudah dipahami',
            'creative': 'kreatif dan menarik'
        }
        
        prompt = f\"\"\"Tulis artikel dalam bahasa Indonesia:
Topik: {topic}
Gaya: {style_config.get(style, 'profesional')}
Panjang: {length_config.get(length, '500-800 kata')}

Format dengan struktur:
# [Judul Menarik]
## Pendahuluan
## [Poin Utama 1]
## [Poin Utama 2]
## Kesimpulan

Artikel harus original, informatif, dan berkualitas tinggi.\"\"\"

        completion = client.chat.completions.create(
            model=\"llama-3.3-70b-versatile\",
            messages=[
                {\"role\": \"system\", \"content\": \"Kamu adalah penulis artikel profesional berbahasa Indonesia.\"},
                {\"role\": \"user\", \"content\": prompt}
            ],
            temperature=0.7,
            max_tokens=2048
        )
        
        article = completion.choices[0].message.content
        word_count = len(article.split())
        
        return jsonify({'status': 'success', 'article': article, 'word_count': word_count})
        
    except Exception as e:
        return jsonify({'status': 'error', 'error': str(e)}), 500
