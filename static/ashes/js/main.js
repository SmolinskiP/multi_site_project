
document.addEventListener('DOMContentLoaded', function() {
    console.log("Mobile menu script loaded");

    function ensureHamburgerA11y(button) {
        if (!button) {
            return;
        }
        button.type = 'button';
        if (!button.getAttribute('aria-label')) {
            button.setAttribute('aria-label', 'Otwórz menu');
        }
        button.setAttribute('aria-controls', 'main-menu');
        if (!button.getAttribute('aria-expanded')) {
            button.setAttribute('aria-expanded', 'false');
        }
        if (!button.querySelector('.sr-only')) {
            button.insertAdjacentHTML('afterbegin', '<span class="sr-only">Menu</span>');
        }
    }

    ensureHamburgerA11y(document.querySelector('.hamburger'));
    
    // Sprawdź, czy jesteśmy na urządzeniu mobilnym
    const isMobile = window.innerWidth <= 768;
    
    if (isMobile) {
        console.log("Mobile device detected");
        
        // Znajdź elementy DOM
        const menuList = document.querySelector('.menu');
        let hamburgerButton = document.querySelector('.hamburger');

        if (!hamburgerButton) {
            hamburgerButton = document.createElement('button');
            hamburgerButton.classList.add('hamburger');
            hamburgerButton.innerHTML = `
                <span class="sr-only">Menu</span>
                <span></span>
                <span></span>
                <span></span>
            `;
            menuList.parentNode.insertBefore(hamburgerButton, menuList);
        }
        ensureHamburgerA11y(hamburgerButton);
        
        // Funkcja przełączająca menu
        function toggleMenu() {
            hamburgerButton.classList.toggle('active');
            menuList.classList.toggle('active');
            const isExpanded = menuList.classList.contains('active');
            hamburgerButton.setAttribute('aria-expanded', isExpanded ? 'true' : 'false');
            hamburgerButton.setAttribute('aria-label', isExpanded ? 'Zamknij menu' : 'Otwórz menu');
            
            // Blokuj przewijanie strony gdy menu jest otwarte
            if (menuList.classList.contains('active')) {
                document.body.style.overflow = 'hidden';
            } else {
                document.body.style.overflow = '';
            }
        }
        
        // Dodaj listener do przycisku hamburger
        hamburgerButton.addEventListener('click', toggleMenu);
        
        // Dodaj listenery do linków menu, aby zamykać menu po kliknięciu
        const menuLinks = menuList.querySelectorAll('a');
        menuLinks.forEach(link => {
            link.addEventListener('click', function() {
                toggleMenu();
            });
        });
        
        // Zamknij menu po kliknięciu poza menu
        document.addEventListener('click', function(event) {
            if (!menuList.contains(event.target) && 
                !hamburgerButton.contains(event.target) && 
                menuList.classList.contains('active')) {
                toggleMenu();
            }
        });
    }
    
    // Dostosuj wysokość głównej sekcji na podstawie wysokości nagłówka
    function adjustMainPadding() {
        const header = document.querySelector('header');
        const main = document.querySelector('main');
        
        if (header && main) {
            const headerHeight = header.offsetHeight;
            main.style.paddingTop = headerHeight + 'px';
        }
    }
    
    // Wywołaj funkcję przy załadowaniu i przy zmianie rozmiaru okna
    adjustMainPadding();
    window.addEventListener('resize', adjustMainPadding);
});
