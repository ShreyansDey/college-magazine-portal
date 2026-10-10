/**
 * main.js - Interactive Controls for Vidyamandira Magazine Portal
 * Refined human-crafted interactions: Slideshow, Multi-Filter, Theme Sync, Drawer, ⌘K Shortcut.
 */

// Ensure page always starts at the top on reload or refresh
if ('scrollRestoration' in history) {
  history.scrollRestoration = 'manual';
}

// Clear lingering hash and reset scroll position to top
if (window.location.hash === '#publications') {
  history.replaceState(null, document.title, window.location.pathname + window.location.search);
}
window.scrollTo(0, 0);

document.addEventListener('DOMContentLoaded', () => {
  window.scrollTo(0, 0);
  initSlideshow();
  initThemeToggle();
  initMagazineFilter();
  initMobileDrawer();
  initKeyboardShortcuts();
  initScrollReveal();
});

/* --------------------------------------------------------------------------
   1. Dynamic 4K Background Slideshow (Ref 1 inspired)
   -------------------------------------------------------------------------- */
let currentSlideIndex = 0;
let slideInterval = null;
const SLIDE_DURATION = 6000; // 6 seconds

function initSlideshow() {
  const slides = document.querySelectorAll('.spotlight-slide');
  const dots = document.querySelectorAll('.slideshow-indicators .dot');
  const counterEl = document.getElementById('slideCounter');
  const prevBtn = document.getElementById('slidePrevBtn');
  const nextBtn = document.getElementById('slideNextBtn');

  if (!slides.length) return;

  // Set background images
  slides.forEach(s => {
    const bg = s.getAttribute('data-bg');
    if (bg) {
      s.style.backgroundImage = `url('${bg}')`;
    }
  });

  function updateCounter(index) {
    if (counterEl) {
      const current = String(index + 1).padStart(2, '0');
      const total = String(slides.length).padStart(2, '0');
      counterEl.textContent = `${current} / ${total}`;
    }
  }

  function showSlide(index) {
    slides.forEach((s, i) => {
      s.classList.toggle('active', i === index);
    });
    dots.forEach((d, i) => {
      d.classList.toggle('active', i === index);
    });
    currentSlideIndex = index;
    updateCounter(index);
  }

  window.goToSlide = function(index) {
    showSlide(index);
    resetSlideTimer();
  };

  function nextSlide() {
    const nextIndex = (currentSlideIndex + 1) % slides.length;
    showSlide(nextIndex);
  }

  function prevSlide() {
    const prevIndex = (currentSlideIndex - 1 + slides.length) % slides.length;
    showSlide(prevIndex);
  }

  if (prevBtn) {
    prevBtn.addEventListener('click', () => {
      prevSlide();
      resetSlideTimer();
    });
  }

  if (nextBtn) {
    nextBtn.addEventListener('click', () => {
      nextSlide();
      resetSlideTimer();
    });
  }

  function startSlideTimer() {
    slideInterval = setInterval(nextSlide, SLIDE_DURATION);
  }

  function resetSlideTimer() {
    clearInterval(slideInterval);
    startSlideTimer();
  }

  updateCounter(0);
  startSlideTimer();
}

/* --------------------------------------------------------------------------
   2. Theme Toggle (Sync across topbar, left rail & admin portal)
   -------------------------------------------------------------------------- */
function initThemeToggle() {
  const topToggleBtn = document.getElementById('themeToggle');
  const railToggleBtn = document.getElementById('themeToggleRail');
  const adminToggleBtn = document.getElementById('adminThemeToggle');
  const allButtons = [topToggleBtn, railToggleBtn, adminToggleBtn].filter(Boolean);

  // Check saved theme or compute ambient surroundings
  let savedTheme = localStorage.getItem('theme');
  if (!savedTheme) {
    const prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
    const hour = new Date().getHours();
    // 6 PM (18:00) to 6 AM is nighttime -> Dark Theme; daytime -> Light Theme
    const isNight = (hour >= 18 || hour < 6);
    savedTheme = (prefersDark || isNight) ? 'dark' : 'light';
  }

  document.documentElement.setAttribute('data-theme', savedTheme);
  updateThemeIcons(savedTheme);

  function toggleTheme() {
    const current = document.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', current);
    localStorage.setItem('theme', current);
    updateThemeIcons(current);
  }

  allButtons.forEach(btn => {
    btn.addEventListener('click', toggleTheme);
  });

  function updateThemeIcons(theme) {
    const iconHtml = theme === 'dark'
      ? '<i class="fa-solid fa-sun" style="color: #f59e0b;"></i>'
      : '<i class="fa-solid fa-moon"></i>';

    allButtons.forEach(btn => {
      btn.innerHTML = iconHtml;
    });
  }
}

