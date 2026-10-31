
import random
import pyxel


class medkitSpawner():
    medkit_package_list = []
    medkit_package_img = 0
    medkit_package_u = 32
    medkit_package_v = 0
    medkit_package_w = 16
    medkit_package_h = 16
    medkit_package_color_exclusion = 0
    medkit_next_check = 0

    MEDKIT_CHECK_INTERVAL = 200         # frames entre sorteios de kit medico
    MEDKIT_CHANCE_HURT = 0.05           # chance com a vida quase cheia...
    MEDKIT_CHANCE_CRITICAL = 0.65       # ...e com a vida quase no fim (interpola entre os dois)
    MEDKIT_HEAL = 25
    HEALTH_MAX = 100

    def resetMedkitSpawner(self):
        self.medkit_package_list = []
        self.medkit_next_check = 0

    def getMedkitSpawnChance(self):
        if self.health >= self.HEALTH_MAX:
            return 0.0                  # vida cheia: nao adianta aparecer kit
        missing = 1.0 - max(self.health, 0) / self.HEALTH_MAX
        return self.MEDKIT_CHANCE_HURT + (self.MEDKIT_CHANCE_CRITICAL - self.MEDKIT_CHANCE_HURT) * missing

    def spawnMedkitInMap(self):
        if self.game_frame < self.medkit_next_check:
            return
        self.medkit_next_check = self.game_frame + self.MEDKIT_CHECK_INTERVAL

        if len(self.medkit_package_list) > 0:
            return                      # um kit por vez no mapa

        if random.random() < self.getMedkitSpawnChance():
            self.medkit_package_list.append({
                "x": float(self.APP_X_MAX_PLAYABLE_AREA + 10),
                "y": random.randint(self.APP_Y_MIN_PLAYABLE_AREA, self.APP_Y_MAX_PLAYABLE_AREA),
                "img": self.medkit_package_img,
                "u": self.medkit_package_u,
                "v": self.medkit_package_v,
                "w": self.medkit_package_w,
                "h": self.medkit_package_h,
                "colkey": self.medkit_package_color_exclusion
            })

    def updateMedkitBox(self):
        remaining = []
        for medkit_box in self.medkit_package_list:
            medkit_box['x'] -= 1
            if abs(self.player_x - medkit_box['x']) <= 16 and abs(self.player_y - medkit_box['y']) <= 16:
                self.health = min(self.HEALTH_MAX, self.health + self.MEDKIT_HEAL)
                pyxel.play(0, 4)
            elif medkit_box['x'] >= self.APP_X_MIN_PLAYABLE_AREA - 16:
                remaining.append(medkit_box)
        self.medkit_package_list = remaining

    def drawMedkitBox(self):
        for medkit_box in self.medkit_package_list:
            pyxel.blt(
                int(medkit_box["x"]),
                medkit_box["y"],
                medkit_box["img"],
                medkit_box["u"],
                medkit_box["v"],
                medkit_box["w"],
                medkit_box["h"],
                medkit_box["colkey"]
            )
