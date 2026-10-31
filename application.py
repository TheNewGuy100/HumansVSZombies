
import pyxel
from scripts.UI.headshotFeedBack import headShotPopUp
from scripts.UI.index import UIUpdate
from scripts.background.blackground import BackgroundClass
from scripts.mechanics.ammoFind import ammoSpawner
from scripts.mechanics.enemies import enemyClass
from scripts.mechanics.medkitFind import medkitSpawner
from scripts.player.index import playerClass
from scripts.player.playerShoot import bulletsController
from scripts.state.gameState import gameStateClass


class App(
        gameStateClass,
        playerClass,
        enemyClass,
        BackgroundClass,
        UIUpdate,
        bulletsController,
        ammoSpawner,
        medkitSpawner,
        headShotPopUp
    ):

    APP_HEIGHT = 120
    APP_WIDTH = 160

    APP_Y_MIN_PLAYABLE_AREA = 30
    APP_Y_MAX_PLAYABLE_AREA = 100
    APP_X_MIN_PLAYABLE_AREA = 0
    APP_X_MAX_PLAYABLE_AREA = 160

    def __init__(self):
        pyxel.init(
            self.APP_WIDTH,
            self.APP_HEIGHT,
            title="Zombies Invasion 1.0",
            quit_key=pyxel.KEY_NONE     # o ESC agora pausa; para sair use o menu de pausa
        )
        pyxel.load("assets/sprites.pyxres")
        self.resetGame()

    def run(self):
        pyxel.run(
            self.update,
            self.draw
        )

    def draw(self):
        self.drawBackground()
        self.drawUI()
        self.drawPlayer()
        self.drawBullets()
        self.drawEnemys()
        self.drawAmmoBox()
        self.drawMedkitBox()
        self.drawHeadShots()
        self.drawStateOverlay()

    def update(self):
        self.updateGameState()
        if not self.isPlaying():
            return

        self.game_frame += 1
        self.updatePlayer()
        if not self.isPlaying():
            return

        self.updateBackground()
        self.updateBullet()
        self.updateEnemys()
        self.updateAmmoBox()
        self.updateMedkitBox()
        self.spawnAmmoInMap()
        self.spawnMedkitInMap()
        self.updateHeadShots()


# APPLICATION CALL
if __name__ == "__main__":
    App().run()
