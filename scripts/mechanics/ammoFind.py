
import random
import pyxel


class ammoSpawner():
    ammo_package_list = []
    ammo_package_img = 0
    ammo_package_u = 48
    ammo_package_v = 0
    ammo_package_w = 16
    ammo_package_h = 16
    ammo_package_color_exclusion = 0
    ammo_next_check = 0

    AMMO_CHECK_INTERVAL = 150           # frames entre sorteios de caixa de municao
    AMMO_CHANCE_FULL = 0.10             # chance quando a municao esta cheia...
    AMMO_CHANCE_EMPTY = 0.80            # ...e quando esta zerada (interpola entre os dois)
    AMMO_FULL_REFERENCE = 60
    AMMO_PACK_SIZE = 40
    AMMO_MAX = 99

    def resetAmmoSpawner(self):
        self.ammo_package_list = []
        self.ammo_next_check = 0

    def getAmmoSpawnChance(self):
        need = 1.0 - min(self.player_ammo, self.AMMO_FULL_REFERENCE) / self.AMMO_FULL_REFERENCE
        return self.AMMO_CHANCE_FULL + (self.AMMO_CHANCE_EMPTY - self.AMMO_CHANCE_FULL) * need

    def spawnAmmoInMap(self):
        if self.game_frame < self.ammo_next_check:
            return
        self.ammo_next_check = self.game_frame + self.AMMO_CHECK_INTERVAL

        if len(self.ammo_package_list) > 0:
            return                      # uma caixa por vez no mapa

        # sem municao: sempre aparece uma; senao, quanto menos municao, maior a chance
        if self.player_ammo <= 0 or random.random() < self.getAmmoSpawnChance():
            self.ammo_package_list.append({
                "x": float(self.APP_X_MAX_PLAYABLE_AREA + 10),
                "y": random.randint(self.APP_Y_MIN_PLAYABLE_AREA, self.APP_Y_MAX_PLAYABLE_AREA),
                "img": self.ammo_package_img,
                "u": self.ammo_package_u,
                "v": self.ammo_package_v,
                "w": self.ammo_package_w,
                "h": self.ammo_package_h,
                "colkey": self.ammo_package_color_exclusion
            })

    def updateAmmoBox(self):
        remaining = []
        for ammo_box in self.ammo_package_list:
            ammo_box['x'] -= 1
            if abs(self.player_x - ammo_box['x']) <= 16 and abs(self.player_y - ammo_box['y']) <= 16:
                self.player_ammo = min(self.AMMO_MAX, self.player_ammo + self.AMMO_PACK_SIZE)
                pyxel.play(0, 4)
            elif ammo_box['x'] >= self.APP_X_MIN_PLAYABLE_AREA - 16:
                remaining.append(ammo_box)
        self.ammo_package_list = remaining

    def drawAmmoBox(self):
        for ammo_box in self.ammo_package_list:
            pyxel.blt(
                int(ammo_box["x"]),
                ammo_box["y"],
                ammo_box["img"],
                ammo_box["u"],
                ammo_box["v"],
                ammo_box["w"],
                ammo_box["h"],
                ammo_box["colkey"]
            )
