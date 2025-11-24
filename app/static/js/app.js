let currentLang = localStorage.getItem('manga_tutor_lang') || 'en';
let currentLesson = null;
let stream = null;

const translations = {
    en: {
        welcome: "Welcome, Student!",
        intro: "Ready to become a Manga Master? Choose a lesson below.",
        back: "← Back",
        instructions: "Instructions",
        your_task: "Your Task:",
        upload_title: "Show Sensei Your Work!",
        camera_btn: "📷 Open Camera",
        upload_btn: "📁 Upload File",
        analyze_btn: "✨ Analyze Drawing",
        analyzing: "Sensei is looking...",
        lesson: "Lesson"
    },
    es: {
        welcome: "¡Bienvenido, Estudiante!",
        intro: "¿Listo para ser un Maestro Manga? Elige una lección.",
        back: "← Volver",
        instructions: "Instrucciones",
        your_task: "Tu Tarea:",
        upload_title: "¡Muestrale a Sensei tu trabajo!",
        camera_btn: "📷 Abrir Cámara",
        upload_btn: "📁 Subir Archivo",
        analyze_btn: "✨ Analizar Dibujo",
        analyzing: "Sensei está mirando...",
        lesson: "Lección"
    }
};

function setLanguage(lang) {
    currentLang = lang;
    localStorage.setItem('manga_tutor_lang', lang);
    updateUI();

    // Update buttons
    document.querySelectorAll('.lang-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.lang === lang);
    });
}

function updateUI() {
    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.dataset.i18n;
        if (translations[currentLang][key]) {
            el.innerText = translations[currentLang][key];
        }
    });

    // Update dynamic content if loaded
    if (currentLesson) {
        document.getElementById('lesson-title').innerText = currentLesson.title[currentLang];
        document.getElementById('lesson-description').innerText = currentLesson.description[currentLang];
        document.getElementById('lesson-task').innerText = currentLesson.task[currentLang];

        // Update Examples
        const goodImg = document.getElementById('example-good');
        if (currentLesson.example_good) {
            goodImg.src = currentLesson.example_good;
            goodImg.parentElement.style.display = 'block';
        } else {
            goodImg.parentElement.style.display = 'none';
        }

        const badContainer = document.getElementById('examples-bad-container');
        badContainer.innerHTML = '';
        if (currentLesson.examples_bad && currentLesson.examples_bad.length > 0) {
            currentLesson.examples_bad.forEach(src => {
                const img = document.createElement('img');
                img.src = src;
                img.style.width = '100%';
                img.style.borderRadius = '8px';
                img.style.border = '2px solid #c0392b';
                badContainer.appendChild(img);
            });
            badContainer.parentElement.style.display = 'block';
        } else {
            badContainer.parentElement.style.display = 'none';
        }
    }

    // Reload curriculum list if on home page
    if (document.getElementById('modules-list')) {
        loadCurriculum();
    }
}

async function loadCurriculum() {
    const list = document.getElementById('modules-list');
    if (!list) return;

    try {
        const response = await fetch('/api/lessons');
        const modules = await response.json();

        list.innerHTML = modules.map(module => `
            <div class="card">
                <h3 class="module-title">${module.title[currentLang]}</h3>
                ${module.lessons.map(lesson => `
                    <div class="lesson-item" onclick="window.location.href='/lesson/${lesson.id}'" style="cursor: pointer;">
                        <span>${translations[currentLang].lesson} ${lesson.id}: ${lesson.title[currentLang]}</span>
                        <span>➜</span>
                    </div>
                `).join('')}
            </div>
        `).join('');
    } catch (e) {
        list.innerHTML = "Error loading lessons.";
    }
}

// Camera & Upload Logic
async function startCamera() {
    const video = document.getElementById('camera-preview');
    const imgPreview = document.getElementById('image-preview');

    try {
        stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' } });
        video.srcObject = stream;
        video.style.display = 'block';
        imgPreview.style.display = 'none';

        // Change button to "Take Photo"
        const btn = document.querySelector('button[onclick="startCamera()"]');
        btn.innerText = "📸 Snap!";
        btn.onclick = takePhoto;
    } catch (e) {
        alert("Camera access denied or not available.");
    }
}

function takePhoto() {
    const video = document.getElementById('camera-preview');
    const canvas = document.getElementById('snapshot-canvas');
    const imgPreview = document.getElementById('image-preview');
    const analyzeBtn = document.getElementById('analyze-btn');

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    canvas.getContext('2d').drawImage(video, 0, 0);

    const dataUrl = canvas.toDataURL('image/jpeg');
    imgPreview.src = dataUrl;
    imgPreview.style.display = 'block';
    video.style.display = 'none';

    // Stop stream
    stream.getTracks().forEach(track => track.stop());

    // Reset button
    const btn = document.querySelector('button[onclick="takePhoto"]'); // Selector might need fix
    // Actually simpler to just reload page to reset or manual reset. 
    // For now let's just show analyze button
    analyzeBtn.style.display = 'block';
}

