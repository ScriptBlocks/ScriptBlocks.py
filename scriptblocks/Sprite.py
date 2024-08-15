class Sprite:
  def __init__(self, path):
    self.id = ""
    
    self.posX = 0
    self.posY = 0
    self.width = 0
    self.height = 0
    self.rotation = 0

    self.visible = True
    
    self.color = (255, 255, 255)
    self.image = path

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

  def getRaw(self):
    return {
      "id": self.id,
      "type": "Sprite",
      "posX": self.posX,
      "posY": self.posY,
      "width": self.width,
      "height": self.height,
      "rotation": self.rotation,
      "visible": self.visible,
      "color": self.color,
      "image": self.image,
      "children": []
    }