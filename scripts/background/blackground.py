
import pyxel


class BackgroundClass():
    """Cenario em camadas com parallax: quanto mais longe a camada, mais devagar ela rola."""

    BACKGROUND_IMAGE_V = 16             # onde o cenario comeca no banco de imagens 0

    # (primeira linha da imagem, quantidade de linhas, velocidade em px/frame, periodo da arte em px)
    # O horizonte e as arvores repetem a cada 248 px (largura da arte); calcada e rua, a cada 160 px.
    BACKGROUND_LAYERS = (
        (0, 17, 0.0, 160),              # ceu (parado)
        (17, 16, 0.30, 248),            # predios e incendios ao longe
        (33, 7, 0.55, 248),             # arvores
        (40, 48, 1.00, 160),            # calcada e postes (mesma velocidade dos itens no chao)
        (88, 32, 2.00, 160),            # rua, em primeiro plano
    )

    # nuvens entre o ceu e os predios: (x inicial, y, largura, altura, velocidade em px/frame)
    BACKGROUND_CLOUDS = (
        (20, 3, 30, 6, 0.08),
        (95, 8, 22, 4, 0.12),
        (150, 2, 26, 5, 0.06),
    )
    BACKGROUND_CLOUD_COLOR = 6
    BACKGROUND_CLOUD_LOOP = 220         # distancia percorrida antes de a nuvem reaparecer

    def drawBackgroundLayer(self, first_row, rows, speed, period):
        offset = int(self.game_frame * speed) % period

        for i in range(2):
            pyxel.blt(
                # X
                i * period - offset,
                # Y
                first_row,
                # IMG
                0,
                # U
                0,
                # V
                self.BACKGROUND_IMAGE_V + first_row,
                # WIDTH
                248,
                # HEIGHT
                rows
            )

    def drawBackgroundClouds(self):
        for x, y, width, height, speed in self.BACKGROUND_CLOUDS:
            cloud_x = (x - self.game_frame * speed) % self.BACKGROUND_CLOUD_LOOP - width
            pyxel.elli(cloud_x, y, width, height, self.BACKGROUND_CLOUD_COLOR)
            pyxel.elli(cloud_x + width * 0.25, y - height * 0.4, width * 0.5, height, self.BACKGROUND_CLOUD_COLOR)

    def drawBackground(self):
        sky, *ground_layers = self.BACKGROUND_LAYERS

        self.drawBackgroundLayer(*sky)
        self.drawBackgroundClouds()
        for layer in ground_layers:
            self.drawBackgroundLayer(*layer)

    def updateBackground(self):
        return
