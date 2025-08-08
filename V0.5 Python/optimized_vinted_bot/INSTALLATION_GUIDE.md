# 🚀 Guide d'Installation - Bot Vinted Discord Optimisé

Ce guide vous accompagnera pas à pas pour installer et configurer le bot Vinted Discord optimisé.

## 📋 Prérequis

### Système
- **Système d'exploitation** : Linux, macOS, ou Windows
- **Python** : Version 3.8 ou supérieure
- **Connexion Internet** stable
- **Espace disque** : Au moins 100 MB libres

### Comptes et services
- **Compte Discord** avec permissions pour créer des bots
- **Serveur Discord** où vous avez les permissions d'administration
- **(Optionnel)** Service de proxies pour éviter les limitations

## 📥 Installation

### Étape 1 : Téléchargement du projet

```bash
# Cloner le repository (ou télécharger le ZIP)
git clone <repository-url>
cd optimized_vinted_bot
```

### Étape 2 : Configuration Discord

#### 2.1 Créer une application Discord
1. Allez sur https://discord.com/developers/applications
2. Cliquez sur "New Application"
3. Donnez un nom à votre application (ex: "Vinted Bot")
4. Cliquez sur "Create"

#### 2.2 Créer un bot
1. Dans votre application, allez dans l'onglet "Bot"
2. Cliquez sur "Add Bot"
3. Copiez le **Token** du bot (vous en aurez besoin plus tard)
4. Activez les "Privileged Gateway Intents" :
   - ✅ Presence Intent
   - ✅ Server Members Intent
   - ✅ Message Content Intent

#### 2.3 Inviter le bot sur votre serveur
1. Allez dans l'onglet "OAuth2" > "URL Generator"
2. Sélectionnez les scopes :
   - ✅ `bot`
   - ✅ `applications.commands`
3. Sélectionnez les permissions du bot :
   - ✅ Send Messages
   - ✅ Use Slash Commands
   - ✅ Embed Links
   - ✅ Attach Files
   - ✅ Read Message History
   - ✅ Add Reactions
4. Copiez l'URL générée et visitez-la pour inviter le bot

### Étape 3 : Installation automatique

Le script d'installation automatique s'occupe de tout :

```bash
# Rendre le script exécutable
chmod +x start_bot.sh

# Lancer l'installation et la configuration
./start_bot.sh
```

Le script va :
- ✅ Créer l'environnement virtuel Python
- ✅ Installer toutes les dépendances
- ✅ Créer le fichier de configuration
- ✅ Vous guider pour la configuration

### Étape 4 : Configuration

#### 4.1 Configuration de base
Éditez le fichier `.env` créé automatiquement :

```bash
nano .env
```

Configuration minimale requise :
```env
# Token du bot Discord (OBLIGATOIRE)
DISCORD_BOT_TOKEN=votre_token_discord_ici

# Configuration des proxies (OPTIONNEL)
PROXY_ENABLED=true
PROXY_ROTATION_ENABLED=true

# Niveau de logs (OPTIONNEL)
LOG_LEVEL=INFO
```

#### 4.2 Configuration des proxies (optionnel)

Si vous avez des proxies, éditez le fichier `config/proxy_list.txt` :

```bash
nano config/proxy_list.txt
```

Format supporté :
```
# Proxies HTTP avec authentification
http://username:password@proxy1.provider.com:8080
http://username:password@proxy2.provider.com:8081

# Proxies SOCKS5
socks5://username:password@proxy3.provider.com:1080

# Proxies sans authentification
192.168.1.100:8080
```

## 🧪 Test de l'installation

### Test automatique
```bash
./start_bot.sh --test
```

### Test manuel
```bash
# Activer l'environnement virtuel
source venv/bin/activate

# Lancer les tests
python3 tests/test_functionality.py
```

Les tests vérifieront :
- ✅ Configuration
- ✅ Base de données
- ✅ Système de proxies
- ✅ API Vinted
- ✅ Logs

