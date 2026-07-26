import pyxel
import sys
import time

# Quitting makes no sense in the browser build, so the menu hides it there
IS_WEB = sys.platform == "emscripten"

# Global Var
level_num = -1
skin_number = 0
level_completed = False
paused = False
reset = False

total_orb_counter = 0
gold_medals = 0
silver_medals = 0
bronze_medals = 0

x_pos = 16
y_pos = 104

# Level 1
block_pos_l1 = [
    (40, 104),
    (48, 104),
    (56, 104),
    (72, 88),
    (80, 88),
    (88, 88),
    (102, 72),
    (110, 72),
    (118, 72),
    (126, 72),
    (134, 72),
]
coin_pos_l1 = [(74, 82)]
medal_times = [(160, 140, 120)]
medals_per_level = [[None, None, None]]

records_dic = {}


# Defines a main function which runs the full program
def main():
    App()


# Creates a class for a mouse point
class Mouse:
    def __init__(self):
        self.img = 0
        self.x = 32
        self.y = 8
        self.w = 4
        self.h = 4

    def draw(self):
        pyxel.blt(
            pyxel.mouse_x, pyxel.mouse_y, self.img, self.x, self.y, self.w, self.h
        )


# Creates a class for buttons
class Button:
    def __init__(
        self,
        x1,
        y1,
        x2,
        y2,
        button_x,
        button_y,
        width,
        height,
        text,
        img,
        text_color1,
        text_color2,
    ):
        # General Button Attributes
        self.button_x = button_x
        self.button_y = button_y
        self.width = width
        self.height = height
        self.text = text
        self.img = img
        # Normal Button Case
        self.x1 = x1
        self.y1 = y1
        self.color1 = text_color1
        # Hovered Button Case
        self.x2 = x2
        self.y2 = y2
        self.color2 = text_color2

    def detect_click(self):
        if (
            self.button_x <= pyxel.mouse_x <= self.button_x + self.width
            and self.button_y <= pyxel.mouse_y <= self.button_y + self.height
            and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT)
        ):
            return True
        return False

    def detect_hovering(self):
        if (
            self.button_x <= pyxel.mouse_x <= self.button_x + self.width
            and self.button_y <= pyxel.mouse_y <= self.button_y + self.height
        ):
            return True
        return False

    def draw_normal_state_button(self):
        pyxel.blt(
            self.button_x,
            self.button_y,
            self.img,
            self.x1,
            self.y1,
            self.width,
            self.height,
            0,
        )
        pyxel.text(self.button_x + 4, self.button_y + 6, self.text, self.color1)

    def draw_hovered_state_button(self):
        pyxel.blt(
            self.button_x,
            self.button_y,
            self.img,
            self.x2,
            self.y2,
            self.width,
            self.height,
            0,
        )
        pyxel.text(self.button_x + 4, self.button_y + 6, self.text, self.color2)

    def draw_level_selecting_button(self, level_to_move_to):
        self.draw_normal_state_button()
        if self.detect_click():
            global level_num
            level_num = level_to_move_to
        if self.detect_hovering():
            self.draw_hovered_state_button()


# Creates a class for the menu screen
class Menu:
    def __init__(self):
        self.tm = 0
        self.u = 24 * 8
        self.v = 0 * 8
        self.width = 192
        self.height = 128

        # Add more Buttons later
        self.play_button = Button(
            32, 96, 32, 112, 120, 50, 48, 16, "PLAY    >", 0, 7, 7
        )
        self.records_button = Button(
            32, 96, 32, 112, 120, 72, 48, 16, "RECORDS >", 0, 7, 7
        )
        self.skins_button = Button(16, 64, 16, 80, 98, 50, 16, 16, "", 0, 7, 7)
        self.quit_button = Button(112, 64, 112, 80, 98, 94, 16, 16, "", 0, 7, 7)

        # Creates a mouse instance
        self.mouse = Mouse()

    def draw(self):
        pyxel.bltm(0, 0, self.tm, self.u, self.v, self.width, self.height)

        self.play_button.draw_level_selecting_button(0)
        self.records_button.draw_level_selecting_button(-2)
        self.skins_button.draw_level_selecting_button(-4)
        if not IS_WEB:
            self.quit_button.draw_level_selecting_button(-6)

        self.mouse.draw()


