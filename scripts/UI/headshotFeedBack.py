
import pyxel


class headShotPopUp():
    headShotsList = []
    framesLimit = 30
    headShotColors = (8, 10)

    def resetHeadShots(self):
        self.headShotsList = []

    def AddHeadShot(self, x, y):
        # um dicionario novo por headshot (antes todos compartilhavam o mesmo objeto)
        self.headShotsList.append({
            "x": x,
            "y": y,
            "message": "HEADSHOT!",
            "framesLimit": self.game_frame + self.framesLimit
        })

    def updateHeadShots(self):
        self.headShotsList = [h for h in self.headShotsList if h['framesLimit'] >= self.game_frame]

    def drawHeadShots(self):
        for headShotMessage in self.headShotsList:
            color = self.headShotColors[(self.game_frame // 5) % 2]
            pyxel.text(
                int(headShotMessage['x']),
                headShotMessage['y'],
                headShotMessage['message'],
                color
            )
