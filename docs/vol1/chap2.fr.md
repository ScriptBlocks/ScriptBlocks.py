# Gestion des objets

Maintenant que nous avons créé notre application, nous devons y ajouter des éléments. Voici comment procéder :

Nous avons une méthode dans la classe App appelée `App().objects`. C'est une classe intégrée dans une classe, mais nous ne pouvons pas l'initialiser. Nous pouvons seulement appeler des fonctions à l'intérieur. Voici les fonctions que nous pouvons appeler :

```py
from scriptblocks import App, Sprite

app = App()

testSprite = Sprite("image.png")

app.objects.add(testSprite.getRaw())
```