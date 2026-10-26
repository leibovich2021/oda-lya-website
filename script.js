// קוד JavaScript לתפריט המובייל
document.addEventListener('DOMContentLoaded', function() {
    // בחירת אלמנטים
    const menuToggle = document.querySelector('.menu-toggle');
    const menu = document.querySelector('.menu');
    
    if (menuToggle && menu) {
        // הוספת אירוע לחיצה על כפתור התפריט
        menuToggle.addEventListener('click', function() {
            menu.classList.toggle('active');
            
            // שינוי אייקון לפי מצב
            if (menu.classList.contains('active')) {
                menuToggle.innerHTML = '&#10005;'; // אייקון X
            } else {
                menuToggle.innerHTML = '&#9776;'; // אייקון תפריט (המבורגר)
            }
        });
        
        // סגירת תפריט בלחיצה על קישור
        const menuLinks = menu.querySelectorAll('a');
        menuLinks.forEach(link => {
            link.addEventListener('click', function() {
                menu.classList.remove('active');
                menuToggle.innerHTML = '&#9776;';
                
                // גלילה חלקה לעוגן
                const targetId = this.getAttribute('href');
                if (targetId.startsWith('#') && targetId.length > 1) {
                    const targetElement = document.querySelector(targetId);
                    if (targetElement) {
                        event.preventDefault();
                        window.scrollTo({
                            top: targetElement.offsetTop - 70,
                            behavior: 'smooth'
                        });
                    }
                }
            });
        });
        
        // סגירת תפריט בלחיצה מחוץ לתפריט
        document.addEventListener('click', function(event) {
            if (!event.target.closest('.menu-toggle') && !event.target.closest('.menu')) {
                if (menu.classList.contains('active')) {
                    menu.classList.remove('active');
                    menuToggle.innerHTML = '&#9776;';
                }
            }
        });
    }
    
    // טיפול בטופס פענוח שמות
    const nameForm = document.querySelector('.name-form .btn');
    if (nameForm) {
        nameForm.addEventListener('click', function() {
            const nameInput = document.getElementById('name');
            const nameResult = document.querySelector('.name-result');
            
            if (nameInput && nameInput.value && nameResult) {
                const name = nameInput.value.trim();
                nameResult.innerHTML = `
                    <h3>פענוח השם: ${name}</h3>
                    <p>השם ${name} מסמל אנרגיה של חכמה ותבונה. אנשים עם שם זה נוטים להיות בעלי אינטואיציה חזקה ויכולת הבנה עמוקה. זהו שם המעניק כוח ריפוי ויכולת לעזור לאחרים.</p>
                `;
            }
        });
    }
    
    // טיפול בטופס יצירת קשר
    const contactForm = document.querySelector('.contact-form .btn');
    if (contactForm) {
        contactForm.addEventListener('click', function() {
            const fullName = document.getElementById('full-name');
            const email = document.getElementById('email');
            const message = document.getElementById('message');
            
            if (fullName && email && message && 
                fullName.value && email.value && message.value) {
                alert('ההודעה נשלחה בהצלחה! נחזור אליך בהקדם.');
                fullName.value = '';
                email.value = '';
                message.value = '';
            } else {
                alert('אנא מלא את כל השדות הנדרשים');
            }
        });
    }
    
    // הוספת מחלקת "active" לקישור התפריט הנוכחי
    // קבלת הנתיב הנוכחי
    const currentPath = window.location.pathname;
    
    // מציאת כל הקישורים בתפריט
    const allMenuLinks = document.querySelectorAll('.menu a');
    
    // בדיקה עבור כל קישור אם הוא מתאים לעמוד הנוכחי
    allMenuLinks.forEach(link => {
        const linkPath = link.getAttribute('href');
        
        // בדיקה אם הקישור מתאים לדף הנוכחי
        if ((currentPath.endsWith(linkPath) && !linkPath.startsWith('#')) || 
            (currentPath === '/' && linkPath === 'index.html') ||
            (currentPath.endsWith('/') && linkPath === 'index.html')) {
            link.classList.add('active');
        }
    });
    
    // הודעה קופצת אחרי 1 שנייה
    setTimeout(function() {
        showPopup();
    }, 1000);
    
    // בדיקה שהקוד עובד
    console.log('הקוד נטען בהצלחה');
    
    // בדיקה נוספת - הודעה מיידית
    console.log('כל הפונקציות זמינות');
    
    // גלריית תמונות זזה
    initGallery();

    // סל קניות
    initCart();
    initSaleBar();
    initCollectionSplash();
 });

// -----------------------------
// סל קניות (מזומן / ביט)
// -----------------------------
const CART_STORAGE_KEY = 'oda_cart_v1';
const CUSTOM_PRICE_NOTE = 'מחיר בהתאמה אישית';
const CART_CURRENCY = 'ILS';
const BIT_PHONE = '0533397827';
const ORDER_CONTACT_WA = '972533397827';
const ORDER_FORM_STORAGE_KEY = 'oda_order_form_v1';
const SALE_PERCENT = 10;
const SALE_STARTS_AT = Date.parse('2026-10-01T00:00:00+03:00');
const SALE_ENDS_AT = Date.parse('2026-11-01T00:00:00+03:00');
const SALE_NAME = 'אוקטובר ורוד';
const SPLASH_STORAGE_KEY = 'oda_pink_october_splash_2026';
let cartPageBound = false;

