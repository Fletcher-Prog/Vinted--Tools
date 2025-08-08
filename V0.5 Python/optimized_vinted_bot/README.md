# 🤖 Optimized Vinted Discord Bot v2.0

Un bot Discord avancé pour surveiller automatiquement les nouvelles annonces Vinted et les publier en temps réel.

## ✨ Fonctionnalités

### 🎯 Fonctionnalités principales
- **Surveillance automatique** des recherches Vinted personnalisées
- **Publication instantanée** des nouveaux articles dans Discord
- **Interface Discord intuitive** avec commandes simples
- **Gestion multi-canaux** - chaque canal peut avoir sa propre recherche

### 🔄 Système de proxies avancé
- **Rotation automatique** des proxies pour éviter les limitations
- **Monitoring de santé** des proxies en temps réel
- **Retry automatique** en cas d'échec
- **Support multiple formats** (HTTP, HTTPS, SOCKS5)

### 📊 Monitoring et statistiques
- **Tableau de bord complet** avec statistiques détaillées
- **Logs structurés** avec rotation automatique
- **Base de données SQLite** pour le tracking des articles
- **Système d'alertes** en cas d'erreur

### 🛡️ Robustesse
- **Gestion d'erreurs avancée** avec retry automatique
- **Rate limiting intelligent** pour respecter les limites de l'API
- **Cache intelligent** pour optimiser les performances
- **Arrêt gracieux** avec sauvegarde des données

## 🚀 Installation

### Prérequis
- Python 3.8+
- Compte Discord avec bot token
- (Optionnel) Proxies pour éviter les limitations

### 1. Cloner le projet
```bash
git clone <repository-url>
cd optimized_vinted_bot
```

### 2. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 3. Configuration

#### Configuration Discord
1. Créez un bot Discord sur https://discord.com/developers/applications
2. Copiez le token du bot
3. Invitez le bot sur votre serveur avec les permissions nécessaires

#### Configuration des variables d'environnement
```bash
# Copiez le fichier d'exemple
cp env_example.txt .env

# Éditez le fichier .env avec vos valeurs
nano .env
```

Variables importantes :
```env
DISCORD_BOT_TOKEN=votre_token_discord
PROXY_ENABLED=true
PROXY_ROTATION_ENABLED=true
LOG_LEVEL=INFO
```

#### Configuration des proxies (optionnel)
Éditez le fichier `config/proxy_list.txt` :
```
# Format: protocol://username:password@host:port
http://user:pass@proxy1.example.com:8080
http://user:pass@proxy2.example.com:8081
socks5://user:pass@proxy3.example.com:1080
```

### 4. Lancement
```bash
python main.py
```

## 📖 Utilisation

### Commandes Discord

#### `!addlink <url>`
Ajoute une URL de recherche Vinted à surveiller
```
!addlink https://www.vinted.fr/catalog?search_text=nike&price_to=50
```

#### `!removelink`
Supprime la surveillance pour ce canal
```
!removelink
```

#### `!viewlink`
Affiche la configuration actuelle du canal
```
!viewlink
```

#### `!test [url]`
Teste une URL de recherche
```
!test https://www.vinted.fr/catalog?search_text=adidas
```

#### `!stats`
Affiche les statistiques du bot
```
!stats
```

#### `!help`
Affiche l'aide
```
!help
```

### Workflow typique

1. **Préparer votre recherche** sur vinted.com
   - Allez sur vinted.com
   - Effectuez votre recherche (mots-clés, prix, taille, etc.)
   - Copiez l'URL de la page de résultats

2. **Configurer le bot**
   ```
   !addlink https://www.vinted.fr/catalog?search_text=your_search
   ```

3. **Le bot surveille automatiquement** et publie les nouveaux articles

## 🏗️ Architecture

### Structure du projet
```
optimized_vinted_bot/
├── config/
│   ├── settings.py          # Configuration centralisée
│   └── proxy_list.txt       # Liste des proxies
├── core/
│   ├── proxy_manager.py     # Gestion des proxies
│   ├── vinted_api.py        # Client API Vinted
│   └── database.py          # Gestion base de données
├── discord_bot/
│   └── bot.py              # Bot Discord principal
├── utils/
│   └── logging_setup.py    # Configuration logging
├── logs/                   # Fichiers de logs
├── data/                   # Base de données
├── requirements.txt        # Dépendances
├── main.py                # Point d'entrée
└── README.md              # Documentation
```

