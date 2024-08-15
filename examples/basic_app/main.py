from scriptblocks import App, Sprite

testApp = App()

testSprite = Sprite("image.png")
testApp.objects.add(testSprite.getRaw())

testApp.render()