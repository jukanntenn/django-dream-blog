(function () {
  const searchToggle =
    document.querySelector<HTMLButtonElement>("#search-toggle");
  const searchOverlay =
    document.querySelector<HTMLDivElement>("#search-overlay");
  const searchClose = document.querySelector<HTMLButtonElement>("#search-close");
  const searchInput = searchOverlay?.querySelector<HTMLInputElement>(
    'input[type="search"]',
  );

  function openSearch() {
    searchOverlay?.classList.remove("hidden");
    searchInput?.focus();
  }

  function closeSearch() {
    searchOverlay?.classList.add("hidden");
  }

  searchToggle?.addEventListener("click", (e) => {
    e.preventDefault();
    openSearch();
  });

  searchClose?.addEventListener("click", (e) => {
    e.preventDefault();
    closeSearch();
  });

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && !searchOverlay?.classList.contains("hidden")) {
      closeSearch();
    }
  });
})();
