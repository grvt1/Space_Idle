from kivy.graphics import Line, Color
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.metrics import dp

def build_vertical_lines(self):
    self.V_NB_LINES = self.NB_lines
    self.V_SPACING_LINES = 0.79/self.V_NB_LINES
    self.v_lines = []
    with self.canvas:
        for i in range(0, self.V_NB_LINES):
            if i == 0 or i == self.V_NB_LINES-1:
                Color(1, 1, 1, 1)
            else:
                Color(1, 1, 1, 0)
            self.v_lines.append(Line())
        
def update_vertical_lines(self):
    spacing = self.width*self.V_SPACING_LINES
    padding = (self.box_layout_x-self.would_be_last_line)/2
    for i in range(0, self.V_NB_LINES):
        self.v_lines[i].points = [spacing*i+padding, 0, spacing*i+padding, self.height]
        self.H_WIDTH = spacing*i
    self.box_layout_x = int(self.width*.76953125)

    last = len(self.v_lines)-1
    self.would_be_last_line = self.v_lines[last].points[0]

def build_horizontal_lines(self):
    self.H_NB_LINES = self.NB_lines
    self.H_SPACING_LINES = 1/self.H_NB_LINES
    self.h_lines = []
    with self.canvas:
        for i in range(0, self.H_NB_LINES+1):
            if i == 0 or i == self.H_NB_LINES:
                Color(1, 1, 1, 0)
            else:
                Color(1, 1, 1, 0)
            self.h_lines.append(Line())
        
def update_horizontal_lines(self):
    spacing = self.height*self.H_SPACING_LINES
    padding = self.padding*self.width+(self.box_layout_x-self.would_be_last_line)
    for i in range(0, self.H_NB_LINES+1):
        self.h_lines[i].points = [0+padding, spacing*i-self.current_y_offset, self.H_WIDTH+padding, spacing*i-self.current_y_offset]
        
def scroll_down(self, time_factor):
    self.move_speed_y = self.default_speed_y*(self.height/self.default_height)
    if self.current_y_offset <= self.height*self.H_SPACING_LINES:
        self.current_y_offset += self.move_speed_y*time_factor
    else:
        self.current_y_offset = 0
        self.current_y_loop += 1
        self.coordinates_enemy_ship()

def update_perspective(self):
    # update perspective_x/y
    perspective_x = self.width/self.default_width
    perspective_y = self.height/self.default_height
    
    for i in self.enemy_ship_coordinates:
        if self.enemy_ship_coordinates[i]["status"] == "online":
            # update coordinates/speed based on perspective (for active ships)
            self.enemy_ship_coordinates[i]["x1"] *= perspective_x
            self.enemy_ship_coordinates[i]["y1"] *= perspective_y
            self.enemy_ship_coordinates[i]["x2"] *= perspective_x
            self.enemy_ship_coordinates[i]["y2"] *= perspective_y
            self.enemy_ship_coordinates[i]["x3"] *= perspective_x
            self.enemy_ship_coordinates[i]["y3"] *= perspective_y
            self.enemy_ship_coordinates[i]["speed"] *= perspective_y

    # update speed in E_CLASS (for new ships)
    for i in self.E_CLASS:
        self.E_CLASS[i]["speed"] *= perspective_y

    # update laser speed
    self.laser_speed *= perspective_y

    # update main ship speed
    self.default_speed_x *= perspective_x

    # info for cross
    if 0 in self.enemy_ship_coordinates:
        if "x1" in self.enemy_ship_coordinates[0]:
            self.center_cross = self.enemy_ship_coordinates[0]["y1"] - (self.enemy_ship_coordinates[0]["y1"] + self.enemy_ship_coordinates[0]["y2"])/2
            self.length_cross = (self.enemy_ship_coordinates[0]["x1"] - self.enemy_ship_coordinates[0]["x3"])/3
            self.perspective_updated = True

    # update default_width/height so that perspective changes only once per window resize
    self.default_width = self.width
    self.default_height = self.height

def build_grid_menu(self):
    pass

def update_money(self):
    self.grid_menu_info["Money"]["final_text"] = self.grid_menu_info["Money"]["Main_text"] + ": " + str(int(self.grid_menu_info["Money"]["cost"]))

