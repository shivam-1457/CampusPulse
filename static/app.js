/**
 * CampusPulse: Accessible Multimodal Health & Safety Companion
 * Client Application Logic
 */

// State
const AppState = {
  currentProtocol: null,
  currentImageBase64: null,
  apiKey: localStorage.getItem('gemini_api_key') || '',
  selectedLanguage: 'en',
  plainLanguage: false,
  isSpeechActive: false,
  isListening: false,
  cprInterval: null,
  isCprRunning: false,
  activeTimer: null,
  activeTimerSeconds: 0,
  activeTimerInterval: null,
  userLocation: {
    building: 'Science Complex',
    room: 'Lab 304',
    lat: null,
    lng: null
  }
};

// DOM Elements
const elements = {
  // Input
  promptInput: document.getElementById('promptInput'),
  fileInput: document.getElementById('fileInput'),
  cameraInput: document.getElementById('cameraInput'),
  dropZone: document.getElementById('dropZone'),
  previewContainer: document.getElementById('previewContainer'),
  imagePreview: document.getElementById('imagePreview'),
  removeMediaBtn: document.getElementById('removeMediaBtn'),
  btnAnalyze: document.getElementById('btnAnalyze'),
  micBtn: document.getElementById('micBtn'),
  langSelect: document.getElementById('langSelect'),
  
  // Results
  resultsContainer: document.getElementById('resultsContainer'),
  resultsPlaceholder: document.getElementById('resultsPlaceholder'),
  protocolTitle: document.getElementById('protocolTitle'),
  severityBanner: document.getElementById('severityBanner'),
  severityText: document.getElementById('severityText'),
  severityBadge: document.getElementById('severityBadge'),
  immediateActionText: document.getElementById('immediateActionText'),
  stepsList: document.getElementById('stepsList'),
  dosList: document.getElementById('dosList'),
  dontsList: document.getElementById('dontsList'),
  redFlagsList: document.getElementById('redFlagsList'),
  redFlagsContainer: document.getElementById('redFlagsContainer'),
  equipmentList: document.getElementById('equipmentList'),
  providerBadge: document.getElementById('providerBadge'),
  
  // Audio & TTS
  btnReadAloud: document.getElementById('btnReadAloud'),
  speechStatus: document.getElementById('speechStatus'),
  
  // Timers & Metronome
  timerContainer: document.getElementById('timerContainer'),
  timerTitle: document.getElementById('timerTitle'),
  timerDisplay: document.getElementById('timerDisplay'),
  btnStartTimer: document.getElementById('btnStartTimer'),
  btnResetTimer: document.getElementById('btnResetTimer'),
  cprContainer: document.getElementById('cprContainer'),
  cprHeart: document.getElementById('cprHeart'),
  btnToggleCpr: document.getElementById('btnToggleCpr'),
  
  // SOS & Modal
  btnOpenSosModal: document.getElementById('btnOpenSosModal'),
  sosModal: document.getElementById('sosModal'),
  btnCloseSosModal: document.getElementById('btnCloseSosModal'),
  btnConfirmDispatch: document.getElementById('btnConfirmDispatch'),
  sosBuildingSelect: document.getElementById('sosBuildingSelect'),
  sosRoomInput: document.getElementById('sosRoomInput'),
  sosGpsStatus: document.getElementById('sosGpsStatus'),
  sosDispatchResult: document.getElementById('sosDispatchResult'),
  btnSosBeacon: document.getElementById('btnSosBeacon'),
  beaconOverlay: document.getElementById('beaconOverlay'),
  
  // Accessibility Toggles
  toggleHighContrast: document.getElementById('toggleHighContrast'),
  toggleDyslexia: document.getElementById('toggleDyslexia'),
  toggleLargeText: document.getElementById('toggleLargeText'),
  togglePlainLanguage: document.getElementById('togglePlainLanguage'),
  
  // API Key Settings Modal
  btnOpenSettings: document.getElementById('btnOpenSettings'),
  settingsModal: document.getElementById('settingsModal'),
  btnCloseSettings: document.getElementById('btnCloseSettings'),
  apiKeyInput: document.getElementById('apiKeyInput'),
  btnSaveApiKey: document.getElementById('btnSaveApiKey'),
  
  // Facilities
  facilitiesList: document.getElementById('facilitiesList'),
  quickChips: document.querySelectorAll('.chip-emergency')
};

