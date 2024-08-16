class Button:
  def __init__(self, text):
    self.text = text
    self.x = 0.0
    self.y = 0.0
    self.width = 0.0
    self.height = 0.0
    self.color = (255, 255, 255)
    self.onClick = None
    self.onHover = None
    self.visible = True
    self.id = ""

  def getRaw(self):
    return {
      "id": self.id,
      "type": "Button",
      "text": self.text,
      "x": self.x,
      "y": self.y,
      "width": self.width,
      "height": self.height,
      "color": self.color,
      "onClick": self.onClick,
      "onHover": self.onHover,
      "visible": self.visible,
      "children": []
    }