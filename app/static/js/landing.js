document.querySelectorAll('.review-chip').forEach((chip) => {
  chip.addEventListener('click', () => {
    const note = chip.closest('.hero-visual').querySelector('.sample-note');
    note.hidden = !note.hidden;
    chip.setAttribute('aria-expanded', String(!note.hidden));
  });
});
