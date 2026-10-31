
import pyxel

STATE_PLAYING = "playing"
STATE_PAUSED = "paused"
STATE_GAME_OVER = "game_over"


class gameStateClass():
    game_state = STATE_PLAYING
    game_frame = 0              # frames de jogo: so avanca enquanto esta jogando (o pyxel.frame_count nao para na pausa)
    high_score = 0
    menu_index = 0

    PAUSE_OPTIONS = ("RESUME", "RESTART", "QUIT")
    GAME_OVER_OPTIONS = ("PLAY AGAIN", "QUIT")

    # ---------------------------------------- RESET ----------------------------------------

    def resetGame(self):
        self.game_frame = 0
        self.game_state = STATE_PLAYING
        self.menu_index = 0
        self.resetPlayer()
        self.resetHealth()
        self.resetScore()
        self.resetAmmoBar()
        self.resetEnemies()
        self.resetBullets()
        self.resetAmmoSpawner()
        self.resetMedkitSpawner()
        self.resetHeadShots()

    # ---------------------------------------- INPUT ----------------------------------------

    def pausePressed(self):
        return pyxel.btnp(pyxel.KEY_P) or pyxel.btnp(pyxel.KEY_ESCAPE) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_START)

    def moveMenuSelection(self, option_count):
        if pyxel.btnp(pyxel.KEY_W) or pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_UP):
            self.menu_index = (self.menu_index - 1) % option_count
        if pyxel.btnp(pyxel.KEY_S) or pyxel.btnp(pyxel.KEY_DOWN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN):
            self.menu_index = (self.menu_index + 1) % option_count

    def menuConfirmed(self):
        return pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A)

    # ---------------------------------------- STATES ---------------------------------------

    def pauseGame(self):
        self.game_state = STATE_PAUSED
        self.menu_index = 0

    def resumeGame(self):
        self.game_state = STATE_PLAYING

    def triggerGameOver(self):
        self.game_state = STATE_GAME_OVER
        self.player_is_alive = False
        self.menu_index = 0
        if self.score > self.high_score:
            self.high_score = self.score
        pyxel.play(3, 5)

    def isPlaying(self):
        return self.game_state == STATE_PLAYING

    def updateGameState(self):
        if self.game_state == STATE_PLAYING:
            if self.pausePressed():
                self.pauseGame()

        elif self.game_state == STATE_PAUSED:
            if self.pausePressed():
                self.resumeGame()
                return
            self.moveMenuSelection(len(self.PAUSE_OPTIONS))
            if self.menuConfirmed():
                option = self.PAUSE_OPTIONS[self.menu_index]
                if option == "RESUME":
                    self.resumeGame()
                elif option == "RESTART":
                    self.resetGame()
                else:
                    pyxel.quit()

        else:
            if pyxel.btnp(pyxel.KEY_R):
                self.resetGame()
                return
            self.moveMenuSelection(len(self.GAME_OVER_OPTIONS))
            if self.menuConfirmed():
                option = self.GAME_OVER_OPTIONS[self.menu_index]
                if option == "PLAY AGAIN":
                    self.resetGame()
                else:
                    pyxel.quit()

    # ---------------------------------------- DRAW -----------------------------------------

    def drawCenteredText(self, y, text, color):
        pyxel.text((self.APP_WIDTH - len(text) * 4) // 2, y, text, color)

    def drawDimmedScreen(self):
        # escurece o jogo e abre um painel solido para o texto ficar legivel
        pyxel.dither(0.5)
        pyxel.rect(0, 0, self.APP_WIDTH, self.APP_HEIGHT, 0)
        pyxel.dither(1.0)
        pyxel.rect(16, 14, self.APP_WIDTH - 32, 92, 0)
        pyxel.rectb(16, 14, self.APP_WIDTH - 32, 92, 13)

    def drawMenuOptions(self, options, first_y):
        for index, option in enumerate(options):
            selected = index == self.menu_index
            label = "> " + option + " <" if selected else option
            self.drawCenteredText(first_y + index * 10, label, 10 if selected else 7)

    def drawStateOverlay(self):
        if self.game_state == STATE_PAUSED:
            self.drawDimmedScreen()
            self.drawCenteredText(22, "PAUSED", 7)
            self.drawCenteredText(34, "SCORE: {}".format(self.score), 13)
            self.drawMenuOptions(self.PAUSE_OPTIONS, 52)
            self.drawCenteredText(94, "W/S MOVE  ENTER OK  P RESUME", 13)

        elif self.game_state == STATE_GAME_OVER:
            self.drawDimmedScreen()
            title_color = 8 if (pyxel.frame_count // 15) % 2 == 0 else 7
            self.drawCenteredText(22, "GAME OVER", title_color)
            self.drawCenteredText(34, "SCORE: {}".format(self.score), 7)
            self.drawCenteredText(43, "BEST:  {}".format(self.high_score), 10)
            self.drawMenuOptions(self.GAME_OVER_OPTIONS, 62)
            self.drawCenteredText(94, "W/S MOVE  ENTER OK  R RETRY", 13)
