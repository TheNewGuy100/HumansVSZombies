
import pyxel


class bulletsController():
    bullet_y = 0
    bullet_img = 0
    bullet_u = 96
    bullet_v = 0
    bullet_width = 16
    bullet_heigth = 16
    bullets_list = []
    bullet_speed = 2
    bullet_alignment = 10
    player_ammo = 60

    def resetBullets(self):
        self.bullets_list = []

    def createBullet(self, x, y):
        self.bullet_x = x
        self.bullet_y = y

        self.bullets_list.append({
            "x": self.bullet_x + self.bullet_alignment,
            "y": self.bullet_y,
            "img": 0,
            "u": 96,
            "v": 0,
            "w": 16,
            "h": 16,
            "colkey": 0,
        })
        self.player_ammo -= 1
        pyxel.play(0, 0)

    def drawBullets(self):
        for bullet in self.bullets_list:
            pyxel.blt(
                int(bullet['x']),
                bullet['y'],
                bullet['img'],
                bullet['u'],
                bullet['v'],
                bullet['w'],
                bullet['h'],
                bullet['colkey']
            )

    def updateBullet(self):
        remaining = []
        for bullet in self.bullets_list:
            bullet['x'] += self.bullet_speed

            hit = None
            for enemy in self.enemys_list:
                if abs(enemy['y'] - bullet['y']) < 16 and abs(bullet['x'] - enemy['x']) < 8:
                    hit = enemy
                    break

            if hit is not None:
                if bullet['y'] < hit['y'] + 3:
                    self.AddHeadShot(hit['x'], hit['y'] + 8)
                    self.score += 50
                self.enemys_list = [enemy for enemy in self.enemys_list if enemy is not hit]
                self.score += 100
                pyxel.play(0, 3)
            elif bullet['x'] <= self.APP_X_MAX_PLAYABLE_AREA:
                remaining.append(bullet)

        self.bullets_list = remaining
