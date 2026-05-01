// ============================================
// OralCareHub - Main JavaScript
// ============================================

document.addEventListener('DOMContentLoaded', () => {

  // ---- MOBILE NAV TOGGLE ----
  const toggle = document.getElementById('navToggle');
  const links = document.getElementById('navLinks');

  if (toggle && links) {
    toggle.addEventListener('click', () => {
      links.classList.toggle('active');
    });
  }

  document.querySelectorAll('.nav-links a').forEach(link => {
    link.addEventListener('click', () => {
      if (links) links.classList.remove('active');
    });
  });

  // ---- HEADER SCROLL EFFECT ----
  const header = document.querySelector('.header');
  if (header) {
    window.addEventListener('scroll', () => {
      if (window.scrollY > 50) {
        header.classList.add('scrolled');
      } else {
        header.classList.remove('scrolled');
      }
    }, { passive: true });
  }

  // ---- SCROLL REVEAL ANIMATIONS ----
  const revealElements = document.querySelectorAll('.reveal, .reveal-left, .reveal-right, .reveal-scale');

  if (revealElements.length > 0) {
    const revealObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          revealObserver.unobserve(entry.target);
        }
      });
    }, {
      threshold: 0.12,
      rootMargin: '0px 0px -40px 0px'
    });

    revealElements.forEach(el => revealObserver.observe(el));
  }

  // ---- AFFILIATE LINK TRACKING ----
  document.querySelectorAll('[data-affiliate]').forEach(link => {
    link.addEventListener('click', (e) => {
      const affiliateId = e.currentTarget.dataset.affiliate;
      console.log(`Affiliate click: ${affiliateId}`);
    });
  });

  // ---- CONTENT LOCKER ----
  initContentLockers();
});

// Content Locker System
function initContentLockers() {
  document.querySelectorAll('.unlock-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      const lockerId = btn.dataset.locker;
      const lockerUrl = btn.dataset.lockerUrl || '#';

      if (lockerUrl === '#') {
        console.warn('No locker URL configured. Set data-locker-url on the button.');
        return;
      }

      const lockerWindow = window.open(lockerUrl, 'locker', 'width=600,height=500');

      const checkInterval = setInterval(() => {
        if (lockerWindow && lockerWindow.closed) {
          clearInterval(checkInterval);
          unlockContent(lockerId);
        }
      }, 1000);
    });
  });

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
