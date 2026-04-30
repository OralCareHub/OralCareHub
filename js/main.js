// ============================================
// OralCareHub - Main JavaScript
// ============================================

// Mobile nav toggle
document.addEventListener('DOMContentLoaded', () => {
  const toggle = document.getElementById('navToggle');
  const links = document.getElementById('navLinks');

  if (toggle && links) {
    toggle.addEventListener('click', () => {
      links.classList.toggle('active');
    });
  }

  // Close mobile nav on link click
  document.querySelectorAll('.nav-links a').forEach(link => {
    link.addEventListener('click', () => {
      if (links) links.classList.remove('active');
    });
  });

  // Track affiliate link clicks (for analytics)
  document.querySelectorAll('[data-affiliate]').forEach(link => {
    link.addEventListener('click', (e) => {
      const affiliateId = e.currentTarget.dataset.affiliate;
      console.log(`Affiliate click: ${affiliateId}`);
      // In production, replace with actual tracking
    });
  });

  // Content locker functionality
  initContentLockers();
});

// Content Locker System
// Replace the locker action URL with your MyLead CPA locker URL
function initContentLockers() {
  document.querySelectorAll('.unlock-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      const lockerId = btn.dataset.locker;

      // === REPLACE THIS URL WITH YOUR MYLEAD CPA LOCKER URL ===
      const lockerUrl = btn.dataset.lockerUrl || '#';

      if (lockerUrl === '#') {
        console.warn('No locker URL configured. Set data-locker-url on the button.');
        return;
      }

      // Open the CPA locker in a new window
      const lockerWindow = window.open(lockerUrl, 'locker', 'width=600,height=500');

      // Poll to check if the locker was completed
      const checkInterval = setInterval(() => {
        if (lockerWindow && lockerWindow.closed) {
          clearInterval(checkInterval);
          unlockContent(lockerId);
        }
      }, 1000);
    });
  });

  // Check if content was previously unlocked (via localStorage)
  document.querySelectorAll('.content-locker').forEach(locker => {
    const lockerId = locker.dataset.lockerId;
    if (localStorage.getItem(`unlocked_${lockerId}`)) {
      unlockContent(lockerId);
    }
  });
}

function unlockContent(lockerId) {
  const locker = document.querySelector(`[data-locker-id="${lockerId}"]`);
  if (!locker) return;

  const overlay = locker.querySelector('.locker-overlay');
  const content = locker.querySelector('.locked-content');

  if (overlay) overlay.style.display = 'none';
  if (content) {
    content.style.filter = 'none';
    content.style.pointerEvents = 'auto';
    content.style.userSelect = 'auto';
  }

  // Remember unlock state
  localStorage.setItem(`unlocked_${lockerId}`, 'true');
}

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', (e) => {
    const target = document.querySelector(anchor.getAttribute('href'));
    if (target) {
      e.preventDefault();
      target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  });
});
