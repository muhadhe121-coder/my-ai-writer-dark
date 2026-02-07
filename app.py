from flask import Flask, request, jsonify
import os
from groq import Groq

app = Flask(__name__)

# Initialize Groq client
api_key = os.environ.get('GROQ_API_KEY')
client = None
if api_key:
    client = Groq(api_key=api_key)

# HTML Template with fixed JavaScript
HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Article Writer - Generate Artikel Berkualitas</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }

        .container {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            max-width: 800px;
            width: 100%;
            padding: 40px;
            backdrop-filter: blur(10px);
        }

        h1 {
            color: #667eea;
            text-align: center;
            margin-bottom: 10px;
            font-size: 2.5em;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
        }

        .subtitle {
            text-align: center;
            color: #666;
            margin-bottom: 30px;
            font-size: 1.1em;
        }

        .form-group {
            margin-bottom: 25px;
        }

        label {
            display: block;
            margin-bottom: 8px;
            color: #333;
            font-weight: 600;
            font-size: 1.1em;
        }

        input[type="text"],
        textarea {
            width: 100%;
            padding: 15px;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            font-size: 16px;
            transition: all 0.3s ease;
            font-family: inherit;
        }

        input[type="text"]:focus,
        textarea:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }

        textarea {
            min-height: 120px;
            resize: vertical;
        }

        .topic-buttons {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
            margin-top: 10px;
        }

        .topic-btn {
            padding: 10px 20px;
            border: 2px solid #667eea;
            background: white;
            color: #667eea;
            border-radius: 25px;
            cursor: pointer;
            transition: all 0.3s ease;
            font-weight: 600;
            font-size: 14px;
        }

        .topic-btn:hover {
            background: #667eea;
            color: white;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
        }

        .topic-btn.active {
            background: #667eea;
            color: white;
        }

        .generate-btn {
            width: 100%;
            padding: 18px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 1.2em;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            margin-top: 20px;
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }

        .generate-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.5);
        }

        .generate-btn:active {
            transform: translateY(0);
        }

        .generate-btn:disabled {
            background: #ccc;
            cursor: not-allowed;
            transform: none;
        }

        .result-container {
            margin-top: 30px;
            padding: 25px;
            background: #f8f9fa;
            border-radius: 10px;
            border-left: 5px solid #667eea;
            display: none;
        }

        .result-container.show {
            display: block;
            animation: slideIn 0.5s ease;
        }

        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .result-title {
            color: #667eea;
            font-size: 1.3em;
            margin-bottom: 15px;
            font-weight: 600;
        }

        .result-content {
            color: #333;
            line-height: 1.8;
            white-space: pre-wrap;
            font-size: 1.05em;
        }

        .loading {
            text-align: center;
            padding: 20px;
            display: none;
        }

        .loading.show {
            display: block;
        }

        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            width: 50px;
            height: 50px;
            animation: spin 1s linear infinite;
            margin: 0 auto;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        .error-message {
            background: #fee;
            color: #c33;
            padding: 15px;
            border-radius: 10px;
            margin-top: 20px;
            border-left: 5px solid #c33;
            display: none;
        }

        .error-message.show {
            display: block;
        }

        .copy-btn {
            margin-top: 15px;
            padding: 10px 20px;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-weight: 600;
            transition: all 0.3s ease;
        }

        .copy-btn:hover {
            background: #5568d3;
            transform: translateY(-2px);
        }

        .footer {
            text-align: center;
            margin-top: 30px;
            color: #666;
            font-size: 0.9em;
        }

        @media (max-width: 600px) {
            .container {
                padding: 25px;
            }

            h1 {
                font-size: 2em;
            }

            .topic-buttons {
                flex-direction: column;
            }

            .topic-btn {
                width: 100%;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>✨ AI Article Writer</h1>
        <p class="subtitle">Generate artikel berkualitas dengan AI dalam hitungan detik</p>

        <form id="articleForm">
            <div class="form-group">
                <label for="topic">📝 Topik Artikel:</label>
                <input type="text" id="topic" name="topic" placeholder="Contoh: Tips Kesehatan Mental di Era Digital" required>
            </div>

            <div class="form-group">
                <label>🎨 Gaya Penulisan:</label>
                <div class="topic-buttons">
                    <button type="button" class="topic-btn active" data-style="casual" onclick="setTopic('casual')">Casual</button>
                    <button type="button" class="topic-btn" data-style="formal" onclick="setTopic('formal')">Formal</button>
                    <button type="button" class="topic-btn" data-style="technical" onclick="setTopic('technical')">Technical</button>
                    <button type="button" class="topic-btn" data-style="creative" onclick="setTopic('creative')">Creative</button>
                    <button type="button" class="topic-btn" data-style="seo" onclick="setTopic('seo')">SEO Friendly</button>
                </div>
                <input type="hidden" id="style" name="style" value="casual">
            </div>

            <div class="form-group">
                <label for="keywords">🔑 Keywords (opsional):</label>
                <input type="text" id="keywords" name="keywords" placeholder="Pisahkan dengan koma, contoh: kesehatan, mental, tips">
            </div>

            <div class="form-group">
                <label for="additional">💡 Instruksi Tambahan (opsional):</label>
                <textarea id="additional" name="additional" placeholder="Contoh: Fokus pada solusi praktis, gunakan bahasa yang mudah dipahami"></textarea>
            </div>

            <button type="submit" class="generate-btn">🚀 Generate Artikel AI</button>
        </form>

        <div class="loading">
            <div class="spinner"></div>
            <p style="margin-top: 15px; color: #667eea; font-weight: 600;">Sedang membuat artikel...</p>
        </div>

        <div class="error-message"></div>

        <div class="result-container">
            <h3 class="result-title">📄 Artikel Anda:</h3>
            <div class="result-content"></div>
            <button class="copy-btn" onclick="copyToClipboard()">📋 Copy Artikel</button>
        </div>

        <div class="footer">
            <p>Powered by Groq AI • Made with ❤️</p>
        </div>
    </div>

    <script>
        let currentStyle = 'casual';

        function setTopic(style) {
            currentStyle = style;
            document.getElementById('style').value = style;
            
            // Update active button
            document.querySelectorAll('.topic-btn').forEach(btn => {
                btn.classList.remove('active');
            });
            event.target.classList.add('active');
        }

        document.getElementById('articleForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            await generateArticle();
        });

        async function generateArticle() {
            const topic = document.getElementById('topic').value;
            const style = document.getElementById('style').value;
            const keywords = document.getElementById('keywords').value;
            const additional = document.getElementById('additional').value;

            // Hide previous results and errors
            document.querySelector('.result-container').classList.remove('show');
            document.querySelector('.error-message').classList.remove('show');
            
            // Show loading
            document.querySelector('.loading').classList.add('show');
            document.querySelector('.generate-btn').disabled = true;

            try {
                const response = await fetch('/generate', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        topic: topic,
                        style: style,
                        keywords: keywords,
                        additional: additional
                    })
                });

                const data = await response.json();

                // Hide loading
                document.querySelector('.loading').classList.remove('show');
                document.querySelector('.generate-btn').disabled = false;

                if (data.error) {
                    showError(data.error);
                } else {
                    showResult(data.article);
                }
            } catch (error) {
                document.querySelector('.loading').classList.remove('show');
                document.querySelector('.generate-btn').disabled = false;
                showError('Terjadi kesalahan: ' + error.message);
            }
        }

        function showResult(article) {
            document.querySelector('.result-content').textContent = article;
            document.querySelector('.result-container').classList.add('show');
            
            // Smooth scroll to result
            document.querySelector('.result-container').scrollIntoView({ 
                behavior: 'smooth', 
                block: 'nearest' 
            });
        }

        function showError(message) {
            const errorDiv = document.querySelector('.error-message');
            errorDiv.textContent = message;
            errorDiv.classList.add('show');
        }

        function copyToClipboard() {
            const content = document.querySelector('.result-content').textContent;
            navigator.clipboard.writeText(content).then(() => {
                const btn = document.querySelector('.copy-btn');
                const originalText = btn.textContent;
                btn.textContent = '✅ Copied!';
                setTimeout(() => {
                    btn.textContent = originalText;
                }, 2000);
            });
        }
    </script>
