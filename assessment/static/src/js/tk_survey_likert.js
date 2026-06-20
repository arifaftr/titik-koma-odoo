document.addEventListener('DOMContentLoaded', function () {

    /* --- Progress bar --- */
    const fillEl    = document.getElementById('tk_progress_fill');
    const currentEl = document.getElementById('tk_current_q');
    const totalEl   = document.getElementById('tk_total_q');

    if (fillEl && totalEl) {
        const total = parseInt(totalEl.textContent) || 1;
        const allPages = document.querySelectorAll('.js_question-el');
        let currentIdx = 1;
        allPages.forEach(function (el, i) {
            if (!el.classList.contains('d-none') && !el.classList.contains('o_hidden')) {
                currentIdx = i + 1;
            }
        });
        if (currentEl) currentEl.textContent = currentIdx;
        const pct = Math.round((currentIdx / total) * 100);
        fillEl.style.width = pct + '%';
    }

    /* --- Likert card: klik + trigger Odoo JS --- */
    document.querySelectorAll('.tk_likert_options').forEach(function (group) {
        const cards = group.querySelectorAll('.tk_likert_card');

        cards.forEach(function (card) {
            card.addEventListener('click', function (e) {
                e.preventDefault();

                cards.forEach(function (c) {
                    c.classList.remove('tk_selected');
                });

                card.classList.add('tk_selected');

                const radio = card.querySelector('.tk_likert_radio');
                if (radio) {
                    radio.checked = true;

                    // Trigger event agar Odoo JS aktifkan tombol Continue
                    radio.dispatchEvent(new Event('change', { bubbles: true }));
                    radio.dispatchEvent(new MouseEvent('click', { bubbles: true }));
                }
            });
        });

        // Restore state jika user kembali
        cards.forEach(function (card) {
            const radio = card.querySelector('.tk_likert_radio');
            if (radio && radio.checked) {
                card.classList.add('tk_selected');
            }
        });
    });

});