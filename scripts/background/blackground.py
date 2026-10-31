
import pyxel


class BackgroundClass():

    def drawBackground(self):
        offset = self.game_frame % 160

        for i in range(2):
            pyxel.blt(
                # X
                i * 160 - offset,
                # Y
                0,
                # IMG
                0,
                # U
                0,
                # V
                16,
                # WIDTH
                248,
                # HEIGHT
                128
            )

    def updateBackground(self):
        return