/* --------------------------------------------------------------------------
   3. Live Search & Multi-Dimensional Category & Session Filter
   -------------------------------------------------------------------------- */
function initMagazineFilter() {
  const searchInput = document.getElementById('searchInput');
  const topSearchInput = document.getElementById('topSearchInput');
  const clearSearchBtn = document.getElementById('clearSearch');
  const categoryButtons = document.querySelectorAll('.cat-filter-btn');
  const yearSelect = document.getElementById('yearSelect');
  const magazineCards = document.querySelectorAll('.publication-bento-card');
  const matchCountEl = document.getElementById('matchCount');
  const emptyState = document.getElementById('emptyState');
  const resetFiltersBtn = document.getElementById('resetFiltersBtn');

  if (!magazineCards.length) return;

  const defaultYear = yearSelect && yearSelect.value ? yearSelect.value : '2025-2026';
  const defaultCategory = 'Hostel';
  let activeCategory = defaultCategory;
  let activeYear = defaultYear;
  let searchQuery = '';

  function applyFilters() {
    let visibleCount = 0;

    magazineCards.forEach(card => {
      const cardTitle = card.getAttribute('data-title') || '';
      const cardDept = card.getAttribute('data-department') || '';
      const cardCat = card.getAttribute('data-category') || '';
      const cardYear = card.getAttribute('data-year') || '';
      const cardTags = card.getAttribute('data-tags') || '';

      const matchesCategory = (activeCategory === 'ALL' || cardCat.toLowerCase() === activeCategory.toLowerCase());
      const matchesYear = (activeYear === 'ALL' || cardYear === activeYear);

      const searchableText = `${cardTitle} ${cardDept} ${cardTags}`.toLowerCase();
      const matchesSearch = (!searchQuery || searchableText.includes(searchQuery));

      if (matchesCategory && matchesYear && matchesSearch) {
        card.classList.remove('hidden');
        card.classList.add('is-revealed');
        visibleCount++;
      } else {
        card.classList.add('hidden');
      }
    });

    if (matchCountEl) matchCountEl.textContent = visibleCount;
    if (emptyState) emptyState.classList.toggle('hidden', visibleCount !== 0);

    const hasActiveFilters = (activeCategory !== defaultCategory || activeYear !== defaultYear || searchQuery.length > 0);
    if (resetFiltersBtn) resetFiltersBtn.classList.toggle('hidden', !hasActiveFilters);
    if (clearSearchBtn) clearSearchBtn.classList.toggle('hidden', searchQuery.length === 0);
  }

  // Sync inputs
  if (searchInput) {
    searchInput.addEventListener('input', (e) => {
      searchQuery = e.target.value.trim().toLowerCase();
      if (topSearchInput) topSearchInput.value = e.target.value;
      applyFilters();
    });
  }

  if (topSearchInput) {
    topSearchInput.addEventListener('input', (e) => {
      searchQuery = e.target.value.trim().toLowerCase();
      if (searchInput) searchInput.value = e.target.value;
      applyFilters();
      // Auto-scroll to catalog if typing
      scrollToPublications();
    });
  }

  if (clearSearchBtn) {
    clearSearchBtn.addEventListener('click', () => {
      if (searchInput) searchInput.value = '';
      if (topSearchInput) topSearchInput.value = '';
      searchQuery = '';
      applyFilters();
      if (searchInput) searchInput.focus();
    });
  }

  // Category buttons
  categoryButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      const cat = btn.getAttribute('data-category');
      categoryButtons.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      activeCategory = cat;
      applyFilters();
    });
  });

  // Academic Session select
  if (yearSelect) {
    yearSelect.addEventListener('change', (e) => {
      activeYear = e.target.value;
      applyFilters();
    });
  }

  // Global reset helper
  window.resetAllFilters = function() {
    activeCategory = defaultCategory;
    activeYear = defaultYear;
    searchQuery = '';

    if (searchInput) searchInput.value = '';
    if (topSearchInput) topSearchInput.value = '';
    if (yearSelect) yearSelect.value = defaultYear;

    categoryButtons.forEach(b => {
      const isDefault = b.getAttribute('data-category').toLowerCase() === defaultCategory.toLowerCase();
      b.classList.toggle('active', isDefault);
    });

    applyFilters();
  };

  if (resetFiltersBtn) {
    resetFiltersBtn.addEventListener('click', window.resetAllFilters);
  }

  // Helper for quick category filtering from any button/card
  window.filterByCategory = function(category) {
    const targetBtn = Array.from(categoryButtons).find(
      b => b.getAttribute('data-category').toLowerCase() === category.toLowerCase()
    );
    if (targetBtn) {
      targetBtn.click();
    }
  };

  window.scrollToPublications = function(e) {
    if (e && e.preventDefault) {
      e.preventDefault();
    }
    const pubSection = document.getElementById('publications');
    if (pubSection) {
      pubSection.scrollIntoView({ behavior: 'smooth' });
    }
  };

  // Check URL query parameters for direct search landing (e.g. from 404 page)
  const urlParams = new URLSearchParams(window.location.search);
  const initialSearch = urlParams.get('search');
  if (initialSearch) {
    searchQuery = initialSearch.trim().toLowerCase();
    if (searchInput) searchInput.value = initialSearch;
    if (topSearchInput) topSearchInput.value = initialSearch;
  }
  applyFilters();
}

