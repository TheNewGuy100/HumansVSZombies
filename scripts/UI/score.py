
import pyxel


class scoreClass():
    score = 0

    def resetScore(self):
        self.score = 0

    def drawScore(self):
        s = "SCORE: {:>4}".format(self.score)
        pyxel.text(2, 10, s, 0)
        pyxel.text(55, 10, "LEVEL: {:>3}".format(self.getLevel()), 0)
        pyxel.text(112, 2, "[P] PAUSE", 0)
