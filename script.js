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
 });