function isSaleActive() {
    const now = Date.now();
    return Number.isFinite(SALE_STARTS_AT) && Number.isFinite(SALE_ENDS_AT)
        && now >= SALE_STARTS_AT && now < SALE_ENDS_AT;
}

function saleBarHtml() {
    return `${SALE_NAME} — <strong>${SALE_PERCENT}% הנחה</strong> על כל הזמנה בחודש אוקטובר`;
}

function saleNoteText() {
    return `${SALE_NAME} — ${SALE_PERCENT}% הנחה על כל הזמנה בחודש אוקטובר.`;
}

function saleDiscountLabel() {
    return `הנחת מבצע ${SALE_PERCENT}%`;
}

function jerusalemDateKey(date) {
    return new Intl.DateTimeFormat('en-CA', {
        timeZone: 'Asia/Jerusalem',
        year: 'numeric',
        month: '2-digit',
        day: '2-digit'
    }).format(date || new Date());
}

function calcCartSubtotal(items) {
    return items.reduce((sum, it) => sum + (Number(it.price) || 0) * (Number(it.qty) || 0), 0);
}

function calcCartDiscount(subtotal) {
    if (!isSaleActive()) return 0;
    return Math.round((Number(subtotal) || 0) * SALE_PERCENT / 100);
}

function calcCartTotals(items) {
    const subtotal = calcCartSubtotal(items);
    const discount = calcCartDiscount(subtotal);
    return { subtotal, discount, total: Math.max(0, subtotal - discount) };
}

function readCart() {
    try {
        const raw = localStorage.getItem(CART_STORAGE_KEY);
        const parsed = raw ? JSON.parse(raw) : [];
        const items = Array.isArray(parsed) ? parsed : [];
        return items.map((it) => {
            const sku = String(it.sku || '');
            if (sku === 'FRAME-DECODE-01') {
                return { ...it, name: 'פענוח שם (ללא קריסטל)', price: 199 };
            }
            if (sku === 'FRAME-DECODE-02') {
                return { ...it, name: 'פענוח שם עם קריסטל', price: 319 };
            }
            if (sku === 'FRAME-DECODE-03') {
                return { ...it, name: 'פענוח שם זוגי (ללא קריסטל)', price: 379 };
            }
            if (sku === 'FRAME-DECODE-04') {
                return { ...it, name: 'זוגי עם קריסטל', price: 549 };
            }
            const isCustom = sku.startsWith('CRYSTAL-') || sku.startsWith('KIT-');
            if (!isCustom) return it;
            if (Number(it.price) === 25 || Number(it.price) === 79) {
                return { ...it, price: 0, priceNote: CUSTOM_PRICE_NOTE };
            }
            if (!(Number(it.price) > 0)) {
                return { ...it, priceNote: CUSTOM_PRICE_NOTE };
            }
            return it;
        });
    } catch {
        return [];
    }
}

function writeCart(items) {
    localStorage.setItem(CART_STORAGE_KEY, JSON.stringify(items));
}

function cartCount(items) {
    return items.reduce((sum, it) => sum + (Number(it.qty) || 0), 0);
}

function formatILS(amount) {
    const n = Number(amount) || 0;
    return `₪${n.toFixed(0)}`;
}

function cartItemPriceNote(it) {
    const sku = String(it.sku || '');
    if ((sku.startsWith('CRYSTAL-') || sku.startsWith('KIT-')) && !(Number(it.price) > 0)) {
        return CUSTOM_PRICE_NOTE;
    }
    if (it.priceNote) return String(it.priceNote);
    return '';
}

const ORDER_SITE_ORIGIN = 'https://oda-lya.co.il';

