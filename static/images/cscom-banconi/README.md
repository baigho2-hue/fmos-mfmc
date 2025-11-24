# CSCom de Banconi

Ce dossier contient les photos du Centre de Santé Communautaire (CSCom) de Banconi.

## Instructions pour ajouter des images

1. Placez vos images dans ce dossier (`static/images/cscom-banconi/`)
2. Nommez-les selon le format : `banconi-1.jpg`, `banconi-2.jpg`, `banconi-3.jpg`, etc.
3. Formats supportés : `.jpg`, `.jpeg`, `.png`
4. Les images seront automatiquement disponibles sur le site web

## Utilisation sur le site web

### Exemple d'utilisation dans un template HTML (Django) :

```html
{% load static %}
<img src="{% static 'images/cscom-banconi/banconi-1.jpg' %}" alt="CSCom de Banconi - Photo 1">
```

### Exemple d'utilisation directe (HTML simple) :

```html
<img src="/static/images/cscom-banconi/banconi-1.jpg" alt="CSCom de Banconi - Photo 1">
```

### Exemple de carousel (comme pour CSCom de Kayes N'di) :

```html
{% load static %}
<div class="image-carousel">
  <div class="carousel-container">
    <div class="carousel-slides">
      <div class="carousel-slide active">
        <img src="{% static 'images/cscom-banconi/banconi-1.jpg' %}" alt="CSCom de Banconi - Photo 1" onerror="this.style.display='none';" />
      </div>
      <div class="carousel-slide">
        <img src="{% static 'images/cscom-banconi/banconi-2.jpg' %}" alt="CSCom de Banconi - Photo 2" onerror="this.style.display='none';" />
      </div>
    </div>
  </div>
</div>
```

## Formats acceptés

- JPG / JPEG
- PNG
- WebP (recommandé pour le web)

## Notes importantes

- Les photos doivent être optimisées pour le web (taille raisonnable)
- **Recommandation : max 2MB par photo**
- **Dimensions recommandées :** largeur minimale de 800px
- Les images seront visibles sur le site une fois placées dans ce dossier
- Le chemin d'accès sera : `/static/images/cscom-banconi/nom_de_la_photo.jpg`

## Structure du dossier

```
static/images/cscom-banconi/
├── README.md (ce fichier)
├── banconi-1.jpg (à ajouter)
├── banconi-2.jpg (à ajouter)
└── ...
```

## Où utiliser ces images ?

Les images peuvent être utilisées dans :
- La page d'accueil (`core/templates/accueil.html`)
- Les pages de présentation des CSCom-U
- Les pages de stages
- Toute autre page du site nécessitant des photos du CSCom de Banconi

