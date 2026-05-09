(function () {
  function onReady(fn) {
    if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", fn);
    else fn();
  }

  function initMenu() {
    var toggle = document.querySelector(".menu-toggle");
    var menu = document.querySelector("#oda-main-menu, .menu");
    if (!toggle || !menu) return;
    toggle.addEventListener("click", function (e) {
      e.preventDefault();
      menu.classList.toggle("active");
      toggle.setAttribute("aria-expanded", menu.classList.contains("active"));
    });
    menu.querySelectorAll("a").forEach(function (a) {
      a.addEventListener("click", function () {
        menu.classList.remove("active");
        toggle.setAttribute("aria-expanded", "false");
      });
    });
    document.addEventListener("click", function (e) {
      if (!menu.classList.contains("active")) return;
      if (!e.target.closest(".menu") && !e.target.closest(".menu-toggle")) {
        menu.classList.remove("active");
        toggle.setAttribute("aria-expanded", "false");
      }
    });
  }

  function initStoreCarousels() {
    var prefersReduced = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    var carousels = document.querySelectorAll(".js-store-carousel");
    if (!carousels.length) return;
    var isRTL = (document.documentElement.getAttribute("dir") || "").toLowerCase() === "rtl";

    carousels.forEach(function (el) {
      var root = el.closest(".jewelry-store__carousel");
      var prev = root ? root.querySelector(".jewelry-store__nav--prev") : null;
      var next = root ? root.querySelector(".jewelry-store__nav--next") : null;
      var autoStoppedByUser = false;

      function step() {
        var first = el.querySelector(".jewelry-store__item");
        var stepPx = first ? first.getBoundingClientRect().width + 16 : 260;
        return stepPx;
      }

      function scrollByDir(dir) {
        var delta = dir * step() * (isRTL ? -1 : 1);
        el.scrollBy({ left: delta, behavior: "smooth" });
      }

      var timer = null;
      function start() {
        if (prefersReduced || autoStoppedByUser) return;
        if (timer) return;
        timer = setInterval(function () {
          var max = el.scrollWidth - el.clientWidth;
          var atEnd = Math.abs(el.scrollLeft) >= max - 4;
          var nextLeft = atEnd ? 0 : el.scrollLeft + step() * (isRTL ? -1 : 1);
          el.scrollTo({ left: nextLeft, behavior: "smooth" });
        }, 3000);
      }
      function stop() {
        if (!timer) return;
        clearInterval(timer);
        timer = null;
      }
      function stopForever() {
        autoStoppedByUser = true;
        stop();
      }

      if (prev) prev.addEventListener("click", function () { stopForever(); scrollByDir(-1); });
      if (next) next.addEventListener("click", function () { stopForever(); scrollByDir(1); });

      start();
      el.addEventListener("mouseenter", stop);
      el.addEventListener("mouseleave", start);
      el.addEventListener("touchstart", stop, { passive: true });
      el.addEventListener("touchend", start);
    });
  }

  function updateCartBadge() {
    fetch("/cart.js")
      .then(function (r) { return r.json(); })
      .then(function (cart) {
        var n = cart.item_count || 0;
        document.querySelectorAll(".cart-badge").forEach(function (b) {
          b.textContent = String(n);
          b.style.display = n > 0 ? "inline-flex" : "none";
        });
      })
      .catch(function () {});
  }

  onReady(function () {
    initMenu();
    initStoreCarousels();
    updateCartBadge();
    document.addEventListener("shopify:section:load", updateCartBadge);
  });
})();
