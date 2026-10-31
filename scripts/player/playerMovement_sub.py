
import pyxel


class playerMovement():
    shoot_delay = 0
    PLAYER_SPEED = 2
    PLAYER_WIDTH = 16
    SHOOT_COOLDOWN = 10

    def checkPlayerMovement(self):
        left = pyxel.btn(pyxel.KEY_A) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT)
        right = pyxel.btn(pyxel.KEY_D) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT)
        up = pyxel.btn(pyxel.KEY_W) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_UP)
        down = pyxel.btn(pyxel.KEY_S) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN)

        move_x = int(right) - int(left)
        move_y = int(down) - int(up)

        self.player_x = max(
            self.APP_X_MIN_PLAYABLE_AREA,
            min(self.player_x + move_x * self.PLAYER_SPEED, self.APP_X_MAX_PLAYABLE_AREA - self.PLAYER_WIDTH)
        )
        self.player_y = max(
            self.APP_Y_MIN_PLAYABLE_AREA,
            min(self.player_y + move_y * self.PLAYER_SPEED, self.APP_Y_MAX_PLAYABLE_AREA)
        )

        # SHOOT (so atira com municao; antes a precedencia de "or" / "and" deixava atirar sem municao)
        wants_to_shoot = pyxel.btn(pyxel.KEY_SPACE) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_B)
        if wants_to_shoot and self.player_ammo > 0 and self.game_frame >= self.shoot_delay:
            self.createBullet(self.player_x, self.player_y)
            self.shoot_delay = self.game_frame + self.SHOOT_COOLDOWN
