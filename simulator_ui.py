"""
AgriLink WhatsApp Integration - Interactive Web Simulator UI
Provides a high-fidelity WhatsApp Web interface for testing, demonstrations, and presentations.
"""

def get_simulator_html() -> str:
    return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AgriLink — WhatsApp Farm Assistant Simulator</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Segoe+UI:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', Helvetica, Arial, sans-serif; }
        body { background: #111b21; height: 100vh; display: flex; justify-content: center; align-items: center; }
        
        .whatsapp-container {
            width: 100%;
            max-width: 900px;
            height: 94vh;
            background: #efeae2;
            display: flex;
            flex-direction: column;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
            position: relative;
        }

        /* HEADER */
        .chat-header {
            background: #008069;
            color: white;
            padding: 12px 18px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            box-shadow: 0 1px 3px rgba(0,0,0,0.2);
            z-index: 10;
        }
        .header-left { display: flex; align-items: center; gap: 12px; }
        .avatar {
            width: 44px; height: 44px; border-radius: 50%;
            background: #25d366; display: flex; align-items: center;
            justify-content: center; font-size: 22px; color: white;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
        }
        .header-info h2 { font-size: 16px; font-weight: 600; }
        .header-info p { font-size: 12px; opacity: 0.85; display: flex; align-items: center; gap: 5px; }
        .online-dot { width: 8px; height: 8px; background: #25d366; border-radius: 50%; display: inline-block; }
        
        .role-selector-wrap { display: flex; align-items: center; gap: 8px; }
        .role-selector-wrap label { font-size: 13px; font-weight: 500; }
        .role-select {
            padding: 6px 12px; border-radius: 20px; border: none;
            background: #ffffff; color: #111b21; font-weight: 600;
            font-size: 13px; cursor: pointer; outline: none;
        }
        .btn-qr-modal {
            background: #25d366; color: #075e54; border: none;
            font-weight: 700; font-size: 12.5px; padding: 6px 14px;
            border-radius: 20px; cursor: pointer; display: flex;
            align-items: center; gap: 5px; box-shadow: 0 1px 3px rgba(0,0,0,0.2);
            transition: all 0.2s;
        }
        .btn-qr-modal:hover { background: #1ebe5d; color: white; }

        /* QR CODE MODAL */
        .qr-overlay {
            display: none; position: absolute; inset: 0;
            background: rgba(0,0,0,0.7); z-index: 100;
            justify-content: center; align-items: center;
        }
        .qr-card {
            background: white; border-radius: 16px; padding: 24px;
            text-align: center; max-width: 340px; box-shadow: 0 10px 25px rgba(0,0,0,0.5);
            animation: fadeIn 0.2s ease-out;
        }
        @keyframes fadeIn { from { opacity: 0; transform: scale(0.95); } to { opacity: 1; transform: scale(1); } }

        /* CHIPS BAR (Quick Actions) */
        .quick-chips {
            background: #f0f2f5;
            padding: 8px 16px;
            display: flex;
            gap: 8px;
            overflow-x: auto;
            border-bottom: 1px solid #e9edef;
            scrollbar-width: none;
        }
        .quick-chips::-webkit-scrollbar { display: none; }
        .chip {
            background: white;
            border: 1px solid #d1d7db;
            color: #111b21;
            padding: 6px 14px;
            border-radius: 16px;
            font-size: 12.5px;
            font-weight: 500;
            cursor: pointer;
            white-space: nowrap;
            transition: all 0.2s;
        }
        .chip:hover { background: #008069; color: white; border-color: #008069; }
        .chip.voice { background: #e7fce3; border-color: #25d366; color: #075e54; font-weight: 600; }
        .chip.voice:hover { background: #25d366; color: white; }

        /* CHAT BODY */
        .chat-body {
            flex: 1;
            padding: 20px 24px;
            overflow-y: auto;
            background-color: #efeae2;
            background-image: radial-gradient(#d3c6b4 0.75px, transparent 0.75px);
            background-size: 16px 16px;
            display: flex;
            flex-direction: column;
            gap: 12px;
        }

        .date-divider {
            align-self: center;
            background: #ffffff;
            color: #54656f;
            font-size: 11px;
            font-weight: 600;
            padding: 4px 12px;
            border-radius: 8px;
            box-shadow: 0 1px 1px rgba(0,0,0,0.1);
            margin: 6px 0;
            text-transform: uppercase;
        }

        .message {
            max-width: 75%;
            padding: 8px 12px 6px 12px;
            border-radius: 8px;
            position: relative;
            font-size: 14px;
            line-height: 1.45;
            box-shadow: 0 1px 1px rgba(0,0,0,0.13);
            word-wrap: break-word;
            white-space: pre-wrap;
        }

        .msg-incoming {
            align-self: flex-start;
            background: #ffffff;
            color: #111b21;
            border-top-left-radius: 0;
        }

        .msg-outgoing {
            align-self: flex-end;
            background: #d9fdd3;
            color: #111b21;
            border-top-right-radius: 0;
        }

        .msg-time {
            float: right;
            margin-left: 10px;
            margin-top: 4px;
            font-size: 10.5px;
            color: #667781;
            display: flex;
            align-items: center;
            gap: 3px;
        }
        .ticks { color: #53bdeb; font-weight: bold; }

        .audio-bubble {
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 6px 0;
        }
        .audio-play {
            width: 36px; height: 36px; border-radius: 50%;
            background: #008069; color: white; display: flex;
            align-items: center; justify-content: center; font-size: 16px;
        }
        .audio-wave {
            flex: 1; height: 16px; background: repeating-linear-gradient(90deg, #008069, #008069 2px, transparent 2px, transparent 4px);
            border-radius: 2px; opacity: 0.5;
        }

        /* INPUT AREA */
        .chat-input-bar {
            background: #f0f2f5;
            padding: 10px 16px;
            display: flex;
            align-items: center;
            gap: 10px;
            border-top: 1px solid #d1d7db;
        }

        .input-box {
            flex: 1;
            background: #ffffff;
            border: 1px solid #ffffff;
            padding: 11px 16px;
            border-radius: 24px;
            font-size: 14.5px;
            outline: none;
            color: #111b21;
        }
        .input-box:focus { border-color: #008069; }

        .btn-icon {
            width: 44px; height: 44px; border-radius: 50%;
            border: none; background: transparent; cursor: pointer;
            display: flex; align-items: center; justify-content: center;
            font-size: 20px; color: #54656f; transition: all 0.2s;
        }
        .btn-icon:hover { background: #e9edef; color: #111b21; }
        .btn-send { background: #008069; color: white; }
        .btn-send:hover { background: #017560; color: white; }

        /* FOOTER BRAND */
        .footer-note {
            background: #f0f2f5;
            text-align: center;
            font-size: 11px;
            color: #667781;
            padding: 4px;
            border-top: 1px solid #e9edef;
        }
        .footer-note b { color: #008069; }
    </style>
</head>
<body>

<div class="whatsapp-container">
    <!-- HEADER -->
    <div class="chat-header">
        <div class="header-left">
            <div class="avatar">🌾</div>
            <div class="header-info">
                <h2>AgriLink Farm Assistant (ಅಗ್ರಿಲಿಂಕ್)</h2>
                <p><span class="online-dot"></span> Online • SFIC 2026 Innovation Challenge</p>
            </div>
        </div>
        <div class="role-selector-wrap">
            <button class="btn-qr-modal" onclick="toggleQRModal(true)">📱 Scan QR</button>
            <label for="roleSelect">Persona:</label>
            <select id="roleSelect" class="role-select" onchange="onRoleChange()">
                <option value="+919876500001" selected>🚜 Farmer (Shivanna - Mandya)</option>
                <option value="+919876500002">🏢 Aggregator (Lakshmi - Maddur Hub)</option>
                <option value="+919876500003">🛒 Customer (Priya - Bengaluru)</option>
                <option value="+919876500004">🏛️ Institutional Buyer (Warden Raghavan)</option>
                <option value="+919876500005">🛵 Delivery Partner (Manjunath K)</option>
                <option value="+918800714533">👤 New WhatsApp User (Onboarding)</option>
            </select>
        </div>
    </div>

    <!-- QUICK CHIPS -->
    <div class="quick-chips" id="quickChips">
        <!-- Dynamically rendered based on selected persona -->
    </div>

    <!-- CHAT MESSAGES -->
    <div class="chat-body" id="chatBody">
        <div class="date-divider">Today</div>
        <!-- Messages rendered here -->
    </div>

    <!-- INPUT BAR -->
    <div class="chat-input-bar">
        <button class="btn-icon" title="Clear chat history" onclick="clearChat()">🗑️</button>
        <button class="btn-icon" title="Send Kannada Voice Note" onclick="sendSampleVoiceNote()">🎙️</button>
        <input type="text" id="messageInput" class="input-box" placeholder="Type a message or select a quick option above..." onkeypress="handleKeyPress(event)">
        <button class="btn-icon btn-send" title="Send" onclick="sendMessage()">➤</button>
    </div>

    <div class="footer-note">
        AgriLink Multi-Actor Gateway • Powered by <b>FastAPI</b> & <b>68-10-14-8 Split Pricing Engine</b>
    </div>

    <!-- QR MODAL OVERLAY -->
    <div class="qr-overlay" id="qrOverlay" onclick="toggleQRModal(false)">
        <div class="qr-card" onclick="event.stopPropagation()">
            <h3 style="font-size: 16px; font-weight: 700; color: #008069; margin-bottom: 4px;">🌾 AgriLink WhatsApp Assistant</h3>
            <p style="font-size: 12px; color: #54656f; margin-bottom: 14px;">Scan with your phone camera to chat on mobile</p>
            <img src="data:image/png;base64,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" 
                 alt="AgriLink QR Code" style="width: 220px; height: 220px; border-radius: 8px; margin: 0 auto 12px auto; display: block; border: 1px solid #d1d7db;">
            <p style="font-size: 11px; color: #008069; font-weight: 600; margin-bottom: 12px;">agrilink-whatsapp.onrender.com</p>
            <button onclick="toggleQRModal(false)" style="background: #008069; color: white; border: none; padding: 8px 24px; border-radius: 20px; font-weight: 600; font-size: 13px; cursor: pointer;">Close</button>
        </div>
    </div>
</div>

<script>
    const CHIP_PRESETS = {
        "+919876500001": [
            { label: "ನಮಸ್ಕಾರ (Menu)", text: "ನಮಸ್ಕಾರ" },
            { label: "1 (Mandi Rates)", text: "1" },
            { label: "Tomato Rate (ಟೊಮೆಟೊ)", text: "1" },
            { label: "3 (Check UPI Payout)", text: "3" },
            { label: "🎙️ Voice: 200 kg Tomato Harvest", text: "ನನ್ನ ಬಳಿ 200 ಕೆಜಿ ಟೊಮೆಟೊ ಇದೆ, ಗುರುವಾರ ಕೊಯ್ಲು ಮಾಡುತ್ತೇನೆ", isVoice: true }
        ],
        "+919876500002": [
            { label: "Menu", text: "menu" },
            { label: "1 (Pickup Manifest)", text: "1" },
            { label: "2 (Grade Incoming Batch)", text: "2" },
            { label: "3 (Request Truck to Bengaluru)", text: "3" },
            { label: "4 (10% Hub Commission)", text: "4" }
        ],
        "+919876500003": [
            { label: "Menu", text: "menu" },
            { label: "1 (Fresh Produce Catalog)", text: "1" },
            { label: "2 (Track Active Order & OTP)", text: "2" },
            { label: "3 (1-Click Weekly Basket Reorder)", text: "3" },
            { label: "4 (Farm Traceability Passport)", text: "4" },
            { label: "5 (Report Damaged Item)", text: "5" }
        ],
        "+919876500004": [
            { label: "Menu", text: "menu" },
            { label: "1 (Recurring Standing Orders)", text: "1" },
            { label: "3 (Download GST Invoice)", text: "3" },
            { label: "4 (Hostel Security Gate Pass)", text: "4" }
        ],
        "+919876500005": [
            { label: "Menu", text: "menu" },
            { label: "1 (Active Run & Google Maps)", text: "1" },
            { label: "4829 (Submit Customer OTP)", text: "4829" },
            { label: "3 (Today's 14% Earnings)", text: "3" }
        ],
        "+918800714533": [
            { label: "Hi", text: "Hi" },
            { label: "1 (Register as Farmer)", text: "1" },
            { label: "2 (Register as Customer)", text: "2" }
        ]
    };

    function getTimeString() {
        const now = new Date();
        return now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    }

    function formatWhatsAppMarkdown(text) {
        // Formats *bold*, _italic_, ~strike~, and URLs
        let formatted = text
            .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
            .replace(/\*(.*?)\*/g, '<strong>$1</strong>')
            .replace(/_(.*?)_/g, '<em>$1</em>')
            .replace(/~(.*?)~/g, '<del>$1</del>')
            .replace(/(https?:\\/\\/[^\\s]+)/g, '<a href="$1" target="_blank" style="color: #027eb5; text-decoration: underline;">$1</a>');
        return formatted;
    }

    function appendMessage(text, isIncoming, isVoice = false) {
        const chatBody = document.getElementById("chatBody");
        const msgDiv = document.createElement("div");
        msgDiv.className = `message ${isIncoming ? 'msg-incoming' : 'msg-outgoing'}`;

        let content = '';
        if (isVoice) {
            content += `
                <div class="audio-bubble">
                    <div class="audio-play">▶</div>
                    <div class="audio-wave"></div>
                    <span style="font-size: 11px; color: #54656f;">0:04</span>
                </div>
            `;
        }
        content += `<div>${formatWhatsAppMarkdown(text)}</div>`;
        content += `
            <div class="msg-time">
                ${getTimeString()}
                ${!isIncoming ? '<span class="ticks">✓✓</span>' : ''}
            </div>
        `;

        msgDiv.innerHTML = content;
        chatBody.appendChild(msgDiv);
        chatBody.scrollTop = chatBody.scrollHeight;
    }

    async function sendTextMessage(messageText, isVoice = false) {
        const phone = document.getElementById("roleSelect").value;
        appendMessage(messageText, false, isVoice);

        try {
            const response = await fetch("/api/v1/whatsapp/simulate", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    from_phone: phone,
                    message: messageText,
                    media_url: isVoice ? "https://mock.audio/voice.ogg" : null,
                    media_content_type: isVoice ? "audio/ogg" : null
                })
            });
            const data = await response.json();
            setTimeout(() => {
                appendMessage(data.reply, true);
            }, 300);
        } catch (error) {
            appendMessage("⚠️ Error communicating with AgriLink service: " + error, true);
        }
    }

    function sendMessage() {
        const input = document.getElementById("messageInput");
        const text = input.value.trim();
        if (!text) return;
        input.value = "";
        sendTextMessage(text);
    }

    function sendSampleVoiceNote() {
        sendTextMessage("ನನ್ನ ಬಳಿ 200 ಕೆಜಿ ಟೊಮೆಟೊ ಇದೆ, ಗುರುವಾರ ಕೊಯ್ಲು ಮಾಡುತ್ತೇನೆ", true);
    }

    function handleKeyPress(e) {
        if (e.key === "Enter") sendMessage();
    }

    function clearChat() {
        const chatBody = document.getElementById("chatBody");
        chatBody.innerHTML = '<div class="date-divider">Today</div>';
    }

    function updateChips(phone) {
        const container = document.getElementById("quickChips");
        container.innerHTML = "";
        const presets = CHIP_PRESETS[phone] || CHIP_PRESETS["+919876500001"];

        presets.forEach(p => {
            const btn = document.createElement("button");
            btn.className = `chip ${p.isVoice ? 'voice' : ''}`;
            btn.textContent = p.label;
            btn.onclick = () => sendTextMessage(p.text, !!p.isVoice);
            container.appendChild(btn);
        });
    }

    function toggleQRModal(show) {
        const overlay = document.getElementById("qrOverlay");
        overlay.style.display = show ? "flex" : "none";
    }

    function onRoleChange() {
        clearChat();
        const phone = document.getElementById("roleSelect").value;
        updateChips(phone);
        // Automatically send greetings on role switch
        sendTextMessage(phone === "+919876500001" ? "ನಮಸ್ಕಾರ" : "menu");
    }

    // Initial setup on load
    window.onload = () => {
        updateChips("+919876500001");
        sendTextMessage("ನಮಸ್ಕಾರ");
    };
</script>

</body>
</html>
"""
