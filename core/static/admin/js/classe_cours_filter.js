// admin/js/classe_cours_filter.js
// Script pour afficher les cours d'une classe sélectionnée dans l'admin Django

(function($) {
    'use strict';
    
    // Fonction pour charger les cours d'une classe
    function loadCoursForClasse(classeId, widgetId) {
        if (!classeId || classeId === '') {
            $('#cours-list-' + widgetId).hide();
            return;
        }
        
        // Faire une requête AJAX pour récupérer les cours
        $.ajax({
            url: '/admin/utilisateurs/cours/get-cours-by-classe/',
            data: {
                'classe_id': classeId
            },
            dataType: 'json',
            success: function(data) {
                var coursList = $('#cours-items-' + widgetId);
                coursList.empty();
                
                if (data.cours && data.cours.length > 0) {
                    $.each(data.cours, function(index, cours) {
                        coursList.append(
                            '<li><strong>' + cours.code + '</strong> - ' + cours.titre + 
                            ' (' + cours.nombre_lecons + ' leçon' + (cours.nombre_lecons > 1 ? 's' : '') + ')</li>'
                        );
                    });
                    $('#cours-list-' + widgetId).show();
                } else {
                    coursList.append('<li>Aucun cours dans cette classe</li>');
                    $('#cours-list-' + widgetId).show();
                }
            },
            error: function(xhr, status, error) {
                console.error('Erreur lors du chargement des cours:', error);
                $('#cours-list-' + widgetId).hide();
            }
        });
    }
    
    // Initialiser quand le DOM est prêt
    $(document).ready(function() {
        // Fonction pour initialiser le widget pour un champ spécifique
        function initClasseWidget($select) {
            var widgetId = $select.attr('id') || $select.attr('name');
            if (!widgetId) return;
            
            // Créer le conteneur pour afficher les cours si il n'existe pas
            if ($('#cours-list-' + widgetId).length === 0) {
                var $container = $select.closest('.form-row, .field-classe, .form-group');
                if ($container.length === 0) {
                    $container = $select.parent();
                }
                $container.after(
                    '<div id="cours-list-' + widgetId + '" class="cours-list-display" style="display: none; margin-top: 10px; margin-bottom: 10px;">' +
                    '<h4 style="margin-top: 0;">Cours de cette classe :</h4>' +
                    '<ul id="cours-items-' + widgetId + '" class="cours-items"></ul>' +
                    '</div>'
                );
            }
            
            // Charger les cours si une classe est déjà sélectionnée
            if ($select.val()) {
                loadCoursForClasse($select.val(), widgetId);
            }
            
            // Écouter les changements de sélection
            $select.off('change.classeCoursFilter').on('change.classeCoursFilter', function() {
                loadCoursForClasse($(this).val(), widgetId);
            });
        }
        
        // Trouver tous les champs de sélection de classe dans le formulaire de cours
        $('select[id*="id_classe"], select[name*="classe"], select.classe-select-field').each(function() {
            initClasseWidget($(this));
        });
        
        // Écouter les événements de changement de formulaire (pour les inlines)
        $(document).on('formset:added', function(event, $row) {
            $row.find('select[id*="id_classe"], select[name*="classe"]').each(function() {
                initClasseWidget($(this));
            });
        });
    });
    
})(django.jQuery);