// Web Audio API Context for CPR Beat and SOS Siren
let audioCtx = null;
function getAudioContext() {
  if (!audioCtx) {
    audioCtx = new (window.AudioContext || window.webkitAudioContext)();
  }
  if (audioCtx.state === 'suspended') {
    audioCtx.resume();
  }
  return audioCtx;
}

function playCprBeep() {
  try {
    const ctx = getAudioContext();
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();
    
    osc.type = 'sine';
    osc.frequency.setValueAtTime(880, ctx.currentTime); // 880 Hz beep (A5)
    
    gain.gain.setValueAtTime(0.3, ctx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.08);
    
    osc.connect(gain);
    gain.connect(ctx.destination);
    
    osc.start();
    osc.stop(ctx.currentTime + 0.08);
  } catch (e) {
    console.warn('Audio play error:', e);
  }
}

let sirenInterval = null;
function playSosAlarm() {
  stopSosAlarm();
  try {
    const ctx = getAudioContext();
    let toggleFreq = false;
    
    sirenInterval = setInterval(() => {
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      osc.type = 'triangle';
      osc.frequency.setValueAtTime(toggleFreq ? 950 : 650, ctx.currentTime);
      gain.gain.setValueAtTime(0.4, ctx.currentTime);
      gain.gain.linearRampToValueAtTime(0.01, ctx.currentTime + 0.28);
      osc.connect(gain);
      gain.connect(ctx.destination);
      osc.start();
      osc.stop(ctx.currentTime + 0.28);
      toggleFreq = !toggleFreq;
    }, 300);
  } catch (e) {
    console.warn('Siren audio error:', e);
  }
}

function stopSosAlarm() {
  if (sirenInterval) {
    clearInterval(sirenInterval);
    sirenInterval = null;
  }
}

// ----------------------------------------------------
// Initialization
// ----------------------------------------------------
document.addEventListener('DOMContentLoaded', () => {
  initEventListeners();
  loadCampusFacilities();
  checkGeolocation();
  
  // Set saved API key into input
  if (AppState.apiKey && elements.apiKeyInput) {
    elements.apiKeyInput.value = AppState.apiKey;
  }
  
  // Load default burn protocol for immediate preview
  loadOfflineProtocol('burn');
});

