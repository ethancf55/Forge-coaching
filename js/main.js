document.addEventListener('DOMContentLoaded', () => {
  const header = document.getElementById('header');
  const navToggle = document.getElementById('navToggle');
  const navLinks = document.getElementById('navLinks');
  const contactForm = document.getElementById('contactForm');
  const toast = document.getElementById('toast');
  const sourceInput = document.getElementById('source');

  // Header scroll effect
  window.addEventListener('scroll', () => {
    header.classList.toggle('scrolled', window.scrollY > 20);
  });

  // Mobile nav toggle
  navToggle.addEventListener('click', () => {
    const isOpen = navLinks.classList.toggle('open');
    navToggle.classList.toggle('active', isOpen);
    navToggle.setAttribute('aria-expanded', isOpen);
    navToggle.setAttribute('aria-label', isOpen ? 'Close menu' : 'Open menu');
  });

  // Close mobile nav on link click
  navLinks.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', () => {
      navLinks.classList.remove('open');
      navToggle.classList.remove('active');
      navToggle.setAttribute('aria-expanded', 'false');
      navToggle.setAttribute('aria-label', 'Open menu');
    });
  });

  // Pricing / CTA buttons can tag interest source before scroll-to-form
  document.querySelectorAll('[data-plan]').forEach(btn => {
    btn.addEventListener('click', () => {
      if (sourceInput && btn.dataset.plan) {
        sourceInput.value = btn.dataset.plan;
      }
    });
  });

  // Intake form submission → /api/contact (emails Ethan via Resend)
  if (contactForm) {
    contactForm.addEventListener('submit', async e => {
      e.preventDefault();

      if (!contactForm.reportValidity()) {
        return;
      }

      const submitBtn = contactForm.querySelector('button[type="submit"]');
      const originalText = submitBtn.textContent;
      submitBtn.disabled = true;
      submitBtn.textContent = 'Sending...';

      const formData = new FormData(contactForm);
      const data = Object.fromEntries(formData.entries());

      try {
        const response = await fetch('/api/contact', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(data),
        });

        const result = await response.json().catch(() => ({}));

        if (!response.ok) {
          throw new Error(result.error || 'Failed to send form');
        }

        contactForm.reset();
        if (sourceInput) {
          sourceInput.value = '12-Week Program — $349';
        }
        showToast('Intake sent. Check your email — I’ll follow up within 24 hours.');
      } catch (error) {
        showToast(
          error.message || 'Something went wrong. Please email ethanflem1@gmail.com directly.'
        );
      } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = originalText;
      }
    });
  }

  function showToast(message) {
    if (!toast) return;
    toast.textContent = message;
    toast.classList.add('show');
    setTimeout(() => toast.classList.remove('show'), 5500);
  }

  // Scroll reveal animations
  const revealElements = document.querySelectorAll(
    '.reveal, .step, .pricing-card, .testimonial-card, .faq-item, .section-header, .audience-card, .offer-callout'
  );

  revealElements.forEach(el => el.classList.add('reveal'));

  const observer = new IntersectionObserver(
    entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.1, rootMargin: '0px 0px -40px 0px' }
  );

  revealElements.forEach(el => observer.observe(el));
});
