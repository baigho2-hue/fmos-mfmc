# 📧 Guide : Messagerie Interne du Site

Votre site dispose maintenant d'un système de messagerie interne complet, sans dépendre de services externes comme Gmail.

---

## 🎯 Fonctionnalités

### ✅ Fonctionnalités Disponibles

- **Envoi de messages** entre utilisateurs du site
- **Réception et lecture** des messages
- **Conversations** organisées par utilisateur
- **Notifications** de messages non lus
- **Réponses** aux messages (threading)
- **Suppression** de messages (soft delete)
- **Pièces jointes** (optionnel, à configurer)

---

## 🚀 Utilisation

### Accéder à la Messagerie

1. Connectez-vous à votre compte
2. Allez sur : `https://fmos-mfmc.onrender.com/messagerie/`
3. Vous verrez la liste de vos conversations

### Envoyer un Message

1. Cliquez sur **"Nouveau message"**
2. Sélectionnez le destinataire
3. Remplissez le sujet (optionnel) et le contenu
4. Cliquez sur **"Envoyer"**

### Lire une Conversation

1. Cliquez sur une conversation dans la liste
2. Vous verrez tous les messages échangés
3. Vous pouvez répondre directement dans la conversation

### Répondre à un Message

1. Ouvrez la conversation
2. Utilisez le formulaire en bas de page
3. Tapez votre réponse et cliquez sur **"Envoyer"**

---

## 📋 URLs Disponibles

- `/messagerie/` - Liste des conversations
- `/messagerie/envoyer/` - Envoyer un nouveau message
- `/messagerie/conversation/<id>/` - Voir une conversation
- `/messagerie/message/<id>/` - Voir un message spécifique

---

## 🔧 Configuration

### Migrations

Les migrations sont déjà appliquées automatiquement. Si ce n'est pas le cas :

```bash
python manage.py makemigrations communications
python manage.py migrate
```

### Admin Django

Les messages sont accessibles dans l'admin Django :
- Allez dans **"Communications"** > **"Messages"**
- Vous pouvez voir, modifier et supprimer tous les messages

---

## 🎨 Personnalisation

### Ajouter un Lien dans le Menu

Pour ajouter un lien vers la messagerie dans votre menu de navigation :

1. Modifiez `core/templates/base.html`
2. Ajoutez un lien vers `{% url 'messagerie_liste' %}`

### Afficher le Nombre de Messages Non Lus

Vous pouvez ajouter un badge avec le nombre de messages non lus dans votre menu :

```html
<a href="{% url 'messagerie_liste' %}">
    Messagerie
    {% if nb_messages_non_lus > 0 %}
    <span class="badge bg-danger">{{ nb_messages_non_lus }}</span>
    {% endif %}
</a>
```

---

## 🔒 Sécurité

- Seuls les utilisateurs connectés peuvent accéder à la messagerie
- Un utilisateur ne peut voir que ses propres messages (envoyés ou reçus)
- Les messages supprimés sont marqués comme supprimés (soft delete) mais restent en base de données

---

## 📊 Statistiques

Dans l'admin Django, vous pouvez voir :
- Le nombre total de messages
- Les messages non lus
- Les conversations les plus actives

---

## 🆘 Résolution de Problèmes

### Les messages ne s'affichent pas

1. Vérifiez que les migrations sont appliquées
2. Vérifiez que vous êtes connecté
3. Vérifiez les logs Django pour voir les erreurs

### Impossible d'envoyer un message

1. Vérifiez que le destinataire existe
2. Vérifiez que vous êtes connecté
3. Vérifiez que le formulaire est correctement rempli

---

## 🎉 Avantages

### ✅ Avantages de la Messagerie Interne

- **Pas de dépendance externe** : Fonctionne sans Gmail ou autres services
- **Données privées** : Tous les messages restent sur votre serveur
- **Intégration** : Intégré directement dans votre site
- **Gratuit** : Pas de coûts supplémentaires
- **Contrôle total** : Vous gérez tous les messages

### ⚠️ Limitations

- **Pas d'emails externes** : Les messages ne sont envoyés qu'aux utilisateurs du site
- **Notifications** : Pas de notifications email automatiques (peut être ajouté)
- **Pièces jointes** : Limitées par la taille des fichiers statiques

---

## 📚 Documentation Technique

### Modèle Message

Le modèle `Message` dans `apps/communications/models.py` contient :
- Expéditeur et destinataire
- Sujet et contenu
- Date d'envoi et de lecture
- Statut lu/non lu
- Support pour les réponses (message_parent)
- Support pour les pièces jointes

### Vues

Les vues dans `apps/communications/views.py` gèrent :
- Liste des conversations
- Affichage d'une conversation
- Envoi de messages
- Suppression de messages
- API pour le nombre de messages non lus

---

## 🚀 Prochaines Améliorations Possibles

- Notifications email pour les nouveaux messages
- Recherche dans les messages
- Filtres et tri avancés
- Messages de groupe
- Pièces jointes améliorées
- Messages système automatiques

---

**Votre messagerie interne est maintenant opérationnelle ! 🎉**

---

**Dernière mise à jour** : Novembre 2025

