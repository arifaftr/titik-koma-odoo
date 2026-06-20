/**
 * Titik Koma - Modern Mental Health Dashboard
 * Enhanced Interactivity and Features
 */

document.addEventListener('DOMContentLoaded', function() {
    initializeDashboard();
});

// Initialize dashboard
function initializeDashboard() {
    setupSidebarToggle();
    setupMenuItems();
    setupCardInteractions();
    setupThemePreferences();
    setupResponsive();
}

// Sidebar toggle functionality
function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    const toggle = document.getElementById('sidebarToggle');

    if (sidebar.classList.contains('collapsed')) {
        sidebar.classList.remove('collapsed');
        if (toggle) toggle.style.left = '250px';
        localStorage.setItem('sidebarCollapsed', 'false');
    } else {
        sidebar.classList.add('collapsed');
        if (toggle) toggle.style.left = '55px';
        localStorage.setItem('sidebarCollapsed', 'true');
    }
}

// Setup sidebar toggle on page load
function setupSidebarToggle() {
    const isSidebarCollapsed = localStorage.getItem('sidebarCollapsed') === 'true';
    const sidebar = document.getElementById('sidebar');
    const toggle = document.getElementById('sidebarToggle');

    if (isSidebarCollapsed) {
        sidebar.classList.add('collapsed');
        if (toggle) toggle.style.left = '55px';
    } else {
        if (toggle) toggle.style.left = '250px';
    }

    // Close sidebar on mobile
    if (window.innerWidth <= 768) {
        sidebar.classList.add('collapsed');
        if (toggle) toggle.style.left = '55px';
    }
}

// Setup menu item active state
function setupMenuItems() {
    const menuItems = document.querySelectorAll('.menu-item');

    menuItems.forEach(item => {
        item.addEventListener('click', function(e) {
            // Remove active class from all items
            menuItems.forEach(m => m.classList.remove('active'));
            // Add active class to clicked item
            this.classList.add('active');
        });
    });
}

// Setup card interactions
function setupCardInteractions() {
    const featureCards = document.querySelectorAll('.feature-card');

    featureCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-8px) scale(1.02)';
        });

        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });

        card.addEventListener('click', function() {
            const btn = this.querySelector('.card-btn');
            if (btn && btn.href !== '#') {
                window.location.href = btn.href;
            }
        });
    });
}

// Theme preference handling
function setupThemePreferences() {
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;

    if (prefersDark) {
        document.body.style.transition = 'background-color 0.3s ease';
    }

    // Save user preference
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
        localStorage.setItem('theme', e.matches ? 'dark' : 'light');
    });
}

// Responsive handling
function setupResponsive() {
    const sidebar = document.getElementById('sidebar');
    const toggle = document.getElementById('sidebarToggle');

    window.addEventListener('resize', () => {
        if (window.innerWidth <= 768 && !sidebar.classList.contains('collapsed')) {
            sidebar.classList.add('collapsed');
            if (toggle) toggle.style.left = '55px';
        }
    });

    // Close sidebar when clicking on menu item on mobile
    if (window.innerWidth <= 768) {
        const menuItems = document.querySelectorAll('.menu-item');
        menuItems.forEach(item => {
            item.addEventListener('click', () => {
                if (!sidebar.classList.contains('collapsed')) {
                    toggleSidebar();
                }
            });
        });
    }
}

// Mood logging functionality
function updateMood(mood) {
    const moodBox = document.querySelector('.mood-box h3');
    if (moodBox) {
        moodBox.textContent = mood + ' ✨';
        // Trigger animation
        moodBox.style.animation = 'none';
        setTimeout(() => {
            moodBox.style.animation = 'fadeIn 0.3s ease';
        }, 10);
    }
}

// Profile menu interaction
function setupProfileMenu() {
    const profileMini = document.querySelector('.profile-mini');
    if (profileMini) {
        profileMini.addEventListener('click', () => {
            // Could open profile modal or navigate to profile page
            console.log('Profile clicked');
        });
    }
}

// Smooth scroll
function smoothScroll(target) {
    const element = document.querySelector(target);
    if (element) {
        element.scrollIntoView({ behavior: 'smooth' });
    }
}

// Export functions for global use
window.toggleSidebar = toggleSidebar;
window.smoothScroll = smoothScroll;
window.updateMood = updateMood;
