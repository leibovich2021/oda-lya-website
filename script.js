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
 });
 
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
