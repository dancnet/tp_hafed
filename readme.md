# Description de la solution
C'est un groupe de conteneurs Docker qui forment une pipile de génération, d'ingestion et de traitement de données. En voici les composants:

1. Les données sont générés et envoyés à Kafka en batches.
2. Les données sont ensuite traités avec Spark (2 workers)
3. Le résultat est sauvegardé dans HBase

Les 20 fichiers sont analysés pour déterminer, pour chaque appareil, combien de fois une action a été executé.

# Installation de la solution
Elle s'installe avec Docker Compose:
```
docker compose up
```
# Execution
**Utilisez toujours l'interpreteur `/usr/local/bin/python`!**

Il faut aller dans le conteneur my-app dans le dossier `/app` et executer le script `init.py` afin de créer le Kafka topic et la table dans HBase.

Ensuite, executez `pipeline.py`. Il va être en attente. Une fois que les données arrivent dans Kafka, il va les procésser avec Spark et stocker le résultat dans HBase.

Commencez à lancer des batch de données. Chaque fichier constitut un batch et chaque batch est envoyé à 20 seconds d'écart. Utilisez le script `data_generator.py`.

Dans le conteneur HBase vous pouvez voir les résultats dans la table `devices`.