def init_menu(self):
    pass
        

def update_menu_text(self):
    self.money_text.text = self.grid_menu_info["Money"]["final_text"]
    self.fighter_money.text = self.grid_menu_info["fighter_money"]["Main_text"] + "       lv. " + str(self.grid_menu_info["fighter_money"]["current_level"]) + "\n" + self.grid_menu_info["fighter_money"]["bottom_text"] + "               cost: " + str(int(self.grid_menu_info["fighter_money"]["cost"]))
    self.fighter_count.text = self.grid_menu_info["fighter_count"]["Main_text"] + "       lv. " + str(self.grid_menu_info["fighter_count"]["current_level"]) + "\n" + self.grid_menu_info["fighter_count"]["bottom_text"] + "               cost: " + str(int(self.grid_menu_info["fighter_count"]["cost"]))
    self.bomber_money.text = self.grid_menu_info["bomber_money"]["Main_text"] + "       lv. " + str(self.grid_menu_info["bomber_money"]["current_level"]) + "\n" + self.grid_menu_info["bomber_money"]["bottom_text"] + "               cost: " + str(int(self.grid_menu_info["bomber_money"]["cost"]))
    self.bomber_count.text = self.grid_menu_info["bomber_count"]["Main_text"] + "       lv. " + str(self.grid_menu_info["bomber_count"]["current_level"]) + "\n" + self.grid_menu_info["bomber_count"]["bottom_text"] + "               cost: " + str(int(self.grid_menu_info["bomber_count"]["cost"]))
    self.attack_speed.text = self.grid_menu_info["attack_speed"]["Main_text"] + "       lv. " + str(self.grid_menu_info["attack_speed"]["current_level"]) + "\n" + self.grid_menu_info["attack_speed"]["bottom_text"] + "               cost: " + str(int(self.grid_menu_info["attack_speed"]["cost"]))
    self.laser_range_menu.text = self.grid_menu_info["laser_range_menu"]["Main_text"] + "       lv. " + str(self.grid_menu_info["laser_range_menu"]["current_level"]) + "\n" + self.grid_menu_info["laser_range_menu"]["bottom_text"] + "               cost: " + str(int(self.grid_menu_info["laser_range_menu"]["cost"]))
    self.ship_move_speed.text = self.grid_menu_info["ship_move_speed"]["Main_text"] + "       lv. " + str(self.grid_menu_info["ship_move_speed"]["current_level"]) + "\n" + self.grid_menu_info["ship_move_speed"]["bottom_text"] + "               cost: " + str(int(self.grid_menu_info["ship_move_speed"]["cost"]))
    self.max_enemies.text = self.grid_menu_info["max_enemies"]["Main_text"] + "       lv. " + str(self.grid_menu_info["max_enemies"]["current_level"]) + "\n" + self.grid_menu_info["max_enemies"]["bottom_text"] + "               cost: " + str(int(self.grid_menu_info["max_enemies"]["cost"]))

def update_menu_status(self):
    self.fighter_money.disabled = self.grid_menu_info["fighter_money"]["status"]
    self.fighter_count.disabled = self.grid_menu_info["fighter_count"]["status"]
    self.bomber_money.disabled = self.grid_menu_info["bomber_money"]["status"]
    self.bomber_count.disabled = self.grid_menu_info["bomber_count"]["status"]
    self.attack_speed.disabled = self.grid_menu_info["attack_speed"]["status"]
    self.laser_range_menu.disabled = self.grid_menu_info["laser_range_menu"]["status"]
    self.ship_move_speed.disabled = self.grid_menu_info["ship_move_speed"]["status"]
    self.max_enemies.disabled = self.grid_menu_info["max_enemies"]["status"]