## 🚀 Démarrage du bot

### Démarrage simple
```bash
./start_bot.sh
```

### Démarrage manuel
```bash
# Activer l'environnement virtuel
source venv/bin/activate

# Démarrer le bot
python3 main.py
```

### Démarrage en arrière-plan (Linux/macOS)
```bash
# Avec nohup
nohup ./start_bot.sh > bot_output.log 2>&1 &

# Avec screen
screen -S vinted_bot ./start_bot.sh

# Avec tmux
tmux new-session -d -s vinted_bot './start_bot.sh'
```

## ✅ Vérification du fonctionnement

### 1. Vérifier les logs
```bash
# Voir les logs en temps réel
tail -f logs/vinted_bot.log

# Voir les dernières lignes
tail -20 logs/vinted_bot.log
```

### 2. Tester dans Discord
Dans un canal de votre serveur Discord :
```
!help
```
Vous devriez voir apparaître l'aide du bot.

### 3. Tester une recherche
```
!test https://www.vinted.fr/catalog?search_text=nike
```

## 🔧 Résolution des problèmes

### Problème : "Module not found"
**Solution** : Réinstallez les dépendances
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Problème : "Invalid Discord token"
**Solution** : Vérifiez votre token Discord
1. Allez sur https://discord.com/developers/applications
2. Sélectionnez votre application
3. Onglet "Bot" > Copiez le nouveau token
4. Mettez à jour le fichier `.env`

### Problème : "Permission denied"
**Solution** : Vérifiez les permissions du bot Discord
1. Réinvitez le bot avec les bonnes permissions
2. Vérifiez que le bot a accès au canal

### Problème : "No items found"
**Solutions possibles** :
1. Vérifiez que l'URL Vinted est correcte
2. Testez sans proxies : `PROXY_ENABLED=false`
3. Vérifiez les logs pour plus de détails

### Problème : "Database locked"
**Solution** : Redémarrez le bot
```bash
# Arrêter le bot (Ctrl+C)
# Puis relancer
./start_bot.sh
```

## 📊 Monitoring

### Voir les statistiques
Dans Discord :
```
!stats
```

### Surveiller les logs
```bash
# Logs généraux
tail -f logs/vinted_bot.log

# Erreurs uniquement
grep "ERROR" logs/vinted_bot.log
```

### Base de données
La base de données SQLite est dans `data/published_items.db`.
Vous pouvez l'examiner avec des outils comme DB Browser for SQLite.

## 🔄 Mise à jour

### Sauvegarde
Avant toute mise à jour :
```bash
# Sauvegarder la configuration
cp .env .env.backup
cp config/proxy_list.txt config/proxy_list.txt.backup

# Sauvegarder la base de données
cp data/published_items.db data/published_items.db.backup
```

### Mise à jour du code
```bash
# Arrêter le bot
# Puis mettre à jour le code
git pull

# Mettre à jour les dépendances si nécessaire
source venv/bin/activate
pip install -r requirements.txt

# Redémarrer
./start_bot.sh
```

## 📞 Support

### Logs utiles pour le support
```bash
# Collecter les informations de debug
echo "=== Configuration ===" > debug_info.txt
cat .env >> debug_info.txt
echo "" >> debug_info.txt

echo "=== Derniers logs ===" >> debug_info.txt
tail -50 logs/vinted_bot.log >> debug_info.txt
echo "" >> debug_info.txt

echo "=== Statistiques système ===" >> debug_info.txt
python3 -c "import sys; print(f'Python: {sys.version}')" >> debug_info.txt
```

### Ressources
- **Documentation** : README.md
- **Tests** : `python3 tests/test_functionality.py`
- **Logs** : `logs/vinted_bot.log`

---

🎉 **Félicitations !** Votre bot Vinted Discord est maintenant installé et configuré.

Pour utiliser le bot, consultez le fichier `README.md` pour la liste des commandes disponibles.