# Creates a class for the records menu
class Records_Menu:
    def __init__(self):
        self.return_to_menu = Button(32, 64, 32, 80, 16, 16, 16, 16, "<-", 0, 7, 7)
        self.mouse = Mouse()

    def draw(self):
        pyxel.bltm(0, 0, 0, 384, 0, 192, 128)
        self.return_to_menu.draw_level_selecting_button(-1)
        y = 16
        for level, record_time in records_dic.items():
            pyxel.text(48, y, f"Level {level}: {round(record_time, 2)}s", 7)
            y += 8

        self.mouse.draw()


# Creates a class for the options menu
class Options_Menu:
    def __init__(self):
        self.return_to_menu = Button(32, 64, 32, 80, 16, 16, 16, 16, "<-", 0, 7, 7)
        self.mouse = Mouse()

    def draw(self):
        pyxel.bltm(0, 0, 0, 384, 0, 192, 128)
        self.return_to_menu.draw_level_selecting_button(-1)

        self.mouse.draw()


# Creates a class for the level selecting menu
class Level_Menu:
    def __init__(self):
        self.return_to_menu = Button(32, 64, 32, 80, 16, 16, 16, 16, "<-", 0, 7, 7)
        self.level1 = Button(32, 64, 32, 80, 40, 16, 16, 16, " 1", 0, 7, 7)
        self.mouse = Mouse()

    def draw(self):
        pyxel.bltm(0, 0, 0, 384, 0, 192, 128)
        pyxel.blt(144, 16, 0, 0, 128, 32, 64, 0)
        pyxel.blt(144, 80, 0, 80, 96, 32, 32, 0)
        pyxel.text(161, 21, f"{gold_medals}", 7)
        pyxel.text(161, 37, f"{silver_medals}", 7)
        pyxel.text(161, 53, f"{bronze_medals}", 7)
        pyxel.text(161, 69, f"{total_orb_counter}", 7)

        self.level1.draw_level_selecting_button(1)
        self.return_to_menu.draw_level_selecting_button(-1)

        for level in medals_per_level:
            if level[0] is not None and level[1] is not None and level[2] is not None:
                pyxel.blt(40, 25, 0, 48, 128, 16, 8, 0)
            elif level[0] is not None and level[1] is not None:
                pyxel.blt(40, 25, 0, 48, 136, 16, 8, 0)
            elif level[0] is not None:
                pyxel.blt(40, 25, 0, 48, 144, 16, 8, 0)

        self.mouse.draw()


# Creates a class for the Skins Menu
class Skins_Menu:
    def __init__(self):
        self.return_to_menu = Button(32, 64, 32, 80, 16, 16, 16, 16, "<-", 0, 7, 7)
        self.mouse = Mouse()
        self.slime_skins = Slime_Skins()

        self.green = Button(0, 0, 0, 0, 40, 16, 8, 16, "", 1, 7, 7)
        self.white = Button(0, 16, 0, 16, 56, 16, 8, 16, "", 1, 7, 7)

    def update(self):
        if self.green.detect_click():
            self.slime_skins.change_skin_to(0)
        elif self.white.detect_click():
            self.slime_skins.change_skin_to(1)

    def draw(self):
        pyxel.bltm(0, 0, 0, 384, 0, 192, 128)
        self.return_to_menu.draw_level_selecting_button(-1)
        # Skin Buttons
        self.green.draw_normal_state_button()
        self.white.draw_normal_state_button()

        self.mouse.draw()


