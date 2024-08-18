# Créer votre première application

Créer des applications peut être difficile, mais avec ScriptBlocks, il est beaucoup plus facile de créer des applications à partir de zéro. Voici comment procéder :

Tout d'abord, ouvrez votre projet ScriptBlocks, si applicable. Ensuite, regardez le panneau principal au centre - c'est là que nous allons taper notre code. Ensuite, tapez le code suivant - c'est le code de base pour notre application :

```py
import scriptblocks

app = scriptblocks.App()
app.name = "Ma première application !"
app.version = "v1.0.0-alpha.1"
app.author = "OmgRod"

app.render()
```
Voyons maintenant le code:

- La ligne 3 initialise l'application
- Les lignes 4 à 6 définissent les informations sur l'application
- La ligne 8 crée la fenêtre de l'application

C'est tout pour la création d'applications, passons maintenant à la gestion des objets.