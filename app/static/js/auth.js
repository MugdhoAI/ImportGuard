(() => {
  const toggle = document.querySelector('[data-password-toggle]');
  const input = document.getElementById('auth-password');
  if (!toggle || !input) return;
  toggle.addEventListener('click', () => {
    const visible = input.type === 'text';
    input.type = visible ? 'password' : 'text';
    toggle.textContent = visible ? 'Show' : 'Hide';
    toggle.setAttribute('aria-label', `${visible ? 'Show' : 'Hide'} password`);
  });
})();
