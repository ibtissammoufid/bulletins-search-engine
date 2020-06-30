# bulletins-search-engine
Etape 1 : Installer Elasticsearch 
Etape 2 : Installer Fscrawler ( attention, télécharger la bonne version de fscrawler qui est compatible avec votre version Elasticsearch (vous pouvez confirmer la compatibilité des versions sur la page github de Fscrawler))
Etape 3 : mettre les fichiers que vous aimeriez pouvoir rechercher dans un dossier dans le meme emplacement (dossier) où vous avez installé Fscawler
Etape 4 : Ouvrez ensuite le terminal et accédez à l'emplacement d'installation de Fscrawler
Etape 5 : Executer la commande suivante pour créeer un index "search_index" bin\fscrawler — config_dir ./DS search_index — loop 1
Etape 6 : Accédez à l'emplacement d'installation de fscrawler> DS> search_index et ouvrez le fichier ‘_settings’, changer la valeur de l'attribut url par le chemin du document contenant les fichiers à indexer.
Etape 7 : Réxecuter la commande de l'etape 5.
Etape 8 : Configuration des dependencies Python. Executer les commandes suivantes : python -m pip install flask,
python -m pip install Elasticsearch, pip install Flask-WTF, pip install flask-sqlalchemy, pip install flask-bcrypt
Etape 9 : Executer le script run.py
Etape 10 : Ouvrez votre navigateur et accédez à http://127.0.0.1:5000