function absoluteProductImageUrl(image) {
    const raw = String(image ?? '').trim();
    if (!raw || /[\u0000-\u001F\u007F]/.test(raw)) return '';
    // Relative product paths are resolved on the shop. Reject non-http schemes.
    if (/^[a-z][a-z0-9+.-]*:/i.test(raw) && !/^https?:/i.test(raw)) return '';

    let url;
    try {
        url = new URL(raw, ORDER_SITE_ORIGIN + '/');
    } catch {
        return '';
    }

    if (url.protocol !== 'http:' && url.protocol !== 'https:') return '';
    if (url.username || url.password) return '';

    const isAbsolute = /^https?:\/\//i.test(raw) || raw.startsWith('//');
    if (!isAbsolute && url.origin !== ORDER_SITE_ORIGIN) return '';

    const host = url.hostname.toLowerCase();
    if (host === 'oda-lya.co.il' || host === 'www.oda-lya.co.il') {
        url.protocol = 'https:';
        url.hostname = 'oda-lya.co.il';
    }

    if (!url.pathname || url.pathname === '/') return '';

    // Apostrophes break some chat link detectors (Tiger's-Eye.png).
    return url.href.replace(/'/g, '%27');
}

function formatOrderForMessage(items) {
    const blocks = items.map((it) => {
        const qty = Number(it.qty) || 1;
        const price = Number(it.price) || 0;
        const quote = cartItemPriceNote(it);
        const note = (it.note || '').trim();
        const pricePart = quote || formatILS(price);
        const sku = String(it.sku || '').replace(/[\u0000-\u001F\u007F]/g, '').trim();
        const imageUrl = absoluteProductImageUrl(it.image);
        const lines = [`- ${it.name} ×${qty} (${pricePart})`];
        if (sku) lines.push(`  מק״ט: ${sku}`);
        if (note) lines.push(`  בקשה: ${note}`);
        if (imageUrl) lines.push(`  תמונה: ${imageUrl}`);
        return lines.join('\n');
    });
    return blocks.join('\n\n');
}

function readOrderForm() {
    try {
        const raw = localStorage.getItem(ORDER_FORM_STORAGE_KEY);
        const parsed = raw ? JSON.parse(raw) : null;
        return parsed && typeof parsed === 'object' ? parsed : {};
    } catch {
        return {};
    }
}

function writeOrderForm(data) {
    localStorage.setItem(ORDER_FORM_STORAGE_KEY, JSON.stringify(data));
}

let toastTimer = null;
function showToast(message) {
    const el = document.getElementById('toast');
    if (!el) return;
    el.textContent = message;
    el.hidden = false;
    el.classList.add('toast--show');

    if (toastTimer) clearTimeout(toastTimer);
    toastTimer = setTimeout(() => {
        el.classList.remove('toast--show');
        setTimeout(() => { el.hidden = true; }, 180);
    }, 3000);
}

function openOrderWhatsApp(items, customer) {
    const { subtotal, discount, total } = calcCartTotals(items);
    const orderLines = formatOrderForMessage(items);
    const totalLines = discount > 0
        ? [
            `לפני הנחה: ${formatILS(subtotal)}`,
            `הנחת מבצע ${SALE_PERCENT}%: −${formatILS(discount)}`,
            `לתשלום: ${formatILS(total)}`
        ]
        : [`סה״כ: ${formatILS(total)}`];
    const text = [
        'התקבלה הזמנה חדשה מהאתר:',
        '',
        `שם: ${customer.name || ''}`,
        `טלפון: ${customer.phone || ''}`,
        `כתובת: ${customer.address || ''}`,
        `עיר: ${customer.city || ''}`,
        customer.email ? `אימייל: ${customer.email}` : '',
        customer.note ? `הערה כללית: ${customer.note}` : '',
        customer.pay === 'bit' ? `תשלום: ביט לטלפון ${BIT_PHONE}` : 'תשלום: מזומן',
        '',
        'פריטים:',
        orderLines || '- (אין פריטים)',
        '',
        ...totalLines
    ].filter(Boolean).join('\n');

    const wa = `https://wa.me/${ORDER_CONTACT_WA}?text=${encodeURIComponent(text)}`;
    window.open(wa, '_blank', 'noopener,noreferrer');
}

function upsertCartItem(nextItem) {
    const items = readCart();
    const idx = items.findIndex(it => String(it.sku) === String(nextItem.sku));
    if (idx >= 0) {
        items[idx].qty = (Number(items[idx].qty) || 0) + (Number(nextItem.qty) || 1);
    } else {
        items.push({ ...nextItem, qty: Number(nextItem.qty) || 1 });
    }
    writeCart(items);
    updateCartBadge();
}

function setCartQty(sku, qty) {
    const nextQty = Math.max(1, Number(qty) || 1);
    const items = readCart().map(it => String(it.sku) === String(sku) ? { ...it, qty: nextQty } : it);
    writeCart(items);
    updateCartBadge();
}

function changeCartQty(sku, delta) {
    const items = readCart();
    const current = items.find(it => String(it.sku) === String(sku));
    if (!current) return;
    const next = (Number(current.qty) || 1) + delta;
    if (next < 1) {
        removeCartItem(sku);
        return;
    }
    setCartQty(sku, next);
}

function setCartNote(sku, note) {
    const safeNote = String(note || '').slice(0, 280);
    const items = readCart().map(it => String(it.sku) === String(sku) ? { ...it, note: safeNote } : it);
    writeCart(items);
}

function removeCartItem(sku) {
    const items = readCart().filter(it => String(it.sku) !== String(sku));
    writeCart(items);
    updateCartBadge();
}

function clearCart() {
    writeCart([]);
    updateCartBadge();
}

function calcCartTotal(items) {
    return calcCartTotals(items).total;
}

function initSaleBar() {
    if (!isSaleActive() || document.querySelector('.sale-bar')) return;
    const bar = document.createElement('div');
    bar.className = 'sale-bar';
    bar.setAttribute('role', 'region');
    bar.setAttribute('aria-label', 'מבצע');
    bar.innerHTML = `<p>${saleBarHtml()}</p>`;
    const header = document.querySelector('body > header');
    const announcement = document.querySelector('.announcement-bar');
    if (announcement) {
        announcement.insertAdjacentElement('beforebegin', bar);
    } else if (header) {
        header.insertAdjacentElement('beforebegin', bar);
    } else {
        document.body.prepend(bar);
    }
}

function updateCartBadge() {
    const items = readCart();
    const badgeEls = document.querySelectorAll('.cart-badge');
    const count = cartCount(items);
    badgeEls.forEach(el => {
        el.textContent = String(count);
        el.style.display = count > 0 ? 'inline-flex' : 'none';
    });
}

function bindStoreAddToCart() {
    document.addEventListener('click', (e) => {
        if (!e.target.closest('.jewelry-store')) return;
        const itemEl = e.target.closest('.jewelry-store__item');
        if (!itemEl) return;

        const addBtn = e.target.closest('.jewelry-store__add');
        const buyLink = e.target.closest('.jewelry-store__details');
        if (!addBtn && !buyLink) return;

        const sku = itemEl.getAttribute('data-sku') || '';
        const name = itemEl.getAttribute('data-name') || '';
        const price = Number(itemEl.getAttribute('data-price') || 0);
        const priceNote = itemEl.getAttribute('data-price-note') || '';
        const currency = itemEl.getAttribute('data-currency') || CART_CURRENCY;
        const image = itemEl.getAttribute('data-image') || '';

        if (!sku || !name) return;
        if (!price && !priceNote) return;

        upsertCartItem({ sku, name, price, priceNote, currency, image, qty: 1 });

        if (addBtn) {
            addBtn.textContent = 'נוסף';
            setTimeout(() => { addBtn.textContent = 'הוספה לסל'; }, 900);
            return;
        }

        if (buyLink) {
            e.preventDefault();
            window.location.href = 'cart.html';
        }
    });
}

function escapeHtml(value) {
    return String(value ?? '')
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;');
}

function refreshCartPage() {
    updateCartBadge();
    renderCartItems();
}

function renderCartItems() {
    const itemsWrap = document.getElementById('cart-items');
    if (!itemsWrap) return;

    const emptyEl = document.getElementById('cart-empty');
    const totalEl = document.getElementById('cart-total');
    const countEl = document.getElementById('cart-count');
    const submitEl = document.getElementById('order-submit');
    const subtotalRow = document.getElementById('cart-subtotal-row');
    const discountRow = document.getElementById('cart-discount-row');
    const saleNote = document.getElementById('cart-sale-note');
    const subtotalEl = document.getElementById('cart-subtotal');
    const discountEl = document.getElementById('cart-discount');
    const items = readCart();
    const isEmpty = items.length === 0;
    const { subtotal, discount, total } = calcCartTotals(items);
    const showSale = !isEmpty && discount > 0;

    if (emptyEl) emptyEl.hidden = !isEmpty;
    itemsWrap.hidden = isEmpty;
    itemsWrap.innerHTML = '';

    if (totalEl) totalEl.textContent = formatILS(total);
    if (countEl) countEl.textContent = String(cartCount(items));
    if (subtotalEl) subtotalEl.textContent = formatILS(subtotal);
    if (discountEl) discountEl.innerHTML = `<span class="cart-minus">−</span>${escapeHtml(formatILS(discount))}`;
    if (subtotalRow) subtotalRow.hidden = !showSale;
    if (discountRow) discountRow.hidden = !showSale;
    if (saleNote) {
        saleNote.hidden = !showSale;
        if (showSale) saleNote.textContent = saleNoteText();
    }
    const discountLabel = document.getElementById('cart-discount-label');
    if (discountLabel && showSale) discountLabel.textContent = saleDiscountLabel();
    if (submitEl) {
        submitEl.classList.toggle('is-disabled', isEmpty);
        submitEl.setAttribute('aria-disabled', isEmpty ? 'true' : 'false');
    }

    document.querySelectorAll('[data-cart-needs-items]').forEach((el) => {
        el.hidden = isEmpty;
    });

    items.forEach((it) => {
        const sku = escapeHtml(it.sku);
        const row = document.createElement('article');
        row.className = 'cart-item';
        row.innerHTML = `
            <button type="button" class="cart-item__media" ${it.image ? '' : 'hidden'} aria-label="הגדלת תמונה של ${escapeHtml(it.name)}">
                ${it.image ? `<img src="${escapeHtml(it.image)}" alt="${escapeHtml(it.name)}" loading="lazy" decoding="async" width="96" height="96">` : ''}
            </button>
            <div class="cart-item__info">
                <h3 class="cart-item__name">${escapeHtml(it.name)}</h3>
                <p class="cart-item__price">${cartItemPriceNote(it) ? escapeHtml(cartItemPriceNote(it)) : `${formatILS(it.price)} ליחידה`}</p>
                <label class="cart-item__note">
                    <span class="cart-item__note-label">בקשה מיוחדת</span>
                    <input class="cart-note" type="text" placeholder="צבע, מידה או הקדשה" value="${escapeHtml(it.note || '')}" data-sku="${sku}">
                </label>
            </div>
            <div class="cart-item__qty" data-sku="${sku}">
                <button class="cart-item__step" type="button" data-cart-minus data-sku="${sku}" aria-label="הפחתת כמות">−</button>
                <input class="cart-qty" type="number" min="1" value="${Number(it.qty) || 1}" data-sku="${sku}" aria-label="כמות">
                <button class="cart-item__step" type="button" data-cart-plus data-sku="${sku}" aria-label="הוספת כמות">+</button>
            </div>
            <div class="cart-item__sum">${cartItemPriceNote(it) ? '—' : formatILS((Number(it.price) || 0) * (Number(it.qty) || 0))}</div>
            <button class="cart-item__remove" type="button" data-cart-remove data-sku="${sku}" aria-label="הסרת ${escapeHtml(it.name)}">הסרה</button>
        `;
        itemsWrap.appendChild(row);
    });
}

function bindCartPageOnce() {
    const itemsWrap = document.getElementById('cart-items');
    if (!itemsWrap || cartPageBound) return;
    cartPageBound = true;

    itemsWrap.addEventListener('click', (e) => {
        const removeBtn = e.target.closest('[data-cart-remove]');
        if (removeBtn) {
            e.preventDefault();
            removeCartItem(removeBtn.getAttribute('data-sku'));
            refreshCartPage();
            showToast('הפריט הוסר מהסל');
            return;
        }
        const minus = e.target.closest('[data-cart-minus]');
        if (minus) {
            changeCartQty(minus.getAttribute('data-sku'), -1);
            refreshCartPage();
            return;
        }
        const plus = e.target.closest('[data-cart-plus]');
        if (plus) {
            changeCartQty(plus.getAttribute('data-sku'), 1);
            refreshCartPage();
        }
    });

    itemsWrap.addEventListener('change', (e) => {
        const qty = e.target.closest('.cart-qty');
        if (!qty) return;
        setCartQty(qty.getAttribute('data-sku'), qty.value);
        refreshCartPage();
    });

    itemsWrap.addEventListener('input', (e) => {
        const note = e.target.closest('.cart-note');
        if (!note) return;
        setCartNote(note.getAttribute('data-sku'), note.value);
    });

    const clearBtn = document.getElementById('cart-clear');
    if (clearBtn) {
        clearBtn.addEventListener('click', () => {
            if (!readCart().length) return;
            clearCart();
            refreshCartPage();
            showToast('הסל נוקה');
        });
    }

    const orderForm = document.getElementById('order-form');
    if (!orderForm) return;

    const nameEl = document.getElementById('order-name');
    const phoneEl = document.getElementById('order-phone');
    const addressEl = document.getElementById('order-address');
    const cityEl = document.getElementById('order-city');
    const emailEl = document.getElementById('order-email');
    const noteEl = document.getElementById('order-note');
    const saved = readOrderForm();

    if (nameEl && saved.name) nameEl.value = saved.name;
    if (phoneEl && saved.phone) phoneEl.value = saved.phone;
    if (addressEl && saved.address) addressEl.value = saved.address;
    if (cityEl && saved.city) cityEl.value = saved.city;
    if (emailEl && saved.email) emailEl.value = saved.email;
    if (noteEl && saved.note) noteEl.value = saved.note;
    const paySaved = document.querySelector(`input[name="pay"][value="${saved.pay === 'bit' ? 'bit' : 'cash'}"]`);
    if (paySaved) paySaved.checked = true;

    orderForm.addEventListener('input', () => {
        writeOrderForm({
            name: nameEl?.value || '',
            phone: phoneEl?.value || '',
            address: addressEl?.value || '',
            city: cityEl?.value || '',
            email: emailEl?.value || '',
            note: noteEl?.value || '',
            pay: document.querySelector('input[name="pay"]:checked')?.value || 'cash'
        });
    });

    orderForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const items = readCart();
        if (!items.length) {
            alert('הסל ריק — צריך להוסיף מוצרים לפני שליחת הזמנה.');
            return;
        }
        const customer = {
            name: nameEl?.value?.trim() || '',
            phone: phoneEl?.value?.trim() || '',
            address: addressEl?.value?.trim() || '',
            city: cityEl?.value?.trim() || '',
            email: emailEl?.value?.trim() || '',
            note: noteEl?.value?.trim() || '',
            pay: document.querySelector('input[name="pay"]:checked')?.value || 'cash'
        };
        if (!customer.name || !customer.phone || !customer.address || !customer.city || !customer.email) {
            alert('נא למלא שם, טלפון, כתובת, עיר ואימייל.');
            return;
        }
        const agreeEl = document.getElementById('order-agree');
        if (!agreeEl?.checked) {
            agreeEl?.focus();
            alert('צריך לאשר את תקנון האתר ואת מדיניות ביטול העסקה לפני השליחה.');
            return;
        }
        openOrderWhatsApp(items, customer);
    });
}

