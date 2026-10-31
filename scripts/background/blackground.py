
import math

import pyxel

from scripts.background.layers import (
    BUILDINGS_V,
    BUSHES_V,
    LAYER_IMAGE,
    SKYLINE_FIRST_ROW,
    SKY_COLOR,
    SOURCE_V,
    STRIP_WIDTH,
    TRANSPARENT,
    BUSH_FIRST_ROW,
    prepareBackgroundLayers,
)


class BackgroundClass():
    """Cenario em camadas com parallax: quanto mais longe a camada, mais devagar ela rola.

    Predios e arbustos eram o mesmo desenho; prepareBackgroundLayers() os separa (e tambem o fogo),
    entao os arbustos passam na frente dos predios e as chamas sao animadas.
    """

    # (banco de imagens, linha de origem no banco, y na tela, linhas, velocidade em px/frame, periodo da arte, cor transparente)
    # O horizonte e os arbustos repetem a cada 248 px (largura da arte); calcada e rua, a cada 160 px.
    BACKGROUND_SKY_HEIGHT = 40                                                                   # ceu (parado): fundo liso atras de predios e arbustos
    BACKGROUND_BUILDINGS = (LAYER_IMAGE, BUILDINGS_V, SKYLINE_FIRST_ROW, 19, 0.30, STRIP_WIDTH, TRANSPARENT)   # predios ao longe
    BACKGROUND_BUSHES = (LAYER_IMAGE, BUSHES_V, BUSH_FIRST_ROW, 7, 0.55, STRIP_WIDTH, TRANSPARENT)             # arbustos, na frente dos predios
    BACKGROUND_GROUND = (
        (0, SOURCE_V + 40, 40, 48, 1.00, 160, None),    # calcada e postes (mesma velocidade dos itens no chao)
        (0, SOURCE_V + 88, 88, 32, 2.00, 160, None),    # rua, em primeiro plano
    )

    # nuvens entre o ceu e os predios: (x inicial, y, largura, altura, velocidade em px/frame)
    BACKGROUND_CLOUDS = (
        (20, 3, 30, 6, 0.08),
        (95, 8, 22, 4, 0.12),
        (150, 2, 26, 5, 0.06),
    )
    BACKGROUND_CLOUD_COLOR = 6
    BACKGROUND_CLOUD_LOOP = 220         # distancia percorrida antes de a nuvem reaparecer

    # fogo
    FIRE_FRAME_DURATION = 6             # frames de jogo por quadro da animacao
    FIRE_FRAME_COUNT = 4
    FIRE_EMBER_COUNT = 3
    FIRE_EMBER_CYCLE = 45               # frames que uma faisca leva para subir e apagar
    FIRE_EMBER_RISE = 0.35              # px por frame

    background_fires = []

    def prepareBackground(self):
        self.background_fires = prepareBackgroundLayers()

    def drawBackgroundLayer(self, image, source_v, screen_y, rows, speed, period, colkey):
        offset = int(self.game_frame * speed) % period

        for i in range(2):
            pyxel.blt(
                # X
                i * period - offset,
                # Y
                screen_y,
                # IMG
                image,
                # U
                0,
                # V
                source_v,
                # WIDTH
                STRIP_WIDTH,
                # HEIGHT
                rows,
                # COLKEY
                colkey
            )

    def drawBackgroundClouds(self):
        for x, y, width, height, speed in self.BACKGROUND_CLOUDS:
            cloud_x = (x - self.game_frame * speed) % self.BACKGROUND_CLOUD_LOOP - width
            pyxel.elli(cloud_x, y, width, height, self.BACKGROUND_CLOUD_COLOR)
            pyxel.elli(cloud_x + width * 0.25, y - height * 0.4, width * 0.5, height, self.BACKGROUND_CLOUD_COLOR)

    def drawFireEmbers(self, fire, screen_x):
        for ember in range(self.FIRE_EMBER_COUNT):
            t = (self.game_frame + fire["seed"] * 13 + ember * (self.FIRE_EMBER_CYCLE // self.FIRE_EMBER_COUNT)) % self.FIRE_EMBER_CYCLE
            x = screen_x + fire["frame_w"] * 0.5 + math.sin((t + ember * 7) * 0.3) * 3 + (ember - 1) * 3
            y = fire["draw_y"] + 4 - t * self.FIRE_EMBER_RISE
            color = 10 if t < self.FIRE_EMBER_CYCLE / 3 else (9 if t < 2 * self.FIRE_EMBER_CYCLE / 3 else 8)
            pyxel.pset(x, y, color)

    def drawBackgroundFires(self):
        speed = self.BACKGROUND_BUILDINGS[4]
        offset = int(self.game_frame * speed) % STRIP_WIDTH

        for fire in self.background_fires:
            frame = (self.game_frame // self.FIRE_FRAME_DURATION + fire["seed"]) % self.FIRE_FRAME_COUNT
            u, v = fire["frames"][frame]
            for i in range(2):
                screen_x = fire["draw_x"] + i * STRIP_WIDTH - offset
                if -fire["frame_w"] < screen_x < pyxel.width:
                    pyxel.blt(screen_x, fire["draw_y"], LAYER_IMAGE, u, v, fire["frame_w"], fire["frame_h"], TRANSPARENT)
                    self.drawFireEmbers(fire, screen_x)

    def drawBackground(self):
        pyxel.rect(0, 0, pyxel.width, self.BACKGROUND_SKY_HEIGHT, SKY_COLOR)
        self.drawBackgroundClouds()
        self.drawBackgroundLayer(*self.BACKGROUND_BUILDINGS)
        self.drawBackgroundFires()
        self.drawBackgroundLayer(*self.BACKGROUND_BUSHES)
        for layer in self.BACKGROUND_GROUND:
            self.drawBackgroundLayer(*layer)

    def updateBackground(self):
        return
