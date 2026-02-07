from flask import Flask, request, jsonify
import os
from groq import Groq

app = Flask(__name__)

# Initialize Groq client
api_key = os.environ.get('GROQ_API_KEY')
client = None
if api_key:
    client = Groq(api_key=api_key)

# HTML Template - Dark Theme Professional
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Writer Pro - Groq Powered</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary: #8B5CF6;
            --primary-dark: #7C3AED;
            --primary-light: #EDE9FE;
            --secondary: #06B6D4;
            --accent: #F59E0B;
            --success: #10B981;
            --dark: #1F2937;
            --darker: #111827;
            --light: #F9FAFB;
            --gray: #6B7280;
            --gray-light: #E5E7EB;
            --card-bg: rgba(255, 255, 255, 0.95);
            --shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
            --gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            --gradient-primary: linear-gradient(135deg, #8B5CF6 0%, #06B6D4 100%);
            --gradient-dark: linear-gradient(135deg, #1F2937 0%, #111827 100%);
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Inter', sans-serif;
            background: linear-gradient(135deg, #0F172A 0%, #1E1B4B 100%);
            min-height: 100vh;
            color: var(--light);
            line-height: 1.6;
            overflow-x: hidden;
        }

        .particles-container {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 0;
        }

        .particle {
            position: absolute;
            background: rgba(139, 92, 246, 0.3);
            border-radius: 50%;
            animation: float 6s ease-in-out infinite;
        }

        @keyframes float {
            0%, 100% { transform: translateY(0px) rotate(0deg); }
            50% { transform: translateY(-20px) rotate(180deg); }
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 30px;
            position: relative;
            z-index: 1;
        }

        /* Header Styles */
        .header {
            text-align: center;
            padding: 4rem 0 3rem;
            position: relative;
        }

        .logo-container {
            display: inline-flex;
            align-items: center;
            gap: 1rem;
            margin-bottom: 2rem;
            padding: 1.5rem 2.5rem;
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(20px);
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }

        .logo {
            font-size: 3.5rem;
            background: var(--gradient-primary);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .logo-text {
            font-size: 2.5rem;
            font-weight: 900;
            background: var(--gradient-primary);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .header h1 {
            font-size: 4rem;
            font-weight: 900;
            margin-bottom: 1.5rem;
            background: linear-gradient(135deg, #8B5CF6 0%, #06B6D4 50%, #F59E0B 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            text-shadow: 0 10px 30px rgba(139, 92, 246, 0.3);
        }

        .header p {
            font-size: 1.4rem;
            color: var(--gray-light);
            margin-bottom: 3rem;
            max-width: 700px;
            margin-left: auto;
            margin-right: auto;
            line-height: 1.8;
        }

        .badges {
            display: flex;
            justify-content: center;
            gap: 1.5rem;
            flex-wrap: wrap;
        }

        .badge {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            background: rgba(139, 92, 246, 0.2);
            padding: 1rem 2rem;
            border-radius: 50px;
            font-size: 1rem;
            font-weight: 600;
            border: 1px solid rgba(139, 92, 246, 0.3);
            color: var(--primary-light);
            backdrop-filter: blur(10px);
            transition: all 0.3s ease;
        }

        .badge:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 25px rgba(139, 92, 246, 0.4);
        }

        /* Main Layout */
        .main-content {
            display: grid;
            grid-template-columns: 2fr 1fr;
            gap: 2.5rem;
            margin-bottom: 4rem;
        }

        @media (max-width: 1200px) {
            .main-content {
                grid-template-columns: 1fr;
            }
        }

        /* Cards */
        .card {
            background: rgba(31, 41, 55, 0.8);
            backdrop-filter: blur(20px);
            border-radius: 25px;
            padding: 3rem;
            border: 1px solid rgba(255, 255, 255, 0.1);
            box-shadow: var(--shadow);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }

        .card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: var(--gradient-primary);
        }

        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 35px 60px rgba(0, 0, 0, 0.3);
        }

        .section-title {
            font-size: 1.8rem;
            font-weight: 800;
            margin-bottom: 2rem;
            color: var(--light);
            display: flex;
            align-items: center;
            gap: 1.2rem;
        }

        .section-title i {
            width: 60px;
            height: 60px;
            background: var(--gradient-primary);
            border-radius: 15px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 1.5rem;
        }

        /* Input Groups */
        .input-group {
            margin-bottom: 2.5rem;
        }

        .topic-input {
            width: 100%;
            padding: 1.5rem 2rem;
            background: rgba(17, 24, 39, 0.8);
            border: 2px solid rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            color: var(--light);
            font-size: 1.1rem;
            transition: all 0.3s ease;
            font-weight: 500;
        }

        .topic-input:focus {
            outline: none;
            border-color: var(--primary);
            box-shadow: 0 0 0 4px rgba(139, 92, 246, 0.2);
            background: rgba(17, 24, 39, 0.9);
        }

        .topic-input::placeholder {
            color: var(--gray);
            font-weight: 400;
        }

        .topic-tags {
            display: flex;
            gap: 1rem;
            flex-wrap: wrap;
            margin-top: 1.5rem;
        }

        .topic-tag {
            background: rgba(139, 92, 246, 0.15);
            color: var(--primary-light);
            padding: 1rem 1.5rem;
            border-radius: 12px;
            font-size: 0.95rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            border: 1px solid rgba(139, 92, 246, 0.2);
        }

        .topic-tag:hover {
            background: var(--primary);
            color: white;
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(139, 92, 246, 0.4);
        }

        /* Options Grid */
        .options-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 1.5rem;
            margin-top: 1.5rem;
        }

        .option-card {
            background: rgba(17, 24, 39, 0.8);
            border: 2px solid rgba(255, 255, 255, 0.1);
            border-radius: 18px;
            padding: 2rem 1.5rem;
            cursor: pointer;
            transition: all 0.3s ease;
            text-align: center;
            position: relative;
            overflow: hidden;
        }

        .option-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: transparent;
            transition: all 0.3s ease;
        }

        .option-card:hover {
            border-color: var(--primary);
            transform: translateY(-5px);
            box-shadow: 0 15px 30px rgba(0, 0, 0, 0.2);
        }

        .option-card:hover::before {
            background: var(--gradient-primary);
        }

        .option-card.selected {
            border-color: var(--primary);
            background: rgba(139, 92, 246, 0.1);
        }

        .option-card.selected::before {
            background: var(--gradient-primary);
        }

        .option-icon {
            font-size: 2.5rem;
            margin-bottom: 1.2rem;
            background: var(--gradient-primary);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .option-title {
            font-size: 1.3rem;
            font-weight: 700;
            margin-bottom: 0.75rem;
            color: var(--light);
        }

        .option-desc {
            font-size: 0.95rem;
            color: var(--gray);
            line-height: 1.5;
        }

        input[type="radio"] {
            display: none;
        }

        /* Generate Button */
        .generate-btn {
            width: 100%;
            background: var(--gradient-primary);
            color: white;
            border: none;
            padding: 1.5rem 2rem;
            border-radius: 15px;
            font-size: 1.3rem;
            font-weight: 800;
            cursor: pointer;
            transition: all 0.3s ease;
            margin-top: 1.5rem;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 1rem;
            position: relative;
            overflow: hidden;
        }

        .generate-btn::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
            transition: left 0.5s;
        }

        .generate-btn:hover::before {
            left: 100%;
        }

        .generate-btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 20px 40px rgba(139, 92, 246, 0.5);
        }

        .generate-btn:active {
            transform: translateY(-1px);
        }

        .generate-btn:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
            box-shadow: none;
        }

        /* Features Sidebar */
        .features-list {
            list-style: none;
        }

        .feature-item {
            display: flex;
            align-items: center;
            gap: 1.5rem;
            padding: 1.5rem 0;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            transition: all 0.3s ease;
        }

        .feature-item:hover {
            transform: translateX(10px);
        }

        .feature-item:last-child {
            border-bottom: none;
        }

        .feature-icon {
            width: 50px;
            height: 50px;
            background: var(--gradient-primary);
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 1.2rem;
            flex-shrink: 0;
        }

        .feature-text {
            font-size: 1.1rem;
            color: var(--light);
            font-weight: 500;
        }

        /* Result Section */
        .result-container {
            display: none;
            margin-top: 2rem;
        }

        .result-container.show {
            display: block;
            animation: slideUp 0.6s ease;
        }

        @keyframes slideUp {
            from {
                opacity: 0;
                transform: translateY(40px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .result-header {
            display: flex;
            align-items: center;
            gap: 1.5rem;
            margin-bottom: 2.5rem;
            padding-bottom: 2rem;
            border-bottom: 2px solid rgba(255, 255, 255, 0.1);
        }

        .result-icon {
            width: 60px;
            height: 60px;
            background: var(--success);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 1.8rem;
            box-shadow: 0 10px 25px rgba(16, 185, 129, 0.4);
        }

        .result-title {
            font-size: 1.8rem;
            font-weight: 800;
            color: var(--light);
        }

        .article-meta {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 1.5rem;
            margin-bottom: 3rem;
            padding: 2rem;
            background: rgba(17, 24, 39, 0.8);
            border-radius: 18px;
            border-left: 4px solid var(--primary);
        }

        .meta-item {
            display: flex;
            align-items: center;
            gap: 1rem;
            color: var(--gray-light);
            font-weight: 500;
        }

        .meta-item i {
            color: var(--primary);
            font-size: 1.2rem;
        }

        .article-content {
            line-height: 1.8;
        }

        .article-title {
            font-size: 2.5rem;
            font-weight: 900;
            margin-bottom: 2rem;
            color: var(--light);
            background: var(--gradient-primary);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            line-height: 1.3;
        }

        .section-heading {
            font-size: 1.8rem;
            font-weight: 800;
            margin: 3rem 0 1.5rem 0;
            color: var(--light);
            padding-bottom: 0.75rem;
            border-bottom: 3px solid var(--primary);
            display: flex;
            align-items: center;
            gap: 1rem;
        }

        .section-heading i {
            color: var(--primary);
        }

        .article-paragraph {
            margin-bottom: 1.8rem;
            color: var(--gray-light);
            font-size: 1.1rem;
            text-align: justify;
        }

        .article-actions {
            display: flex;
            gap: 1.5rem;
            margin-top: 4rem;
            padding-top: 2.5rem;
            border-top: 2px solid rgba(255, 255, 255, 0.1);
        }

        .action-btn {
            flex: 1;
            padding: 1.2rem 1.5rem;
            border: none;
            border-radius: 12px;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 0.75rem;
            font-size: 1rem;
        }

        .copy-btn {
            background: var(--primary);
            color: white;
        }

        .download-btn {
            background: var(--secondary);
            color: white;
        }

        .regenerate-btn {
            background: var(--accent);
            color: white;
        }

        .action-btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
        }

        /* Loading State */
        .loading {
            text-align: center;
            padding: 4rem 2rem;
        }

        .loading-icon {
            font-size: 4rem;
            background: var(--gradient-primary);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 2rem;
            animation: pulse 2s infinite, rotate 3s linear infinite;
        }

        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.1); }
        }

        @keyframes rotate {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
        }

        .loading h3 {
            margin-bottom: 1.5rem;
            color: var(--light);
            font-size: 1.5rem;
            font-weight: 700;
        }

        .loading p {
            color: var(--gray);
            margin-bottom: 0.75rem;
            font-size: 1.1rem;
        }

        /* Notification */
        .notification {
            position: fixed;
            top: 30px;
            right: 30px;
            background: var(--success);
            color: white;
            padding: 1.2rem 2rem;
            border-radius: 12px;
            box-shadow: var(--shadow);
            transform: translateX(400px);
            transition: transform 0.4s ease;
            z-index: 1000;
            display: flex;
            align-items: center;
            gap: 1rem;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }

        .notification.show {
            transform: translateX(0);
        }

        .notification.error {
            background: #DC2626;
        }

        /* Responsive */
        @media (max-width: 768px) {
            .container {
                padding: 20px;
            }
            
            .header h1 {
                font-size: 2.5rem;
            }
            
            .logo-text {
                font-size: 1.8rem;
            }
            
            .logo-container {
                padding: 1rem 1.5rem;
            }
            
            .options-grid {
                grid-template-columns: 1fr;
            }
            
            .article-meta {
                grid-template-columns: 1fr;
            }
            
            .article-actions {
                flex-direction: column;
            }
            
            .article-title {
                font-size: 2rem;
            }
            
            .card {
                padding: 2rem;
            }
            
            .section-title {
                font-size: 1.5rem;
            }
            
            .section-title i {
                width: 50px;
                height: 50px;
                font-size: 1.2rem;
            }
        }

        @media (max-width: 480px) {
            .header h1 {
                font-size: 2rem;
            }
            
            .header p {
                font-size: 1.1rem;
            }
            
            .badges {
                gap: 1rem;
            }
            
            .badge {
                padding: 0.75rem 1.5rem;
                font-size: 0.9rem;
            }
        }
    </style>