function renderCartPage() {
    bindCartPageOnce();
    refreshCartPage();
}

function initCart() {
    updateCartBadge();
    bindStoreAddToCart();
    renderCartPage();
    initStoreCarousels();
}

function initStoreCarousels() {
    const prefersReduced = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    const carousels = document.querySelectorAll('.js-store-carousel');
    if (!carousels.length) return;
    const isRTL = (document.documentElement.getAttribute('dir') || '').toLowerCase() === 'rtl';

    carousels.forEach((el) => {
        const root = el.closest('.jewelry-store__carousel');
        const prev = root ? root.querySelector('.jewelry-store__nav--prev') : null;
        const next = root ? root.querySelector('.jewelry-store__nav--next') : null;
        let autoStoppedByUser = false;

        const step = () => {
            const first = el.querySelector('.jewelry-store__item');
            const stepPx = first ? first.getBoundingClientRect().width + 16 : 260;
            return stepPx;
        };

        const scrollByDir = (dir) => {
            const delta = dir * step() * (isRTL ? -1 : 1);
            el.scrollBy({ left: delta, behavior: 'smooth' });
        };

        let timer = null;
        const start = () => {
            if (prefersReduced || autoStoppedByUser) return;
            if (timer) return;
            timer = setInterval(() => {
                const max = el.scrollWidth - el.clientWidth;
                const atEnd = Math.abs(el.scrollLeft) >= max - 4;
                const nextLeft = atEnd ? 0 : (el.scrollLeft + (step() * (isRTL ? -1 : 1)));
                el.scrollTo({ left: nextLeft, behavior: 'smooth' });
            }, 3000);
        };
        const stop = () => {
            if (!timer) return;
            clearInterval(timer);
            timer = null;
        };

        const stopForever = () => {
            autoStoppedByUser = true;
            stop();
        };

        if (prev) prev.addEventListener('click', () => { stopForever(); scrollByDir(-1); });
        if (next) next.addEventListener('click', () => { stopForever(); scrollByDir(1); });

        start();
        el.addEventListener('mouseenter', stop);
        el.addEventListener('mouseleave', start);
        el.addEventListener('focusin', stop);
        el.addEventListener('focusout', start);
        el.addEventListener('touchstart', stop, { passive: true });
        el.addEventListener('touchend', start);
    });
}
 
