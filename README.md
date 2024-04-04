># | **Projet CRM EpicEvent** |
>
>> Bienvenue dans le projet CRM ! Ce système de gestion de la relation client (CRM) 
est développé en Python avec l'architecture MVC (Modèle-Vue-Contrôleur)
et utilise le framework Peewee pour la gestion de la base de données PostgreSQL.
>##  | **Cloner le Dépôt** |
>
>>### Instructions pour cloner un dépôt depuis PyCharm
>>
>> - Pour les utilisateurs de la version PyCharm communautaire 2023.3.5, il est recommandé de passer sur l'ancienne version UI afin de trouver l'onglet "Git".
>>   - Dans le menu déroulant de Git, vous verrez une option "Clone". Renseignez le dépôt distant suivant: [Depot github](https://github.com/Saurelien/OPC_P12_CRM.git).
>>   - Cette action vous créera un nouveau projet du nom du dépôt distant.
>## | **Installation de PostgreSQL** |
>
>>### Sous Windows 10+
>>- Téléchargez l'installeur de PostgreSQL depuis [ce lien](https://www.postgresql.org/download/windows/).
>>  - Exécutez l'installeur téléchargé et suivez les instructions à l'écran pour installer PostgreSQL.
>>  - Lors de l'installation, notez les paramètres tels que le nom d'utilisateur et le mot de passe que vous définissez pour l'utilisateur administrateur de PostgreSQL.
>>  - Après l'installation, assurez-vous que le service PostgreSQL est en cours d'exécution en vérifiant sa présence dans le gestionnaire des tâches de Windows.
>
>>### Sous Linux
>> - Sur la plupart des OS Linux, PostgreSQL est disponible dans les dépôts officiels. Vous pouvez l'installer en utilisant le gestionnaire de paquets. 
>>```bash
>> sudo apt update
>> sudo apt install postgresql
># | **Installation des dépendances** |
>>### Installez les dépendances du projet à partir du fichier requirements.txt.
>> 
>> - pip install -r requirements.txt