function handleFileUpload(input) {
    if (input.files && input.files[0]) {
        const reader = new FileReader();
        reader.onload = function (e) {
            const imgPreview = document.getElementById('image-preview');
            imgPreview.src = e.target.result;
            imgPreview.style.display = 'block';
            document.getElementById('camera-preview').style.display = 'none';
            document.getElementById('analyze-btn').style.display = 'block';
        }
        reader.readAsDataURL(input.files[0]);
    }
}

async function analyzeDrawing() {
    const imgPreview = document.getElementById('image-preview');
    const feedbackArea = document.getElementById('feedback-area');
    const feedbackText = document.getElementById('feedback-text');
    const analyzeBtn = document.getElementById('analyze-btn');

    analyzeBtn.disabled = true;
    analyzeBtn.innerText = translations[currentLang].analyzing;

    // Convert data URL to blob
    const res = await fetch(imgPreview.src);
    const blob = await res.blob();

    const formData = new FormData();
    formData.append('file', blob, 'drawing.jpg');
    formData.append('task', document.getElementById('lesson-task').innerText);
    formData.append('language', currentLang);

    try {
        const response = await fetch('/api/analyze', {
            method: 'POST',
            body: formData
        });
        const data = await response.json();

        feedbackText.innerText = data.feedback;
        feedbackArea.style.display = 'block';

        // Auto-speak? Maybe optional.
    } catch (e) {
        feedbackText.innerText = "Error analyzing drawing.";
    } finally {
        analyzeBtn.disabled = false;
        analyzeBtn.innerText = translations[currentLang].analyze_btn;
    }
}

// Audio Logic
let voices = [];

function loadVoices() {
    voices = window.speechSynthesis.getVoices();
}

if (speechSynthesis.onvoiceschanged !== undefined) {
    speechSynthesis.onvoiceschanged = loadVoices;
}

function getVoiceForLang(lang) {
    if (voices.length === 0) loadVoices();

    // Try to find a specific voice for the language
    // For "anime" feel, maybe higher pitch female voices often work well if available
    const langCode = lang === 'es' ? 'es' : 'en';
    return voices.find(v => v.lang.startsWith(langCode) && v.name.includes('Google')) ||
        voices.find(v => v.lang.startsWith(langCode)) ||
        null;
}

function speakText(text) {
    if (!window.speechSynthesis) {
        alert("Text-to-Speech is not supported in this browser.");
        return;
    }

    window.speechSynthesis.cancel(); // Stop previous

    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = currentLang === 'es' ? 'es-ES' : 'en-US';
    utterance.rate = 1.0;
    utterance.pitch = 1.2; // Anime style pitch

    const voice = getVoiceForLang(currentLang);
    if (voice) {
        utterance.voice = voice;
    }

    // Visual Feedback
    const btn = document.querySelector('button[onclick="speakFeedback()"]');
    const originalText = btn ? btn.innerText : "";
    if (btn) btn.innerText = "🔊 Speaking...";

    utterance.onend = () => {
        if (btn) btn.innerText = originalText;
    };

    utterance.onerror = (e) => {
        console.error("TTS Error:", e);
        if (btn) btn.innerText = "❌ Error";
        setTimeout(() => { if (btn) btn.innerText = originalText; }, 2000);
    };

    window.speechSynthesis.speak(utterance);
}

function speakFeedback() {
    const text = document.getElementById('feedback-text').innerText;
    if (!text || text === "...") {
        alert("No feedback to read yet!");
        return;
    }
    speakText(text);
}

function testAudio() {
    const text = currentLang === 'es' ? "¡Hola! Soy Sensei Yuki. ¿Puedes escucharme?" : "Hello! I am Sensei Yuki. Can you hear me?";
    speakText(text);
}

function speakInstructions() {
    const desc = document.getElementById('lesson-description').innerText;
    const task = document.getElementById('lesson-task').innerText;
    const fullText = desc + ". " + translations[currentLang].your_task + " " + task;

    speakText(fullText);
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    setLanguage(currentLang);

    // If on lesson page, load details
    const path = window.location.pathname;
    if (path.startsWith('/lesson/')) {
        const id = path.split('/').pop();
        fetch(`/api/lessons/${id}`)
            .then(r => r.json())
            .then(data => {
                currentLesson = data;
                updateUI();
            });
    }
});