// פונקציה לאתחול הגלריה
function initGallery() {
    const galleryTrack = document.querySelector('.gallery-track');
    const slides = document.querySelectorAll('.gallery-slide');
    const prevBtn = document.querySelector('.gallery-btn-prev');
    const nextBtn = document.querySelector('.gallery-btn-next');
    const indicators = document.querySelectorAll('.indicator');
    
    if (!galleryTrack || !slides.length) {
        console.log('גלריה לא נמצאה');
        return;
    }
    
    // טעינת תמונות מראש ובדיקה שהן נטענו
    let imagesLoaded = 0;
    const totalImages = slides.length;
    
    slides.forEach((slide, index) => {
        const img = slide.querySelector('.gallery-image');
        if (img) {
            // בדיקה אם התמונה כבר נטענה
            if (img.complete && img.naturalHeight !== 0) {
                imagesLoaded++;
                console.log('תמונה כבר נטענה:', img.src);
            } else {
                img.onerror = function() {
                    console.error('תמונה לא נטענה:', img.src);
                    console.error('נסה לבדוק את הנתיב:', img.getAttribute('src'));
                };
                img.onload = function() {
                    imagesLoaded++;
                    console.log('תמונה נטענה:', img.src, '(' + imagesLoaded + '/' + totalImages + ')');
                };
            }
        }
    });
    
    let currentSlide = 0;
    const totalSlides = slides.length;
    
    console.log('מספר תמונות בגלריה:', totalSlides);
    
    // וידוא שהתמונות נטענו לפני תחילת הגלריה
    function checkImagesAndInit() {
        if (imagesLoaded === totalImages) {
            console.log('כל התמונות נטענו בהצלחה!');
            updateGallery();
        } else {
            console.log('ממתין לטעינת תמונות...', imagesLoaded + '/' + totalImages);
            setTimeout(checkImagesAndInit, 100);
        }
    }
    
    // פונקציה לעדכון הגלריה
    function updateGallery() {
        if (currentSlide < 0) currentSlide = totalSlides - 1;
        if (currentSlide >= totalSlides) currentSlide = 0;
        
        // כל תמונה תופסת 100% מהרוחב, אז נזיז ב-100% לכל תמונה
        const translateX = -currentSlide * 100;
        galleryTrack.style.transform = `translateX(${translateX}%)`;
        
        console.log('תמונה:', currentSlide + 1, 'מתוך', totalSlides, '| translateX:', translateX + '%');
        
        // בדיקה שהתמונה הנוכחית קיימת ונשלפה
        const currentSlideElement = slides[currentSlide];
        if (currentSlideElement) {
            const img = currentSlideElement.querySelector('.gallery-image');
            if (img) {
                console.log('תמונה נוכחית:', img.src);
                // בדיקה אם התמונה נטענה
                if (!img.complete || img.naturalHeight === 0) {
                    console.warn('⚠️ תמונה לא נטענה:', img.src);
                    // ניסיון לטעון מחדש
                    const originalSrc = img.src;
                    img.src = '';
                    setTimeout(() => {
                        img.src = originalSrc;
                    }, 100);
                } else {
                    console.log('✅ תמונה נטענה בהצלחה:', img.src);
                }
                
                // וידוא שהתמונה נראית
                img.style.display = 'block';
                img.style.visibility = 'visible';
                img.style.opacity = '1';
            }
        }
        
        // עדכון אינדיקטורים
        indicators.forEach((indicator, index) => {
            if (index === currentSlide) {
                indicator.classList.add('active');
            } else {
                indicator.classList.remove('active');
            }
        });
    }
    
    // כפתור הבא
    if (nextBtn) {
        nextBtn.addEventListener('click', function() {
            currentSlide = (currentSlide + 1) % totalSlides;
            updateGallery();
        });
    }
    
    // כפתור הקודם
    if (prevBtn) {
        prevBtn.addEventListener('click', function() {
            currentSlide = (currentSlide - 1 + totalSlides) % totalSlides;
            updateGallery();
        });
    }
    
    // לחיצה על אינדיקטורים - רק עבור התמונות הקיימות
    indicators.forEach((indicator, index) => {
        if (index < totalSlides) {
            indicator.addEventListener('click', function() {
                currentSlide = index;
                updateGallery();
            });
        }
    });
    
    // הזזה אוטומטית (אופציונלי - כל 5 שניות)
    let autoSlideInterval = setInterval(function() {
        currentSlide = (currentSlide + 1) % totalSlides;
        updateGallery();
    }, 5000);
    
    // עצירת הזזה אוטומטית כשהעכבר על הגלריה
    const gallerySection = document.querySelector('.image-gallery-section');
    if (gallerySection) {
        gallerySection.addEventListener('mouseenter', function() {
            clearInterval(autoSlideInterval);
        });
        
        gallerySection.addEventListener('mouseleave', function() {
            autoSlideInterval = setInterval(function() {
                currentSlide = (currentSlide + 1) % totalSlides;
                updateGallery();
            }, 5000);
        });
    }
    
    // אתחול ראשוני - ממתין שהתמונות יטענו
    checkImagesAndInit();
}

