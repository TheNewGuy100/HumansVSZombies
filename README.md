![Zombies Invasion in play: the player shoots zombies on a street with burning buildings in the background](docs/preview.png)

# HumansVSZombies (Zombies Invasion)

Pixel art shooter made with Python and [Pyxel](https://github.com/kitao/pyxel): you are the last human on a street overrun by zombies. Shoot, pick up ammo and medkits, and survive as long as you can.

## Controls

| Input | Action |
| --- | --- |
| `W` `A` `S` `D` or gamepad d-pad | Move |
| `Space` or gamepad B button | Shoot |
| `P`, `ESC` or gamepad Start | Pause and resume |
| `W` / `S` and `Enter` (or `Space`) | Navigate and choose in the menus |
| `R` | Play again on the game over screen |

Hitting the head gives a bonus (**HEADSHOT!**).

## Features

- Shooting with limited ammo and a **headshot** bonus.
- Zombies, ammo and medkits are **generated adaptively**: difficulty rises with the score, and items show up more when you need them.
- **Pause menu** and game over screen, with a session high score.
- **Parallax** scenery, with buildings, bushes and ground in layers, clouds and **animated fire**.
- Keyboard and gamepad support.

## Procedural generation

Zombies, ammo and medkits are generated dynamically instead of at fixed intervals.

| Element | How it is generated |
| --- | --- |
| **Level** | Goes up every 500 points (up to 20) |
| **Zombies** | The on-screen cap grows with the level (from 5 to 16), the interval between zombies shrinks, each one gets its speed rolled once, and the chance of a runner zombie increases. They never spawn on top of each other |
| **Ammo** | A roll happens every 2.5 s. The chance goes from 10% (full) to 80% (empty), and a box always shows up when you run out. One box at a time |
| **Medkits** | A roll happens every 3.3 s. The chance goes from 5% to 65% as health drops, and one never appears at full health |

All values are constants at the top of each class, in `scripts/mechanics/`.

## Scenery

The scenery has parallax: sky, buildings, bushes and ground (sidewalk and road, together) scroll at different speeds, and clouds drift by. The original art combined buildings, bushes and fire in a single image; when the game opens, `scripts/background/layers.py` splits these parts into layers (in memory, without changing `sprites.pyxres`), and the bushes are drawn in front of the buildings. The fire is animated in four frames (sway, color and flame tip) and gives off sparks.

## Pause menu and game over

- **Pause:** freezes the world (including the scenery) and offers *Resume*, *Restart* and *Quit*.
- **Game over:** shows the score and the session high score, with *Play again* and *Quit*.

## Running

```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python application.py
```

The `assets/sprites.pyxres` file was created in an old Pyxel version; the game loads it normally and Pyxel prints a warning suggesting to save it again in the editor.

## Structure

| Folder | Contents |
| --- | --- |
| `application.py` | Window, main loop and class composition |
| `scripts/state/` | Game states (playing, pause, game over) and the menus |
| `scripts/player/` | Movement, animation, shooting and collision with zombies |
| `scripts/mechanics/` | Zombies, ammo boxes and medkits |
| `scripts/UI/` | Health, ammo, score, level and headshot notice |
| `scripts/background/` | Scrolling scenery |
