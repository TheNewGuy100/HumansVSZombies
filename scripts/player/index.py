
from scripts.player.checkPlayerDead_sub import playerCheckDead
from scripts.player.drawPlayer_sub import drawPlayerInit
from scripts.player.playerAnimations_sub import playerAnimations
from scripts.player.playerMovement_sub import playerMovement

PLAYER_START_X = 6
PLAYER_START_Y = 53


class playerClass(
    drawPlayerInit,
    playerMovement,
    playerCheckDead,
    playerAnimations
):
    player_x = PLAYER_START_X
    player_y = PLAYER_START_Y
    player_vy = 0
    player_is_alive = True

    def resetPlayer(self):
        self.player_x = PLAYER_START_X
        self.player_y = PLAYER_START_Y
        self.player_vy = 0
        self.player_is_alive = True
        self.shoot_delay = 0

    # GAME UPDATES MID-GAME
    def updatePlayer(self):
        self.checkPlayerAnimations()
        self.checkPlayerDead()
        self.checkPlayerMovement()
