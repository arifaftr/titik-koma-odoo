(function () {
    "use strict";

    const $ = window.jQuery || window.$;
    if (!$) {
        console.error('mental_health_chatbot: jQuery is not available');
        return;
    }

    // Vector SVG avatars for high-fidelity rendering without asset file dependencies
    const hijabSvg = `data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><circle cx="50" cy="50" r="50" fill="%23A78BFA"/><path d="M50,15 C30,15 25,35 25,55 C25,75 35,85 50,85 C65,85 75,75 75,55 C75,35 70,15 50,15 Z" fill="%23312E81"/><ellipse cx="50" cy="53" rx="18" ry="24" fill="%23FDBA74"/><path d="M35,45 C35,32 65,32 65,45" fill="none" stroke="%23312E81" stroke-width="4"/><circle cx="43" cy="52" r="3" fill="%23312E81"/><circle cx="57" cy="52" r="3" fill="%23312E81"/><circle cx="43" cy="52" r="8" fill="none" stroke="%23312E81" stroke-width="1.5"/><circle cx="57" cy="52" r="8" fill="none" stroke="%23312E81" stroke-width="1.5"/><path d="M48,52 L52,52" stroke="%23312E81" stroke-width="1.5"/><path d="M46,64 C48,67 52,67 54,64" fill="none" stroke="%23312E81" stroke-width="2.5" stroke-linecap="round"/><path d="M25,55 C25,75 32,85 50,85 C68,85 75,75 75,55 C75,80 65,92 50,92 C35,92 25,80 25,55 Z" fill="%23EF4444"/></svg>`;
    const boySvg = `data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><circle cx="50" cy="50" r="50" fill="%23A7F3D0"/><path d="M50,18 C35,18 30,30 30,42 C30,55 35,65 50,65 C65,65 70,55 70,42 C70,30 65,18 50,18 Z" fill="%2378350F"/><ellipse cx="50" cy="50" rx="18" ry="20" fill="%23FDBA74"/><path d="M30,42 C30,30 40,25 50,25 C60,25 70,30 70,42 C70,32 60,30 50,30 C40,30 30,32 30,42 Z" fill="%23451A03"/><circle cx="44" cy="48" r="3" fill="%23312E81"/><circle cx="56" cy="48" r="3" fill="%23312E81"/><path d="M47,58 C49,60 51,60 53,58" fill="none" stroke="%23312E81" stroke-width="2" stroke-linecap="round"/><path d="M30,62 C40,75 60,75 70,62 L70,85 C70,85 60,95 50,95 C40,95 30,85 30,85 Z" fill="%233B82F6"/></svg>`;
    const girlSvg = `data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><circle cx="50" cy="50" r="50" fill="%23FEE2E2"/><path d="M50,16 C32,16 26,28 26,55 C26,75 32,92 50,92 C68,92 74,75 74,55 C74,28 68,16 50,16 Z" fill="%231F2937"/><ellipse cx="50" cy="48" rx="18" ry="20" fill="%23FDBA74"/><path d="M32,32 C38,24 62,24 68,32 C60,28 40,28 32,32 Z" fill="%23111827"/><circle cx="44" cy="46" r="3" fill="%23312E81"/><circle cx="56" cy="46" r="3" fill="%23312E81"/><path d="M47,56 C49,58 51,58 53,56" fill="none" stroke="%23111827" stroke-width="2" stroke-linecap="round"/><path d="M32,65 C40,78 60,78 68,65 L68,85 C68,90 60,95 50,95 C40,95 32,90 32,85 Z" fill="%23EC4899"/></svg>`;

    const AVATARS = {
        hijab: hijabSvg,
        boy: boySvg,
        girl: girlSvg
    };

    $(document).ready(function () {
        const $root = $('#mhc-chatbot-root');
        if ($root.length === 0) {
            return;
        }

        console.log('mental_health_chatbot: JS assets loaded');

        let currentSessionId = 'sess_' + Date.now() + '_'
            + Math.random().toString(36).substr(2, 9);

        function getCsrfToken() {
            if (typeof odoo !== 'undefined' && odoo.csrf_token) {
                return odoo.csrf_token;
            }
            const meta = document.querySelector('meta[name="csrf-token"]');
            return meta ? meta.getAttribute('content') : '';
        }

        function jsonRpc(url, params) {
            const headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'X-Requested-With': 'XMLHttpRequest',
            };
            const csrf = getCsrfToken();
            if (csrf) {
                headers['X-CSRF-TOKEN'] = csrf;
            }
            return fetch(url, {
                method: 'POST',
                headers: headers,
                body: JSON.stringify({
                    jsonrpc: '2.0',
                    method: 'call',
                    params: params || {},
                    id: Date.now(),
                }),
            }).then(function (response) {
                if (!response.ok) {
                    throw new Error('HTTP status ' + response.status);
                }
                return response.json();
            }).then(function (data) {
                if (data.error) {
                    throw new Error(data.error.data?.message || data.error.message || 'RPC error');
                }
                return data.result;
            });
        }

        function escapeHtml(text) {
            return $('<div>').text(text || '').html();
        }

        const MHC_WELCOME_TEXT =
            'Halo! Saya adalah TiKo AI dari Titik koma. Saya di sini siap mendengarkan cerita dan perasaanmu hari ini.';
        const MHC_BOT_AVATAR_HTML =
            '<div class="mhc-avatar mhc-avatar-bot" role="img" aria-label="TiKo AI"></div>';

        function getUserAvatarLabel() {
            const name = localStorage.getItem('chatbot_user_name')
                || $root.find('#top-username').text().trim()
                || 'U';
            const parts = name.trim().split(/\s+/).filter(Boolean);
            if (parts.length >= 2) {
                return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase();
            }
            return (parts[0] && parts[0][0] ? parts[0][0] : 'U').toUpperCase();
        }

        function buildWelcomeMessageHtml() {
            return buildMessageHtml('bot', MHC_WELCOME_TEXT, null).replace(
                'class="mhc-message mhc-message-bot"',
                'class="mhc-message mhc-message-bot" data-mhc-welcome="1"'
            );
        }

        function ensureWelcomeMessage($container) {
            if (!$container || !$container.length) {
                return;
            }
            if ($container.find('[data-mhc-welcome]').length === 0) {
                $container.prepend(buildWelcomeMessageHtml());
            }
        }

        function buildMessageHtml(role, text, time) {
            const isBot = role === 'bot';
            const safeText = escapeHtml(text);
            const timeHtml = time
                ? '<span class="mhc-time">' + escapeHtml(time) + '</span>'
                : '';
            const avatarHtml = isBot
                ? MHC_BOT_AVATAR_HTML
                : '<div class="mhc-avatar mhc-avatar-user">'
                    + escapeHtml(getUserAvatarLabel()) + '</div>';
            const bubbleHtml =
                '<div class="mhc-bubble mhc-bubble-' + role + '">'
                + safeText + timeHtml + '</div>';
            const inner = isBot
                ? avatarHtml + bubbleHtml
                : bubbleHtml + avatarHtml;
            return '<div class="mhc-message mhc-message-' + role + '">' + inner + '</div>';
        }

        function buildTypingHtml() {
            return ''
                + '<div class="mhc-message mhc-message-bot typing-indicator-wrapper">'
                + MHC_BOT_AVATAR_HTML
                + '<div class="mhc-bubble mhc-bubble-bot">'
                + '<div class="typing-indicator">'
                + '<div class="typing-dot"></div>'
                + '<div class="typing-dot"></div>'
                + '<div class="typing-dot"></div>'
                + '</div></div></div>';
        }

        function migrateLegacyChatMessages($container) {
            if (!$container || !$container.length) {
                return;
            }
            $container.find('.user-message-row, .bot-message-row').each(function () {
                const $row = $(this);
                if ($row.hasClass('mhc-message-bot') || $row.hasClass('mhc-message-user')) {
                    return;
                }
                const isBot = $row.hasClass('bot-message-row');
                const $bubble = $row.find('.message-bubble-bot, .message-bubble-user');
                const $time = $bubble.find('.mhc-message-time, .mhc-time');
                const time = $time.length ? $time.text().trim() : '';
                const text = $bubble.clone().children('.mhc-message-time, .mhc-time').remove().end()
                    .text().trim();
                $row.replaceWith(buildMessageHtml(isBot ? 'bot' : 'user', text, time || null));
            });
        }

        // --- 1. Original Widget Code (Preserved) ---
        // Widget send (delegated and scoped to root)
        $root.on('click', '#send-btn', function () {
            let message = $root.find('#chat-input').val();
            if (!message) return;

            const $widgetBody = $root.find('#chat-body');
            $widgetBody.append(`
                <div class="user-message">
                    ${message}
                </div>
            `);
            $root.find('#chat-input').val('');

            fetch('/mental/chatbot/send', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: JSON.stringify({
                    message: message,
                    session_id: currentSessionId,
                })
            }).then(function (response) {
                if (!response.ok) {
                    throw new Error('HTTP status ' + response.status);
                }
                return response.json();
            }).then(function (result) {
                const replyText = (result && (result.reply || (result.result && result.result.reply))) ? (result.reply || result.result.reply) : 'Maaf, tidak ada respon dari server.';
                $widgetBody.append(`
                    <div class="bot-message">
                        ${replyText}
                    </div>
                `);
                $widgetBody.scrollTop($widgetBody[0].scrollHeight);
            }).catch(function (error) {
                $widgetBody.append(`
                    <div class="bot-message">
                        Maaf, terjadi kesalahan koneksi. Silakan coba lagi.
                    </div>
                `);
                $widgetBody.scrollTop($widgetBody[0].scrollHeight);
                console.error('mental_health_chatbot: send error', error);
            });
        });


        // --- 2. Dashboard Code & Features ---
        // Profile & Theme Initialization
        let storedName = localStorage.getItem('chatbot_user_name') || $('#top-username').text().trim() || 'Arifa Fitra Salima';
        let storedAvatar = localStorage.getItem('chatbot_user_avatar') || 'hijab';
        let storedMood = localStorage.getItem('chatbot_user_mood') || 'Amazing';
        let storedMoodEmoji = localStorage.getItem('chatbot_user_mood_emoji') || '\uD83E\uDD29';
        let storedMoodDate = localStorage.getItem('chatbot_user_mood_date') || getFormattedDate();

        function getFormattedDate() {
            const today = new Date();
            const dd = String(today.getDate()).padStart(2, '0');
            const mm = String(today.getMonth() + 1).padStart(2, '0');
            const yyyy = today.getFullYear();
            return `${dd}-${mm}-${yyyy}`;
        }

        // Apply profile & mood states to dashboard
        function applyProfileState() {
            $('#top-username').text(storedName);
            $('.display-username').text(storedName.split(' ')[0]); // Display first name in greeting
            $('#profile-name-display').text(storedName);
            $('#profile-input-name').val(storedName);

            // Set Avatar Images
            const avatarUrl = AVATARS[storedAvatar] || AVATARS.hijab;
            $('#top-avatar').css('background-image', `url('${avatarUrl}')`);
            $('#profile-avatar-placeholder-large').css('background-image', `url('${avatarUrl}')`);

            // Apply selected avatar in choice modal
            $root.find('.mhc-avatar-choice').removeClass('active');
            $root.find(`.mhc-avatar-choice[data-avatar="${storedAvatar}"]`).addClass('active');

            // Apply Mood
            $('#home-mood-emoji').text(storedMoodEmoji);
            $('#home-mood-value').text(storedMood);
            $('#home-mood-date').text(storedMoodDate);
        }
        applyProfileState();

        // Save mood tracking
        function setMood(mood, emoji) {
            storedMood = mood;
            storedMoodEmoji = emoji;
            storedMoodDate = getFormattedDate();
            
            localStorage.setItem('chatbot_user_mood', storedMood);
            localStorage.setItem('chatbot_user_mood_emoji', storedMoodEmoji);
            localStorage.setItem('chatbot_user_mood_date', storedMoodDate);
            
            applyProfileState();
        }

        // Save profile editor
        function saveProfile(name, avatar) {
            storedName = name;
            storedAvatar = avatar;
            
            localStorage.setItem('chatbot_user_name', storedName);
            localStorage.setItem('chatbot_user_avatar', storedAvatar);
            
            applyProfileState();
        }

        // Tab Switching Logic
        $root.find('.mhc-nav-item').click(function (e) {
            e.preventDefault();
            const tabId = $(this).data('tab');
            if (tabId === 'chat') {
                openDashboardChatOverlay();
            } else {
                switchTab(tabId);
            }
        });

        // Quick access link clicks (using event delegation to ensure it catches dynamically loaded elements)
        $root.on('click', '.btn-quick-start, .btn-go-chat', function (e) {
            e.preventDefault();
            const tabId = $(this).data('target-tab');
            switchTab(tabId);
        });

        function switchTab(tabId) {
            if (!tabId) return;
            $root.find('.mhc-nav-item').removeClass('active');
            $root.find(`.mhc-nav-item[data-tab="${tabId}"]`).addClass('active');
            
            $root.find('.mhc-tab-pane').removeClass('active');
            $root.find(`#tab-${tabId}`).addClass('active');
            
            // Set breadcrumb text
            const tabTitles = {
                home: 'My home',
                chat: 'Chat AI',
                assessment: 'Self-assessment',
                tools: 'Self-Help Tools'
            };
            $('#current-tab-title').text(tabTitles[tabId] || 'My home');
        }

        const chatbotNamespace = window.mentalHealthChatbot = window.mentalHealthChatbot || {};
        chatbotNamespace.openDashboardTab = switchTab;

        // --- Chat Overlay ---
        function appendMessageTo($logContainer, sender, text, time) {
            const role = sender === 'user' ? 'user' : 'bot';
            $logContainer.append(buildMessageHtml(role, text, time));
            $logContainer.scrollTop($logContainer[0].scrollHeight);
        }

        function showTypingIndicatorTo($logContainer) {
            $logContainer.append(buildTypingHtml());
            $logContainer.scrollTop($logContainer[0].scrollHeight);
        }

        function removeTypingIndicatorFrom($logContainer) {
            $logContainer.find('.typing-indicator-wrapper').remove();
        }

        function sendMessageOverlay() {
            const $input = $root.find('#chat-dashboard-input-overlay');
            const $log = $root.find('#chat-conversation-log-overlay');
            if ($input.length === 0 || $log.length === 0) {
                console.warn('mental_health_chatbot: overlay send elements missing');
                return;
            }

            const message = $input.val().trim();
            if (!message) {
                console.warn('mental_health_chatbot: empty message, not sending');
                return;
            }
            $input.val('');

            appendMessageTo($log, 'user', message);
            showTypingIndicatorTo($log);
            console.log('mental_health_chatbot: sending message', message);

            fetch('/mental/chatbot/send', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: JSON.stringify({
                    message: message,
                    session_id: currentSessionId,
                })
            }).then(function (response) {
                if (!response.ok) {
                    throw new Error('HTTP status ' + response.status);
                }
                return response.json();
            }).then(function (result) {
                removeTypingIndicatorFrom($log);
                console.log('mental_health_chatbot: received reply', result);
                const replyText = (result && (result.reply || (result.result && result.result.reply))) ? (result.reply || result.result.reply) : 'Maaf, tidak ada respon dari server.';
                appendMessageTo($log, 'bot', replyText);
            }).catch(function (error) {
                removeTypingIndicatorFrom($log);
                console.error('mental_health_chatbot: send error', error);
                appendMessageTo($log, 'bot', 'Maaf, terjadi kesalahan koneksi. Silakan coba lagi.');
            });
        }

        // Delegate overlay bindings to root to ensure handlers exist reliably
        $root.on('click', '#chat-dashboard-send-overlay', sendMessageOverlay);
        $root.on('keypress', '#chat-dashboard-input-overlay', function (e) {
            if (e.which === 13) {
                sendMessageOverlay();
            }
        });

        const openDashboardChatOverlay = function () {
            console.log('mental_health_chatbot: openDashboardChatOverlay called');
            const $overlay = $('#mhc-chat-overlay');
            if ($overlay.length === 0) {
                console.warn('mental_health_chatbot: mhc-chat-overlay element not found');
                return;
            }

            if ($overlay.hasClass('mhc-d-none')) {
                $overlay.removeClass('mhc-d-none');
                $overlay.css('display', 'flex');
                $overlay.find('#chat-dashboard-send-overlay').off('click').on('click', sendMessageOverlay);
                $overlay.find('#chat-dashboard-input-overlay').off('keypress').on('keypress', function (e) {
                    if (e.which === 13) sendMessageOverlay();
                });
                $overlay.find('.mhc-chat-overlay-close').off('click').on('click', function () {
                    $overlay.addClass('mhc-d-none');
                });
            } else {
                $overlay.addClass('mhc-d-none');
            }
        };
        chatbotNamespace.openDashboardChatOverlay = openDashboardChatOverlay;

        // --- 3. Modals & Dialogs ---
        // Mood Picker Modal
        $('#btn-change-mood').click(function() {
            $('#mood-picker-modal').removeClass('mhc-d-none');
        });
        $('#btn-close-mood-modal, #mood-picker-modal').click(function(e) {
            if (e.target === this) {
                $('#mood-picker-modal').addClass('mhc-d-none');
            }
        });
        $root.find('.mood-selection-option').click(function() {
            const mood = $(this).data('mood');
            const emoji = $(this).data('emoji');
            setMood(mood, emoji);
            $('#mood-picker-modal').addClass('mhc-d-none');
        });

        // Profile Editor Modal
        $('#btn-edit-profile-action').click(function() {
            $('#edit-profile-modal').removeClass('mhc-d-none');
        });
        $('#btn-close-profile-modal, #edit-profile-modal').click(function(e) {
            if (e.target === this) {
                $('#edit-profile-modal').addClass('mhc-d-none');
            }
        });
        $root.find('.mhc-avatar-choice').click(function() {
            $root.find('.mhc-avatar-choice').removeClass('active');
            $(this).addClass('active');
        });
        $('#btn-save-profile-modal-btn').click(function() {
            const name = $('#profile-input-name').val().trim() || 'Arifa Fitra Salima';
            const avatar = $root.find('.mhc-avatar-choice.active').data('avatar') || 'hijab';
            saveProfile(name, avatar);
            $('#edit-profile-modal').addClass('mhc-d-none');
        });

        // Counselor Contact Modal
        $('#btn-contact-counselor').click(function() {
            $('#counselor-modal').removeClass('mhc-d-none');
        });
        $('#btn-close-counselor-modal, #counselor-modal').click(function(e) {
            if (e.target === this) {
                $('#counselor-modal').addClass('mhc-d-none');
            }
        });


        // --- 4. Chat Dashboard Panel ---
        const $chatLog = $root.find('#chat-conversation-log');
        const $chatInput = $root.find('#chat-dashboard-input');
        const $chatSend = $root.find('#chat-dashboard-send');

        migrateLegacyChatMessages($chatLog);
        migrateLegacyChatMessages($root.find('#chat-conversation-log-overlay'));
        ensureWelcomeMessage($chatLog);
        ensureWelcomeMessage($root.find('#chat-conversation-log-overlay'));

        function appendMessage(sender, text, time) {
            const role = sender === 'user' ? 'user' : 'bot';
            $chatLog.append(buildMessageHtml(role, text, time));
            $chatLog.scrollTop($chatLog[0].scrollHeight);
        }

        function showTypingIndicator() {
            $chatLog.append(buildTypingHtml());
            $chatLog.scrollTop($chatLog[0].scrollHeight);
        }

        function removeTypingIndicator() {
            $chatLog.find('.typing-indicator-wrapper').remove();
        }

        function sendMessage() {
            let message = $chatInput.val().trim();
            if (!message) return;

            $chatInput.val('');
            appendMessage('user', message);
            showTypingIndicator();

            fetch('/mental/chatbot/send', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: JSON.stringify({
                    message: message,
                    session_id: currentSessionId,
                })
            }).then(function (response) {
                if (!response.ok) {
                    throw new Error('HTTP status ' + response.status);
                }
                return response.json();
            }).then(function (result) {
                removeTypingIndicator();
                appendMessage('bot', (result && (result.reply || (result.result && result.result.reply))) || 'Maaf, tidak ada respon dari server.');
            }).catch(function (error) {
                removeTypingIndicator();
                appendMessage('bot', 'Maaf, terjadi kesalahan koneksi. Silakan periksa koneksi Anda dan coba lagi.');
            });
        }

        // Use delegated handlers on root so dynamically shown/hidden overlay and dashboard bindings always work
        $root.on('click', '#chat-dashboard-send', sendMessage);
        $root.on('keypress', '#chat-dashboard-input', function (e) {
            if (e.which === 13) {
                sendMessage();
            }
        });

        // Chat Suggestion pills
        $root.find('.suggestion-pill').click(function() {
            const msg = $(this).data('msg');
            $chatInput.val(msg);
            sendMessage();
        });

        // --- 4b. Conversation history panel ---
        function renderSessionList(sessions) {
            const container = document.getElementById('mhc-session-list');
            if (!container) {
                return;
            }

            if (!sessions || sessions.length === 0) {
                container.innerHTML =
                    '<div class="mhc-session-empty">' +
                    '💬 Belum ada riwayat percakapan' +
                    '</div>';
                return;
            }

            const grouped = {};
            sessions.forEach(function (s) {
                const d = s.date;
                if (!grouped[d]) {
                    grouped[d] = [];
                }
                grouped[d].push(s);
            });

            let html = '';
            Object.keys(grouped).forEach(function (date) {
                html += '<div class="mhc-session-date-label">' + escapeHtml(date) + '</div>';
                grouped[date].forEach(function (s) {
                    html += '<div class="mhc-session-item" data-session="'
                        + escapeHtml(s.session_id) + '">'
                        + '<span class="mhc-session-icon">💬</span>'
                        + '<span class="mhc-session-preview">'
                        + escapeHtml(s.preview) + '</span>'
                        + '</div>';
                });
            });
            container.innerHTML = html;

            container.querySelectorAll('.mhc-session-item').forEach(function (el) {
                el.addEventListener('click', function () {
                    const sid = this.dataset.session;
                    loadSessionMessages(sid);
                    container.querySelectorAll('.mhc-session-item')
                        .forEach(function (e) { e.classList.remove('active'); });
                    this.classList.add('active');
                    toggleHistoryPanel(false);
                });
            });
        }

        function loadChatSessions() {
            return jsonRpc('/mental/chatbot/sessions', {}).then(function (sessions) {
                renderSessionList(sessions || []);
            }).catch(function (error) {
                console.error('mental_health_chatbot: load sessions error', error);
                renderSessionList([]);
            });
        }

        function loadSessionMessages(sessionId) {
            return jsonRpc('/mental/chatbot/session/messages', {
                session_id: sessionId,
            }).then(function (messages) {
                currentSessionId = sessionId;

                const chatBody = document.getElementById('chat-conversation-log');
                if (!chatBody) {
                    return;
                }
                chatBody.innerHTML = '';
                chatBody.insertAdjacentHTML('afterbegin', buildWelcomeMessageHtml());

                (messages || []).forEach(function (m) {
                    appendMessage('user', m.user_message, m.time);
                    appendMessage('bot', m.bot_response, m.time);
                });

                chatBody.scrollTop = chatBody.scrollHeight;
            }).catch(function (error) {
                console.error('mental_health_chatbot: load session messages error', error);
            });
        }

        function toggleHistoryPanel(forceState) {
            const panel = document.getElementById('mhc-history-panel');
            const btn = document.getElementById('mhc-history-toggle');
            if (!panel) {
                return;
            }

            const isOpen = panel.classList.contains('open');
            const shouldOpen = forceState !== undefined ? forceState : !isOpen;

            if (shouldOpen) {
                panel.classList.add('open');
                if (btn) {
                    btn.classList.add('active');
                }
                loadChatSessions();
            } else {
                panel.classList.remove('open');
                if (btn) {
                    btn.classList.remove('active');
                }
            }
        }

        window.toggleHistoryPanel = toggleHistoryPanel;
        chatbotNamespace.toggleHistoryPanel = toggleHistoryPanel;

        $root.on('click', '#mhc-history-toggle', function () {
            toggleHistoryPanel();
        });
        $root.on('click', '#mhc-history-close', function () {
            toggleHistoryPanel(false);
        });


        // --- 5. Self-Assessment Wizard ---
        const questions = [
            "Apakah Anda merasa sulit untuk bersantai atau menenangkan diri akhir-akhir ini?",
            "Apakah Anda merasa cemas, khawatir berlebihan, atau takut tanpa alasan yang jelas?",
            "Apakah Anda merasa lelah, kurang bertenaga, atau sulit termotivasi untuk mengerjakan tugas kuliah?",
            "Apakah Anda sering mengalami kesulitan tidur atau tidur yang tidak nyenyak?",
            "Apakah Anda merasa sedih, murung, atau putus asa tentang masa depan akademis Anda?",
            "Apakah Anda merasa mudah tersinggung, marah, atau frustrasi karena hal-hari kecil?",
            "Apakah Anda merasa kesulitan untuk berkonsentrasi saat kuliah atau belajar mandiri?"
        ];

        let currentQuestionIndex = 0;
        let totalScore = 0;

        $('#btn-start-quiz-action').click(function() {
            currentQuestionIndex = 0;
            totalScore = 0;
            $('#quiz-intro').addClass('mhc-d-none');
            $('#quiz-results-box').addClass('mhc-d-none');
            $('#quiz-question-box').removeClass('mhc-d-none');
            renderQuestion();
        });

        function renderQuestion() {
            const questionText = questions[currentQuestionIndex];
            const progress = ((currentQuestionIndex + 1) / questions.length) * 100;
            
            $('#question-number').text(`Pertanyaan ${currentQuestionIndex + 1} dari ${questions.length}`);
            $('#question-text').text(questionText);
            $('#quiz-progress-fill').css('width', `${progress}%`);
        }

        $root.find('.btn-quiz-option').click(function() {
            const score = parseInt($(this).data('score'));
            totalScore += score;
            
            currentQuestionIndex++;
            if (currentQuestionIndex < questions.length) {
                renderQuestion();
            } else {
                showQuizResults();
            }
        });

        function showQuizResults() {
            $('#quiz-question-box').addClass('mhc-d-none');
            $('#quiz-results-box').removeClass('mhc-d-none');
            
            $('#results-score-value').text(`${totalScore} / ${questions.length * 3}`);
            
            let status = 'Stres Ringan / Normal';
            let recommendation = 'Kondisi emosional Anda relatif stabil dan normal. Pertahankan pola hidup sehat Anda, seimbangkan waktu belajar dan istirahat.';
            
            if (totalScore >= 8 && totalScore <= 14) {
                status = 'Stres Sedang';
                recommendation = 'Anda terindikasi memiliki tingkat stres sedang. Kami menyarankan Anda untuk mencoba teknik relaksasi harian seperti Box Breathing di tab "Self-Help Tools", atau mencurahkan pikiran Anda ke AI Chatbot.';
            } else if (totalScore >= 15) {
                status = 'Stres Tinggi / Parah';
                recommendation = 'Tingkat stres Anda tergolong tinggi. Ingatlah bahwa Anda tidak sendirian. Sangat disarankan untuk meluangkan waktu beristirahat total, bercerita dengan teman terdekat, atau menghubungi Layanan Konseling Kampus kami untuk berkonsultasi dengan profesional secara gratis.';
            }
            
            $('#results-status-label').text(status);
            $('#results-rec-text').text(recommendation);
        }

        $('#btn-retry-quiz-action').click(function() {
            $('#quiz-results-box').addClass('mhc-d-none');
            $('#quiz-question-box').removeClass('mhc-d-none');
            currentQuestionIndex = 0;
            totalScore = 0;
            renderQuestion();
        });


        // --- 6. Self-Help Tools Logic ---
        // Breathing Tool (Box Breathing)
        let breathingTimer = null;
        let isBreathing = false;
        let breathingStep = 0; // 0: inhale, 1: hold, 2: exhale, 3: hold
        
        const $breathingBubble = $('#breathing-bubble');
        const $breathingStatus = $('#breathing-status');
        const $breathingBtn = $('#btn-breathing-control');

        function runBreathingStep() {
            if (!isBreathing) return;
            
            $breathingBubble.removeClass('inhale hold exhale');
            
            if (breathingStep === 0) {
                $breathingStatus.text('Tarik Napas (4s)');
                $breathingBubble.addClass('inhale');
                breathingStep = 1;
            } else if (breathingStep === 1) {
                $breathingStatus.text('Tahan Napas (4s)');
                $breathingBubble.addClass('hold');
                breathingStep = 2;
            } else if (breathingStep === 2) {
                $breathingStatus.text('Hembuskan (4s)');
                $breathingBubble.addClass('exhale');
                breathingStep = 3;
            } else {
                $breathingStatus.text('Tahan Napas (4s)');
                breathingStep = 0;
            }
            
            breathingTimer = setTimeout(runBreathingStep, 4000);
        }

        function stopBreathing() {
            isBreathing = false;
            clearTimeout(breathingTimer);
            $breathingBubble.removeClass('inhale hold exhale');
            $breathingStatus.text('Mulai');
            $breathingBtn.text('Mulai Latihan');
            breathingStep = 0;
        }

        $breathingBtn.click(function() {
            if (isBreathing) {
                stopBreathing();
            } else {
                isBreathing = true;
                $breathingBtn.text('Hentikan Latihan');
                breathingStep = 0;
                runBreathingStep();
            }
        });

        // Expandable Tips Accordion
        $root.find('.mhc-accordion-header').click(function() {
            const $item = $(this).parent('.mhc-accordion-item');
            const isActive = $item.hasClass('active');
            
            $root.find('.mhc-accordion-item').removeClass('active').find('.mhc-accordion-body').slideUp();
            
            if (!isActive) {
                $item.addClass('active');
                $item.find('.mhc-accordion-body').slideDown();
            }
        });

        // Personal Reflection Journal
        let journalEntries = JSON.parse(localStorage.getItem('chatbot_journal_entries') || '[]');

        function renderJournalList() {
            const $logs = $('#journal-logs');
            $logs.empty();
            
            if (journalEntries.length === 0) {
                $logs.append('<div class="journal-empty-msg">Belum ada jurnal yang disimpan hari ini.</div>');
                return;
            }
            
            journalEntries.forEach(function(entry) {
                $logs.append(`
                    <div class="journal-entry-item">
                        <div class="journal-entry-header">
                            <span>${entry.mood}</span>
                            <span>${entry.time}</span>
                        </div>
                        <div class="journal-entry-content">
                            ${entry.text}
                        </div>
                    </div>
                `);
            });
        }
        renderJournalList();

        $('#btn-save-journal-entry').click(function() {
            const text = $('#journal-text-input').val().trim();
            if (!text) return;
            
            const mood = $('#journal-mood-select-box').val();
            const time = new Date().toLocaleTimeString('id-ID', { hour: '2-digit', minute: '2-digit' });
            
            const entry = { text, mood, time };
            journalEntries.unshift(entry);
            
            localStorage.setItem('chatbot_journal_entries', JSON.stringify(journalEntries));
            $('#journal-text-input').val('');
            
            renderJournalList();
        });

    });
})();

