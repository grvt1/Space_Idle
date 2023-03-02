from kivy.graphics import Color, Triangle
import random

def build_enemy_ship(self):
    inited = 0
    for i in self.E_CLASS:
        inited += self.E_CLASS[i]["inited"]

    with self.canvas:
        for y in self.E_CLASS:
            for i in range(self.E_CLASS[y]["inited"], self.E_CLASS[y]["max_online"]):
                if self.E_CLASS[y]["color"] == "green":
                    Color(.4, 1, .4)
                elif self.E_CLASS[y]["color"] == "blue":           
                    Color(.4, .4, 1)
                self.enemy_ship.append(Triangle(points=(0,0,0,0,0,0)))
                self.E_CLASS[y]["inited"] += 1
                self.status_offline(inited)
                inited += 1

def status_offline(self, i):
    if i in self.enemy_ship_coordinates:
        if "status" not in self.enemy_ship_coordinates[i]:
            self.enemy_ship_coordinates[i] = {"status": "offline"}
    else:
        self.enemy_ship_coordinates[i] = {"status": "offline"}
    
def get_class(self, current_ship_update):
    if "Class" in self.enemy_ship_coordinates[current_ship_update]:
        e_class_get = self.enemy_ship_coordinates[current_ship_update]["Class"]
    else:
        stop = False
        for i in self.E_CLASS:
            if self.E_CLASS[i]["current_online"] < self.E_CLASS[i]["max_online"] and stop == False:
                e_class_get = i
                stop = True
    self.E_CLASS[e_class_get]["current_online"] += 1
    self.enemy_ship_coordinates[current_ship_update].update({"Class": e_class_get})
    
def x_position(self, current_ship_update, random_list):
    get_random = random.randint(0, self.NB_lines-2)
    while get_random in random_list:
        get_random = random.randint(0, self.NB_lines-2)
    self.enemy_ship_coordinates[current_ship_update].update({"random": get_random})
  
    return get_random

def coordinates_enemy_ship(self):
    random_list = []
    updated = 0
    for i in range(0, len(self.enemy_ship_coordinates)):
        if self.enemy_ship_coordinates[i]["status"] == "offline" and updated <= self.NB_lines-2:
            self.get_class(i)         # get class
            speed = self.E_CLASS[self.enemy_ship_coordinates[i]["Class"]]["speed"]            # get speed
            
            random_pos = self.x_position(i, random_list)
            random_list.append(random_pos)       # get position x

            # position
            center_ship = self.enemy_ship_coordinates[i]["random"]*(self.width*self.V_SPACING_LINES)
            padding = (self.box_layout_x-self.would_be_last_line)/2
            center_x = self.width*self.V_SPACING_LINES/2
            offset = center_x *.1
            center_y = self.height-((self.height*self.H_SPACING_LINES)*.5)
            offscreen_start = self.height*.15
            x1, y1 = center_ship + padding + offset, self.height+offscreen_start
            x2, y2 = x1 + center_x - offset, center_y+offscreen_start
            x3, y3 = x2 + center_x - offset, self.height+offscreen_start

            # update all
            self.enemy_ship_coordinates[i].update({"x1": x1, "y1": y1, "x2": x2, "y2": y2, "x3": x3, "y3": y3, "status": "online", "speed": speed})
            self.E_NB_ships_online += 1
            updated += 1
            

# move all enemy ships down
def update_enemy_ship(self, time_factor):
    for i in range(0, len(self.enemy_ship_coordinates)):
        if self.enemy_ship_coordinates[i]["status"] == "online":
            speed = self.enemy_ship_coordinates[i]["speed"] * time_factor
            self.enemy_ship_coordinates[i]["y1"] -= speed 
            self.enemy_ship_coordinates[i]["y2"] -= speed
            self.enemy_ship_coordinates[i]["y3"] -= speed
            self.enemy_ship[i].points = [self.enemy_ship_coordinates[i]["x1"], self.enemy_ship_coordinates[i]["y1"], self.enemy_ship_coordinates[i]["x2"], self.enemy_ship_coordinates[i]["y2"], self.enemy_ship_coordinates[i]["x3"], self.enemy_ship_coordinates[i]["y3"]]
        for laser_i in self.laser_coordinates:
            if self.laser_coordinates[laser_i]["status"] == True and self.laser_coordinates[laser_i]["enemy_number"] == i:
                self.first_to_hit_laser(laser_i)
                self.enemy_hit_laser(laser_i)
    self.update_NB_ship()            

def off_screen_enemy(self):
    for i in self.enemy_ship_coordinates:
        if self.enemy_ship_coordinates[i]["status"] == "online":
            if self.enemy_ship_coordinates[i]["y1"] < -(self.height*.05):
                self.enemy_ship_coordinates[i]["status"] = "offline"
                self.E_CLASS[self.enemy_ship_coordinates[i]["Class"]]["current_online"] -= 1
                self.E_NB_ships_online -= 1

def turn_off_enemy(self, i):
    if i >= 0:
        self.enemy_ship[i].points = [0, 0, 0, 0, 0, 0]
        self.enemy_ship_coordinates[i]["status"] = "offline"
        self.grid_menu_info["Money"]["cost"] += self.E_CLASS[self.enemy_ship_coordinates[i]["Class"]]["money"]
        self.E_CLASS[self.enemy_ship_coordinates[i]["Class"]]["current_online"] -= 1
        self.E_NB_ships_online -= 1
        self.lowest_enemy_x()
        self.update_money()
        self.update_menu()

def update_NB_ship(self):
    self.E_NB_ships = 0
    for i in self.E_CLASS:
        self.E_NB_ships += self.E_CLASS[i]["max_online"]