/* --------------------------------------------------------------------------
   4. Mobile Navigation Drawer
   -------------------------------------------------------------------------- */
function initMobileDrawer() {
  const toggleBtn = document.getElementById('mobileToggle');
  const closeBtn = document.getElementById('drawerCloseBtn');
  const drawer = document.getElementById('mobileDrawer');
  const backdrop = document.getElementById('drawerBackdrop');

  function openDrawer() {
    if (drawer) drawer.classList.add('open');
    if (backdrop) backdrop.classList.add('open');
    document.body.style.overflow = 'hidden';
  }

  window.closeDrawer = function() {
    if (drawer) drawer.classList.remove('open');
    if (backdrop) backdrop.classList.remove('open');
    document.body.style.overflow = '';
  };

  if (toggleBtn) toggleBtn.addEventListener('click', openDrawer);
  if (closeBtn) closeBtn.addEventListener('click', window.closeDrawer);
  if (backdrop) backdrop.addEventListener('click', window.closeDrawer);
}

/* --------------------------------------------------------------------------
   5. Keyboard Shortcuts (⌘K / Ctrl+K)
   -------------------------------------------------------------------------- */
function initKeyboardShortcuts() {
  document.addEventListener('keydown', (e) => {
    if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
      e.preventDefault();
      const topSearch = document.getElementById('topSearchInput');
      const catalogSearch = document.getElementById('searchInput');
      if (topSearch && window.innerWidth > 900) {
        topSearch.focus();
      } else if (catalogSearch) {
        catalogSearch.focus();
        catalogSearch.scrollIntoView({ behavior: 'smooth' });
      }
    }
  });
}

/* --------------------------------------------------------------------------
   6. Global Publication Card Click Handler & In-Compilation Modal Controller
   -------------------------------------------------------------------------- */
window.handlePublicationCardClick = function(element) {
  if (!element) return;
  const hasReader = element.dataset.hasReader === 'true' || element.getAttribute('data-has-reader') === 'true';
  const readUrl = element.dataset.readUrl || element.getAttribute('data-read-url');

  if (hasReader && readUrl) {
    window.location.href = readUrl;
    return;
  }

  // Fallback: open the compilation modal
  window.openComingSoonModal(element);
};