</head>
<body>
    <div class="particles-container" id="particles"></div>
    
    <div class="container">
        <!-- Header -->
        <div class="header">
            <div class="logo-container">
                <div class="logo">
                    <i class="fas fa-robot"></i>
                </div>
                <div class="logo-text">AI Writer Pro</div>
            </div>
            <h1>Generate Artikel Berkualitas Tinggi</h1>
            <p>Dengan teknologi AI terdepan dari Groq, buat artikel original dalam hitungan detik. Pilih gaya penulisan dan panjang artikel sesuai kebutuhan Anda.</p>
            <div class="badges">
                <div class="badge">
                    <i class="fas fa-bolt"></i> Powered by Groq
                </div>
                <div class="badge">
                    <i class="fas fa-rocket"></i> Ultra Fast
                </div>
                <div class="badge">
                    <i class="fas fa-crown"></i> 100% Gratis
                </div>
                <div class="badge">
                    <i class="fas fa-shield-alt"></i> Original Content
                </div>
            </div>
        </div>

        <!-- Main Content -->
        <div class="main-content">
            <!-- Form Section -->
            <div class="card">
                <div class="input-group">
                    <h2 class="section-title">
                        <i class="fas fa-edit"></i>
                        Topik Artikel
                    </h2>
                    <input type="text" id="topic" class="topic-input" placeholder="Contoh: Cara belajar Python untuk pemula, Manfaat olahraga rutin, Teknologi AI masa depan..." autofocus>
                    
                    <div class="topic-tags">
                        <div class="topic-tag" onclick="setTopic('Cara belajar programming untuk pemula dari nol')">Programming</div>
                        <div class="topic-tag" onclick="setTopic('Manfaat artificial intelligence dalam kehidupan sehari-hari')">AI & Teknologi</div>
                        <div class="topic-tag" onclick="setTopic('Tips menjaga kesehatan mental di era digital')">Kesehatan</div>
                        <div class="topic-tag" onclick="setTopic('Strategi memulai bisnis online yang sukses')">Bisnis</div>
                        <div class="topic-tag" onclick="setTopic('Perkembangan teknologi blockchain dan cryptocurrency')">Blockchain</div>
                        <div class="topic-tag" onclick="setTopic('Cara meningkatkan produktivitas kerja sehari-hari')">Produktivitas</div>
                    </div>
                </div>

                <div class="input-group">
                    <h2 class="section-title">
                        <i class="fas fa-palette"></i>
                        Gaya Penulisan
                    </h2>
                    <div class="options-grid">
                        <label class="option-card">
                            <input type="radio" name="writing-style" value="formal" checked>
                            <div class="option-icon"><i class="fas fa-user-tie"></i></div>
                            <div class="option-title">Formal</div>
                            <div class="option-desc">Profesional & Akademis, cocok untuk konten bisnis dan pendidikan</div>
                        </label>
                        <label class="option-card">
                            <input type="radio" name="writing-style" value="casual">
                            <div class="option-icon"><i class="fas fa-comments"></i></div>
                            <div class="option-title">Casual</div>
                            <div class="option-desc">Santai & Mudah dipahami, seperti percakapan sehari-hari</div>
                        </label>
                        <label class="option-card">
                            <input type="radio" name="writing-style" value="creative">
                            <div class="option-icon"><i class="fas fa-lightbulb"></i></div>
                            <div class="option-title">Kreatif</div>
                            <div class="option-desc">Inspiratif & Menarik, dengan bahasa yang memikat pembaca</div>
                        </label>
                    </div>
                </div>

                <div class="input-group">
                    <h2 class="section-title">
                        <i class="fas fa-ruler"></i>
                        Panjang Artikel
                    </h2>
                    <div class="options-grid">
                        <label class="option-card">
                            <input type="radio" name="article-length" value="short">
                            <div class="option-icon"><i class="fas fa-file-alt"></i></div>
                            <div class="option-title">Pendek</div>
                            <div class="option-desc">300-500 kata, ringkas dan langsung ke inti</div>
                        </label>
                        <label class="option-card">
                            <input type="radio" name="article-length" value="medium" checked>
                            <div class="option-icon"><i class="fas fa-file"></i></div>
                            <div class="option-title">Medium</div>
                            <div class="option-desc">500-800 kata, lengkap dengan penjelasan mendalam</div>
                        </label>
                        <label class="option-card">
                            <input type="radio" name="article-length" value="long">
                            <div class="option-icon"><i class="fas fa-file-invoice"></i></div>
                            <div class="option-title">Panjang</div>
                            <div class="option-desc">800-1200 kata, komprehensif dengan detail lengkap</div>
                        </label>
                    </div>
                </div>

                <button class="generate-btn" onclick="generateArticle()">
                    <i class="fas fa-bolt"></i> Generate Artikel AI
                </button>
            </div>

            <!-- Features Sidebar -->
            <div class="card">
                <h2 class="section-title">
                    <i class="fas fa-star"></i>
                    Keunggulan Kami
                </h2>
                <ul class="features-list">
                    <li class="feature-item">
                        <div class="feature-icon">
                            <i class="fas fa-check"></i>
                        </div>
                        <span class="feature-text">Konten 100% Original & Unik</span>
                    </li>
                    <li class="feature-item">
                        <div class="feature-icon">
                            <i class="fas fa-check"></i>
                        </div>
                        <span class="feature-text">3 Pilihan Gaya Penulisan</span>
                    </li>
                    <li class="feature-item">
                        <div class="feature-icon">
                            <i class="fas fa-check"></i>
                        </div>
                        <span class="feature-text">Kontrol Panjang Artikel</span>
                    </li>
                    <li class="feature-item">
                        <div class="feature-icon">
                            <i class="fas fa-check"></i>
                        </div>
                        <span class="feature-text">Export ke PDF & Copy Text</span>
                    </li>
                    <li class="feature-item">
                        <div class="feature-icon">
                            <i class="fas fa-check"></i>
                        </div>
                        <span class="feature-text">Proses Ultra Cepat dengan Groq</span>
                    </li>
                    <li class="feature-item">
                        <div class="feature-icon">
                            <i class="fas fa-check"></i>
                        </div>
                        <span class="feature-text">Optimasi SEO Ready</span>
                    </li>
                    <li class="feature-item">
                        <div class="feature-icon">
                            <i class="fas fa-check"></i>
                        </div>
                        <span class="feature-text">Gratis Tanpa Batas</span>
                    </li>
                </ul>
            </div>
        </div>

        <!-- Result Section -->
        <div id="result" class="card result-container"></div>
    </div>

    <!-- Notification -->
    <div id="notification" class="notification">
        <i class="fas fa-check-circle"></i>
        <span id="notification-text"></span>
    </div>

    <script>
        // Configuration
        const CONFIG = {
            wordCounts: {
                short: "300-500",
                medium: "500-800", 
                long: "800-1200"
            },
            styleNames: {
                formal: 'Formal & Professional',
                casual: 'Casual & Santai', 
                creative: 'Kreatif & Menarik'
            },
            lengthNames: {
                short: 'Pendek (300-500 kata)',
                medium: 'Medium (500-800 kata)',
                long: 'Panjang (800-1200 kata)'
            }
        };

        // Create floating particles
        function createParticles() {
            const container = document.getElementById('particles');
            const particleCount = 15;
            
            for (let i = 0; i < particleCount; i++) {
                const particle = document.createElement('div');
                particle.className = 'particle';
                
                // Random properties
                const size = Math.random() * 60 + 20;
                const left = Math.random() * 100;
                const top = Math.random() * 100;
                const delay = Math.random() * 5;
                const duration = Math.random() * 3 + 4;
                
                particle.style.width = `${size}px`;
                particle.style.height = `${size}px`;
                particle.style.left = `${left}%`;
                particle.style.top = `${top}%`;
                particle.style.animationDelay = `${delay}s`;
                particle.style.animationDuration = `${duration}s`;
                
                container.appendChild(particle);
            }
        }

        // Set topic function
        function setTopic(topic) {
            document.getElementById('topic').value = topic;
            document.getElementById('topic').focus();
            showNotification(`Topik disetel: "${topic}"`);
        }

        // Show notification
        function showNotification(message, type = 'success') {
            const notification = document.getElementById('notification');
            const notificationText = document.getElementById('notification-text');
            const notificationIcon = notification.querySelector('i');
            
            notificationText.textContent = message;
            
            if (type === 'error') {
                notification.style.background = '#dc2626';
                notificationIcon.className = 'fas fa-exclamation-triangle';
                notification.classList.add('error');
            } else {
                notification.style.background = '#10b981';
                notificationIcon.className = 'fas fa-check-circle';
                notification.classList.remove('error');
            }
            
            notification.classList.add('show');
            
            setTimeout(() => {
                notification.classList.remove('show');
            }, 4000);
        }

        // Generate article function
        async function generateArticle() {
            const topic = document.getElementById('topic').value.trim();
            const style = document.querySelector('input[name="writing-style"]:checked').value;
            const length = document.querySelector('input[name="article-length"]:checked').value;
            
            const resultDiv = document.getElementById('result');
            const generateBtn = document.querySelector('.generate-btn');
            
            if (!topic) {
                showNotification('Masukkan topik artikel terlebih dahulu!', 'error');
                document.getElementById('topic').focus();
                return;
            }
            
            if (topic.length < 5) {
                showNotification('Topik terlalu pendek. Masukkan topik yang lebih spesifik!', 'error');
                return;
            }
            
            // Show loading
            generateBtn.disabled = true;
            generateBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> AI Sedang Menulis...';
            
            resultDiv.innerHTML = `
                <div class="loading">
                    <div class="loading-icon">
                        <i class="fas fa-robot"></i>
                    </div>
                    <h3>AI Sedang Menulis Artikel</h3>
                    <p>Topik: <strong>${topic}</strong></p>
                    <p>Gaya: <strong>${CONFIG.styleNames[style]}</strong></p>
                    <p>Panjang: <strong>${CONFIG.lengthNames[length]}</strong></p>
                    <p><small>Menggunakan Groq AI • Proses sangat cepat</small></p>
                </div>
            `;
            resultDiv.classList.add('show');
            
            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        topic: topic,
                        style: style,
                        length: length
                    })
                });
                
                const data = await response.json();
                
                if (data.status === 'success') {
                    const articleHTML = formatArticle(data.article);
                    const articleInfo = updateArticleInfo({
                        style: style,
                        length: length,
                        wordCount: data.word_count
                    });
                    
                    resultDiv.innerHTML = `
                        <div class="result-header">
                            <div class="result-icon">
                                <i class="fas fa-check-circle"></i>
                            </div>
                            <div class="result-title">Artikel Berhasil Digenerate!</div>
                        </div>
                        <div class="article-content">
                            ${articleInfo}
                            ${articleHTML}
                            <div class="article-actions">
                                <button class="action-btn copy-btn" onclick="copyArticle()">
                                    <i class="fas fa-copy"></i> Salin Artikel
                                </button>
                                <button class="action-btn download-btn" onclick="downloadArticle()">
                                    <i class="fas fa-download"></i> Download TXT
                                </button>
                                <button class="action-btn regenerate-btn" onclick="generateArticle()">
                                    <i class="fas fa-sync"></i> Generate Ulang
                                </button>
                            </div>
                        </div>
                    `;
                    showNotification('✅ Artikel berhasil digenerate oleh AI!');
                } else {
                    throw new Error(data.error || 'Unknown error from server');
                }
                
            } catch (error) {
                console.error('Error:', error);
                resultDiv.innerHTML = `
                    <div style="display: flex; align-items: center; gap: 1.5rem; padding: 2.5rem; background: rgba(220, 38, 38, 0.1); border-radius: 18px; border: 1px solid rgba(220, 38, 38, 0.3);">
                        <div style="font-size: 2.5rem; color: #dc2626;">
                            <i class="fas fa-exclamation-triangle"></i>
                        </div>
                        <div>
                            <strong style="color: #dc2626; font-size: 1.2rem;">Error:</strong> ${error.message}
                            <br><br>
                            <small style="color: var(--gray);">Pastikan:<br>
                            • GROQ_API_KEY sudah di-set di Vercel<br>
                            • Server berjalan dengan baik<br>
                            • Koneksi internet stabil</small>
                            <br><br>
                            <button class="action-btn" onclick="generateArticle()" style="background: #dc2626;">
                                <i class="fas fa-redo"></i> Coba Lagi
                            </button>
                        </div>
                    </div>
                `;
                showNotification('❌ Gagal generate artikel!', 'error');
            } finally {
                generateBtn.disabled = false;
                generateBtn.innerHTML = '<i class="fas fa-bolt"></i> Generate Artikel AI';
            }
        }

        // Update article info
        function updateArticleInfo(articleData) {
            return `
                <div class="article-meta">
                    <div class="meta-item">
                        <i class="fas fa-palette"></i>
                        <span>Gaya: ${CONFIG.styleNames[articleData.style] || articleData.style}</span>
                    </div>
                    <div class="meta-item">
                        <i class="fas fa-ruler"></i>
                        <span>Panjang: ${CONFIG.lengthNames[articleData.length] || articleData.length}</span>
                    </div>
                    <div class="meta-item">
                        <i class="fas fa-file-word"></i>
                        <span>${articleData.wordCount || '0'} kata</span>
                    </div>
                    <div class="meta-item">
                        <i class="fas fa-bolt"></i>
                        <span>Powered by Groq AI</span>
                    </div>
                </div>
            `;
        }

        // Format article
        function formatArticle(articleText) {
            if (!articleText) return '<p class="article-paragraph">Artikel tidak tersedia.</p>';
            
            const paragraphs = articleText.split('\\n\\n').filter(p => p.trim());
            let html = '';
            
            paragraphs.forEach(paragraph => {
                const trimmed = paragraph.trim();
                if (trimmed) {
                    if (trimmed.match(/^#{1,3}\\s/)) {
                        if (trimmed.startsWith('# ')) {
                            html += `<h1 class="article-title">${trimmed.replace('# ', '')}</h1>`;
                        } else if (trimmed.startsWith('## ')) {
                            html += `<h2 class="section-heading"><i class="fas fa-star"></i> ${trimmed.replace('## ', '')}</h2>`;
                        } else if (trimmed.startsWith('### ')) {
                            html += `<h3 style="font-size: 1.4rem; font-weight: 700; margin: 2rem 0 1rem 0; color: var(--light); padding-left: 1rem; border-left: 4px solid var(--secondary);">${trimmed.replace('### ', '')}</h3>`;
                        }
                    } else {
                        html += `<p class="article-paragraph">${trimmed}</p>`;
                    }
                }
            });
            
            return html;
        }
        
        // Copy article function
        function copyArticle() {
            const articleContent = document.querySelector('.article-content');
            const tempDiv = document.createElement('div');
            tempDiv.innerHTML = articleContent.innerHTML;
            
            const actionButtons = tempDiv.querySelector('.article-actions');
            if (actionButtons) {
                actionButtons.remove();
            }
            
            const textToCopy = tempDiv.textContent || tempDiv.innerText || '';
            
            navigator.clipboard.writeText(textToCopy.trim()).then(() => {
                const copyBtn = document.querySelector('.copy-btn');
                const originalHTML = copyBtn.innerHTML;
                
                copyBtn.innerHTML = '<i class="fas fa-check"></i> Tersalin!';
                copyBtn.style.background = '#10b981';
                
                setTimeout(() => {
                    copyBtn.innerHTML = originalHTML;
                    copyBtn.style.background = '';
                }, 2000);
                
                showNotification('📋 Artikel berhasil disalin ke clipboard!');
            }).catch(err => {
                console.error('Gagal menyalin: ', err);
                showNotification('❌ Gagal menyalin artikel!', 'error');
            });
        }
        
        // Download article function
        function downloadArticle() {
            try {
                const articleContent = document.querySelector('.article-content');
                const topic = document.getElementById('topic').value.trim() || 'Artikel';
                
                const textContent = articleContent.textContent || articleContent.innerText || '';
                const blob = new Blob([textContent], { type: 'text/plain' });
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `Artikel-${topic.replace(/[^a-zA-Z0-9]/g, '-')}.txt`;
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                window.URL.revokeObjectURL(url);
                
                showNotification('📄 Artikel berhasil diunduh!');
                
            } catch (error) {
                console.error('Error generating download:', error);
                showNotification('❌ Gagal mengunduh artikel!', 'error');
            }
        }
        
        // Event listeners
        document.getElementById('topic').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                generateArticle();
            }
        });
        
        // Initialize
        document.addEventListener('DOMContentLoaded', function() {
            createParticles();
            
            document.querySelectorAll('.option-card').forEach(card => {
                card.addEventListener('click', function() {
                    const radio = this.querySelector('input[type="radio"]');
                    radio.checked = true;
                    
                    const groupName = radio.name;
                    document.querySelectorAll(`input[name="${groupName}"]`).forEach(otherRadio => {
                        otherRadio.closest('.option-card').classList.remove('selected');
                    });
                    
                    this.classList.add('selected');
                });
            });
            
            document.querySelectorAll('input[type="radio"]:checked').forEach(radio => {
                radio.closest('.option-card').classList.add('selected');
            });
            
            document.getElementById('topic').focus();
        });
    </script>
