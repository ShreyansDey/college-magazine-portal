/**
 * script.js - Interactive Controls & Navigation Highlighting
 * Lightweight, vanilla JavaScript with zero external dependencies.
 */

// Highlight navigation links smoothly as the reader scrolls through sections
document.addEventListener('DOMContentLoaded', () => {
  const navLinks = document.querySelectorAll('.editorial-nav-link');
  const sections = document.querySelectorAll('section[id]');

  window.addEventListener('scroll', () => {
    let current = '';
    const scrollPos = window.scrollY + 120;

    sections.forEach(section => {
      const top = section.offsetTop;
      const height = section.offsetHeight;
      if (scrollPos >= top && scrollPos < top + height) {
        current = section.getAttribute('id');
      }
    });

    navLinks.forEach(link => {
      link.classList.remove('active');
      if (link.getAttribute('href') === `#${current}`) {
        link.classList.add('active');
      }
    });
  });

  // Friendly console banner for student editorial teams
  console.log(
    "%c Ramakrishna Mission Vidyamandira \n%c Official Student Magazine Edition \n%c Built with Micro-Frontend Architecture • Belur Math",
    "color: #c9933b; font-size: 16px; font-weight: bold;",
    "color: #141518; font-size: 13px; font-weight: 600;",
    "color: #5c6068; font-size: 11px;"
  );
});
