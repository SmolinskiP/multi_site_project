document.addEventListener('DOMContentLoaded', () => {
    // Obsługa menu mobilnego
    const menuToggle = document.querySelector('.menu-toggle');
    const menu = document.querySelector('.menu');
    
    if (menuToggle && menu) {
        menuToggle.addEventListener('click', () => {
            menu.classList.toggle('active');
        });
    }
});

document.addEventListener('DOMContentLoaded', function() {
    // Pobieramy aktualny miesiąc (0-11)
    const currentDate = new Date();
    const currentMonth = currentDate.getMonth();
    
    // Mapowanie numerów miesięcy (0-11) na nazwy plików
    const monthImages = [
        'bg.jpeg',  // 0 - styczeń
        'bg.jpeg',  // 1 - luty
        'bg.jpeg',  // 2 - marzec
        'bg.jpeg',  // 3 - kwiecień
        'bg.jpeg',  // 4 - maj
        'bg.jpeg',  // 5 - czerwiec
        'bg.jpeg',  // 6 - lipiec
        'bg.jpeg',  // 7 - sierpień
        'bg.jpeg',  // 8 - wrzesień
        'bg.jpeg',  // 9 - październik
        'bg.jpeg',  // 10 - listopad
        'bg.jpeg'   // 11 - grudzień
    ];
    
    // Wybieramy odpowiedni obraz dla aktualnego miesiąca
    const backgroundImage = monthImages[currentMonth];
    
    // Ustawiamy tło dla body
    document.body.style.backgroundImage = `url('/static/dailystoic/img/bg2.jpg')`;
    document.body.style.backgroundSize = 'cover';
    document.body.style.backgroundAttachment = 'fixed';
    document.body.style.backgroundPosition = 'center';
});