(function () {
  function onReady(fn) {
    if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", fn);
    else fn();
  }

  function scheduleIdle(fn) {
    if (typeof window.requestIdleCallback === "function") {
      window.requestIdleCallback(fn, { timeout: 2500 });
    } else {
      window.setTimeout(fn, 200);
    }
  }

  /** ניסיון הפעלה מפורש — חלק מהדפדפנים במובייל חוסמים autoplay עד ש־muted/playsinline מאומתים ב‑JS */
  function initBgHeroVideo() {
    var root = document.querySelector(".oda-global-bg-host");
    if (!root) return;
    root.querySelectorAll("video").forEach(function (v) {
      v.muted = true;
      v.defaultMuted = true;
      v.setAttribute("playsinline", "");
      v.setAttribute("webkit-playsinline", "");
      var p = v.play();
      if (p && typeof p.then === "function") p.catch(function () {});
    });
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

  function updateCartBadge(cartFromCaller) {
    function apply(cart) {
      var n = cart.item_count || 0;
      document.querySelectorAll(".cart-badge").forEach(function (b) {
        b.textContent = String(n);
        b.style.display = "inline-flex";
      });
      document.querySelectorAll(".js-oda-cart-nav-item").forEach(function (el) {
        el.removeAttribute("hidden");
      });
    }
    if (cartFromCaller != null && typeof cartFromCaller === "object" && "item_count" in cartFromCaller) {
      apply(cartFromCaller);
      return;
    }
    var cartJs = (window.odaRoutes && window.odaRoutes.cartJsUrl) || "/cart.js";
    fetch(cartJs)
      .then(function (r) { return r.json(); })
      .then(function (cart) {
        apply(cart);
      })
      .catch(function () {});
  }

  function cartUpdateJsFetch(payload) {
    var url = (window.odaRoutes && window.odaRoutes.cartUpdateUrl) || "/cart/update.js";
    return fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
      body: JSON.stringify(payload),
    }).then(function (r) {
      if (!r.ok) throw new Error("cart update failed");
      return r.json();
    });
  }

  function cartAddFetch(variantId, qty) {
    var url =
      (window.odaRoutes && window.odaRoutes.cartAddUrl) || "/cart/add.js";
    return fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
      body: JSON.stringify({ items: [{ id: variantId, quantity: qty || 1 }] }),
    }).then(function (r) {
      if (!r.ok) throw new Error("cart add failed");
      return r.json();
    });
  }

  /** Product forms with class oda-product-form: add via Ajax, stay on page */
  function initAjaxAddToCartForms() {
    document.addEventListener("submit", function (e) {
      var form = e.target && e.target.closest && e.target.closest("form.oda-product-form");
      if (!form) return;
      e.preventDefault();
      var idInput = form.querySelector('input[name="id"]');
      var vid = idInput ? parseInt(idInput.value, 10) : 0;
      if (!vid) return;
      cartAddFetch(vid, 1)
        .then(function () {
          updateCartBadge();
        })
        .catch(function () {});
    });
  }

  function cartJsFetch() {
    var url = (window.odaRoutes && window.odaRoutes.cartJsUrl) || "/cart.js";
    return fetch(url).then(function (r) {
      return r.json();
    });
  }

  function cartChangeFetch(payload) {
    var url = (window.odaRoutes && window.odaRoutes.cartChangeUrl) || "/cart/change.js";
    return fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
      body: JSON.stringify(payload),
    }).then(function (r) {
      if (!r.ok) throw new Error("cart change failed");
      return r.json();
    });
  }

  /** תצוגת סכומים בזמן אמת: תוספת אבן +50 ש״ח × כמות למסגרות */
  var ODA_STONE_UNIT_CENTS = 5000;
  var ODA_SHIP_GUSH_CENTS = 3000;
  var ODA_SHIP_FAR_CENTS = 4500;

  function odaShippingExtraCentsFromValue(v) {
    if (v === "gush_dan") return ODA_SHIP_GUSH_CENTS;
    if (v === "far") return ODA_SHIP_FAR_CENTS;
    return 0;
  }

  function formatIlsCents(cents) {
    var n = Number(cents);
    if (isNaN(n) || n < 0) n = 0;
    return (n / 100).toFixed(2) + ' ש"ח';
  }

  function initCartStonePricingPreview() {
    var form = document.getElementById("oda-cart-form");
    if (!form) return;

    function rowLineBaseCents(row) {
      var unit = parseInt(row.getAttribute("data-oda-unit-cents") || "0", 10);
      var qtyEl = row.querySelector("[data-oda-qty]");
      var qty = qtyEl ? parseInt(qtyEl.value, 10) : 0;
      if (isNaN(qty) || qty < 0) qty = 0;
      return unit * qty;
    }

    function rowDisplayCents(row) {
      var base = rowLineBaseCents(row);
      if (row.getAttribute("data-oda-kind") !== "frame") return base;
      var qtyEl = row.querySelector("[data-oda-qty]");
      var qty = qtyEl ? parseInt(qtyEl.value, 10) : 0;
      if (isNaN(qty) || qty < 0) qty = 0;
      var cb = row.querySelector(".oda-stone-cb");
      if (cb && cb.checked) return base + qty * ODA_STONE_UNIT_CENTS;
      return base;
    }

    function update() {
      var sum = 0;
      form.querySelectorAll("[data-oda-cart-row]").forEach(function (row) {
        var c = rowDisplayCents(row);
        sum += c;
        var pe = row.querySelector(".oda-cart-row__price");
        if (pe) pe.textContent = formatIlsCents(c);
      });
      var te = document.getElementById("oda-cart-total-display");
      if (te) te.textContent = formatIlsCents(sum);
      var shipEl = document.querySelector('input[name="oda_shipping_type"]:checked');
      var ship = odaShippingExtraCentsFromValue(shipEl ? shipEl.value : "");
      var ge = document.getElementById("oda-cart-grand-total-display");
      if (ge) ge.textContent = formatIlsCents(sum + ship);
    }

    function onDocChangeForTotals(e) {
      var t = e.target;
      if (!t) return;
      if (t.name === "oda_shipping_type" || t.name === "oda_preferred_payment") update();
    }

    form.addEventListener("change", function (e) {
      var t = e.target;
      if (!t) return;
      if (t.classList && t.classList.contains("oda-stone-cb")) update();
      if (t.hasAttribute && t.hasAttribute("data-oda-qty")) update();
    });
    form.addEventListener("input", function (e) {
      var t = e.target;
      if (t && t.hasAttribute && t.hasAttribute("data-oda-qty")) update();
    });
    document.addEventListener("change", onDocChangeForTotals);
    document.addEventListener("oda:cart-lines-updated", update);

    update();
  }

  function getOdaCartBootstrap() {
    var el = document.getElementById("oda-cart-bootstrap");
    if (!el) return { stoneAddonVariantId: 0 };
    try {
      return JSON.parse(el.textContent);
    } catch (e) {
      return { stoneAddonVariantId: 0 };
    }
  }

  function showOdaCartRemovedToast() {
    var id = "oda-cart-toast";
    var prev = document.getElementById(id);
    if (prev) prev.remove();
    var el = document.createElement("div");
    el.id = id;
    el.className = "oda-cart-toast";
    el.setAttribute("role", "status");
    el.setAttribute("aria-live", "polite");
    el.textContent = "המוצר הוסר בהצלחה";
    document.body.appendChild(el);
    window.requestAnimationFrame(function () {
      el.classList.add("oda-cart-toast--visible");
    });
    window.setTimeout(function () {
      el.classList.remove("oda-cart-toast--visible");
      window.setTimeout(function () {
        if (el.parentNode) el.parentNode.removeChild(el);
      }, 380);
    }, 3000);
  }

  function odaReplaceCartWithEmptyMessage() {
    var section = document.querySelector(".oda-cart-section");
    if (!section) return;
    var layout = section.querySelector(".oda-cart-layout");
    var container = section.querySelector(".container");
    if (!container) return;
    if (layout) layout.remove();
    if (container.querySelector(".oda-cart-empty-inline")) return;
    var productsUrl = section.getAttribute("data-oda-products-url") || "/collections/all";
    var p = document.createElement("p");
    p.className = "oda-cart-empty-inline";
    var a = document.createElement("a");
    a.href = productsUrl;
    a.textContent = "למוצרים";
    p.appendChild(document.createTextNode("הסל ריק — "));
    p.appendChild(a);
    container.appendChild(p);
  }

  function initOdaCartPage() {
    var form = document.getElementById("oda-cart-form");
    if (!form) return;

    var checkoutBtns = document.querySelectorAll(".oda-cart-section .js-oda-checkout");
    var boot = getOdaCartBootstrap();
    var stoneVid = Number(boot.stoneAddonVariantId) || 0;

    function validateFrames() {
      var ok = true;
      form.querySelectorAll('[data-oda-cart-row][data-oda-kind="frame"]').forEach(function (row) {
        var name = row.querySelector('[name="oda_frame_name"]');
        var date = row.querySelector('[name="oda_frame_date"]');
        if (!name || !date) return;
        if (!String(name.value || "").trim() || !String(date.value || "").trim()) {
          ok = false;
        }
      });
      if (!ok) window.alert("למסגרות יש למלא שם ותאריך לפני המשך.");
      return ok;
    }

    function buildPayloadForRow(row, cartItem) {
      var key = row.getAttribute("data-line-key");
      var kind = row.getAttribute("data-oda-kind");
      var qtyInput = row.querySelector("[data-oda-qty]");
      var qty = qtyInput ? parseInt(qtyInput.value, 10) : cartItem.quantity;
      if (isNaN(qty) || qty < 0) qty = cartItem.quantity;

      var payload = { id: key, quantity: qty };

      if (kind === "jewelry") {
        var lenEl = row.querySelector('[name="oda_length"]');
        var notesEl = row.querySelector('[name="oda_notes"]');
        payload.properties = {
          "אורך (ס״מ)": lenEl ? String(lenEl.value || "").trim() : "",
          "הערות מיוחדות": notesEl ? String(notesEl.value || "").trim() : "",
        };
      } else if (kind === "frame") {
        var nm = row.querySelector('[name="oda_frame_name"]');
        var dt = row.querySelector('[name="oda_frame_date"]');
        var stone = row.querySelector(".oda-stone-cb");
        payload.properties = {
          שם: nm ? String(nm.value || "").trim() : "",
          תאריך: dt ? String(dt.value || "").trim() : "",
          "תוספת אבן": stone && stone.checked ? "כן" : "לא",
        };
      }

      return payload;
    }

    function applyRowUpdates() {
      var rows = Array.prototype.slice.call(form.querySelectorAll("[data-oda-cart-row]"));
      return rows.reduce(function (seq, row) {
        return seq.then(function () {
          return cartJsFetch().then(function (cart) {
            var key = row.getAttribute("data-line-key");
            var item = cart.items.find(function (it) {
              return it.key === key;
            });
            if (!item) return cart;
            var payload = buildPayloadForRow(row, item);
            return cartChangeFetch(payload);
          });
        });
      }, Promise.resolve());
    }

    function stripAllStoneAddonLines() {
      if (!stoneVid) return Promise.resolve();
      return cartJsFetch().then(function stripOnce(cart) {
        var stoneLine = cart.items.find(function (line) {
          return (
            Number(line.variant_id) === stoneVid &&
            line.properties &&
            line.properties["_oda_parent_key"]
          );
        });
        if (!stoneLine) return Promise.resolve();
        return cartChangeFetch({ id: stoneLine.key, quantity: 0 }).then(function () {
          return cartJsFetch().then(stripOnce);
        });
      });
    }

    function refreshDomLineKeys() {
      return cartJsFetch().then(function (cart) {
        var rows = Array.prototype.slice.call(form.querySelectorAll("[data-oda-cart-row]"));
        var used = {};
        rows.forEach(function (row) {
          var vid = Number(row.getAttribute("data-variant-id"));
          var pid = Number(row.getAttribute("data-product-id"));
          var match = cart.items.find(function (it) {
            if (used[it.key]) return false;
            if (
              stoneVid &&
              Number(it.variant_id) === stoneVid &&
              it.properties &&
              it.properties["_oda_parent_key"]
            )
              return false;
            return Number(it.variant_id) === vid && Number(it.product_id) === pid;
          });
          if (!match) {
            var wrap = row.closest(".oda-cart-row");
            if (wrap) wrap.remove();
            return;
          }
          used[match.key] = true;
          row.setAttribute("data-line-key", match.key);
        });
      });
    }

    function desiredStoneAddons() {
      var desired = {};
      form.querySelectorAll('[data-oda-cart-row][data-oda-kind="frame"]').forEach(function (row) {
        var rowKey = row.getAttribute("data-line-key");
        var qtyInput = row.querySelector("[data-oda-qty]");
        var q = qtyInput ? parseInt(qtyInput.value, 10) : 0;
        if (isNaN(q) || q < 0) q = 0;
        var cb = row.querySelector(".oda-stone-cb");
        var wantStone = cb && cb.checked;
        desired[rowKey] = wantStone ? q : 0;
      });
      return desired;
    }

    function addStoneLinesFromDesired(desired) {
      if (!stoneVid) return Promise.resolve();
      var addUrl = (window.odaRoutes && window.odaRoutes.cartAddUrl) || "/cart/add.js";
      var keys = Object.keys(desired).filter(function (k) {
        return desired[k] > 0;
      });
      return keys.reduce(function (seq, pk) {
        return seq.then(function () {
          var wq = desired[pk];
          return fetch(addUrl, {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              Accept: "application/json",
            },
            body: JSON.stringify({
              items: [
                {
                  id: stoneVid,
                  quantity: wq,
                  properties: { _oda_parent_key: pk },
                },
              ],
            }),
          }).then(function (r) {
            if (!r.ok) throw new Error("add stone failed");
            return r.json();
          });
        });
      }, Promise.resolve());
    }

    function saveBuyerAndPrefsToCart() {
      return cartJsFetch().then(function (cart) {
        var attrs = {};
        if (cart.attributes && typeof cart.attributes === "object") {
          Object.keys(cart.attributes).forEach(function (k) {
            attrs[k] = cart.attributes[k];
          });
        }
        var nameEl = document.getElementById("oda-buyer-name");
        var phoneEl = document.getElementById("oda-buyer-phone");
        var emailEl = document.getElementById("oda-buyer-email");
        var addrEl = document.getElementById("oda-buyer-address");
        var payEl = document.querySelector('input[name="oda_preferred_payment"]:checked');
        var shipEl = document.querySelector('input[name="oda_shipping_type"]:checked');
        attrs.buyer_name = nameEl ? String(nameEl.value || "").trim() : "";
        attrs.buyer_phone = phoneEl ? String(phoneEl.value || "").trim() : "";
        attrs.buyer_email = emailEl ? String(emailEl.value || "").trim() : "";
        attrs.buyer_shipping_address = addrEl ? String(addrEl.value || "").trim() : "";
        attrs.preferred_payment = payEl ? String(payEl.value) : "paypal";
        attrs.shipping_type = shipEl ? String(shipEl.value) : "pickup";
        var feeCents = odaShippingExtraCentsFromValue(attrs.shipping_type);
        attrs.shipping_fee_cents = String(feeCents);
        var lines = [];
        if (attrs.buyer_name) lines.push("שם: " + attrs.buyer_name);
        if (attrs.buyer_phone) lines.push("טלפון: " + attrs.buyer_phone);
        if (attrs.buyer_email) lines.push("אימייל: " + attrs.buyer_email);
        if (attrs.buyer_shipping_address) lines.push("כתובת למשלוח: " + attrs.buyer_shipping_address);
        if (attrs.shipping_type === "pickup") lines.push("משלוח: הגעה עצמית");
        else if (attrs.shipping_type === "gush_dan") lines.push("משלוח: גוש דן והסביבה (30 ש״ח)");
        else if (attrs.shipping_type === "far") lines.push("משלוח: מעבר לגוש דן (45 ש״ח)");
        lines.push("תשלום מועדף בקופה: " + (attrs.preferred_payment === "bit" ? "ביט" : "PayPal / כרטיס"));
        return cartUpdateJsFetch({ attributes: attrs, note: lines.join(" | ") });
      });
    }

    function setCheckoutDisabled(disabled) {
      checkoutBtns.forEach(function (b) {
        b.disabled = disabled;
      });
    }

    function runSaveToCheckout() {
      if (!validateFrames()) return;
      setCheckoutDisabled(true);

      applyRowUpdates()
        .then(function () {
          return refreshDomLineKeys();
        })
        .then(function () {
          return stripAllStoneAddonLines();
        })
        .then(function () {
          return addStoneLinesFromDesired(desiredStoneAddons());
        })
        .then(function () {
          return saveBuyerAndPrefsToCart();
        })
        .then(function () {
          updateCartBadge();
          window.location.assign(
            (window.odaRoutes && window.odaRoutes.checkoutUrl) || "/checkout"
          );
        })
        .catch(function () {
          window.alert("לא ניתן לעדכן את הסל. נסו שוב.");
        })
        .then(function () {
          setCheckoutDisabled(false);
        });
    }

    form.querySelectorAll(".oda-cart-remove").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var key = btn.getAttribute("data-line-key");
        if (!key || btn.disabled) return;
        btn.disabled = true;
        cartJsFetch()
          .then(function (cart) {
            if (!stoneVid) {
              return cartChangeFetch({ id: key, quantity: 0 });
            }
            var addon = cart.items.find(function (line) {
              return (
                Number(line.variant_id) === stoneVid &&
                line.properties &&
                line.properties["_oda_parent_key"] === key
              );
            });
            if (addon) {
              return cartChangeFetch({ id: addon.key, quantity: 0 }).then(function () {
                return cartChangeFetch({ id: key, quantity: 0 });
              });
            }
            return cartChangeFetch({ id: key, quantity: 0 });
          })
          .then(function () {
            showOdaCartRemovedToast();
            return cartJsFetch();
          })
          .then(function (cart) {
            var keys = {};
            (cart.items || []).forEach(function (it) {
              keys[it.key] = true;
            });
            form.querySelectorAll("[data-oda-cart-row]").forEach(function (row) {
              var rk = row.getAttribute("data-line-key");
              if (!rk || !keys[rk]) row.remove();
            });
            updateCartBadge(cart);
            document.dispatchEvent(new CustomEvent("oda:cart-lines-updated"));
            if (!cart.item_count) {
              odaReplaceCartWithEmptyMessage();
            }
            btn.disabled = false;
          })
          .catch(function () {
            btn.disabled = false;
            window.alert("לא ניתן להסיר את הפריט. נסו שוב.");
          });
      });
    });

    checkoutBtns.forEach(function (btn) {
      btn.addEventListener("click", function () {
        runSaveToCheckout();
      });
    });
  }

  onReady(function () {
    initBgHeroVideo();
    initMenu();
    initStoreCarousels();
    initAjaxAddToCartForms();
    initOdaCartPage();
    initCartStonePricingPreview();
    scheduleIdle(updateCartBadge);
    document.addEventListener("shopify:section:load", updateCartBadge);
  });
})();
