# Modélisation du projet

### Objectifs du projet

Dans un entrepôt fictif, acheminer des colis d'un point A à un point B grâce à flotte de 3 robots , suivant les commandes qui arrivent

- Amener des colis de stocks dans une zone de dépôt en un temps raisonnable
- Bien vérifier la localisation des robots
- Implémenter l'optimisation du chemin
- Connecter les robots
- Recevoir une liste d'ordres et les traiter correctement (dans l'ordre ou par priorité -> ici dans l'ordre)


### Découpage du projet et questions principales

- Déplacement du robot :
    - Contrôler le robot et sa trajectoire (commande robuste des sytèmes, etc)
    - Décider du chemin à suivre (systèmes multi-agents, optimisation, etc)
- Communication :
    - Architecture centralisée VS architecture distribuée : est-ce que les robots communiquent entre eux via un système centralisé ou pas ?
    - Comment communiquer avec un robot ? Notamment pour fournir les commandes
- Gestion des commandes :
    - Dans quel ordre les distribuer et à qui ? Quelle stratégie adopter ?
- Localiser les robots :
    - Les robots se localisent eux-mêmes ? Ou système de localisation centralisé ?



On développe qu'une partie du robot (pas le chassis mais le code)

On développe pas l'entrepôt

De quel état part le système ?

Comment l'utilisateur intéragit ? Qu'est ce qui se déclenche ?





But :

* Le système doit pouvoir livrer les commandes d'un client.
* Le système doit pouvoir récolter et enregistrer des commandes.
* Le système doit pouvoir informer le client que la commande a été livrée ou si elle est en rupture de stock.

De quel état part le système ?
* A l'état initial, le système est juste en mode attente. Il ne se passe rien en attendant la première commande.

Comment l'utilisateur intéragit ?
* L'utilisateur donne une liste de commandes à réaliser.

Qu'est ce qui se déclenche ?
* Le système se met en marche pour honorer les commandes.