class Slime_Skins:
    def __init__(self):
        self.img = 1

    def change_skin_to(self, new_skin_number):
        global skin_number
        skin_number = new_skin_number

    def get_skin(self, right, crouched, x_pos, y_pos):
        global skin_number
        if not crouched:
            if right:
                if skin_number == 0:
                    pyxel.blt(x_pos, y_pos, self.img, 0, 0, 8, 16, 0)
                elif skin_number == 1:
                    pyxel.blt(x_pos, y_pos, self.img, 0, 16, 8, 16, 0)
            else:
                if skin_number == 0:
                    pyxel.blt(x_pos, y_pos, self.img, 8, 0, 8, 16, 0)
                elif skin_number == 1:
                    pyxel.blt(x_pos, y_pos, self.img, 8, 16, 8, 16, 0)
        else:
            if right:
                if skin_number == 0:
                    pyxel.blt(x_pos, y_pos, self.img, 16, 0, 8, 16, 0)
                elif skin_number == 1:
                    pyxel.blt(x_pos, y_pos, self.img, 16, 16, 8, 16, 0)
            else:
                if skin_number == 0:
                    pyxel.blt(x_pos, y_pos, self.img, 24, 0, 8, 16, 0)
                elif skin_number == 1:
                    pyxel.blt(x_pos, y_pos, self.img, 24, 16, 8, 16, 0)


# Creates a class for the Skill Tree menu
class Skill_Tree_Menu:
    def __init__(self):
        self.return_to_menu = Button(32, 64, 32, 80, 16, 16, 16, 16, "<-", 0, 7, 7)
        self.mouse = Mouse()

    def draw(self):
        pyxel.bltm(0, 0, 0, 384, 0, 192, 128)
        self.return_to_menu.draw_level_selecting_button(-1)
        self.mouse.draw()


# Creates a class for the Quit function
class Quit:
    def __init__(self):
        pass

    def quit_game(self):
        pyxel.quit()


# Creates a class for the time needed to complete a level
class Time:
    def __init__(self):
        self.start_time = 0
        self.total_time = 0
        self.stopped = False
        self.stopped_time = 0

    def update(self):
        if not self.stopped:
            if self.start_time == 0:
                self.start_time = time.time()
            self.total_time = time.time() - self.start_time + self.stopped_time
        return round(self.total_time, 2)

    def stop(self):
        self.stopped_time = self.total_time
        self.start_time = 0
        self.stopped = True


# Creates a class for the finish portal
class Portal:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def check_if_portal_near(self, slime_x, slime_y):
        if self.x < slime_x + 8 < self.x + 16 and self.y < slime_y + 8 < self.y + 16:
            return True
        return False

    def draw(self):
        pyxel.blt(self.x, self.y, 0, 64, 0, 16, 16)


# Creates a class for the completed (finish) level screen
class Completed_Level_Screen:
    def __init__(self):
        global level_num
        self.level_num = level_num
        self.last_time = time.time()
        self.text_color = 7
        self.current_time_time = 0
        self.record = False
        self.record_time = 0

        self.medals = Medals()
        self.bronze = False
        self.silver = False
        self.gold = False

        self.restart_button = Button(
            32, 96, 32, 112, 72, 64, 48, 16, "RESTART >", 0, 7, 7
        )
        self.levels_button = Button(
            32, 96, 32, 112, 72, 83, 48, 16, "LEVELS  >", 0, 7, 7
        )
        self.menu_button = Button(
            32, 96, 32, 112, 72, 102, 48, 16, "MENU    >", 0, 7, 7
        )

        self.mouse = Mouse()

    def update(self, current_time):
        if time.time() - self.last_time >= 0.5:
            self.last_time = time.time()
            self.text_color = 10 if self.text_color == 7 else 7
        if (
            self.levels_button.detect_click()
            or self.menu_button.detect_click()
            or self.restart_button.detect_click()
            or pyxel.btnp(pyxel.KEY_R)
        ):
            global reset
            global level_completed
            level_completed = False
            reset = True
        self.record_time = records_dic[level_num]
        self.current_time = current_time
        if self.current_time == self.record_time:
            self.record = True
        if self.medals.check_bronze_medal():
            self.bronze = True
        if self.medals.check_silver_medal():
            self.silver = True
        if self.medals.check_gold_medal():
            self.gold = True

    def draw(self):
        pyxel.bltm(0, 0, 0, 576, 0, 192, 128)
        pyxel.blt(64, 10, 0, 48, 64, 64, 24, 0)
        pyxel.text(74, 16, "L1 COMPLETE", self.text_color)
        if self.record:
            pyxel.text(76, 40, "NEW RECORD!", 10)
        pyxel.text(76, 48, f"TIME: {round(self.current_time, 2)}", 0)
        pyxel.text(74, 56, f"RECORD: {round(self.record_time, 2)}", 0)
        if self.bronze:
            pyxel.blt(76, 24, 0, 32, 160, 16, 16, 0)
        if self.silver:
            pyxel.blt(88, 24, 0, 32, 144, 16, 16, 0)
        if self.gold:
            pyxel.blt(100, 24, 0, 32, 128, 16, 16, 0)

        self.menu_button.draw_level_selecting_button(-1)
        self.levels_button.draw_level_selecting_button(0)
        self.restart_button.draw_level_selecting_button(level_num)

        self.mouse.draw()


