/**
 * Real-time filter & search for /frameworks/
 */
document.addEventListener('DOMContentLoaded', () => {
  const searchInput = document.getElementById('fw-search-input');
  const chips = document.querySelectorAll('.fw-chip');
  const grid = document.getElementById('fw-grid');
  const countDisplay = document.getElementById('fw-count-display');

  if (!grid) return;

  const cards = Array.from(grid.querySelectorAll('.fw-card'));
  let currentFilter = 'all';
  let searchQuery = '';

  function applyFilter() {
    let visibleCount = 0;

    cards.forEach(card => {
      const title = (card.getAttribute('data-title') || '').toLowerCase();
      const tags = (card.getAttribute('data-tags') || '').toLowerCase();
      const chip = (card.getAttribute('data-chip') || '').toLowerCase();
      const text = card.textContent.toLowerCase();

      // Check category chip
      let matchesCat = (currentFilter === 'all');
      if (currentFilter === 'ai') {
        matchesCat = tags.includes('ai') || tags.includes('aeo') || tags.includes('llm') || chip.includes('ai');
      } else if (currentFilter === 'recovery') {
        matchesCat = tags.includes('recovery') || tags.includes('ymyl') || chip.includes('recovery');
      } else if (currentFilter === 'architecture') {
        matchesCat = tags.includes('eav') || tags.includes('taxonomy') || tags.includes('crawl') || chip.includes('semantic');
      }

      // Check search query
      const matchesSearch = !searchQuery || text.includes(searchQuery) || title.includes(searchQuery);

      if (matchesCat && matchesSearch) {
        card.style.display = '';
        visibleCount++;
      } else {
        card.style.display = 'none';
      }
    });

    if (countDisplay) {
      countDisplay.textContent = `Showing ${visibleCount} of ${cards.length} technical playbooks`;
    }
  }

  if (searchInput) {
    searchInput.addEventListener('input', (e) => {
      searchQuery = e.target.value.trim().toLowerCase();
      applyFilter();
    });
  }

  chips.forEach(chip => {
    chip.addEventListener('click', () => {
      chips.forEach(c => {
        c.classList.remove('active');
        c.style.background = '';
        c.style.color = '';
      });
      chip.classList.add('active');
      chip.style.background = 'var(--primary)';
      chip.style.color = '#fff';

      currentFilter = chip.getAttribute('data-filter') || 'all';
      applyFilter();
    });
  });

  applyFilter();
});
