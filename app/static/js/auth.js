(() => {
  const toggle = document.querySelector('[data-password-toggle]');
  const input = document.getElementById('auth-password');
  if (toggle && input) {
    toggle.addEventListener('click', () => {
      const visible = input.type === 'text';
      input.type = visible ? 'password' : 'text';
      toggle.textContent = visible ? 'Show' : 'Hide';
      toggle.setAttribute('aria-label', `${visible ? 'Show' : 'Hide'} password`);
    });
  }

  document.querySelectorAll('[data-oauth-link]').forEach((link) => {
    link.addEventListener('click', () => {
      link.setAttribute('aria-busy', 'true');
      link.classList.add('is-loading');
      link.textContent = `Connecting with ${link.dataset.provider}…`;
    }, { once: true });
  });
})();
