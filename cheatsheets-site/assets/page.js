// Скрипт для страниц шпаргалок: кнопка "наверх", копирование кода,
// подсветка активного раздела в оглавлении.
(function () {
  // ── Кнопка "наверх" ────────────────────────────────────────────
  const backTop = document.getElementById("backTop");
  if (backTop) {
    const toggle = () =>
      backTop.classList.toggle("visible", window.scrollY > 400);
    window.addEventListener("scroll", toggle, { passive: true });
    toggle();
    backTop.addEventListener("click", () =>
      window.scrollTo({ top: 0, behavior: "smooth" })
    );
  }

  // ── Подсветка активного раздела в TOC ──────────────────────────
  const headings = Array.from(document.querySelectorAll("article h2, article h3"));
  const tocLinks = Array.from(document.querySelectorAll(".toc a[href^='#']"));

  if (headings.length && tocLinks.length) {
    const byId = new Map(headings.map((h) => [h.id, h]));

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            tocLinks.forEach((link) => {
              const active = link.getAttribute("href") === "#" + entry.target.id;
              link.style.color = active ? "var(--accent-2)" : "";
              link.style.fontWeight = active ? "700" : "";
              link.style.borderLeftColor = active
                ? "var(--accent-2)"
                : "transparent";
            });
          }
        });
      },
      { rootMargin: "-80px 0px -70% 0px" }
    );

    headings.forEach((h) => h.id && observer.observe(h));
  }

  // ── Кнопка "копировать" у блоков кода ──────────────────────────
  const pres = Array.from(document.querySelectorAll("article pre"));
  pres.forEach((pre) => {
    const btn = document.createElement("button");
    btn.className = "copy-btn";
    btn.textContent = "копировать";
    btn.setAttribute("aria-label", "Скопировать код");

    btn.addEventListener("click", async () => {
      const code = pre.querySelector("code");
      const text = code ? code.textContent : pre.textContent;
      try {
        await navigator.clipboard.writeText(text);
        btn.textContent = "✓ скопировано";
        btn.classList.add("copied");
        setTimeout(() => {
          btn.textContent = "копировать";
          btn.classList.remove("copied");
        }, 1500);
      } catch {
        btn.textContent = "ошибка";
        setTimeout(() => (btn.textContent = "копировать"), 1500);
      }
    });

    pre.style.position = "relative";
    pre.appendChild(btn);
  });

  // ── Горячие клавиши навигации ──────────────────────────────────
  document.addEventListener("keydown", (e) => {
    // Не реагируем, если фокус в поле ввода
    const tag = document.activeElement.tagName;
    if (tag === "INPUT" || tag === "TEXTAREA") return;

    // Ctrl/Cmd + ← / →  →  пагинация
    if ((e.ctrlKey || e.metaKey) && e.key === "ArrowLeft") {
      const prev = document.querySelector(".pager.prev");
      if (prev && prev.tagName === "A") {
        e.preventDefault();
        window.location.href = prev.href;
      }
    }
    if ((e.ctrlKey || e.metaKey) && e.key === "ArrowRight") {
      const next = document.querySelector(".pager.next");
      if (next && next.tagName === "A") {
        e.preventDefault();
        window.location.href = next.href;
      }
    }
    // "g" затем "h" → на главную
    if (e.key === "g") {
      const onH = (ev) => {
        if (ev.key === "h") window.location.href = "index.html";
        document.removeEventListener("keydown", onH);
      };
      document.addEventListener("keydown", onH);
      setTimeout(() => document.removeEventListener("keydown", onH), 1000);
    }
  });
})();
