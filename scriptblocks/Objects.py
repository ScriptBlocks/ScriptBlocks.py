class Objects:
  def __init__(self):
    self.objs = []

  def get(self):
    return self.objs

  def replaceAll(self, newObjs):
    self.objs = newObjs



'''
As of writing this sentence, the Objects class is very small, difficult to understand and undocumented. Below is how the Objects class should be used:

Imagine this as an Objects list:

[
  {
    "id": "fake-sprite-id-name",
    "type": "Sprite",
    "posX": 0,
    "posY": 0,
    "width": 0,
    "height": 0,
    "rotation": 0,
    "visible": True,
    "color": (255, 255, 255),
    "image": "assets/sprites/sprite.png",
    "children": [
      {
        "id": "example-node",
        "type": "Node",
        "posX": 0,
        "posY": 0
      }
    ]
  }
]
'''