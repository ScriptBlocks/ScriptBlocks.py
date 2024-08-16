class Node:
  def __init__(self):
    self.id = ""
    self.posX = 0.0
    self.posY = 0.0
    self.visible = True

  def getRaw(self):
    return {
      "id": self.id,
      "type": "Node",
      "posX": self.posX,
      "posY": self.posY,
      "visible": self.visible,
      "children": []
    }

# tbh idk why im here