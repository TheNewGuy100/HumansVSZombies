
import pyxel


class healthBarStatus():
    health = 100

    def resetHealth(self):
        self.health = 100

    def drawHealthBar(self):
        healthDraw = "HEALTH: {:>4}".format(max(self.health, 0))
        pyxel.text(2, 2, healthDraw, 8)
