
import pyxel


class playerCheckDead():
    ENEMY_HIT_DAMAGE = 25

    def checkPlayerDead(self):
        survivors = []
        for enemy in self.enemys_list:
            if abs(enemy['y'] - self.player_y) < 16 and abs(self.player_x - enemy['x']) < 8:
                self.health -= self.ENEMY_HIT_DAMAGE
                pyxel.play(0, 5)
            else:
                survivors.append(enemy)
        self.enemys_list = survivors

        if self.health <= 0 and self.isPlaying():
            self.triggerGameOver()