function initEventListeners() {
  // Multimodal File & Image Input
  if (elements.dropZone) {
    elements.dropZone.addEventListener('click', () => elements.fileInput.click());
    elements.dropZone.addEventListener('dragover', (e) => {
      e.preventDefault();
      elements.dropZone.classList.add('dragover');
    });
    elements.dropZone.addEventListener('dragleave', () => elements.dropZone.classList.remove('dragover'));
    elements.dropZone.addEventListener('drop', (e) => {
      e.preventDefault();
      elements.dropZone.classList.remove('dragover');
      if (e.dataTransfer.files && e.dataTransfer.files[0]) {
        handleImageFile(e.dataTransfer.files[0]);
      }
    });
  }

  if (elements.fileInput) {
    elements.fileInput.addEventListener('change', (e) => {
      if (e.target.files && e.target.files[0]) {
        handleImageFile(e.target.files[0]);
      }
    });
  }

  if (elements.removeMediaBtn) {
    elements.removeMediaBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      clearMediaPreview();
    });
  }

  // Analyze Button
  if (elements.btnAnalyze) {
    elements.btnAnalyze.addEventListener('click', () => analyzeIncident());
  }

  // Textarea enter key (Ctrl+Enter or Enter)
  if (elements.promptInput) {
    elements.promptInput.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) {
        e.preventDefault();
        analyzeIncident();
      }
    });
  }

  // Speech Recognition (Mic)
  if (elements.micBtn) {
    elements.micBtn.addEventListener('click', toggleVoiceInput);
  }

  // Text to Speech
  if (elements.btnReadAloud) {
    elements.btnReadAloud.addEventListener('click', toggleReadAloud);
  }

  // Quick Chips
  elements.quickChips.forEach(chip => {
    chip.addEventListener('click', () => {
      elements.quickChips.forEach(c => c.classList.remove('active'));
      chip.classList.add('active');
      const protoKey = chip.getAttribute('data-protocol');
      loadOfflineProtocol(protoKey);
    });
  });

  // CPR Metronome
  if (elements.btnToggleCpr) {
    elements.btnToggleCpr.addEventListener('click', toggleCprMetronome);
  }

  // Timers
  if (elements.btnStartTimer) {
    elements.btnStartTimer.addEventListener('click', toggleCountdownTimer);
  }
  if (elements.btnResetTimer) {
    elements.btnResetTimer.addEventListener('click', resetCountdownTimer);
  }

  // SOS Modal
  if (elements.btnOpenSosModal) {
    elements.btnOpenSosModal.addEventListener('click', openSosModal);
  }
  if (elements.btnCloseSosModal) {
    elements.btnCloseSosModal.addEventListener('click', closeSosModal);
  }
  if (elements.btnConfirmDispatch) {
    elements.btnConfirmDispatch.addEventListener('click', executeSosDispatch);
  }

  // SOS Beacon
  if (elements.btnSosBeacon) {
    elements.btnSosBeacon.addEventListener('click', startSosBeacon);
  }
  if (elements.beaconOverlay) {
    elements.beaconOverlay.addEventListener('click', stopSosBeacon);
  }

  // Accessibility Toggles
  if (elements.toggleHighContrast) {
    elements.toggleHighContrast.addEventListener('change', (e) => {
      document.body.classList.toggle('high-contrast', e.target.checked);
    });
  }
  if (elements.toggleDyslexia) {
    elements.toggleDyslexia.addEventListener('change', (e) => {
      document.body.classList.toggle('dyslexia-mode', e.target.checked);
    });
  }
  if (elements.toggleLargeText) {
    elements.toggleLargeText.addEventListener('change', (e) => {
      document.body.classList.toggle('large-text', e.target.checked);
    });
  }
  if (elements.togglePlainLanguage) {
    elements.togglePlainLanguage.addEventListener('change', (e) => {
      AppState.plainLanguage = e.target.checked;
      if (AppState.currentProtocol) {
        renderProtocol(AppState.currentProtocol);
      }
    });
  }

  // Language Change
  if (elements.langSelect) {
    elements.langSelect.addEventListener('change', (e) => {
      AppState.selectedLanguage = e.target.value;
      if (AppState.currentProtocol) {
        translateCurrentProtocol(e.target.value);
      }
    });
  }

  // Settings Modal (API Key)
  if (elements.btnOpenSettings) {
    elements.btnOpenSettings.addEventListener('click', () => {
      elements.settingsModal.classList.add('active');
    });
  }
  if (elements.btnCloseSettings) {
    elements.btnCloseSettings.addEventListener('click', () => {
      elements.settingsModal.classList.remove('active');
    });
  }
  if (elements.btnSaveApiKey) {
    elements.btnSaveApiKey.addEventListener('click', () => {
      const key = elements.apiKeyInput.value.trim();
      AppState.apiKey = key;
      localStorage.setItem('gemini_api_key', key);
      elements.settingsModal.classList.remove('active');
      showNotification('Gemini API key saved successfully!');
    });
  }
}

