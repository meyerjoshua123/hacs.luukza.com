// Theme toggle (remembers your choice) and mobile menu.
(function () {
  var root = document.documentElement;
  var KEY = "hacs-luukza-theme";

  document.addEventListener("click", function (event) {
    var themeBtn = event.target.closest("[data-theme-toggle]");
    if (themeBtn) {
      var dark = !root.classList.contains("dark");
      root.classList.toggle("dark", dark);
      try { localStorage.setItem(KEY, dark ? "dark" : "light"); } catch (e) {}
      return;
    }
    var menuBtn = event.target.closest("[data-menu-toggle]");
    if (menuBtn) {
      var nav = document.querySelector(".nav");
      var open = nav.classList.toggle("open");
      menuBtn.setAttribute("aria-expanded", open ? "true" : "false");
    }
  });
})();