### Composants clés

#### ProxyManager
- Rotation intelligente des proxies
- Monitoring de santé en temps réel
- Support de multiples formats de proxies
- Retry automatique en cas d'échec

#### VintedAPIClient
- Communication directe avec l'API Vinted
- Cache intelligent pour optimiser les performances
- Rate limiting pour respecter les limites
- Gestion d'erreurs robuste

#### DatabaseManager
- Stockage SQLite pour le tracking des articles
- Évite les doublons automatiquement
- Statistiques et monitoring
- Nettoyage automatique des anciennes données

#### VintedDiscordBot
- Interface Discord complète
- Commandes intuitives
- Gestion multi-canaux
- Monitoring en temps réel

## ⚙️ Configuration avancée

### Paramètres de proxy
```python
# Dans config/settings.py
@dataclass
class ProxySettings:
    enabled: bool = True
    rotation_enabled: bool = True
    max_retries: int = 3
    timeout: int = 10
    health_check_interval: int = 300  # 5 minutes
```

### Paramètres API
```python
@dataclass
class VintedAPISettings:
    base_url: str = "https://www.vinted.com"
    rate_limit_delay: float = 1.0  # secondes entre requêtes
    max_retries: int = 5
    timeout: int = 30
```

### Paramètres monitoring
```python
@dataclass
class MonitoringSettings:
    enabled: bool = True
    health_check_interval: int = 60  # secondes
    metrics_retention_days: int = 7
    alert_threshold_error_rate: float = 0.1  # 10% d'erreurs
```

## 📊 Monitoring

### Logs
Les logs sont automatiquement sauvegardés dans `logs/vinted_bot.log` avec rotation automatique.

Niveaux de logs :
- `DEBUG` : Informations détaillées de débogage
- `INFO` : Informations générales de fonctionnement
- `WARNING` : Avertissements non critiques
- `ERROR` : Erreurs nécessitant attention
- `CRITICAL` : Erreurs critiques

### Base de données
La base de données SQLite stocke :
- Articles publiés (évite les doublons)
- Configurations des canaux
- Statistiques du bot
- Logs d'erreurs

### Statistiques en temps réel
Utilisez `!stats` pour voir :
- Uptime du bot
- Nombre d'articles publiés
- Taux de succès des requêtes API
- État des proxies
- Statistiques de la base de données

## 🔧 Dépannage

### Problèmes courants

#### Bot ne démarre pas
1. Vérifiez le token Discord dans `.env`
2. Vérifiez que Python 3.8+ est installé
3. Vérifiez que toutes les dépendances sont installées

#### Pas de nouveaux articles détectés
1. Testez l'URL avec `!test <url>`
2. Vérifiez les logs pour les erreurs
3. Vérifiez que l'URL Vinted est correcte

#### Erreurs de proxy
1. Vérifiez la configuration dans `config/proxy_list.txt`
2. Testez les proxies manuellement
3. Désactivez les proxies temporairement avec `PROXY_ENABLED=false`

#### Performances dégradées
1. Vérifiez les statistiques avec `!stats`
2. Analysez les logs pour identifier les goulots d'étranglement
3. Ajustez les paramètres de rate limiting

### Logs utiles
```bash
# Voir les logs en temps réel
tail -f logs/vinted_bot.log

# Rechercher des erreurs
grep "ERROR" logs/vinted_bot.log

# Voir les statistiques de proxy
grep "proxy" logs/vinted_bot.log
```

## 🤝 Contribution

Les contributions sont les bienvenues ! Pour contribuer :

1. Fork le projet
2. Créez une branche pour votre fonctionnalité
3. Committez vos changements
4. Pushez vers la branche
5. Ouvrez une Pull Request

## 📜 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## ⚠️ Avertissements

- **Utilisation responsable** : Respectez les conditions d'utilisation de Vinted
- **Rate limiting** : Le bot implémente des délais pour éviter la surcharge
- **Proxies** : Utilisez des proxies de qualité pour éviter les bannissements
- **Monitoring** : Surveillez régulièrement les logs pour détecter les problèmes

## 📞 Support

Pour obtenir de l'aide :
1. Consultez cette documentation
2. Vérifiez les logs d'erreur
3. Ouvrez une issue sur GitHub avec les détails du problème

---

**Note** : Ce bot utilise l'API publique de Vinted et respecte leurs limitations de taux. Il est conçu pour un usage personnel et éducatif.
