# 🏎️ Stream Chat Racing - World Championship

<img width="1024" height="400" alt="Gemini_Generated_Image_y983sny983sny983" src="https://github.com/user-attachments/assets/6955bcee-8d50-4bb8-ba08-6b6d61712a04" />

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Pygame](https://img.shields.io/badge/Library-Pygame-yellow)
![Platform](https://img.shields.io/badge/Platform-Twitch%20%7C%20YouTube-purple)

Un jeu de course interactif codé en Python où **votre chat contrôle la course**. Les spectateurs tapent le nom d'un pays pour booster la voiture associée vers la victoire. Compatible avec Twitch et YouTube (simultanément ou séparément).

## ✨ Fonctionnalités

🌐 Support Multi-Plateforme :** Connectez Twitch et YouTube en même temps.
🎮 Interaction en temps réel :** Chaque message dans le chat booste la voiture correspondante.
📊 Statistiques en direct :** Affichage du nombre de joueurs, moyenne par partie et classement des victoires.
🎨 Visuels soignés :** Effets de particules, cycles jour/nuit (lignes de route), et dégradés de couleurs pour chaque pays.
🔊 Audio :** Support pour musique d'ambiance et effets sonores (moteur, victoire).
🛠️ Personnalisable :** Facile d'ajouter de nouveaux pays ou de changer les couleurs.

## ⚙️ Prérequis

* Python 3.x installé.
* Les bibliothèques Python suivantes :

bash
pip install pygame pytchat
(Note : pytchat n'est nécessaire que si vous utilisez YouTube)🚀 Installation & ConfigurationCloner le projet ou télécharger les fichiers.Préparer les dossiers (à la racine du projet) :Créez un dossier flags/ et ajoutez vos images .png (ex: usa.png, france.png).Créez un dossier sounds/ et ajoutez music.mp3, vroom.mp3, win.mp3.Configurer le script game.py :Ouvrez le fichier et modifiez la section CONFIGURATION au début :Python# Choisir la plateforme: "twitch", "youtube", ou "both"
PLATFORM = "both"

# Twitch
TWITCH_CHANNEL = "votre_chaine"
TWITCH_TOKEN = "oauth:xxxxxxxxxxxx" # Obtenir sur [https://twitchapps.com/tmi/](https://twitchapps.com/tmi/)

# YouTube
YOUTUBE_VIDEO_ID = "ID_DE_VOTRE_LIVE" # L'ID à la fin de l'URL youtube v=
🕹️ Contrôles (Clavier)ToucheActionF11Basculer en Plein ÉcranESCQuitter le jeuMCouper / Activer la musiqueCTRL + ESPACEMode Test (Simule des boosts)🌍 Comment jouer (Pour le Chat)Les spectateurs doivent simplement écrire le nom du pays ou son code dans le chat :"France" ou "fr""USA" ou "America""Bresil" ou "br"... et bien d'autres (Maroc, Algérie, Canada, Japon, etc.)Tout pays non listé dans les 12 principaux fera avancer la voiture "AUTRE".🔧 Structure des fichiersPlaintext📁 Racine du projet
├── game.py            # Le code principal
├── README.md          # Ce fichier
├── 📁 flags/          # Vos drapeaux (optionnel, sinon utilise des couleurs)
│   ├── france.png
│   ├── usa.png
│   └── ...
└── 📁 sounds/         # Vos sons (optionnel)
    ├── music.mp3
    ├── vroom.mp3

    └── win.mp3
