// Живой поиск по карточкам на главной странице.
// Ищет по заголовку, описанию и тегам (без учёта регистра).
(function () {
  const input = document.getElementById("search");
  if (!input) return; // не главная страница

  const cards = Array.from(document.querySelectorAll(".card"));
  const grid = document.getElementById("cards");

  // Кэшируем текст карточек для быстрого поиска
  const indexed = cards.map((card) => ({
    el: card,
    text: card.textContent.toLowerCase(),
  }));

  let noResultsEl = null;
  function ensureNoResults() {
    if (!noResultsEl) {
      noResultsEl = document.createElement("div");
      noResultsEl.className = "no-results";
      noResultsEl.textContent = "Ничего не найдено 🤔";
      grid.appendChild(noResultsEl);
    }
    return noResultsEl;
  }

  input.addEventListener("input", () => {
    const q = input.value.trim().toLowerCase();
    let visibleCount = 0;

    indexed.forEach(({ el, text }) => {
      const match = !q || text.includes(q);
      el.classList.toggle("hidden", !match);
      if (match) visibleCount++;
    });

    ensureNoResults().style.display = visibleCount === 0 ? "block" : "none";
  });

  // Горячая клавиша "/" для фокуса на поиск
  document.addEventListener("keydown", (e) => {
    if (e.key === "/" && document.activeElement !== input) {
      e.preventDefault();
      input.focus();
    }
    if (e.key === "Escape" && document.activeElement === input) {
      input.value = "";
      input.dispatchEvent(new Event("input"));
      input.blur();
    }
  });
})();
