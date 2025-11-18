// Carousel d'images pour la section Médecine de Famille et Médecine Communautaire
(function() {
    'use strict';
    
    // Attendre que le DOM soit chargé
    document.addEventListener('DOMContentLoaded', function() {
        const carousel = document.querySelector('.image-carousel');
        if (!carousel) return;
        
        const slides = carousel.querySelectorAll('.carousel-slide:not(.fallback)');
        const fallbackSlide = carousel.querySelector('.carousel-slide.fallback');
        const prevBtn = carousel.querySelector('.carousel-prev');
        const nextBtn = carousel.querySelector('.carousel-next');
        const indicatorsContainer = carousel.querySelector('.carousel-indicators');
        
        // Filtrer les slides qui ont des images valides (vérification initiale)
        let validSlides = Array.from(slides).filter(slide => {
            const img = slide.querySelector('img');
            if (!img) return false;
            // Vérifier si l'image est chargée et n'est pas l'image de fallback
            if (img.complete && img.naturalWidth > 0) {
                return !img.src.includes('medecine-famille.jpg');
            }
            return false;
        });
        
        // Si aucune image valide, utiliser l'image de fallback
        if (validSlides.length === 0 && fallbackSlide) {
            fallbackSlide.classList.add('active');
            return;
        }
        
        // Si on a des slides valides, masquer le fallback
        if (fallbackSlide) {
            fallbackSlide.style.display = 'none';
        }
        
        let currentIndex = 0;
        let autoplayInterval = null;
        const autoplayDelay = 5000; // 5 secondes entre chaque image
        
        // Créer les indicateurs
        function createIndicators() {
            indicatorsContainer.innerHTML = '';
            validSlides.forEach((slide, index) => {
                const indicator = document.createElement('span');
                indicator.className = 'carousel-indicator';
                if (index === 0) {
                    indicator.classList.add('active');
                }
                indicator.addEventListener('click', () => goToSlide(index));
                indicatorsContainer.appendChild(indicator);
            });
        }
        
        // Aller à une slide spécifique
        function goToSlide(index) {
            if (validSlides.length === 0) return;
            
            // Retirer la classe active de toutes les slides et indicateurs
            validSlides.forEach(slide => slide.classList.remove('active'));
            const indicators = indicatorsContainer.querySelectorAll('.carousel-indicator');
            indicators.forEach(indicator => indicator.classList.remove('active'));
            
            // Ajouter la classe active à la slide et l'indicateur correspondants
            currentIndex = index;
            validSlides[currentIndex].classList.add('active');
            if (indicators[currentIndex]) {
                indicators[currentIndex].classList.add('active');
            }
            
            // Redémarrer l'autoplay
            resetAutoplay();
        }
        
        // Slide suivante
        function nextSlide() {
            if (validSlides.length === 0) return;
            const nextIndex = (currentIndex + 1) % validSlides.length;
            goToSlide(nextIndex);
        }
        
        // Slide précédente
        function prevSlide() {
            if (validSlides.length === 0) return;
            const prevIndex = (currentIndex - 1 + validSlides.length) % validSlides.length;
            goToSlide(prevIndex);
        }
        
        // Démarrer l'autoplay
        function startAutoplay() {
            if (validSlides.length <= 1) return;
            autoplayInterval = setInterval(nextSlide, autoplayDelay);
        }
        
        // Arrêter l'autoplay
        function stopAutoplay() {
            if (autoplayInterval) {
                clearInterval(autoplayInterval);
                autoplayInterval = null;
            }
        }
        
        // Redémarrer l'autoplay
        function resetAutoplay() {
            stopAutoplay();
            startAutoplay();
        }
        
        // Vérifier les images chargées après un délai
        function checkImagesLoaded() {
            setTimeout(() => {
                validSlides = Array.from(slides).filter(slide => {
                    const img = slide.querySelector('img');
                    if (!img) return false;
                    // Vérifier si l'image a été chargée ou si elle utilise l'image de fallback
                    return img.complete && img.naturalWidth > 0 && !img.src.includes('medecine-famille.jpg');
                });
                
                if (validSlides.length === 0 && fallbackSlide) {
                    validSlides.forEach(s => s.classList.remove('active'));
                    fallbackSlide.classList.add('active');
                    fallbackSlide.style.display = 'block';
                    return;
                }
                
                if (validSlides.length > 0 && fallbackSlide) {
                    fallbackSlide.style.display = 'none';
                }
                
                // Réinitialiser le carousel avec les images valides
                if (validSlides.length > 0) {
                    createIndicators();
                    goToSlide(0);
                    startAutoplay();
                }
            }, 500);
        }
        
        // Événements
        if (prevBtn) {
            prevBtn.addEventListener('click', () => {
                prevSlide();
                stopAutoplay();
                setTimeout(startAutoplay, 3000); // Redémarrer après 3 secondes
            });
        }
        
        if (nextBtn) {
            nextBtn.addEventListener('click', () => {
                nextSlide();
                stopAutoplay();
                setTimeout(startAutoplay, 3000); // Redémarrer après 3 secondes
            });
        }
        
        // Pause au survol
        carousel.addEventListener('mouseenter', stopAutoplay);
        carousel.addEventListener('mouseleave', startAutoplay);
        
        // Initialisation
        if (validSlides.length > 0) {
            createIndicators();
            goToSlide(0);
            startAutoplay();
        } else {
            checkImagesLoaded();
        }
        
        // Vérifier les images qui se chargent après le DOM
        slides.forEach(slide => {
            const img = slide.querySelector('img');
            if (img) {
                img.addEventListener('load', checkImagesLoaded);
                img.addEventListener('error', checkImagesLoaded);
            }
        });
    });
})();

