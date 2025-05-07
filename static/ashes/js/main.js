
document.addEventListener('DOMContentLoaded', function() {
    console.log("Mobile menu script loaded");
    
    // Sprawdź, czy jesteśmy na urządzeniu mobilnym
    const isMobile = window.innerWidth <= 768;
    
    if (isMobile) {
        console.log("Mobile device detected");
        
        // Znajdź elementy DOM
        const menuList = document.querySelector('.menu');
        const hamburgerButton = document.createElement('button');
        
        // Dodaj klasę dla hamburger button
        hamburgerButton.classList.add('hamburger');
        
        // Dodaj wewnętrzną strukturę hamburgera
        hamburgerButton.innerHTML = `
            <span></span>
            <span></span>
            <span></span>
        `;
        
        // Dodaj przycisk hamburger do DOM, zaraz przed menu
        menuList.parentNode.insertBefore(hamburgerButton, menuList);
        
        // Funkcja przełączająca menu
        function toggleMenu() {
            hamburgerButton.classList.toggle('active');
            menuList.classList.toggle('active');
            
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