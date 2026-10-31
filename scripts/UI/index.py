
from scripts.UI.ammoBar import ammoBar
from scripts.UI.healthBar import healthBarStatus
from scripts.UI.options import optionsClass
from scripts.UI.score import scoreClass


class UIUpdate(
    optionsClass,
    scoreClass,
    healthBarStatus,
    ammoBar
):
    def drawUI(self):
        self.drawScore()
        self.drawHealthBar()
        self.drawAmmoBar()