window.openComingSoonModal = function(param) {
  let title = 'Collegiate Publication';
  let dept = 'Ramakrishna Mission Vidyamandira';
  let cat = 'Departmental';
  let year = '2025–2026';
  let desc = 'This digital edition is currently being compiled and reviewed by the student editorial board. Full interactive layouts, research papers, and literary articles will be published shortly via the College Editorial Portal.';

  if (param instanceof HTMLElement) {
    title = param.getAttribute('data-pub-title') || param.getAttribute('data-title') || title;
    dept = param.getAttribute('data-pub-dept') || param.getAttribute('data-department') || dept;
    cat = param.getAttribute('data-pub-category') || param.getAttribute('data-category') || cat;
    year = param.getAttribute('data-pub-year') || param.getAttribute('data-year') || year;
    desc = param.getAttribute('data-pub-desc') || param.getAttribute('data-desc') || desc;
  } else if (typeof param === 'object' && param !== null) {
    title = param.title || title;
    dept = param.department || dept;
    cat = param.category || cat;
    year = param.year || year;
    desc = param.desc || desc;
  }

  const titleEl = document.getElementById('comingSoonTitle');
  const deptEl = document.getElementById('comingSoonDept');
  const catEl = document.getElementById('comingSoonCategory');
  const yearEl = document.getElementById('comingSoonYear');
  const descEl = document.getElementById('comingSoonDesc');
  const pubEl = document.getElementById('comingSoonPublisher');
  const sessEl = document.getElementById('comingSoonSession');

  if (titleEl) titleEl.textContent = title;
  if (deptEl) deptEl.textContent = dept;
  if (catEl) catEl.textContent = cat;
  if (yearEl) yearEl.textContent = year;
  if (descEl) descEl.textContent = desc;
  if (pubEl) pubEl.textContent = dept;
  if (sessEl) sessEl.textContent = year;

  const backdrop = document.getElementById('comingSoonBackdrop');
  const modal = document.getElementById('comingSoonModal');
  if (backdrop && modal) {
    backdrop.removeAttribute('hidden');
    modal.removeAttribute('hidden');
    void modal.offsetWidth; // Force DOM reflow
    backdrop.classList.add('active');
    modal.classList.add('active');
    document.body.style.overflow = 'hidden';
  }
};

window.closeComingSoonModal = function() {
  const backdrop = document.getElementById('comingSoonBackdrop');
  const modal = document.getElementById('comingSoonModal');
  if (backdrop && modal) {
    backdrop.classList.remove('active');
    modal.classList.remove('active');
    setTimeout(() => {
      backdrop.setAttribute('hidden', '');
      modal.setAttribute('hidden', '');
    }, 250);
    document.body.style.overflow = '';
  }
};

document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') {
    window.closeComingSoonModal();
  }
});

/* --------------------------------------------------------------------------
   6. Dynamic Scroll Reveal ("Coming Out of Vanish")
   Observes cards & content blocks as the user scrolls, materializing them
   smoothly from empty blur and translated space into sharp focus.
   -------------------------------------------------------------------------- */
function initScrollReveal() {
  const selector = [
    '.category-bento-card',
    '.publication-bento-card',
    '.bhavan-edition-item',
    '.dept-issue-row',
    '.annual-edition-card',
    '.suggested-item-row',
    '.heritage-retrospective-card',
    '.metric-bento-card',
    '.spec-card',
    '.rule-guide-box',
    '.scroll-reveal'
  ].join(', ');

  const targets = document.querySelectorAll(selector);
  if (!targets.length) return;

  // Add the initial vanish class and calculate stagger delays
  targets.forEach((el, index) => {
    const rect = el.getBoundingClientRect();
    const isAboveFold = rect.top < window.innerHeight && rect.bottom > 0;

    el.classList.add('reveal-on-scroll');
    const delayStep = (index % 5) + 1;
    el.setAttribute('data-delay', delayStep.toString());

    if (isAboveFold) {
      setTimeout(() => {
        el.classList.add('is-revealed');
      }, 70 * delayStep);
    }
  });

  if (!('IntersectionObserver' in window)) {
    targets.forEach(el => el.classList.add('is-revealed'));
    return;
  }

  const observerOptions = {
    root: null,
    rootMargin: '0px 0px -40px 0px',
    threshold: 0.08
  };

  const revealObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-revealed');
        observer.unobserve(entry.target);
      }
    });
  }, observerOptions);

  targets.forEach(el => {
    if (!el.classList.contains('is-revealed')) {
      revealObserver.observe(el);
    }
  });
}

