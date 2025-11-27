"""
Commande pour créer la table CompetenceJalon si elle n'existe pas
"""
from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = "Crée la table CompetenceJalon si elle n'existe pas"

    def handle(self, *args, **options):
        cursor = connection.cursor()
        
        # Vérifier si la table existe
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = 'utilisateurs_competencejalon'
            );
        """)
        table_exists = cursor.fetchone()[0]
        
        if table_exists:
            self.stdout.write(self.style.SUCCESS('✓ La table utilisateurs_competencejalon existe déjà'))
            return
        
        self.stdout.write(self.style.WARNING('⚠ La table n\'existe pas. Création...'))
        
        # Supprimer la migration de django_migrations si elle existe
        try:
            cursor.execute("""
                DELETE FROM django_migrations 
                WHERE app = 'utilisateurs' 
                AND name = '0040_competencejalon';
            """)
            self.stdout.write(self.style.SUCCESS('✓ Migration 0040 supprimée de django_migrations'))
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'Note: {e}'))
        
        # Créer la table
        try:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS utilisateurs_competencejalon (
                    id BIGSERIAL PRIMARY KEY,
                    titre VARCHAR(300) NOT NULL,
                    description TEXT NOT NULL,
                    echelle_evaluation VARCHAR(20) NOT NULL DEFAULT '1-5',
                    ordre INTEGER NOT NULL DEFAULT 0,
                    actif BOOLEAN NOT NULL DEFAULT TRUE,
                    classe_id BIGINT NOT NULL REFERENCES utilisateurs_classe(id) ON DELETE CASCADE,
                    competence_id BIGINT NOT NULL REFERENCES utilisateurs_competence(id) ON DELETE CASCADE
                );
            """)
            
            cursor.execute("""
                CREATE UNIQUE INDEX IF NOT EXISTS utilisateurs_competencejalon_competence_id_classe_id_titre_unique 
                ON utilisateurs_competencejalon(competence_id, classe_id, titre);
            """)
            
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS utilisateurs_competencejalon_classe_id_idx 
                ON utilisateurs_competencejalon(classe_id);
            """)
            
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS utilisateurs_competencejalon_competence_id_idx 
                ON utilisateurs_competencejalon(competence_id);
            """)
            
            # Créer la table de relation ManyToMany
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS utilisateurs_cours_jalons_competence (
                    id BIGSERIAL PRIMARY KEY,
                    cours_id BIGINT NOT NULL REFERENCES utilisateurs_cours(id) ON DELETE CASCADE,
                    competencejalon_id BIGINT NOT NULL REFERENCES utilisateurs_competencejalon(id) ON DELETE CASCADE,
                    CONSTRAINT utilisateurs_cours_jalons_competence_cours_id_competencejalon_id_unique 
                        UNIQUE (cours_id, competencejalon_id)
                );
            """)
            
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS utilisateurs_cours_jalons_competence_cours_id_idx 
                ON utilisateurs_cours_jalons_competence(cours_id);
            """)
            
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS utilisateurs_cours_jalons_competence_competencejalon_id_idx 
                ON utilisateurs_cours_jalons_competence(competencejalon_id);
            """)
            
            connection.commit()
            self.stdout.write(self.style.SUCCESS('✓ Table créée avec succès'))
            
            # Marquer la migration comme appliquée
            cursor.execute("""
                INSERT INTO django_migrations (app, name, applied)
                VALUES ('utilisateurs', '0040_competencejalon', NOW())
                ON CONFLICT DO NOTHING;
            """)
            connection.commit()
            self.stdout.write(self.style.SUCCESS('✓ Migration marquée comme appliquée'))
            
        except Exception as e:
            connection.rollback()
            self.stdout.write(self.style.ERROR(f'✗ Erreur: {e}'))
            raise

