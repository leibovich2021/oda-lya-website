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
    
    // טיפול בטופס פיענוח שמות
    const nameForm = document.querySelector('.name-form .btn');
    if (nameForm) {
        nameForm.addEventListener('click', function() {
            const nameInput = document.getElementById('name');
            const nameResult = document.querySelector('.name-result');
            
            if (nameInput && nameInput.value && nameResult) {
                const name = nameInput.value.trim();
                nameResult.innerHTML = `
                    <h3>פיענוח השם: ${name}</h3>
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
 });

// -----------------------------
// סל קניות + PayPal (אתר סטטי)
// -----------------------------
const CART_STORAGE_KEY = 'oda_cart_v1';

// הכניסי כאן Client ID של PayPal (Sandbox/Live)
// דוגמה: 'AbCdEf...'
const PAYPAL_CLIENT_ID = '';
const PAYPAL_CURRENCY = 'ILS';
const BIT_PHONE = '0533397827';
const ORDER_CONTACT_WA = '972533397827';
const ORDER_FORM_STORAGE_KEY = 'oda_order_form_v1';

function readCart() {
    try {
        const raw = localStorage.getItem(CART_STORAGE_KEY);
        const parsed = raw ? JSON.parse(raw) : [];
        return Array.isArray(parsed) ? parsed : [];
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

function formatOrderForMessage(items) {
    const lines = items.map((it) => {
        const qty = Number(it.qty) || 1;
        const price = Number(it.price) || 0;
        const note = (it.note || '').trim();
        const notePart = note ? ` | בקשה: ${note}` : '';
        return `- ${it.name} ×${qty} (${formatILS(price)})${notePart}`;
    });
    return lines.join('\n');
}

function openBitPayment(items) {
    const total = calcCartTotal(items);
    const orderLines = formatOrderForMessage(items);
    const text = [
        'שלום, אני רוצה לבצע תשלום ב-Bit על ההזמנה באתר.',
        '',
        `טלפון לתשלום ב-Bit: ${BIT_PHONE}`,
        '',
        'פריטים:',
        orderLines || '- (אין פריטים)',
        '',
        `סה״כ לתשלום: ${formatILS(total)}`,
        '',
        'אחרי התשלום אשמח לאישור 🙂'
    ].join('\n');

    // שולחים לוואטסאפ כדי לקבל הודעה מסודרת + תשלום בביט באופן ידני
    const wa = `https://wa.me/972533397827?text=${encodeURIComponent(text)}`;
    window.open(wa, '_blank', 'noopener,noreferrer');
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
    const total = calcCartTotal(items);
    const orderLines = formatOrderForMessage(items);
    const text = [
        'התקבלה הזמנה חדשה מהאתר:',
        '',
        `שם: ${customer.name || ''}`,
        `טלפון: ${customer.phone || ''}`,
        `כתובת: ${customer.address || ''}`,
        `עיר: ${customer.city || ''}`,
        customer.email ? `אימייל: ${customer.email}` : '',
        customer.note ? `הערה כללית: ${customer.note}` : '',
        '',
        'פריטים:',
        orderLines || '- (אין פריטים)',
        '',
        `סה״כ: ${formatILS(total)}`
    ].filter(Boolean).join('\n');

    const wa = `https://wa.me/${ORDER_CONTACT_WA}?text=${encodeURIComponent(text)}`;
    window.open(wa, '_blank', 'noopener,noreferrer');
}

function upsertCartItem(nextItem) {
    const items = readCart();
    const idx = items.findIndex(it => it.sku === nextItem.sku);
    if (idx >= 0) {
        items[idx].qty = (Number(items[idx].qty) || 0) + (Number(nextItem.qty) || 1);
    } else {
        items.push({ ...nextItem, qty: Number(nextItem.qty) || 1 });
    }
    writeCart(items);
    updateCartBadge();
}

function setCartQty(sku, qty) {
    const items = readCart().map(it => it.sku === sku ? { ...it, qty: Math.max(1, Number(qty) || 1) } : it);
    writeCart(items);
    updateCartBadge();
}

function setCartNote(sku, note) {
    const safeNote = String(note || '').slice(0, 280);
    const items = readCart().map(it => it.sku === sku ? { ...it, note: safeNote } : it);
    writeCart(items);
}

function removeCartItem(sku) {
    const items = readCart().filter(it => it.sku !== sku);
    writeCart(items);
    updateCartBadge();
}

function clearCart() {
    writeCart([]);
    updateCartBadge();
}

function calcCartTotal(items) {
    return items.reduce((sum, it) => sum + (Number(it.price) || 0) * (Number(it.qty) || 0), 0);
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
    const store = document.querySelector('.jewelry-store');
    if (!store) return;

    store.addEventListener('click', (e) => {
        const itemEl = e.target.closest('.jewelry-store__item');
        if (!itemEl) return;

        const addBtn = e.target.closest('.jewelry-store__add');
        const buyLink = e.target.closest('.jewelry-store__details');
        if (!addBtn && !buyLink) return;

        const sku = itemEl.getAttribute('data-sku') || '';
        const name = itemEl.getAttribute('data-name') || '';
        const price = Number(itemEl.getAttribute('data-price') || 0);
        const currency = itemEl.getAttribute('data-currency') || PAYPAL_CURRENCY;
        const image = itemEl.getAttribute('data-image') || '';

        if (!sku || !name || !price) return;

        upsertCartItem({ sku, name, price, currency, image, qty: 1 });

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

function renderCartPage() {
    const itemsWrap = document.getElementById('cart-items');
    if (!itemsWrap) return;

    const emptyEl = document.getElementById('cart-empty');
    const totalEl = document.getElementById('cart-total');
    const clearBtn = document.getElementById('cart-clear');
    const bitBtn = document.getElementById('bit-pay');
    const orderForm = document.getElementById('order-form');

    const items = readCart();
    const isEmpty = items.length === 0;

    if (emptyEl) emptyEl.hidden = !isEmpty;
    itemsWrap.innerHTML = '';

    if (totalEl) totalEl.textContent = formatILS(calcCartTotal(items));

    if (bitBtn) {
        bitBtn.disabled = isEmpty;
        bitBtn.addEventListener('click', () => openBitPayment(readCart()));
    }

    if (orderForm) {
        const saved = readOrderForm();
        const nameEl = document.getElementById('order-name');
        const phoneEl = document.getElementById('order-phone');
        const addressEl = document.getElementById('order-address');
        const cityEl = document.getElementById('order-city');
        const emailEl = document.getElementById('order-email');
        const noteEl = document.getElementById('order-note');
        const submitEl = document.getElementById('order-submit');

        if (nameEl && saved.name) nameEl.value = saved.name;
        if (phoneEl && saved.phone) phoneEl.value = saved.phone;
        if (addressEl && saved.address) addressEl.value = saved.address;
        if (cityEl && saved.city) cityEl.value = saved.city;
        if (emailEl && saved.email) emailEl.value = saved.email;
        if (noteEl && saved.note) noteEl.value = saved.note;

        if (submitEl) {
            // לא משתמשים ב-disabled כדי שנוכל להציג הודעה בלחיצה
            submitEl.classList.toggle('is-disabled', isEmpty);
            submitEl.setAttribute('aria-disabled', isEmpty ? 'true' : 'false');
        }

        orderForm.addEventListener('input', () => {
            writeOrderForm({
                name: nameEl?.value || '',
                phone: phoneEl?.value || '',
                address: addressEl?.value || '',
                city: cityEl?.value || '',
                email: emailEl?.value || '',
                note: noteEl?.value || ''
            });
        });

        orderForm.addEventListener('submit', (e) => {
            e.preventDefault();
            if (isEmpty) {
                alert('הסל ריק — צריך להוסיף מוצרים לפני שליחת הזמנה.');
                return;
            }
            const customer = {
                name: nameEl?.value?.trim() || '',
                phone: phoneEl?.value?.trim() || '',
                address: addressEl?.value?.trim() || '',
                city: cityEl?.value?.trim() || '',
                email: emailEl?.value?.trim() || '',
                note: noteEl?.value?.trim() || ''
            };
            if (!customer.name || !customer.phone || !customer.address || !customer.city || !customer.email) {
                alert('נא למלא שם, טלפון, כתובת, עיר ואימייל.');
                return;
            }
            openOrderWhatsApp(readCart(), customer);
        });
    }

    if (clearBtn) {
        clearBtn.addEventListener('click', () => {
            clearCart();
            renderCartPage();
            showToast('הסל נוקה');
        });
    }

    if (isEmpty) {
        initPayPalButton([]);
        return;
    }

    items.forEach(it => {
        const row = document.createElement('div');
        row.className = 'cart-item';
        row.innerHTML = `
            <div class="cart-item__media">
                ${it.image ? `<img src="${it.image}" alt="" loading="lazy" decoding="async" width="80" height="80">` : ''}
            </div>
            <div class="cart-item__info">
                <div class="cart-item__name">${it.name}</div>
                <div class="cart-item__meta">
                    <span class="cart-item__price">${formatILS(it.price)}</span>
                </div>
                <label class="cart-item__note">
                    <span class="cart-item__note-label">בקשה מיוחדת</span>
                    <input class="cart-note" type="text" placeholder="למשל: צבע/מידה/הקדשה..." value="${(it.note || '').replace(/\"/g,'&quot;')}" data-sku="${it.sku}">
                </label>
            </div>
            <div class="cart-item__qty">
                <label>
                    <span class="sr-only">כמות</span>
                    <input class="cart-qty" type="number" min="1" value="${Number(it.qty) || 1}" data-sku="${it.sku}">
                </label>
            </div>
            <div class="cart-item__sum">${formatILS((Number(it.price)||0) * (Number(it.qty)||0))}</div>
            <button class="cart-item__remove" type="button" data-sku="${it.sku}" aria-label="הסרה">×</button>
        `;
        itemsWrap.appendChild(row);
    });

    itemsWrap.addEventListener('input', (e) => {
        const note = e.target.closest('.cart-note');
        if (!note) return;
        setCartNote(note.dataset.sku, note.value);
    });

    itemsWrap.addEventListener('input', (e) => {
        const input = e.target.closest('.cart-qty');
        if (!input) return;
        setCartQty(input.dataset.sku, input.value);
        renderCartPage();
    }, { once: true });

    itemsWrap.addEventListener('click', (e) => {
        const rm = e.target.closest('.cart-item__remove');
        if (!rm) return;
        removeCartItem(rm.dataset.sku);
        renderCartPage();
    }, { once: true });

    initPayPalButton(items);
}

function ensurePayPalSdkLoaded() {
    return new Promise((resolve) => {
        if (window.paypal) return resolve(true);
        if (!PAYPAL_CLIENT_ID) return resolve(false);

        const existing = document.querySelector('script[data-paypal-sdk]');
        if (existing) {
            existing.addEventListener('load', () => resolve(true), { once: true });
            existing.addEventListener('error', () => resolve(false), { once: true });
            return;
        }

        const s = document.createElement('script');
        s.src = `https://www.paypal.com/sdk/js?client-id=${encodeURIComponent(PAYPAL_CLIENT_ID)}&currency=${encodeURIComponent(PAYPAL_CURRENCY)}&intent=capture`;
        s.async = true;
        s.defer = true;
        s.setAttribute('data-paypal-sdk', '1');
        s.addEventListener('load', () => resolve(true), { once: true });
        s.addEventListener('error', () => resolve(false), { once: true });
        document.head.appendChild(s);
    });
}

async function initPayPalButton(items) {
    const container = document.getElementById('paypal-button-container');
    if (!container) return;
    container.innerHTML = '';

    const missing = document.getElementById('paypal-missing');
    const ok = await ensurePayPalSdkLoaded();
    if (!ok || !window.paypal || items.length === 0) {
        if (missing) missing.hidden = !!PAYPAL_CLIENT_ID && items.length > 0;
        return;
    }
    if (missing) missing.hidden = true;

    const total = calcCartTotal(items);
    const itemTotal = total.toFixed(2);

    window.paypal.Buttons({
        style: { layout: 'vertical', shape: 'rect', label: 'paypal' },
        createOrder: (data, actions) => {
            const noteLines = items
                .filter(it => (it.note || '').trim().length > 0)
                .map(it => `${it.sku}: ${(it.note || '').trim()}`)
                .join(' | ')
                .slice(0, 120);

            return actions.order.create({
                purchase_units: [{
                    description: noteLines ? `בקשות מיוחדות: ${noteLines}` : undefined,
                    amount: {
                        currency_code: PAYPAL_CURRENCY,
                        value: itemTotal,
                        breakdown: { item_total: { currency_code: PAYPAL_CURRENCY, value: itemTotal } }
                    },
                    items: items.map(it => ({
                        name: it.name,
                        description: (it.note || '').trim().slice(0, 127) || undefined,
                        unit_amount: { currency_code: PAYPAL_CURRENCY, value: (Number(it.price) || 0).toFixed(2) },
                        quantity: String(Number(it.qty) || 1),
                        sku: it.sku
                    }))
                }]
            });
        },
        onApprove: async (data, actions) => {
            const details = await actions.order.capture();
            clearCart();
            renderCartPage();
            alert('התשלום בוצע בהצלחה. תודה רבה!');
            console.log('PayPal capture:', details);
        }
    }).render('#paypal-button-container');
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