def update_menu_css(self):
    # size hint
    self.fighter_money.size_hint = self.menu_size_hint
    self.fighter_count.size_hint = self.menu_size_hint
    self.bomber_money.size_hint = self.menu_size_hint
    self.bomber_count.size_hint = self.menu_size_hint
    self.attack_speed.size_hint = self.menu_size_hint
    self.laser_range_menu.size_hint = self.menu_size_hint
    self.ship_move_speed.size_hint = self.menu_size_hint
    self.max_enemies.size_hint = self.menu_size_hint

    # halign
    self.fighter_money.halign = self.menu_halign
    self.fighter_count.halign = self.menu_halign
    self.bomber_money.halign = self.menu_halign
    self.bomber_count.halign = self.menu_halign
    self.attack_speed.halign = self.menu_halign
    self.laser_range_menu.halign = self.menu_halign
    self.ship_move_speed.halign = self.menu_halign
    self.max_enemies.halign = self.menu_halign

    # valign
    self.fighter_money.valign = self.menu_valign
    self.fighter_count.valign = self.menu_valign
    self.bomber_money.valign = self.menu_valign
    self.bomber_count.valign = self.menu_valign
    self.attack_speed.valign = self.menu_valign
    self.laser_range_menu.valign = self.menu_valign
    self.ship_move_speed.valign = self.menu_valign
    self.max_enemies.valign = self.menu_valign

    # pos_hint
    self.fighter_money.pos_hint = self.menu_pos_hint
    self.fighter_count.pos_hint = self.menu_pos_hint
    self.bomber_money.pos_hint = self.menu_pos_hint
    self.bomber_count.pos_hint = self.menu_pos_hint
    self.attack_speed.pos_hint = self.menu_pos_hint
    self.laser_range_menu.pos_hint = self.menu_pos_hint
    self.ship_move_speed.pos_hint = self.menu_pos_hint
    self.max_enemies.pos_hint = self.menu_pos_hint
    

def hide_upgrade(self, i):
    if self.grid_menu_info[i]['hide']:
        if i == 'fighter_money':
            self.fighter_money.height, self.fighter_money.size_hint_y, self.fighter_money.disabled, self.fighter_money.opacity = 0, None, True, 0
        elif i == 'fighter_count':
            self.fighter_count.height, self.fighter_count.size_hint_y, self.fighter_count.disabled, self.fighter_count.opacity = 0, None, True, 0
        elif i == 'bomber_money':
            self.bomber_money.height, self.bomber_money.size_hint_y, self.bomber_money.disabled, self.bomber_money.opacity = 0, None, True, 0
        elif i == 'bomber_count':
            self.bomber_count.height, self.bomber_count.size_hint_y, self.bomber_count.disabled, self.bomber_count.opacity = 0, None, True, 0
        elif i == 'attack_speed':
            self.attack_speed.height, self.attack_speed.size_hint_y, self.attack_speed.disabled, self.attack_speed.opacity = 0, None, True, 0
        elif i == 'laser_range_menu':
            self.laser_range_menu.height, self.laser_range_menu.size_hint_y, self.laser_range_menu.disabled, self.laser_range_menu.opacity = 0, None, True, 0
        elif i == 'ship_move_speed':
            self.ship_move_speed.height, self.ship_move_speed.size_hint_y, self.ship_move_speed.disabled, self.ship_move_speed.opacity = 0, None, True, 0
        elif i == 'max_enemies':
            self.max_enemies.height, self.max_enemies.size_hint_y, self.max_enemies.disabled, self.max_enemies.opacity = 0, None, True, 0

def disable_upgrade(self, i):
    if self.grid_menu_info[i]['status']:
        if i == 'fighter_money':
            self.fighter_money.disabled = True
        elif i == 'fighter_count':
            self.fighter_count.disabled = True
        elif i == 'bomber_money':
            self.bomber_money.disabled = True
        elif i == 'bomber_count':
            self.bomber_count.disabled = True
        elif i == 'attack_speed':
            self.attack_speed.disabled = True
        elif i == 'laser_range_menu':
            self.laser_range_menu.disabled = True
        elif i == 'ship_move_speed':
            self.ship_move_speed.disabled = True
        elif i == 'max_enemies':
            self.max_enemies.disabled = True

