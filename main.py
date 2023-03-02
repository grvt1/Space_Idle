from kivy.config import Config
Config.set("graphics", "width", 1024)
Config.set("graphics", "height", 780)

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.graphics import Line, Color
from kivy.clock import Clock
from kivy.properties import NumericProperty, ObjectProperty
import time
from main_menu import Settings, MenuScreen

class mainKV(App):
    def build(self):
        # Create the screen manager
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(Settings(name='settings'))
        sm.add_widget(GameWidget(name='game'))
        return sm


class GameWidget(Screen):
    from game_grid import update_horizontal_lines, update_vertical_lines, build_horizontal_lines, build_vertical_lines, scroll_down, update_perspective, build_grid_menu, update_money, init_menu, make_upgrade, update_menu, update_condition_menu, update_menu_text, update_menu_status, update_menu_css, hide_upgrade
    from game_main_ship import build_main_ship, move_main_ship, update_main_ship, lowest_enemy_x, build_cross, update_cross_coordinates, cross_get_to_coordinates
    from game_enemy import build_enemy_ship, status_offline, x_position, coordinates_enemy_ship, update_enemy_ship, off_screen_enemy, update_NB_ship, get_class, turn_off_enemy

    game_started = 0
    fps = 60
    NB_lines = 6
    padding = .01
    default_width = 1024
    default_height = 780
    perspective_updated = False

    box_layout_x = NumericProperty(0)
    would_be_last_line = 0
    grid_menu = []
    grid_menu_info = {
"Money": {"Main_text": "Credits", "bottom_text": 0, "Info_text": "", "cost": 10000, "final_text": "aa", "type": "label"},
"fighter_money": {"Main_text": "Fighter value", "bottom_text": "Increase by 30%", "Info_text": "", "action": 1.3, "cost": 10, "margin": 1.3, "status": True, "final_text": "", "max_level": 100, "current_level": 1, "condition": {"upgrade": "", "level_needed": 0}, "hide": False},
"fighter_count": {"Main_text": "Increase Fighters", "bottom_text": "Increase by 1", "Info_text": "", "action": 1, "cost": 100, "margin": 1.8, "status": True, "final_text": "", "max_level": 100, "current_level": 3, "condition": {"upgrade": "max_enemies", "level_needed": 0}, "hide": False},
"bomber_money": {"Main_text": "Bomber value", "bottom_text": "Increase by 10%", "Info_text": "", "action": 1.5, "cost": 100, "margin": 1.3, "status": True, "final_text": "", "max_level": 100, "current_level": 1, "condition": {"upgrade": "bomber_count", "level_needed": 0}, "hide": False},
"bomber_count": {"Main_text": "Increase Bombers", "bottom_text": "Increase by 1", "Info_text": "", "action": 1, "cost": 1000, "margin": 1.9, "status": True, "final_text": "", "max_level": 100, "current_level": 1, "condition": {"upgrade": "max_enemies", "level_needed": 0}, "hide": False},
"attack_speed": {"Main_text": "Attack Speed", "bottom_text": "Increase by 10%", "Info_text": "", "action": .9, "cost": 50, "margin": 4.1, "status": True, "final_text": "", "max_level": 25, "current_level": 1, "condition": {"upgrade": "", "level_needed": 0}, "hide": False},
"laser_range_menu": {"Main_text": "Laser range", "bottom_text": "Increase by 3 clicks", "Info_text": "", "action": 3, "cost": 650, "margin": 3.6, "status": True, "final_text": "", "max_level": 25, "current_level": 1, "condition": {"upgrade": "", "level_needed": 0}, "hide": False},
"ship_move_speed": {"Main_text": "Ship move speed", "bottom_text": "Increase by 10%", "Info_text": "", "action": 1.1, "cost": 50,  "margin": 10, "status": True, "final_text": "", "max_level": 10, "current_level": 1, "condition": {"upgrade": "", "level_needed": 0}, "hide": False},
"max_enemies": {"Main_text": "Increase max enemies", "bottom_text": "Increase by 1", "Info_text": "", "action": 2, "cost": 1,  "margin": 1.1, "status": True, "final_text": "", "max_level": 23, "current_level": 3, "condition": {"upgrade": "", "level_needed": 0}, "hide": False}
                }

    money_text = ObjectProperty(None)

    fighter_money = ObjectProperty(None)
    fighter_count = ObjectProperty(None)
    bomber_money = ObjectProperty(None)
    bomber_count = ObjectProperty(None)
    attack_speed = ObjectProperty(None)
    laser_range_menu = ObjectProperty(None)
    ship_move_speed = ObjectProperty(None)
    max_enemies = ObjectProperty(None)

    menu_size_hint = 1, .11
    menu_text_size_x = .22, .20
    menu_text_size_y = 50
    menu_halign = 'left'
    menu_valign = 'top'
    menu_pos_hint = {"top": 1}


    V_NB_LINES = NB_lines
    V_SPACING_LINES = 0.79/V_NB_LINES
    v_lines = []
    last = NB_lines-1

    H_NB_LINES = NB_lines
    H_SPACING_LINES = 1/H_NB_LINES
    H_WIDTH = 0
    h_lines = []
    move_speed_y = 0
    default_speed_y = 2
    current_y_offset = 0
    current_y_loop = 0
    loop = 0

    main_ship = []
    x1, y1 = 0, 10
    x2, y2 = 0, 0
    x3, y3 = 0, 10
    move_ship_to = 0
    move_ship_to_y_pos = 0
    # closest_x_enemy = default_width
    difference_x = 0
    move_speed_x = 0
    default_speed_x = 2
    current_x_offset = 0
    lowest_enemy_last_update = 0

    cross = []
    cross_coordinates = {"x": 0, "y": 0}
    cross_get_to = {}
    cross_lock_to = False
    center_cross = 0        # center of the enemy
    length_cross = 0        # length of each line in cross
    width_cross = 1.5       # width of the cross
    circle = []

    laser = []
    laser_coordinates = {}
    laser_count = 1
    laser_speed = 4 # how fast it will travel
    laser_shoot_speed = 1.5   # how often it will shoot (in seconds)
    laser_shot_at = 0   # last time laser was shot
    laser_range = 0
    laser_range_loops = 3
    

    enemy_ship = []
    enemy_ship_coordinates = {}
    # E_NB_ships = 0
    E_NB_ships_online = 0
    E_CLASS = {"Fighter": {"speed": 2, "color": "green", "max_online": 3, "current_online": 0, "inited": 0, "money": 1},
                "Bomber": {"speed": 1, "color": "blue", "max_online": 0, "current_online": 0, "inited": 0, "money": 4}
            }

    def __init__(self, **kw):
        super().__init__(**kw)
        self.width = self.default_width
        self.height = self.default_height
        # self.build_grid_menu()
        self.update_NB_ship()
        self.build_vertical_lines()
        self.build_horizontal_lines()
        self.build_main_ship()
        self.build_enemy_ship()
        self.build_cross()
        self.lowest_enemy_x()
        # self.init_menu()
        self.update_money()
        self.update_menu()
        
        Clock.schedule_interval(self.update, 1/self.fps)

    def build_laser(self):
        with self.canvas:
            Color(1, .7, 0)
            if self.laser_shot_at + self.laser_shoot_speed < time.time():
                self.laser_shot_at = time.time()
                self.laser_range = (self.H_SPACING_LINES * self.height)*self.laser_range_loops
                # find if there are lasers already offline
                update_laser = False
                for i in self.laser_coordinates:
                    if self.laser_coordinates[i]["status"] == False:
                        update_laser = i             # if offline then update that laser

                # if there is not yet any laser then add a new laser
                if update_laser == False:
                    self.laser.append(Line())
                    update_laser = len(self.laser)-1

                # initiate laser    
                self.update_laser(update_laser)
    
    def update_laser(self, i):
        x1, y1 = self.x2, self.y2
        x2, y2 = self.x2, self.y2 + self.length_cross
        self.laser[i].points = [x1, y1, x2, y2]
        self.laser[i].width = 2
        self.laser_coordinates[i] = {"x1": x1, "y1": y1, "x2": x2, "y2": y2, "status": True, "hit_y": self.laser_range, "enemy_number": False}

    def coordinates_laser(self, time_factor):
        speed = self.laser_speed * time_factor
        for i in self.laser_coordinates:
            if self.laser_coordinates[i]["status"] == True:
                self.laser_coordinates[i]["y1"] += speed
                self.laser_coordinates[i]["y2"] += speed
                self.laser[i].points = [self.laser_coordinates[i]["x1"], self.laser_coordinates[i]["y1"], self.laser_coordinates[i]["x2"], self.laser_coordinates[i]["y2"]]
                self.update_laser_status(i)
            self.first_to_hit_laser(i)

    def update_laser_status(self, i):
        if self.laser_coordinates[i]["y1"]-self.laser_speed >= self.laser_coordinates[i]["hit_y"] or self.laser_coordinates[i]["y1"] >= self.laser_range:
            self.laser_coordinates[i]["status"] = False
            self.laser_coordinates[i].update({"x1": 0, "y1": 0, "x2": 0, "y2": 0, })
            self.laser_coordinates[i]["enemy_number"] = False
            self.laser[i].points = [0, 0, 0, 0]
        return self.laser_coordinates[i]["status"]

    def first_to_hit_laser(self, laser_i):
        lowest = self.height
        for i in range(0, len(self.enemy_ship_coordinates)):
            if self.enemy_ship_coordinates[i]["status"] == "online":
                if self.enemy_ship_coordinates[i]["x1"] < self.laser_coordinates[laser_i]["x2"] < self.enemy_ship_coordinates[i]["x3"]:
                    if self.enemy_ship_coordinates[i]["y2"] <= lowest and self.enemy_ship_coordinates[i]["y2"] >= self.height*.05:
                        lowest = self.enemy_ship_coordinates[i]["y2"]
                        y1_y2 = (self.enemy_ship_coordinates[i]["y1"]-self.enemy_ship_coordinates[i]["y2"])/2
                        plus_x = self.enemy_ship_coordinates[i]["x2"] - self.laser_coordinates[laser_i]["x2"]
                        if plus_x < 0:
                            plus_x *= -1
                        if plus_x == 0:
                            y1_y2 = 2
                        if lowest+plus_x > self.enemy_ship_coordinates[i]["y1"]:
                            self.laser_coordinates[laser_i]["hit_y"] = self.enemy_ship_coordinates[i]["y1"]
                        else:
                            self.laser_coordinates[laser_i]["hit_y"] = lowest+plus_x
                        self.laser_coordinates[laser_i]["enemy_number"] = i

    def enemy_hit_laser(self, i):
        del_list = []
        status = self.laser_coordinates[i]["status"]
        enemy_no = self.laser_coordinates[i]["enemy_number"]
        enemy_y2 = self.enemy_ship_coordinates[enemy_no]["y2"]


        if status == True:
            if self.laser_coordinates[i]["hit_y"] >= enemy_y2 and self.laser_coordinates[i]["hit_y"] <= self.laser_coordinates[i]["y1"]:
                self.laser_coordinates[i].update({"x1": 0, "y1": 0, "x2": 0, "y2": 0, })
                self.laser[i].points = [0, 0, 0, 0]
                
                self.turn_off_enemy(self.laser_coordinates[i]["enemy_number"])
                self.laser_coordinates[i]["status"] = False
                self.laser_coordinates[i]["enemy_number"] = False
                for y in self.laser_coordinates:
                    if y != i:
                        self.laser_coordinates[y]["hit_y"] = self.laser_range
                        self.laser_coordinates[y]["enemy_number"] = False
                    self.first_to_hit_laser(i)
                # self.update_laser_status(i)
                del_list.append(i)
                            
        # self.del_laser(del_list)

    def del_laser(self, del_list):
        for i in del_list:
            del self.laser_coordinates[i]
            del self.laser[i]

    def update(self, dt):
        time_factor = dt*self.fps

        self.update_vertical_lines()
        self.update_horizontal_lines()
        self.scroll_down(time_factor)       
        self.move_main_ship(time_factor)
        self.update_main_ship()
        self.update_enemy_ship(time_factor)
        self.off_screen_enemy()
        if self.lowest_enemy_last_update + 1 <= int(time.time()):
            self.lowest_enemy_x()
            self.lowest_enemy_last_update = int(time.time())
        self.cross_get_to_coordinates()
        self.update_cross_coordinates(time_factor)
        
        # update cross size
        enemy_x_length = 0
        found_enemy_x_length = False
        for i in self.enemy_ship_coordinates:
            if self.enemy_ship_coordinates[i]["status"] == "online" and found_enemy_x_length == False:
                enemy_x_length = self.enemy_ship_coordinates[i]["x2"] - self.enemy_ship_coordinates[i]["x1"]
                found_enemy_x_length = True

        if self.cross_get_to["x"]-enemy_x_length <= self.x2 <= self.cross_get_to["x"]+enemy_x_length:
            self.build_laser()

        # update cross y posizition based on enemy y position
        if self.cross_lock_to in self.enemy_ship_coordinates and self.enemy_ship_coordinates[self.cross_lock_to]["status"] == "online":
            self.move_ship_to_y_pos = self.enemy_ship_coordinates[self.cross_lock_to]["y2"]

        self.coordinates_laser(time_factor)
        # self.enemy_hit_laser()

        # update perspective
        if self.width != self.default_width or self.height != self.default_height or self.perspective_updated == False:
            self.update_perspective()

        if self.cross_lock_to != False:
            if self.enemy_ship_coordinates[self.cross_lock_to]["y2"] <= self.height*.15:
                self.lowest_enemy_x()

        print(self.laser_range_loops)
mainKV().run()