# Creates a Pause Menu class
class Pause_Menu:
    def __init__(self):
        self.continue_button = Button(
            32, 96, 32, 112, 72, 50, 48, 16, "CONTINUE >", 0, 7, 7
        )
        self.restart_button = Button(
            32, 96, 32, 112, 72, 72, 48, 16, "RESTART  >", 0, 7, 7
        )
        self.menu_button = Button(32, 96, 32, 112, 72, 94, 48, 16, "MENU    >", 0, 7, 7)
        self.mouse = Mouse()

        self.tm = 0
        self.u = 0
        self.v = 0
        self.width = 192
        self.height = 128

        self.restart = False

    def update(self):
        global paused
        if paused:
            if pyxel.btnp(pyxel.KEY_P) or self.continue_button.detect_click():
                paused = False
            if pyxel.btnp(pyxel.KEY_R) or self.restart_button.detect_click():
                self.restart = True

    def draw(self):
        global paused
        global level_num

        if paused:
            pyxel.bltm(0, 0, self.tm, self.u, self.v, self.width, self.height)
            pyxel.blt(64, 16, 0, 48, 64, 64, 24, 0)
            pyxel.text(80, 22, "PAUSE ||", 7)
            pyxel.text(10, 10, "Level 1", 2)
            self.continue_button.draw_level_selecting_button(level_num)
            self.restart_button.draw_level_selecting_button(level_num)
            self.menu_button.draw_level_selecting_button(-1)
            self.mouse.draw()


# Creates a medal class
class Medals:
    def check_bronze_medal(self):
        if medals_per_level[level_num - 1][0] is not None:
            return True
        return False

    def check_silver_medal(self):
        if medals_per_level[level_num - 1][1] is not None:
            return True
        return False

    def check_gold_medal(self):
        if medals_per_level[level_num - 1][2] is not None:
            return True
        return False


