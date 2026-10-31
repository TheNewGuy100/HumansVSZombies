
import math

import pyxel

# Cores da arte original do cenario (paleta do pyxres)
SKY_COLOR = 12
BUILDING_COLORS = (0, 1)        # silhueta e janelas
FIRE_COLORS = (8, 9, 10)        # do mais frio (vermelho) ao mais quente (amarelo)
BUSH_COLORS = (3, 11)
TRANSPARENT = SKY_COLOR         # nas camadas novas, a cor do ceu e a cor transparente

LAYER_IMAGE = 1                 # banco de imagens onde as camadas separadas sao montadas em tempo de execucao
SOURCE_IMAGE = 0
SOURCE_V = 16                   # onde o cenario comeca no banco 0
STRIP_WIDTH = 248
SKYLINE_FIRST_ROW = 17
SKYLINE_LAST_ROW = 35           # ultima linha que mistura predios e topo dos arbustos
BUSH_FIRST_ROW = 33
BUSH_LAST_ROW = 39

# Posicao das camadas montadas no banco de imagens 1
BUILDINGS_V = 0
BUSHES_V = 24
FIRES_V = 36

FIRE_FRAME_COUNT = 4
FIRE_TOP_MARGIN = 3             # linhas extras no topo para a chama poder "lamber" para cima


def _copyBuildings(src, dst):
    """Predios sem arbustos nem fogo: o que esta atras e preenchido com a silhueta escura."""
    for x in range(STRIP_WIDTH):
        top = None
        for y in range(SKYLINE_FIRST_ROW, SKYLINE_LAST_ROW + 1):
            if src.pget(x, SOURCE_V + y) in BUILDING_COLORS:
                top = y
                break
        for y in range(SKYLINE_FIRST_ROW, SKYLINE_LAST_ROW + 1):
            color = TRANSPARENT
            if top is not None and y >= top:
                original = src.pget(x, SOURCE_V + y)
                color = original if original in BUILDING_COLORS else BUILDING_COLORS[0]
            dst.pset(x, BUILDINGS_V + y - SKYLINE_FIRST_ROW, color)


def _copyBushes(src, dst):
    """So os arbustos: tudo o que nao e verde vira transparente."""
    for x in range(STRIP_WIDTH):
        for y in range(BUSH_FIRST_ROW, BUSH_LAST_ROW + 1):
            color = src.pget(x, SOURCE_V + y)
            dst.pset(x, BUSHES_V + y - BUSH_FIRST_ROW, color if color in BUSH_COLORS else TRANSPARENT)


def _findFires(src):
    """Agrupa os pixels de fogo em chamas (componentes conexos, juntando pedacos a ate 3 px de distancia)."""
    pixels = {}
    for y in range(SKYLINE_FIRST_ROW, SKYLINE_LAST_ROW + 1):
        for x in range(STRIP_WIDTH):
            color = src.pget(x, SOURCE_V + y)
            if color in FIRE_COLORS:
                pixels[(x, y)] = color

    groups = []
    unvisited = set(pixels)
    while unvisited:
        start = unvisited.pop()
        group = [start]
        queue = [start]
        while queue:
            cx, cy = queue.pop()
            for dx in range(-3, 4):
                for dy in range(-3, 4):
                    neighbor = (cx + dx, cy + dy)
                    if neighbor in unvisited:
                        unvisited.remove(neighbor)
                        group.append(neighbor)
                        queue.append(neighbor)
        groups.append(group)

    fires = []
    for group in groups:
        xs = [p[0] for p in group]
        ys = [p[1] for p in group]
        x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
        fires.append({
            "x": x0,
            "y": y0,
            "w": x1 - x0 + 1,
            "h": y1 - y0 + 1,
            "pixels": [(px - x0, py - y0, pixels[(px, py)]) for px, py in group],
        })
    fires.sort(key=lambda fire: fire["x"])
    return fires


def _hotter(color):
    return FIRE_COLORS[min(len(FIRE_COLORS) - 1, FIRE_COLORS.index(color) + 1)]


def _cooler(color):
    return FIRE_COLORS[max(0, FIRE_COLORS.index(color) - 1)]


def _fireFrame(fire, frame):
    """Gera um quadro da animacao: a chama balanca (mais no topo), a cor oscila e a ponta pisca."""
    w, h = fire["w"], fire["h"]
    grid = {}
    for x, y, color in fire["pixels"]:
        top_weight = 1.0 - y / max(1, h - 1)            # 1 no topo da chama, 0 na base
        sway = int(round(math.sin(frame * math.pi / 2 + y * 0.8) * 1.4 * top_weight))
        nx = x + sway + 1                                # +1 deixa uma coluna livre a esquerda para o balanco
        ny = y + FIRE_TOP_MARGIN

        if frame % 2 == 1 and top_weight > 0.5:
            color = _cooler(color)
        elif frame % 2 == 0 and frame > 0 and top_weight > 0.5:
            color = _hotter(color)

        if frame in (1, 3) and top_weight > 0.8 and (x + y + frame) % 3 == 0:
            continue                                     # a ponta da chama "falha"
        grid[(nx, ny)] = color

    if frame == 2:                                       # lingua de fogo para cima
        for (x, y), color in list(grid.items()):
            if y == min(p[1] for p in grid) and (x % 2 == 0):
                grid[(x, y - 1)] = _hotter(color)
                grid[(x, y - 2)] = FIRE_COLORS[0]

    return grid, w + 2, h + FIRE_TOP_MARGIN


def prepareBackgroundLayers():
    """Separa o cenario em camadas (predios, fogo animado e arbustos) no banco de imagens 1.

    A arte original junta tudo em uma imagem so; separar permite que cada camada ande em uma
    velocidade (parallax) e que o fogo tenha animacao. Retorna a lista de chamas para o desenho.
    """
    src = pyxel.images[SOURCE_IMAGE]
    dst = pyxel.images[LAYER_IMAGE]
    dst.rect(0, 0, 256, 256, TRANSPARENT)

    _copyBuildings(src, dst)
    _copyBushes(src, dst)

    fires = _findFires(src)
    next_v = FIRES_V
    for index, fire in enumerate(fires):
        fire["frames"] = []
        u = 0
        row_height = 0
        for frame in range(FIRE_FRAME_COUNT):
            grid, frame_w, frame_h = _fireFrame(fire, frame)
            for (x, y), color in grid.items():
                if 0 <= x < frame_w and 0 <= y < frame_h:
                    dst.pset(u + x, next_v + y, color)
            fire["frames"].append((u, next_v))
            u += frame_w + 2
            row_height = max(row_height, frame_h)
        fire["frame_w"] = fire["w"] + 2
        fire["frame_h"] = row_height
        fire["draw_x"] = fire["x"] - 1
        fire["draw_y"] = fire["y"] - FIRE_TOP_MARGIN
        fire["seed"] = index
        next_v += row_height + 2
    return fires
