<div style="border: 1px solid black; padding: 10px;">

<div align="center">
  <h1><strong>Projet CRM EpicEvent</strong></h1>
</div>

<div align="center" style="border: 1px solid black; padding: 10px;">
  <p>
    Bienvenue dans le projet CRM ! Ce système de gestion de la relation client (CRM)
    est développé en Python avec l'architecture MVC (Modèle-Vue-Contrôleur) et utilise
    le framework Peewee pour la gestion de la base de données PostgreSQL.
  </p>
</div>

<div align="center">
  <h1><strong>Cloner le Dépôt</strong></h1>
</div>

<div align="center" style="border: 1px solid black; padding: 10px;">
    <h1>Instructions pour cloner un dépot depuis pycharm</h1>
    <ul style="list-style-type: none; padding: 0; text-align: left;">
        <li>Etape1: Pour les utilisateur de la version pycharm communautaire
        2023.3.5 il est recommandé de passer sur l'ancienne version UI
        afin de trouver l'onglet " Git " 
        </li>
        <li>
        Dans le menu deroulant de git vous verrez une option " clone ", dans celui-ci renseigné le depot distant suivant: <a href="https://github.com/Saurelien/OPC_P12_CRM.git">Depot github</a></a>
        </li>
        <li>
        Cette action vous créera un nouveau projet du nom du dépot distant.
        </li>
    </ul>
</div>


<div align="center">
  <h1><strong>Installation de PostgreSQL</strong></h1>
</div>

<div align="center" style="border: 1px solid black; padding: 10px;">
    <h1>Sous Windows 10+</h1>
    <ul style="list-style-type: none; padding: 0; text-align: left;">
        <li>1- Téléchargez l'installeur de PostgreSQL depuis <a href="https://www.postgresql.org/download/windows/">ce lien</a>.</li>
        <li>2- Exécutez l'installeur téléchargé et suivez les instructions à l'écran pour installer PostgreSQL.</li>
        <li>3- Lors de l'installation, notez les paramètres tels que le nom d'utilisateur et le mot de passe que vous définissez pour l'utilisateur administrateur de PostgreSQL. </li>
        <li>4- Après l'installation, assurez-vous que le service PostgreSQL est en cours d'exécution en vérifiant sa présence dans le gestionnaire des taches de windows.</li>
    </ul>
</div>
<div align="center" style="border: 1px solid black; padding: 10px;">
    <h1>Sous Linux</h1>
    <ul style="list-style-type: none; padding: 0; text-align: left;">
        <li>1- Sur la pluspart des Os Linux,Linux, PostgreSQL est disponible dans les dépôts officiels. Vous pouvez l'installer en utilisant le gestionnaire de paquets.</li>
        <li><code style="font-weight: bold;">sudo apt update</code></li>
        <li><code style="font-weight: bold;">sudo apt install postgresql</code></li>
    </ul>
</div>

<div align="center">
  <h1><strong>Installation des dépendances</strong></h1>
</div>

<div align="center" style="border: 1px solid black; padding: 10px;">
    <h1>Installez les dépendances du projet à partir du fichier </h1>
    <ul style="list-style-type: none; padding: 0; text-align: left;">
        <li><code style="font-weight: bold;">pip install -r requirements.txt</code></li>
    </ul>
</div>