def make_upgrade(self, i):
    self.grid_menu_info[i]["status"] = True
    self.grid_menu_info["Money"]["cost"] -= self.grid_menu_info[i]["cost"]
    self.grid_menu_info[i]["cost"] *= self.grid_menu_info[i]["margin"]
    self.grid_menu_info[i]["current_level"] += 1
    self.update_money()
    self.update_menu()

    if i == "fighter_money":
        self.E_CLASS["Fighter"]["money"] *= self.grid_menu_info[i]["action"]
    elif i == "fighter_count":
        self.E_CLASS["Fighter"]["max_online"] += self.grid_menu_info[i]["action"]
        self.build_enemy_ship()
    elif i == "bomber_money":
        self.E_CLASS["Bomber"]["money"] *= self.grid_menu_info[i]["action"]
    elif i == "bomber_count":
        self.E_CLASS["Bomber"]["max_online"] += self.grid_menu_info[i]["action"]
        self.build_enemy_ship()
    elif i == "attack_speed":
        self.laser_shoot_speed *= self.grid_menu_info[i]["action"]
    elif i == "laser_range_menu":
        self.laser_range_loops += self.grid_menu_info[i]["action"]
    elif i == "ship_move_speed":
        self.default_speed_x *= self.grid_menu_info[i]["action"]
    elif i == "max_enemies":
        self.NB_lines += self.grid_menu_info[i]["action"]
        self.update_condition_menu()
        print('It is done')


        # rebuild vertical lines
        for i in range(0, self.V_NB_LINES):
            self.v_lines[i].points = [-2, -2, -1, -1]
        self.build_vertical_lines()

        # rebuild horizontal lines
        for i in range(0, self.H_NB_LINES):
            self.h_lines[i].points = [-2, -2, -1, -1]
        self.build_horizontal_lines()

        # resize ships
        for i in self.enemy_ship_coordinates:
            center_ship = self.enemy_ship_coordinates[i]["random"]*(self.width*self.V_SPACING_LINES)
            padding = self.padding*self.width
            center_x = self.width*self.V_SPACING_LINES/2
            offset = center_x *.1

            x1 = center_ship + padding + offset
            x2 = x1 + center_x - offset
            x3 = x2 + center_x - offset
            y2 = self.enemy_ship_coordinates[i]["y1"]-((self.height*self.H_SPACING_LINES)*.5)

            # update all
            self.enemy_ship_coordinates[i].update({"x1": x1, "x2": x2, "x3": x3, "y2": y2})

        self.center_cross = self.enemy_ship_coordinates[0]["y1"] - (self.enemy_ship_coordinates[0]["y1"] + self.enemy_ship_coordinates[0]["y2"])/2
        self.length_cross = (self.enemy_ship_coordinates[0]["x1"] - self.enemy_ship_coordinates[0]["x3"])/3

    self.update_menu()
    self.update_perspective()

def update_condition_menu(self):
    self.grid_menu_info["fighter_count"]["condition"]["level_needed"] = self.grid_menu_info['max_enemies']['current_level']
    self.grid_menu_info["bomber_count"]["condition"]["level_needed"] = self.grid_menu_info['max_enemies']['current_level']

def update_menu(self):
    for i in self.grid_menu_info:
        if i != "Money":
            if self.grid_menu_info["Money"]["cost"] >= self.grid_menu_info[i]["cost"] and self.grid_menu_info[i]["current_level"] <= self.grid_menu_info[i]["max_level"]:
                if self.grid_menu_info[i]["condition"]["upgrade"] != "":
                    # condition_upgrade = self.grid_menu_info[i]["condition"]["upgrade"]
                    # conditions_level = self.grid_menu_info[condition_upgrade]["current_level"]
                    conditions_level = self.grid_menu_info[i]['current_level']
                    level_needed = self.grid_menu_info[i]["condition"]["level_needed"]

                    if conditions_level > level_needed:
                        self.grid_menu_info[i]["status"] = True
                        self.disable_upgrade(i)
                    else:
                        self.grid_menu_info[i]["status"] = False
                else:
                    self.grid_menu_info[i]["status"] = False

            elif self.grid_menu_info[i]["max_level"] <= self.grid_menu_info[i]["current_level"]:
                self.grid_menu_info[i]["hide"] = True
                self.hide_upgrade(i)

            else:
                self.grid_menu_info[i]["status"] = True
                self.disable_upgrade(i)

    self.update_menu_text()
    self.update_menu_status()
    self.update_menu_css()
    

    