function wasSplashDismissedToday() {
    try {
        return localStorage.getItem(SPLASH_STORAGE_KEY) === jerusalemDateKey();
    } catch {
        return false;
    }
}

function markSplashDismissed() {
    try {
        localStorage.setItem(SPLASH_STORAGE_KEY, jerusalemDateKey());
    } catch {
        /* ignore quota / private-mode failures */
    }
}

function initCollectionSplash() {
    const splash = document.getElementById('collection-splash');
    if (!splash) return;

    const removeSplash = function () {
        if (splash.parentNode) splash.parentNode.removeChild(splash);
    };

    if (!isSaleActive() || wasSplashDismissedToday()) {
        removeSplash();
        return;
    }

    const hideSplash = function () {
        markSplashDismissed();
        splash.classList.remove('is-visible');
        splash.classList.add('is-gone');
        window.setTimeout(removeSplash, 450);
    };

    requestAnimationFrame(function () {
        splash.classList.add('is-visible');
    });

    const timer = window.setTimeout(hideSplash, 6000);
    const closeBtn = splash.querySelector('.collection-splash__close');
    const closeNow = function (event) {
        if (event) event.stopPropagation();
        window.clearTimeout(timer);
        hideSplash();
    };
    if (closeBtn) closeBtn.addEventListener('click', closeNow);
    splash.addEventListener('click', function (event) {
        if (event.target === splash) closeNow(event);
    });
    document.addEventListener('keydown', function onKey(event) {
        if (event.key === 'Escape') {
            closeNow(event);
            document.removeEventListener('keydown', onKey);
        }
    });
}

