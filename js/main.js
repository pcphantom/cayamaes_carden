/* ============================================================
   CAYAMAES ANCIENT GARDEN — Main JS
   ============================================================ */

'use strict';

// ── Prevent Unwanted Scroll Restoration ─────────────────────
// Browsers can restore the previous scroll position on reload. Combined with
// smooth scrolling, that looks like the page is scrolling by itself.
if ('scrollRestoration' in history) {
  history.scrollRestoration = 'manual';
}

function resetUnlinkedScrollPosition() {
  if (window.location.hash) return;

  const root = document.documentElement;
  const previousBehavior = root.style.scrollBehavior;
  root.style.scrollBehavior = 'auto';
  window.scrollTo(0, 0);
  root.style.scrollBehavior = previousBehavior;
}

resetUnlinkedScrollPosition();
window.addEventListener('pageshow', resetUnlinkedScrollPosition);

// ── Nav Scroll Behavior ──────────────────────────────────────
const nav = document.getElementById('nav');
window.addEventListener('scroll', () => {
  nav.classList.toggle('scrolled', window.scrollY > 60);
}, { passive: true });

// ── Mobile Menu ──────────────────────────────────────────────
const hamburger   = document.getElementById('hamburger');
const mobileMenu  = document.getElementById('mobileMenu');
const menuClose   = document.getElementById('menuClose');

hamburger.addEventListener('click', () => {
  mobileMenu.classList.add('open');
  hamburger.setAttribute('aria-expanded', 'true');
});
menuClose.addEventListener('click', () => {
  mobileMenu.classList.remove('open');
  hamburger.setAttribute('aria-expanded', 'false');
});
mobileMenu.querySelectorAll('a').forEach(a =>
  a.addEventListener('click', () => {
    mobileMenu.classList.remove('open');
    hamburger.setAttribute('aria-expanded', 'false');
  })
);

// ── Scroll Reveal ────────────────────────────────────────────
const revealObserver = new IntersectionObserver((entries) => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      e.target.classList.add('visible');
      revealObserver.unobserve(e.target);
    }
  });
}, { threshold: 0.12 });

document.querySelectorAll('.reveal').forEach(el => revealObserver.observe(el));

// ── Product Filter ───────────────────────────────────────────
const filterBtns  = document.querySelectorAll('.filter-btn');
const productCards = document.querySelectorAll('.product-card');
const filterLinks = document.querySelectorAll('[data-set-filter]');

function applyProductFilter(category) {
  filterBtns.forEach(button => {
    button.classList.toggle('active', button.dataset.filter === category);
  });

  productCards.forEach(card => {
    const match = category === 'all' || card.dataset.category === category;
    card.style.display = match ? '' : 'none';
  });
}

filterBtns.forEach(btn => {
  btn.addEventListener('click', () => {
    applyProductFilter(btn.dataset.filter);
  });
});

filterLinks.forEach(link => {
  link.addEventListener('click', () => {
    const category = link.dataset.setFilter;
    if (category) {
      applyProductFilter(category);
    }
  });
});

// ── Add to Cart (placeholder) ────────────────────────────────
document.querySelectorAll('.product-add').forEach(btn => {
  btn.addEventListener('click', (e) => {
    e.stopPropagation();
    const name = btn.closest('.product-card').querySelector('.product-name').textContent;
    showToast(`"${name}" added to inquiry`);
  });
});

function showToast(msg) {
  const toast = document.createElement('div');
  toast.className = 'toast';
  toast.textContent = msg;
  Object.assign(toast.style, {
    position: 'fixed',
    bottom: '2rem',
    right: '2rem',
    background: 'var(--forest)',
    color: 'var(--gold-pale)',
    border: '1px solid rgba(200,151,58,0.4)',
    borderRadius: '4px',
    padding: '0.9rem 1.6rem',
    fontFamily: 'var(--font-ui)',
    fontSize: '0.82rem',
    letterSpacing: '0.05em',
    zIndex: '9999',
    opacity: '0',
    transform: 'translateY(10px)',
    transition: 'opacity 0.3s, transform 0.3s',
    boxShadow: '0 8px 25px rgba(0,0,0,0.35)'
  });
  document.body.appendChild(toast);
  requestAnimationFrame(() => {
    toast.style.opacity = '1';
    toast.style.transform = 'translateY(0)';
  });
  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateY(10px)';
    setTimeout(() => toast.remove(), 300);
  }, 2500);
}

// ── Smooth scroll for hero CTA ────────────────────────────────
document.querySelectorAll('a[href^="#"]').forEach(a => {
  a.addEventListener('click', e => {
    const href = a.getAttribute('href');
    if (!href || href === '#') {
      e.preventDefault();
      return;
    }

    const target = document.querySelector(href);
    if (target) {
      e.preventDefault();
      target.scrollIntoView({ behavior: 'smooth' });
    }
  });
});