// ----------------------------------------------------
// Image Processing
// ----------------------------------------------------
function handleImageFile(file) {
  if (!file.type.startsWith('image/')) {
    alert('Please upload an image file (PNG, JPG, WebP).');
    return;
  }
  const reader = new FileReader();
  reader.onload = (e) => {
    AppState.currentImageBase64 = e.target.result;
    elements.imagePreview.src = e.target.result;
    elements.previewContainer.style.display = 'block';
    elements.dropZone.style.display = 'none';
  };
  reader.readAsDataURL(file);
}

function clearMediaPreview() {
  AppState.currentImageBase64 = null;
  elements.imagePreview.src = '';
  elements.previewContainer.style.display = 'none';
  elements.dropZone.style.display = 'flex';
  if (elements.fileInput) elements.fileInput.value = '';
}

// ----------------------------------------------------
// Incident Analysis (Multimodal AI)
// ----------------------------------------------------
async function analyzeIncident() {
  const queryText = elements.promptInput.value.trim();
  const imageBase64 = AppState.currentImageBase64;
  
  if (!queryText && !imageBase64) {
    alert('Please enter a description or upload an image of the emergency/hazard.');
    return;
  }

  // Show loading
  elements.btnAnalyze.disabled = true;
  elements.btnAnalyze.innerHTML = `<span class="loader-spinner"></span> Analyzing Triage...`;

  try {
    const res = await fetch('/api/analyze', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        text: queryText,
        image_base64: imageBase64,
        language: AppState.selectedLanguage,
        api_key: AppState.apiKey
      })
    });

    if (!res.ok) throw new Error('Analysis server error');
    const data = await res.json();
    AppState.currentProtocol = data;
    renderProtocol(data);

    // Auto voice announcement of immediate action if severe
    if (data.severity === 'severe') {
      speakText(`Urgent safety action: ${data.immediate_action}`);
    }
  } catch (err) {
    console.error('Analysis error:', err);
    // Fallback locally
    loadOfflineProtocol('burn');
  } finally {
    elements.btnAnalyze.disabled = false;
    elements.btnAnalyze.innerHTML = `<span>⚡</span> Immediate Triage & Action`;
  }
}