document.addEventListener('DOMContentLoaded', function () {
    const zoom = document.getElementById('product-zoom');
    if (!zoom) return;

    const zoomImg = zoom.querySelector('.product-zoom__img');
    const zoomName = zoom.querySelector('.product-zoom__name');
    const zoomDesc = zoom.querySelector('.product-zoom__desc');
    const closeBtn = zoom.querySelector('.product-zoom__close');
    let zoomSku = zoom.querySelector('.product-zoom__sku');
    if (!zoomSku && zoomName) {
        zoomSku = document.createElement('p');
        zoomSku.className = 'product-zoom__sku';
        zoomName.insertAdjacentElement('afterend', zoomSku);
    }

    const setZoomSku = function (sku) {
        if (!zoomSku) return;
        const clean = String(sku || '').replace(/[\u0000-\u001F\u007F]/g, '').trim();
        zoomSku.hidden = !clean;
        zoomSku.innerHTML = clean ? `מק״ט: <bdi>${escapeHtml(clean)}</bdi>` : '';
    };

    const openZoom = function (src, name, descHtml, sku) {
        if (!src) return;
        zoomImg.src = src;
        zoomImg.alt = name || 'תמונת מוצר';
        zoomName.textContent = name || '';
        setZoomSku(sku);
        if (zoomDesc) {
            const html = (descHtml || '').trim();
            zoomDesc.innerHTML = html;
        }
        zoom.classList.toggle('product-zoom--story', Boolean((descHtml || '').trim()));
        zoom.hidden = false;
        requestAnimationFrame(function () {
            zoom.classList.add('is-open');
        });
        document.body.classList.add('is-product-zoom-open');
        if (closeBtn) closeBtn.focus();
    };

    const closeZoom = function () {
        zoom.classList.remove('is-open');
        document.body.classList.remove('is-product-zoom-open');
        window.setTimeout(function () {
            if (!zoom.classList.contains('is-open')) {
                zoom.hidden = true;
                zoomImg.removeAttribute('src');
                zoom.classList.remove('product-zoom--story');
                if (zoomDesc) {
                    zoomDesc.innerHTML = '';
                }
                setZoomSku('');
            }
        }, 280);
    };

    document.addEventListener('click', function (event) {
        const cartMedia = event.target.closest('.cart-item__media');
        if (cartMedia) {
            const photo = cartMedia.querySelector('img');
            const item = cartMedia.closest('.cart-item');
            const nameEl = item ? item.querySelector('.cart-item__name') : null;
            if (!photo) return;
            event.preventDefault();
            const skuEl = item ? item.querySelector('[data-sku]') : null;
            openZoom(
                photo.currentSrc || photo.getAttribute('src'),
                nameEl ? nameEl.textContent.trim() : (photo.alt || ''),
                '',
                item?.getAttribute('data-sku') || skuEl?.getAttribute('data-sku') || ''
            );
            return;
        }

        const workItem = event.target.closest('.frames-work__item');
        if (workItem) {
            const workPhoto = workItem.querySelector('img');
            if (!workPhoto) return;
            event.preventDefault();
            openZoom(workPhoto.currentSrc || workPhoto.getAttribute('src'), workPhoto.alt || 'העבודה שלי');
            return;
        }

        const media = event.target.closest('.jewelry-store__media');
        if (!media || !media.closest('.jewelry-store__item')) return;
        const photo = media.querySelector('img');
        const item = media.closest('.jewelry-store__item');
        if (!photo) return;
        const story = item.querySelector('.jewelry-store__story')
            || item.querySelector('.jewelry-store__body .jewelry-store__story');
        event.preventDefault();
        openZoom(
            photo.currentSrc || photo.getAttribute('src'),
            item.getAttribute('data-name') || photo.alt || '',
            story ? String(story.innerHTML || '').trim() : '',
            item.getAttribute('data-sku') || ''
        );
    });

    if (closeBtn) closeBtn.addEventListener('click', closeZoom);
    zoom.addEventListener('click', function (event) {
        if (event.target === zoom) closeZoom();
    });
    document.addEventListener('keydown', function (event) {
        if (event.key === 'Escape' && zoom.classList.contains('is-open')) {
            closeZoom();
        }
    });
});

