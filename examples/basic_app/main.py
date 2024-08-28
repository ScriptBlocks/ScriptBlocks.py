from scriptblocks import App, Sprite

testApp = App(width=800, height=600, mode="windowed")

testSprite = Sprite("image.png")
testSprite.width = testApp.width * 0.2

testApp.objects.add(testSprite.getRaw())

testApp.render()