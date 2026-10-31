
import random
import pyxel


class enemyClass():
    frame_start = 100                   # frames de jogo antes do primeiro zumbi
    enemys_list = []
    enemy_sprite_u1 = 64
    enemy_sprite_v1 = 0
    enemy_sprite_u2 = 80
    enemy_sprite_v2 = 0
    enemy_spawn_range_min = 30          # os zumbis nascem fora da tela, a essa distancia da borda direita
    enemy_spawn_range_max = 60
    enemy_delay = 0
    color_key = 12

    # ---- geracao procedural: tudo cresce com o nivel (1 nivel a cada LEVEL_SCORE_STEP pontos) ----
    LEVEL_SCORE_STEP = 500
    LEVEL_MAX = 20
    ENEMY_LIMIT_BASE = 4                # zumbis ao mesmo tempo no nivel 1 (+1 por nivel)
    ENEMY_LIMIT_MAX = 16
    ENEMY_SPAWN_INTERVAL_BASE = 45      # frames entre zumbis no nivel 1 (-4 por nivel)
    ENEMY_SPAWN_INTERVAL_MIN = 12
    ENEMY_SPEED_BASE = 0.5              # pixels por frame
    ENEMY_SPEED_VARIATION = 0.5         # sorteado uma vez por zumbi (antes mudava a cada frame)
    ENEMY_SPEED_PER_LEVEL = 0.07
    ENEMY_FAST_CHANCE_PER_LEVEL = 0.04  # chance de um zumbi corredor (+60% de velocidade)
    ENEMY_FAST_CHANCE_MAX = 0.4
    ENEMY_SPEED_MAX = 2.4
    ENEMY_MIN_Y_SPACING = 12            # evita nascer em cima de outro zumbi

    def resetEnemies(self):
        self.enemys_list = []
        self.enemy_delay = 0

    def getLevel(self):
        return min(self.LEVEL_MAX, 1 + self.score // self.LEVEL_SCORE_STEP)

    def getEnemyLimit(self):
        return min(self.ENEMY_LIMIT_MAX, self.ENEMY_LIMIT_BASE + self.getLevel())

    def getEnemySpawnInterval(self):
        interval = self.ENEMY_SPAWN_INTERVAL_BASE - (self.getLevel() - 1) * 4
        interval = max(self.ENEMY_SPAWN_INTERVAL_MIN, interval)
        return int(interval * random.uniform(0.8, 1.2))

    def getEnemySpeed(self):
        level = self.getLevel()
        speed = self.ENEMY_SPEED_BASE + random.random() * self.ENEMY_SPEED_VARIATION + level * self.ENEMY_SPEED_PER_LEVEL
        fast_chance = min(self.ENEMY_FAST_CHANCE_MAX, level * self.ENEMY_FAST_CHANCE_PER_LEVEL)
        if random.random() < fast_chance:
            speed *= 1.6
        return min(self.ENEMY_SPEED_MAX, speed)

    def pickEnemySpawnY(self, spawn_x):
        y = random.randint(self.APP_Y_MIN_PLAYABLE_AREA, self.APP_Y_MAX_PLAYABLE_AREA)
        for _ in range(6):
            free = all(
                abs(enemy['y'] - y) >= self.ENEMY_MIN_Y_SPACING or abs(enemy['x'] - spawn_x) > 24
                for enemy in self.enemys_list
            )
            if free:
                return y
            y = random.randint(self.APP_Y_MIN_PLAYABLE_AREA, self.APP_Y_MAX_PLAYABLE_AREA)
        return y

    def spawnEnemy(self):
        spawn_x = self.APP_X_MAX_PLAYABLE_AREA + random.randint(self.enemy_spawn_range_min, self.enemy_spawn_range_max)
        self.enemys_list.append({
            "x": float(spawn_x),
            "y": self.pickEnemySpawnY(spawn_x),
            "speed": self.getEnemySpeed(),
            "phase": random.randint(0, 1),
            "img": 0,
            "u": self.enemy_sprite_u1,
            "v": self.enemy_sprite_v1,
            "w": 16,
            "h": 16,
            "colkey": self.color_key,
        })

    def drawEnemys(self):
        for enemy in self.enemys_list:
            walking = (self.game_frame // 10 + enemy['phase']) % 2 == 0
            enemy['u'] = self.enemy_sprite_u1 if walking else self.enemy_sprite_u2
            pyxel.blt(
                int(enemy['x']),
                enemy['y'],
                enemy['img'],
                enemy['u'],
                enemy['v'],
                enemy['w'],
                enemy['h'],
                enemy['colkey']
            )

    def updateEnemys(self):
        if self.game_frame <= self.frame_start:
            return

        if self.game_frame >= self.enemy_delay and len(self.enemys_list) < self.getEnemyLimit():
            self.enemy_delay = self.game_frame + self.getEnemySpawnInterval()
            self.spawnEnemy()

        for enemy in self.enemys_list:
            enemy['x'] -= enemy['speed']

        # quem saiu pela esquerda some (reconstruir a lista evita pular itens ao remover durante o laco)
        self.enemys_list = [enemy for enemy in self.enemys_list if enemy['x'] >= self.APP_X_MIN_PLAYABLE_AREA]
