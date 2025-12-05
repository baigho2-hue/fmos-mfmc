// Gestion du menu hamburger pour mobile
document.addEventListener('DOMContentLoaded', function() {
    const menuToggle = document.querySelector('.menu-toggle');
    const mainMenu = document.querySelector('.main-menu');
    
    if (menuToggle && mainMenu) {
        // Toggle du menu principal
        menuToggle.addEventListener('click', function(e) {
            e.stopPropagation();
            const isExpanded = menuToggle.getAttribute('aria-expanded') === 'true';
            
            // Toggle l'état du menu
            menuToggle.setAttribute('aria-expanded', !isExpanded);
            mainMenu.classList.toggle('active');
        });
        
        // Gestion des sous-menus sur mobile (toggle au clic)
        const menuItemsWithSubmenu = mainMenu.querySelectorAll('.has-submenu > a');
        menuItemsWithSubmenu.forEach(item => {
            item.addEventListener('click', function(e) {
                // Vérifier si on est sur tablette ou mobile (largeur <= 1024px)
                if (window.innerWidth <= 1024) {
                    e.preventDefault();
                    const parentLi = this.parentElement;
                    const submenu = parentLi.querySelector('.submenu');
                    
                    // Fermer les autres sous-menus ouverts
                    mainMenu.querySelectorAll('.has-submenu').forEach(li => {
                        if (li !== parentLi) {
                            li.classList.remove('active');
                        }
                    });
                    
                    // Toggle le sous-menu actuel
                    parentLi.classList.toggle('active');
                }
            });
        });
        
        // Gestion des sous-sous-menus
        const submenuItems = mainMenu.querySelectorAll('.submenu > li');
        submenuItems.forEach(item => {
            const subsubmenu = item.querySelector('.subsubmenu');
            if (subsubmenu) {
                const link = item.querySelector('a');
                link.addEventListener('click', function(e) {
                    if (window.innerWidth <= 1024) {
                        e.preventDefault();
                        item.classList.toggle('active');
                    }
                });
            }
        });
        
        // Fermer le menu quand on clique sur un lien final (sur mobile)
        const finalLinks = mainMenu.querySelectorAll('a');
        finalLinks.forEach(link => {
            link.addEventListener('click', function(e) {
                // Vérifier si on est sur tablette ou mobile et si c'est un lien final (pas un parent de sous-menu)
                if (window.innerWidth <= 1024) {
                    const parentLi = this.closest('li');
                    const hasSubmenu = parentLi && parentLi.querySelector('.submenu, .subsubmenu');
                    
                    // Si c'est un lien final (pas de sous-menu), fermer le menu
                    if (!hasSubmenu || this.parentElement === parentLi && !parentLi.classList.contains('has-submenu')) {
                        menuToggle.setAttribute('aria-expanded', 'false');
                        mainMenu.classList.remove('active');
                        // Réinitialiser tous les sous-menus
                        mainMenu.querySelectorAll('.has-submenu, .submenu li').forEach(li => {
                            li.classList.remove('active');
                        });
                    }
                }
            });
        });
        
        // Fermer le menu si on clique en dehors (sur tablette ou mobile)
        document.addEventListener('click', function(e) {
            if (window.innerWidth <= 1024) {
                if (!mainMenu.contains(e.target) && !menuToggle.contains(e.target)) {
                    menuToggle.setAttribute('aria-expanded', 'false');
                    mainMenu.classList.remove('active');
                    mainMenu.querySelectorAll('.has-submenu, .submenu li').forEach(li => {
                        li.classList.remove('active');
                    });
                }
            }
        });
        
        // Fermer le menu si on redimensionne la fenêtre vers desktop
        window.addEventListener('resize', function() {
            if (window.innerWidth > 1024) {
                menuToggle.setAttribute('aria-expanded', 'false');
                mainMenu.classList.remove('active');
                mainMenu.querySelectorAll('.has-submenu, .submenu li').forEach(li => {
                    li.classList.remove('active');
                });
            }
        });
    }
    
    // Gestion des sous-sous-menus (niveau 3) si présents
    document.querySelectorAll('.has-subsubmenu').forEach(item => {
        item.addEventListener('mouseenter', () => {
            const submenu = item.querySelector('.subsubmenu-level3');
            if(submenu) {
                submenu.style.display = 'flex';
                setTimeout(()=>submenu.style.opacity='1',10);
            }
        });
        item.addEventListener('mouseleave', () => {
            const submenu = item.querySelector('.subsubmenu-level3');
            if(submenu) {
                submenu.style.opacity='0';
                setTimeout(()=>submenu.style.display='none',250);
            }
        });
    });
    
    // S'assurer que les sous-menus s'affichent correctement au survol (desktop)
    if (window.innerWidth > 1024) {
        const menuItemsWithSubmenu = document.querySelectorAll('.has-submenu');
        menuItemsWithSubmenu.forEach(item => {
            item.addEventListener('mouseenter', function() {
                const submenu = this.querySelector('.submenu');
                if (submenu) {
                    submenu.style.display = 'block';
                    submenu.style.opacity = '1';
                    submenu.style.visibility = 'visible';
                }
            });
            item.addEventListener('mouseleave', function() {
                const submenu = this.querySelector('.submenu');
                if (submenu && window.innerWidth > 1024) {
                    // Ne pas cacher immédiatement, laisser le CSS gérer
                    setTimeout(() => {
                        if (!this.matches(':hover') && !submenu.matches(':hover')) {
                            submenu.style.display = 'none';
                        }
                    }, 200);
                }
            });
        });
    }
});
