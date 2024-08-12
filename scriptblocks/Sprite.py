class Sprite:
  def __init__(self, path):
    self.posX = 0
    self.posY = 0
    self.width = 0
    self.height = 0
    self.rotation = 0

    self.visible = True
    
    self.color = (255, 255, 255)
    self.image = path

    self.type = "Sprite"

  def changePos(self, x, y):
    self.posX += x
    self.posY += y

  def changeSize(self, width, height):
    self.width += width
    self.height += height

  def changeRotation(self, rotation):
    self.rotation += rotation

  def toggleVisible(self):
    self.visible = not self.visible