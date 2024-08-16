from scriptblocks import App, Sprite

testApp = App()

testSprite = Sprite("image.png")
testSprite.width = testApp.width * 0.2

testApp.objects.add(testSprite.getRaw())

testApp.render()