# Creates a level class for the first level
class Level1:
    def __init__(self):
        self.tm = 0
        self.u = 0
        self.v = 0
        self.width = 192
        self.height = 128

        self.ground_y = 104
        self.wall_left = 8
        self.wall_right = 176

        self.time_counter = Time()
        self.coins = [
            Coin(1, coin_pos_l1[i][0], coin_pos_l1[i][1])
            for i in range(len(coin_pos_l1))
        ]
        self.portal = Portal(126, 56)
        self.level_orb_counter = 0

        global block_pos_l1
        self.block_positions = block_pos_l1

        self.pause_menu = Pause_Menu()
        self.completed_screen = Completed_Level_Screen()
        global reset
        reset = False

        global x_pos
        global y_pos
        x_pos = 16
        y_pos = 104
        self.slime = Slime(x_pos, y_pos)
        self.collision = Collision_detection(self)

    def start_level(self):
        self.slime.x = 16
        self.slime.y = 104
        self.time_counter.update()

    def restart_level(self):
        self.__init__()
        self.start_level()

    def draw_blocks(self):
        global level_completed
        if not level_completed:
            for x, y in self.block_positions:
                pyxel.blt(x, y, 0, 32, 16, 8, 8)

    def update(self):
        global paused
        global reset
        global x_pos
        global y_pos
        global level_completed

        if reset:
            self.restart_level()
            return

        if paused:
            if self.pause_menu.restart:
                paused = False
                self.restart_level()
            self.pause_menu.update()
            return

        self.time_counter.stopped = False

        self.slime.movement(self.collision)

        self.level_orb_counter = 0
        for coin in self.coins:
            coin.check_if_coin_nearby(5, x_pos, y_pos)
            self.level_orb_counter += coin.local_orb_counter

        if self.portal.check_if_portal_near(x_pos, y_pos):
            self.finished()

        if pyxel.btnp(pyxel.KEY_P):
            self.time_counter.stop()
            paused = True

        if pyxel.btnp(pyxel.KEY_R):
            self.restart_level()

    def finished(self):
        global level_completed
        global total_orb_counter
        global records_dic
        global bronze_medals
        global silver_medals
        global gold_medals
        global medal_times
        global medals_per_level

        if not level_completed:
            total_orb_counter += self.level_orb_counter

        level_completed = True

        self.time_counter.stop()
        self.current_time = self.time_counter.stopped_time
        # Check for Record Time
        if level_num not in records_dic or self.current_time < records_dic[level_num]:
            records_dic[level_num] = self.current_time
        # Check for Bronze Medal
        if (
            self.current_time < medal_times[level_num - 1][0]
            and medals_per_level[level_num - 1][0] is None
        ):
            bronze_medals += 1
            medals_per_level[level_num - 1][0] = True
        # Check for Silver Medal
        if (
            self.current_time < medal_times[level_num - 1][1]
            and medals_per_level[level_num - 1][1] is None
        ):
            silver_medals += 1
            medals_per_level[level_num - 1][1] = True
        # Check for Gold Medal
        if (
            self.current_time < medal_times[level_num - 1][2]
            and medals_per_level[level_num - 1][2] is None
        ):
            gold_medals += 1
            medals_per_level[level_num - 1][2] = True

    def draw(self):
        global paused
        global level_num

        if not level_completed and not paused:
            pyxel.bltm(0, 0, self.tm, self.u, self.v, self.width, self.height)
            pyxel.text(10, 10, f"Level {level_num}", 2)
            # TIME
            pyxel.text(10, 20, f"{self.time_counter.update()}s", 7)
            for coin in self.coins:
                coin.draw()
            pyxel.text(10, 30, f"Orbs: {self.level_orb_counter}", 7)
            self.draw_blocks()
            self.portal.draw()
            self.slime.draw()
        elif level_completed:
            self.completed_screen.update(self.current_time)
            self.completed_screen.draw()
            self.slime.draw()
        elif paused:
            self.pause_menu.draw()
            pyxel.text(10, 20, f"{self.time_counter.update()}s", 7)
            pyxel.text(10, 30, f"Orbs: {self.level_orb_counter}", 7)


# Creates a class for the slime sprite
class Slime:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 1
        self.right = True
        self.y_velocity = 0
        self.is_jumping = False
        self.crouch_time = None
        self.current_time = None
        self.freeze_duration = 0.3
        self.frozen = False
        self.slime_skins = Slime_Skins()

    def movement(self, collision):
        global paused
        if paused:
            return
        self.current_time = time.time()
        # Slime stays above ground when completed
        if level_completed:
            if self.y > 112:
                self.y = 112
                self.y_velocity = 0
        # Slime is frozen (e.g. after crouching)
        if self.frozen:
            if self.current_time - self.crouch_time >= self.freeze_duration:
                self.frozen = False
            else:
                return
        # Slime moves left
        if pyxel.btn(pyxel.KEY_A) and not collision.check_wall_left(self.x):
            self.x -= self.speed
            self.right = False
        # Slime moves right
        elif pyxel.btn(pyxel.KEY_D) and not collision.check_wall_right(self.x):
            self.x += self.speed
            self.right = True
        # Slime Jumps
        if pyxel.btn(pyxel.KEY_SPACE) and (
            collision.check_ground(self.y)
            or collision.check_block_below(self.x, self.y)
        ):
            if self.crouch_time and (time.time() - self.crouch_time <= 1):
                self.y_velocity = -4.5
            else:
                self.y_velocity = -3
            self.is_jumping = True
            self.crouch_time = None
        # Gravity
        if self.is_jumping:
            self.y_velocity += 0.2
            self.y += self.y_velocity
            if collision.check_ground(self.y) or collision.check_block_below(
                self.x, self.y
            ):
                self.y_velocity = 0
                self.is_jumping = False
        else:
            if not collision.check_ground(self.y) and not collision.check_block_below(
                self.x, self.y
            ):
                self.y_velocity += 0.2
                self.y += self.y_velocity
        # Slime Crouches
        if pyxel.btn(pyxel.KEY_S) and (
            collision.check_ground(self.y)
            or collision.check_block_below(self.x, self.y)
        ):
            self.crouch_time = self.current_time
            self.frozen = True

        global x_pos
        global y_pos
        x_pos = self.x
        y_pos = self.y

    def draw(self):
        global paused
        if paused:
            return

        self.slime_skins.get_skin(self.right, self.frozen, self.x, self.y)