// ----------------------------------------------------
// Protocol Rendering
// ----------------------------------------------------
function renderProtocol(data) {
  elements.resultsPlaceholder.style.display = 'none';
  elements.resultsContainer.style.display = 'block';

  // Title
  elements.protocolTitle.textContent = data.title;
  
  // Provider badge
  if (data.is_fallback) {
    elements.providerBadge.textContent = 'Verified Offline Protocol';
    elements.providerBadge.className = 'offline-pill fallback';
  } else {
    elements.providerBadge.textContent = 'Gemini Multimodal Live Triage';
    elements.providerBadge.className = 'offline-pill';
  }

  // Severity
  const sev = (data.severity || 'moderate').toLowerCase();
  elements.severityBanner.className = `severity-banner ${sev}`;
  elements.severityText.textContent = data.severity_badge || `${sev.toUpperCase()} PRIORITY`;
  elements.severityBadge.textContent = `SEVERITY: ${sev.toUpperCase()}`;

  // Immediate Action
  elements.immediateActionText.textContent = data.immediate_action;

  // Steps Checklist
  elements.stepsList.innerHTML = '';
  (data.steps || []).forEach((step, idx) => {
    const li = document.createElement('div');
    li.className = 'step-item';
    li.innerHTML = `
      <input type="checkbox" class="step-checkbox" id="step_${idx}">
      <div class="step-content">
        <label for="step_${idx}" style="cursor:pointer;">
          <span class="step-num">Step ${idx + 1}:</span> ${step}
        </label>
      </div>
    `;
    const cb = li.querySelector('.step-checkbox');
    cb.addEventListener('change', () => {
      li.classList.toggle('completed', cb.checked);
    });
    elements.stepsList.appendChild(li);
  });

  // Do's
  elements.dosList.innerHTML = '';
  (data.dos || []).forEach(item => {
    const li = document.createElement('li');
    li.textContent = item;
    elements.dosList.appendChild(li);
  });

  // Don'ts
  elements.dontsList.innerHTML = '';
  (data.donts || []).forEach(item => {
    const li = document.createElement('li');
    li.textContent = item;
    elements.dontsList.appendChild(li);
  });

  // Red Flags
  if (data.red_flags && data.red_flags.length > 0) {
    elements.redFlagsContainer.style.display = 'block';
    elements.redFlagsList.innerHTML = '';
    data.red_flags.forEach(flag => {
      const li = document.createElement('li');
      li.textContent = flag;
      elements.redFlagsList.appendChild(li);
    });
  } else {
    elements.redFlagsContainer.style.display = 'none';
  }

  // Equipment
  elements.equipmentList.innerHTML = '';
  (data.recommended_equipment || []).forEach(eq => {
    const span = document.createElement('span');
    span.className = 'facility-badge';
    span.textContent = eq;
    elements.equipmentList.appendChild(span);
  });

  // Setup Timers / CPR Metronome based on protocol
  configureToolsForProtocol(data);

  // Scroll to results smoothly
  elements.resultsContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// ----------------------------------------------------
// Timers & CPR Metronome
// ----------------------------------------------------
function configureToolsForProtocol(data) {
  const timerType = data.timer_type || 'none';
  const duration = data.timer_duration_seconds || 0;

  // CPR Metronome
  if (timerType === 'cpr_metronome') {
    elements.cprContainer.style.display = 'block';
    elements.timerContainer.style.display = 'none';
  } else if (duration > 0) {
    elements.cprContainer.style.display = 'none';
    elements.timerContainer.style.display = 'block';
    
    let title = 'First-Aid Treatment Timer';
    if (timerType === 'burn_rinse') title = '💧 Cool Water Rinse Timer (15 Min)';
    else if (timerType === 'eyewash') title = '👁️ Continuous Eyewash Flush Timer (15 Min)';
    else if (timerType === 'bleeding_pressure') title = '🩸 Direct Pressure Timer (5 Min)';
    else if (timerType === 'ice_pack') title = '🧊 Cold Pack Application Timer (15 Min)';
    
    elements.timerTitle.textContent = title;
    setupCountdownTimer(duration);
  } else {
    elements.cprContainer.style.display = 'none';
    elements.timerContainer.style.display = 'none';
  }
}

function setupCountdownTimer(seconds) {
  clearInterval(AppState.activeTimerInterval);
  AppState.activeTimerSeconds = seconds;
  AppState.activeTimerRunning = false;
  elements.btnStartTimer.textContent = 'Start Timer';
  updateTimerDisplay();
}

function updateTimerDisplay() {
  const mins = Math.floor(AppState.activeTimerSeconds / 60);
  const secs = AppState.activeTimerSeconds % 60;
  elements.timerDisplay.textContent = `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
}

function toggleCountdownTimer() {
  if (AppState.activeTimerRunning) {
    clearInterval(AppState.activeTimerInterval);
    AppState.activeTimerRunning = false;
    elements.btnStartTimer.textContent = 'Resume Timer';
  } else {
    AppState.activeTimerRunning = true;
    elements.btnStartTimer.textContent = 'Pause Timer';
    AppState.activeTimerInterval = setInterval(() => {
      if (AppState.activeTimerSeconds > 0) {
        AppState.activeTimerSeconds--;
        updateTimerDisplay();
        if (AppState.activeTimerSeconds === 0) {
          clearInterval(AppState.activeTimerInterval);
          AppState.activeTimerRunning = false;
          elements.btnStartTimer.textContent = 'Completed!';
          speakText('Timer complete. Assess patient status.');
          playCprBeep();
        }
      }
    }, 1000);
  }
}

function resetCountdownTimer() {
  clearInterval(AppState.activeTimerInterval);
  AppState.activeTimerRunning = false;
  if (AppState.currentProtocol && AppState.currentProtocol.timer_duration_seconds) {
    AppState.activeTimerSeconds = AppState.currentProtocol.timer_duration_seconds;
  } else {
    AppState.activeTimerSeconds = 900;
  }
  elements.btnStartTimer.textContent = 'Start Timer';
  updateTimerDisplay();
}

function toggleCprMetronome() {
  if (AppState.isCprRunning) {
    clearInterval(AppState.cprInterval);
    AppState.cprInterval = null;
    AppState.isCprRunning = false;
    elements.btnToggleCpr.textContent = 'Start CPR Metronome (110 BPM)';
    elements.btnToggleCpr.classList.remove('btn-sos-primary');
    elements.cprHeart.classList.remove('beat');
  } else {
    AppState.isCprRunning = true;
    elements.btnToggleCpr.textContent = 'Stop Metronome';
    elements.btnToggleCpr.classList.add('btn-sos-primary');
    
    // 110 BPM = 60000ms / 110 = 545.45 ms per beat
    const intervalMs = 60000 / 110;
    
    // Play first beat immediately
    playCprBeep();
    elements.cprHeart.classList.add('beat');
    setTimeout(() => elements.cprHeart.classList.remove('beat'), 150);

    AppState.cprInterval = setInterval(() => {
      playCprBeep();
      elements.cprHeart.classList.add('beat');
      setTimeout(() => elements.cprHeart.classList.remove('beat'), 150);
    }, intervalMs);
  }
}

// ----------------------------------------------------
// Offline Protocol Quick Loader
// ----------------------------------------------------
async function loadOfflineProtocol(protoKey) {
  try {
    const res = await fetch('/api/protocols');
    const allProtocols = await res.json();
    if (allProtocols[protoKey]) {
      const data = allProtocols[protoKey];
      data.is_fallback = true;
      AppState.currentProtocol = data;
      renderProtocol(data);
    }
  } catch (err) {
    console.error('Failed to load protocol:', err);
  }
}

// ----------------------------------------------------
// Text-to-Speech (TTS) & Speech Recognition (STT)
// ----------------------------------------------------
function toggleReadAloud() {
  if (!('speechSynthesis' in window)) {
    alert('Speech synthesis is not supported on your device.');
    return;
  }
  if (window.speechSynthesis.speaking) {
    window.speechSynthesis.cancel();
    AppState.isSpeechActive = false;
    elements.btnReadAloud.classList.remove('active');
    elements.speechStatus.textContent = 'Read Aloud';
  } else {
    if (!AppState.currentProtocol) return;
    const p = AppState.currentProtocol;
    const textToSpeak = `${p.title}. Severity: ${p.severity}. Immediate Action: ${p.immediate_action}. Steps: ${p.steps.join('. ')}`;
    speakText(textToSpeak);
  }
}

function speakText(text) {
  if (!('speechSynthesis' in window)) return;
  window.speechSynthesis.cancel();
  
  const utterance = new SpeechSynthesisUtterance(text);
  utterance.rate = 1.0;
  utterance.pitch = 1.0;
  
  // Set language
  if (AppState.selectedLanguage === 'es') utterance.lang = 'es-ES';
  else if (AppState.selectedLanguage === 'hi') utterance.lang = 'hi-IN';
  else if (AppState.selectedLanguage === 'zh') utterance.lang = 'zh-CN';
  else if (AppState.selectedLanguage === 'fr') utterance.lang = 'fr-FR';
  else if (AppState.selectedLanguage === 'ar') utterance.lang = 'ar-SA';
  else if (AppState.selectedLanguage === 'de') utterance.lang = 'de-DE';
  else utterance.lang = 'en-US';

  utterance.onstart = () => {
    AppState.isSpeechActive = true;
    elements.btnReadAloud.classList.add('active');
    elements.speechStatus.textContent = 'Speaking...';
  };
  utterance.onend = () => {
    AppState.isSpeechActive = false;
    elements.btnReadAloud.classList.remove('active');
    elements.speechStatus.textContent = 'Read Aloud';
  };

  window.speechSynthesis.speak(utterance);
}

function toggleVoiceInput() {
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SpeechRecognition) {
    alert('Speech recognition is not supported in this browser. Please use Chrome/Edge or type your description.');
    return;
  }

  if (AppState.isListening) {
    if (AppState.recognitionInstance) AppState.recognitionInstance.stop();
    return;
  }

  const recognition = new SpeechRecognition();
  recognition.lang = 'en-US';
  recognition.interimResults = false;
  recognition.maxAlternatives = 1;

  recognition.onstart = () => {
    AppState.isListening = true;
    AppState.recognitionInstance = recognition;
    elements.micBtn.classList.add('listening');
  };

  recognition.onresult = (event) => {
    const transcript = event.results[0][0].transcript;
    elements.promptInput.value = (elements.promptInput.value + ' ' + transcript).trim();
  };

  recognition.onend = () => {
    AppState.isListening = false;
    elements.micBtn.classList.remove('listening');
  };

  recognition.onerror = (event) => {
    console.warn('Speech recognition error:', event.error);
    AppState.isListening = false;
    elements.micBtn.classList.remove('listening');
  };

  recognition.start();
}

// ----------------------------------------------------
// Multilingual Translation
// ----------------------------------------------------
async function translateCurrentProtocol(lang) {
  if (lang === 'en' || !AppState.currentProtocol) return;
  
  try {
    const res = await fetch('/api/translate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        text: AppState.currentProtocol.immediate_action,
        target_language: lang,
        api_key: AppState.apiKey
      })
    });
    const data = await res.json();
    if (data.translated_text) {
      elements.immediateActionText.innerHTML = `
        <span style="display:block; margin-bottom:0.35rem; color:#38bdf8;">[${lang.toUpperCase()}] ${data.translated_text}</span>
        <span style="font-size:0.85rem; opacity:0.75; font-weight:normal;">(EN) ${AppState.currentProtocol.immediate_action}</span>
      `;
    }
  } catch (err) {
    console.error('Translation error:', err);
  }
}

// ----------------------------------------------------
// Geolocation & Facilities
// ----------------------------------------------------
function checkGeolocation() {
  if ('geolocation' in navigator) {
    navigator.geolocation.getCurrentPosition(
      (pos) => {
        AppState.userLocation.lat = pos.coords.latitude;
        AppState.userLocation.lng = pos.coords.longitude;
        if (elements.sosGpsStatus) {
          elements.sosGpsStatus.textContent = `📍 GPS Fixed: ${pos.coords.latitude.toFixed(4)}, ${pos.coords.longitude.toFixed(4)} (±${Math.round(pos.coords.accuracy)}m)`;
        }
      },
      (err) => {
        if (elements.sosGpsStatus) {
          elements.sosGpsStatus.textContent = '📍 GPS: Indoor / Campus Network Fallback';
        }
      },
      { timeout: 8000, enableHighAccuracy: true }
    );
  }
}

async function loadCampusFacilities() {
  try {
    const res = await fetch('/api/facilities');
    const facilities = await res.json();
    if (elements.facilitiesList) {
      elements.facilitiesList.innerHTML = '';
      facilities.forEach(fac => {
        const item = document.createElement('div');
        item.className = 'facility-item';
        item.innerHTML = `
          <div>
            <div style="font-weight:700; font-size:0.95rem;">${fac.name}</div>
            <div style="font-size:0.8rem; color:var(--text-secondary);">${fac.building} • ${fac.floor}</div>
          </div>
          <div style="text-align:right;">
            <span class="facility-badge">${fac.type}</span>
            <div style="font-size:0.75rem; color:#38bdf8; margin-top:2px;">${fac.distance} away</div>
          </div>
        `;
        elements.facilitiesList.appendChild(item);
      });
    }
  } catch (e) {
    console.warn('Failed to load facilities:', e);
  }
}

// ----------------------------------------------------
// SOS Emergency Dispatch
// ----------------------------------------------------
function openSosModal() {
  elements.sosModal.classList.add('active');
  elements.sosDispatchResult.style.display = 'none';
}

function closeSosModal() {
  elements.sosModal.classList.remove('active');
}

async function executeSosDispatch() {
  const building = elements.sosBuildingSelect.value;
  const room = elements.sosRoomInput.value.trim() || 'Main Area';
  const incidentTitle = AppState.currentProtocol ? AppState.currentProtocol.title : 'Unspecified Medical Emergency';
  const severity = AppState.currentProtocol ? AppState.currentProtocol.severity : 'severe';
  const summary = AppState.currentProtocol ? AppState.currentProtocol.immediate_action : 'Urgent first-aid response requested.';

  elements.btnConfirmDispatch.disabled = true;
  elements.btnConfirmDispatch.innerHTML = `<span class="loader-spinner"></span> Broadcasting SOS...`;

  try {
    const res = await fetch('/api/sos/dispatch', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        incident_type: incidentTitle,
        severity: severity,
        location: {
          building: building,
          room: room,
          latitude: AppState.userLocation.lat,
          longitude: AppState.userLocation.lng
        },
        summary: summary,
        contacts_to_notify: ['campus_police', 'health_center', 'lab_safety', 'dorm_ra']
      })
    });

    const data = await res.json();
    elements.sosDispatchResult.style.display = 'block';
    elements.sosDispatchResult.innerHTML = `
      <div style="background:rgba(16, 185, 129, 0.2); border:1px solid #10b981; border-radius:12px; padding:1rem; margin-top:1rem;">
        <h3 style="color:#34d399; margin-bottom:0.5rem; font-size:1.1rem;">✓ Emergency Alert Dispatched!</h3>
        <p style="font-size:0.85rem; color:var(--text-primary);">Tracking Code: <strong>${data.tracking_id}</strong></p>
        <p style="font-size:0.85rem; color:var(--text-primary);">Estimated First Responder ETA: <strong>${data.estimated_response_eta_minutes} Minutes</strong></p>
        <div style="margin-top:0.75rem; display:flex; gap:0.5rem; flex-wrap:wrap;">
          <a href="${data.sms_url}" class="btn-primary" style="text-decoration:none; padding:0.5rem 0.75rem; font-size:0.85rem;">
            📱 Open Pre-filled SMS (911)
          </a>
          <a href="${data.whatsapp_url}" target="_blank" class="btn-secondary" style="text-decoration:none; padding:0.5rem 0.75rem; font-size:0.85rem;">
            💬 WhatsApp Security
          </a>
          <a href="tel:911" class="btn-sos-primary" style="text-decoration:none; padding:0.5rem 0.75rem; font-size:0.85rem;">
            📞 Speed Dial 911
          </a>
        </div>
      </div>
    `;
  } catch (err) {
    console.error('Dispatch error:', err);
    alert('Could not dispatch online. Please speed dial Campus Security at 911 / 555-019-9111 immediately.');
  } finally {
    elements.btnConfirmDispatch.disabled = false;
    elements.btnConfirmDispatch.innerHTML = `🚨 CONFIRM & BROADCAST EMERGENCY SOS`;
  }
}

// ----------------------------------------------------
// SOS Beacon (Strobe + Alarm)
// ----------------------------------------------------
function startSosBeacon() {
  elements.beaconOverlay.classList.add('active');
  playSosAlarm();
}

function stopSosBeacon() {
  elements.beaconOverlay.classList.remove('active');
  stopSosAlarm();
}

// Notification Helper
function showNotification(msg) {
  const toast = document.createElement('div');
  toast.style.cssText = `
    position: fixed;
    bottom: 24px;
    right: 24px;
    background: #10b981;
    color: white;
    padding: 12px 20px;
    border-radius: 9999px;
    font-weight: 700;
    box-shadow: 0 10px 25px rgba(0,0,0,0.5);
    z-index: 300;
    animation: fadein 0.3s;
  `;
  toast.textContent = msg;
  document.body.appendChild(toast);
  setTimeout(() => {
    toast.remove();
  }, 3000);
}
