# Nour Chatbot - Assistant Vocal pour le Cancer du Sein 🎗️

**Nour** est une assistante virtuelle empathique et vocale conçue pour accompagner les femmes marocaines atteintes du cancer du sein. Elle agit comme une "grande sœur" bienveillante (*khti*), fournissant des informations médicales fiables et un soutien émotionnel en **Darija** et en **Français**.

## 🌟 Fonctionnalités Clés

- **🗣️ Interface Voice-First** : Conçue pour l'accessibilité, notamment pour les utilisatrices analphabètes ou fatiguées. L'utilisatrice parle, et Nour répond oralement.
- **🇲🇦 Support Bilingue Adapté** :
    - **Entrée** : Comprend le Darija, le Français et l'Arabe.
    - **Sortie Visuelle** : Texte en **Français** (pour la clarté médicale et la lecture).
    - **Sortie Audio** : Voix en **Darija** (pour la proximité émotionnelle et la compréhension).
- **🧠 Intelligence Artificielle Avancée** :
    - **RAG (Retrieval Augmented Generation)** : Utilise une base de connaissances médicale vérifiée pour répondre aux questions.
    - **Détection d'Émotion** : Adapte son ton si l'utilisatrice exprime de la peur ou de la détresse.
- **🛡️ Sécurité & Éthique** :
    - Ne fait **jamais** de diagnostic médical.
    - Ne prescrit **jamais** de médicaments.
    - Redirige vers les urgences en cas de crise critique.

## 🏗️ Architecture Technique

L'application suit une architecture client-serveur moderne :

### Frontend (Client)
- **Framework** : React 19 + Vite
- **Styling** : TailwindCSS (Design responsive et épuré)
- **Composants Clés** :
    - `AudioRecorder.jsx` : Gestion de l'enregistrement vocal et visualisation audio.
    - `App.jsx` : Orchestration de l'interface de chat.

### Backend (Serveur)
- **Framework** : FastAPI (Python)
- **Services** :
    - **STT (Speech-to-Text)** : Transcription de l'audio utilisateur (Gemini/OpenAI).
    - **LLM (Logic)** : Google Gemini (Modèle `gemini-2.5-flash`) pour la génération de réponse et l'analyse d'intention.
    - **RAG** : ChromaDB pour le stockage vectoriel de la base de connaissances (`knowledge.json`).
    - **TTS (Text-to-Speech)** : Génération de la réponse audio en Darija.

## 🚀 Installation et Démarrage

### Pré-requis
- Node.js & npm
- Python 3.9+
- Clé API Google Gemini (dans un fichier `.env`)

### 1. Backend
```bash
cd backend
python -m venv venv
# Windows
.\venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
uvicorn main:app --reload
```
Le serveur sera accessible sur `http://localhost:8000`.

### 2. Frontend
```bash
cd frontend
npm install
npm run dev
```
L'application sera accessible sur `http://localhost:5173`.

## 📂 Structure du Projet

```
nour_chatbot/
├── backend/
│   ├── data/               # Base de connaissances (knowledge.json)
│   ├── services/           # Logique métier (LLM, RAG, STT, TTS)
│   ├── chroma_db/          # Base de données vectorielle
│   ├── main.py             # Point d'entrée API
│   ├── ingest.py           # Script d'ingestion des données RAG
│   └── requirements.txt    # Dépendances Python
└── frontend/
    ├── src/
    │   ├── components/     # Composants React (AudioRecorder...)
    │   ├── App.jsx         # Main UI
    │   └── index.css       # Styles Tailwind
    ├── package.json        # Dépendances Node
    └── vite.config.js      # Configuration Vite
```

## 🛡️ Guardrails (Sécurité)

Le système de prompts (`prompts.py`) impose des limites strictes :
1.  **NO PERSONAL DIAGNOSIS** : Interdiction de diagnostiquer.
2.  **EDUCATIONAL ONLY** : Fournit des explications générales sur les symptômes et traitements.
3.  **NO PRESCRIPTIONS** : Refus de modifier les traitements médicaux.
4.  **EMERGENCY** : Redirection immédiate si des mots-clés de danger (suicide, crise cardiaque) sont détectés.

---
*Développé avec ❤️ pour R&D S9.*