document.addEventListener('DOMContentLoaded', function () {
    const analyzeBtn = document.getElementById('orders-analyze-name-btn');
    const nameInput = document.getElementById('orders-name-input');
    if (!analyzeBtn || !nameInput) return;

    analyzeBtn.addEventListener('click', function () {
        const name = nameInput.value.trim();
        if (!name) {
            nameInput.focus();
            return;
        }
        const message = `שלום, אשמח לקבל פענוח שם בתשלום של 100 שקלים, לשם: ${name}`;
        window.open(`https://wa.me/972533397827?text=${encodeURIComponent(message)}`, '_blank', 'noopener,noreferrer');
    });
});

// פונקציות להודעה קופצת
function showPopup() {
    const overlay = document.getElementById('popup-overlay');
    const popup = document.getElementById('popup-message');
    
    if (overlay && popup) {
        overlay.classList.add('show');
        popup.classList.add('show');
    }
}

function closePopup() {
    const overlay = document.getElementById('popup-overlay');
    const popup = document.getElementById('popup-message');
    
    if (overlay && popup) {
        overlay.classList.remove('show');
        popup.classList.remove('show');
    }
}

// סגירת ההודעה בלחיצה על הרקע
document.addEventListener('click', function(event) {
    if (event.target.id === 'popup-overlay') {
        closePopup();
    }
});