# Creates a coin class for coin logic
class Coin:
    def __init__(self, value, x, y):
        self.value = value
        self.x = x
        self.y = y
        self.collected = False
        self.coin_nearby = False
        self.local_orb_counter = 0

    def check_if_coin_nearby(self, collecting_distance, slime_x, slime_y):
        self.coin_nearby = False
        slime_center_x = slime_x + 4
        slime_center_y = slime_y + 12
        coin_center_x = self.x + 2
        coin_center_y = self.y + 2
        if collecting_distance >= abs(
            slime_center_x - coin_center_x
        ) and collecting_distance >= abs(slime_center_y - coin_center_y):
            self.coin_nearby = True

    def draw(self):
        if not self.collected:
            if self.value == 1 and not self.coin_nearby:
                pyxel.blt(self.x, self.y, 0, 36, 8, 4, 4)
            elif self.value == 1 and self.coin_nearby:
                self.collected = True
                pyxel.blt(self.x, self.y, 0, 36, 8, 4, 4)
                self.local_orb_counter += 1


# Creates a class for colision detection regarding the slime
class Collision_detection:
    def __init__(self, level):
        self.level = level
        global block_pos_l1
        self.block_positions = block_pos_l1

    # Checks if Slime touches the left border wall
    def check_wall_left(self, x):
        if x <= self.level.wall_left:
            return True
        return False

    # Checks if Slime touches the right border wall
    def check_wall_right(self, x):
        if x >= self.level.wall_right:
            return True
        return False

    # Checks if Slime touches the ground
    def check_ground(self, y):
        if y >= self.level.ground_y:
            return True
        return False

    def check_block_below(self, x, y):
        global level_completed
        if not level_completed:
            slime_bottom_y = y + 16  # Bottom edge of slime
            for block_x, block_y in self.level.block_positions:
                if (
                    block_x <= x + 7 and x <= block_x + 7
                ):  # Ensure X is within block range
                    if (
                        block_y - 1 <= slime_bottom_y <= block_y + 2
                    ):  # Allow slight tolerance
                        return True
        return False


# Creates a class that manages the full program
class App:
    def __init__(self):
        pyxel.init(192, 128, fps=60)
        pyxel.load("resources.pyxres")

        self.level1 = None
        self.menu = Menu()
        self.level_menu = Level_Menu()
        self.records_menu = Records_Menu()
        self.options_menu = Options_Menu()
        self.skins_menu = Skins_Menu()
        self.skill_tree_menu = Skill_Tree_Menu()
        self.quit = Quit()

        pyxel.run(self.update, self.draw)

    def initiate_level(self):
        global level_num
        if level_num == 1 and self.level1 is None:
            self.level1 = Level1()

    def update(self):
        global level_num
        if level_num == -4:
            self.skins_menu.update()
        if level_num == 1:
            self.level1.update()

    def draw(self):
        pyxel.cls(0)
        global level_num
        if level_num == -6:
            self.quit.quit_game()
        if level_num == -5:
            self.skill_tree_menu.draw()
        if level_num == -4:
            self.skins_menu.draw()
        if level_num == -3:
            self.options_menu.draw()
        if level_num == -2:
            self.records_menu.draw()
        if level_num == -1:
            global paused
            paused = False
            self.level1 = None
            self.menu.draw()
        if level_num == 0:
            self.level_menu.draw()
        if level_num == 1:
            self.initiate_level()
            self.level1.draw()


# Runs the main function if not imported
if __name__ == "__main__":
    main()
