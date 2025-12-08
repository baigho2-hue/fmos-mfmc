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
                // Fermer tous les autres sous-menus d'abord
                menuItemsWithSubmenu.forEach(otherItem => {
                    if (otherItem !== this) {
                        const otherSubmenu = otherItem.querySelector('.submenu');
                        if (otherSubmenu) {
                            otherSubmenu.style.display = 'none';
                            otherSubmenu.style.opacity = '0';
                            otherSubmenu.style.visibility = 'hidden';
                        }
                        // Fermer aussi les sous-sous-menus
                        const otherSubsubmenus = otherItem.querySelectorAll('.subsubmenu');
                        otherSubsubmenus.forEach(subsubmenu => {
                            subsubmenu.style.display = 'none';
                            subsubmenu.style.opacity = '0';
                            subsubmenu.style.visibility = 'hidden';
                        });
                    }
                });
                
                // Afficher le sous-menu de l'élément survolé
                const submenu = this.querySelector('.submenu');
                if (submenu) {
                    submenu.style.display = 'block';
                    submenu.style.opacity = '1';
                    submenu.style.visibility = 'visible';
                }
            });
            item.addEventListener('mouseleave', function(e) {
                const submenu = this.querySelector('.submenu');
                if (submenu && window.innerWidth > 1024) {
                    // Vérifier si on passe vers un autre élément de menu
                    const relatedTarget = e.relatedTarget;
                    const isMovingToSubmenu = submenu.contains(relatedTarget);
                    const isMovingToOtherMenu = relatedTarget && relatedTarget.closest('ul.menu > li.has-submenu') && !this.contains(relatedTarget);
                    
                    if (!isMovingToSubmenu && !isMovingToOtherMenu) {
                        // Fermer immédiatement si on ne va pas vers le sous-menu ou un autre menu
                        submenu.style.display = 'none';
                        submenu.style.opacity = '0';
                        submenu.style.visibility = 'hidden';
                        
                        // Fermer aussi tous les sous-sous-menus
                        const subsubmenus = this.querySelectorAll('.subsubmenu');
                        subsubmenus.forEach(subsubmenu => {
                            subsubmenu.style.display = 'none';
                            subsubmenu.style.opacity = '0';
                            subsubmenu.style.visibility = 'hidden';
                        });
                    } else if (!isMovingToSubmenu) {
                        // Délai seulement si on va vers un autre menu
                        setTimeout(() => {
                            if (!this.matches(':hover') && !submenu.matches(':hover')) {
                                submenu.style.display = 'none';
                                submenu.style.opacity = '0';
                                submenu.style.visibility = 'hidden';
                                
                                // Fermer aussi tous les sous-sous-menus
                                const subsubmenus = this.querySelectorAll('.subsubmenu');
                                subsubmenus.forEach(subsubmenu => {
                                    subsubmenu.style.display = 'none';
                                    subsubmenu.style.opacity = '0';
                                    subsubmenu.style.visibility = 'hidden';
                                });
                            }
                        }, 150);
                    }
                }
            });
            
            // Gérer aussi le mouseleave sur le sous-menu lui-même
            const submenu = item.querySelector('.submenu');
            if (submenu) {
                submenu.addEventListener('mouseleave', function(e) {
                    if (window.innerWidth > 1024) {
                        const relatedTarget = e.relatedTarget;
                        const parentLi = this.closest('li.has-submenu');
                        const isMovingToParent = parentLi && parentLi.contains(relatedTarget);
                        
                        if (!isMovingToParent) {
                            setTimeout(() => {
                                if (!parentLi.matches(':hover') && !this.matches(':hover')) {
                                    this.style.display = 'none';
                                    this.style.opacity = '0';
                                    this.style.visibility = 'hidden';
                                    
                                    // Fermer aussi tous les sous-sous-menus
                                    const subsubmenus = this.querySelectorAll('.subsubmenu');
                                    subsubmenus.forEach(subsubmenu => {
                                        subsubmenu.style.display = 'none';
                                        subsubmenu.style.opacity = '0';
                                        subsubmenu.style.visibility = 'hidden';
                                    });
                                }
                            }, 150);
                        }
                    }
                });
            }
        });
        
        // Gestion spécifique des sous-sous-menus pour les groupes
        const submenuGroups = document.querySelectorAll('.submenu-group');
        submenuGroups.forEach(group => {
            group.addEventListener('mouseenter', function() {
                // Fermer tous les autres sous-sous-menus du même niveau
                const parentSubmenu = this.closest('.submenu');
                if (parentSubmenu) {
                    parentSubmenu.querySelectorAll('.submenu-group').forEach(otherGroup => {
                        if (otherGroup !== this) {
                            const otherSubsubmenu = otherGroup.querySelector('.subsubmenu');
                            if (otherSubsubmenu) {
                                otherSubsubmenu.style.display = 'none';
                                otherSubsubmenu.style.opacity = '0';
                                otherSubsubmenu.style.visibility = 'hidden';
                            }
                        }
                    });
                }
                
                const subsubmenu = this.querySelector('.subsubmenu');
                if (subsubmenu) {
                    subsubmenu.style.display = 'block';
                    subsubmenu.style.opacity = '1';
                    subsubmenu.style.visibility = 'visible';
                }
            });
            group.addEventListener('mouseleave', function() {
                const subsubmenu = this.querySelector('.subsubmenu');
                if (subsubmenu) {
                    setTimeout(() => {
                        if (!this.matches(':hover') && !subsubmenu.matches(':hover')) {
                            subsubmenu.style.display = 'none';
                            subsubmenu.style.opacity = '0';
                            subsubmenu.style.visibility = 'hidden';
                        }
                    }, 150);
                }
            });
        });
        
        // S'assurer que le sous-sous-menu reste visible au survol
        const subsubmenus = document.querySelectorAll('.subsubmenu');
        subsubmenus.forEach(subsubmenu => {
            subsubmenu.addEventListener('mouseenter', function() {
                this.style.display = 'block';
                this.style.opacity = '1';
                this.style.visibility = 'visible';
            });
            subsubmenu.addEventListener('mouseleave', function() {
                setTimeout(() => {
                    if (!this.matches(':hover')) {
                        this.style.display = 'none';
                        this.style.opacity = '0';
                        this.style.visibility = 'hidden';
                    }
                }, 150);
            });
        });
        
        // Fermer tous les sous-menus quand on clique ailleurs ou qu'on survole un autre élément
        document.addEventListener('click', function(e) {
            if (window.innerWidth > 1024) {
                const clickedInsideMenu = e.target.closest('.main-menu');
                if (!clickedInsideMenu) {
                    menuItemsWithSubmenu.forEach(item => {
                        const submenu = item.querySelector('.submenu');
                        if (submenu) {
                            submenu.style.display = 'none';
                            submenu.style.opacity = '0';
                            submenu.style.visibility = 'hidden';
                        }
                        const subsubmenus = item.querySelectorAll('.subsubmenu');
                        subsubmenus.forEach(subsubmenu => {
                            subsubmenu.style.display = 'none';
                            subsubmenu.style.opacity = '0';
                            subsubmenu.style.visibility = 'hidden';
                        });
                    });
                }
            }
        });
        
        // Fermer tous les sous-menus quand on survole un élément sans sous-menu
        const menuItemsWithoutSubmenu = document.querySelectorAll('ul.menu > li:not(.has-submenu)');
        menuItemsWithoutSubmenu.forEach(item => {
            item.addEventListener('mouseenter', function() {
                // Fermer tous les sous-menus ouverts
                menuItemsWithSubmenu.forEach(menuItem => {
                    const submenu = menuItem.querySelector('.submenu');
                    if (submenu) {
                        submenu.style.display = 'none';
                        submenu.style.opacity = '0';
                        submenu.style.visibility = 'hidden';
                    }
                    const subsubmenus = menuItem.querySelectorAll('.subsubmenu');
                    subsubmenus.forEach(subsubmenu => {
                        subsubmenu.style.display = 'none';
                        subsubmenu.style.opacity = '0';
                        subsubmenu.style.visibility = 'hidden';
                    });
                });
            });
        });
    }
});