</body>
</html>'''

@app.route('/')
def index():
    return HTML_TEMPLATE

@app.route('/generate', methods=['POST'])
def generate_article():
    if not client:
        return jsonify({'error': 'GROQ_API_KEY tidak ditemukan. Silakan set environment variable.'}), 500
    
    try:
        data = request.json
        topic = data.get('topic', '')
        style = data.get('style', 'casual')
        keywords = data.get('keywords', '')
        additional = data.get('additional', '')

        # Build prompt
        prompt = f"""Buatkan artikel dalam bahasa Indonesia tentang: {topic}

Gaya penulisan: {style}
"""
        
        if keywords:
            prompt += f"Keywords yang harus dimasukkan: {keywords}\n"
        
        if additional:
            prompt += f"Instruksi tambahan: {additional}\n"

        prompt += """
Buatkan artikel yang:
1. Memiliki judul yang menarik
2. Pembukaan yang engaging
3. Isi yang informatif dan terstruktur dengan baik
4. Penutup yang kuat
5. Panjang minimal 500 kata
6. Gunakan subjudul untuk memudahkan pembacaan

Format artikel dengan rapi dan mudah dibaca."""

        # Call Groq API
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "Kamu adalah penulis artikel profesional yang ahli dalam membuat konten berkualitas tinggi dalam bahasa Indonesia."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.7,
            max_tokens=2000,
        )

        article = chat_completion.choices[0].message.content

        return jsonify({'article': article})

    except Exception as e:
        return jsonify({'error': f'Terjadi kesalahan: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True) 
 