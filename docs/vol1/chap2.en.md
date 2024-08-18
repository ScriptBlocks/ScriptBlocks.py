# Object Management

Now that we have created our app, we need to put stuff inside it. So, here's how:

We have a method in the App class called `App().objects`. This is a class embedded in a class, however we cannot initialise it. We can only call functions in it. Here are the functions we can call in it:

```py
from scriptblocks import App, Sprite

app = App()

testSprite = Sprite("image.png")

app.objects.add(testSprite.getRaw())
```