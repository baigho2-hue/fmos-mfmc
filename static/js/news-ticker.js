// Gestion de la bande news roulante
document.addEventListener('DOMContentLoaded', function() {
    const newsTickerContent = document.querySelector('.news-ticker-content');
    
    if (newsTickerContent) {
        // Dupliquer le contenu pour créer une animation infinie fluide
        const originalContent = newsTickerContent.innerHTML;
        newsTickerContent.innerHTML = originalContent + originalContent;
        
        // Ajuster la vitesse d'animation en fonction du nombre d'éléments
        const newsItems = document.querySelectorAll('.news-item');
        const totalItems = newsItems.length;
        
        // Calculer la durée de l'animation (environ 3 secondes par élément)
        const animationDuration = totalItems * 3;
        
        // Appliquer la durée d'animation
        newsTickerContent.style.animationDuration = animationDuration + 's';
    }
});

