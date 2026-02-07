cat > /home/claude/script.js << 'JSEOF'
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

// Generate article function - UPDATED to use /api/generate
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
        // Call API - UPDATED endpoint to /api/generate
        const response = await fetch('/api/generate', {
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
    
    const paragraphs = articleText.split('\n\n').filter(p => p.trim());
    let html = '';
    
    paragraphs.forEach(paragraph => {
        const trimmed = paragraph.trim();
        if (trimmed) {
            if (trimmed.match(/^#{1,3}\s/)) {
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