</body>
</html>
'''

@app.route('/')
def home():
    """Render halaman utama"""
    return HTML_TEMPLATE

@app.route('/chat', methods=['POST'])
def chat():
    """Endpoint untuk generate artikel dengan Groq AI"""
    if not client:
        return jsonify({
            'status': 'error',
            'error': 'GROQ_API_KEY tidak ditemukan. Pastikan environment variable sudah di-set di Vercel.'
        }), 500
    
    try:
        data = request.json
        topic = data.get('topic', '')
        style = data.get('style', 'formal')
        length = data.get('length', 'medium')
        
        # Validasi input
        if not topic or len(topic.strip()) < 5:
            return jsonify({
                'status': 'error',
                'error': 'Topik terlalu pendek atau kosong'
            }), 400
        
        # Konfigurasi panjang artikel
        length_config = {
            'short': '300-500 kata',
            'medium': '500-800 kata',
            'long': '800-1200 kata'
        }
        
        # Konfigurasi gaya penulisan
        style_config = {
            'formal': 'profesional dan akademis dengan bahasa baku',
            'casual': 'santai dan mudah dipahami seperti percakapan sehari-hari',
            'creative': 'kreatif dan menarik dengan bahasa yang inspiratif'
        }
        
        # Prompt untuk Groq AI
        prompt = f"""Tulis artikel dalam bahasa Indonesia dengan detail berikut:

Topik: {topic}
Gaya: {style_config.get(style, 'profesional dan akademis')}
Panjang: {length_config.get(length, '500-800 kata')}

Format artikel dengan struktur berikut:
# [Judul Artikel yang Menarik dan SEO-Friendly]

## Pendahuluan
[Paragraf pembuka yang engaging dan menarik perhatian pembaca]

## [Subjudul 1 - Poin Utama Pertama]
[Konten mendalam dengan penjelasan detail]

## [Subjudul 2 - Poin Utama Kedua]
[Konten mendalam dengan penjelasan detail]

## [Subjudul 3 - Poin Utama Ketiga]
[Konten mendalam dengan penjelasan detail]

## Kesimpulan
[Paragraf penutup yang merangkum poin-poin penting]

Pastikan artikel:
- 100% original dan unik
- Informatif dan berkualitas tinggi
- Terstruktur dengan baik menggunakan heading dan subheading
- Sesuai dengan panjang {length_config.get(length, '500-800 kata')}
- Menggunakan gaya penulisan {style_config.get(style, 'profesional')}
- Mudah dibaca dan dipahami
- Menggunakan bahasa Indonesia yang baik dan benar"""

        # Call Groq API
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "Kamu adalah penulis artikel profesional berbahasa Indonesia yang ahli dalam menulis konten berkualitas tinggi, informatif, engaging, dan SEO-friendly. Kamu selalu menghasilkan artikel yang terstruktur dengan baik, mudah dibaca, dan memberikan nilai tambah kepada pembaca."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=2048,
            top_p=0.9
        )
        
        article = completion.choices[0].message.content
        word_count = len(article.split())
        
        return jsonify({
            'status': 'success',
            'article': article,
            'word_count': word_count,
            'style': style,
            'length': length
        })
        
    except Exception as e:
        print(f"Error in /chat endpoint: {str(e)}")
        return jsonify({
            'status': 'error',
            'error': f'Terjadi kesalahan: {str(e)}'
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)