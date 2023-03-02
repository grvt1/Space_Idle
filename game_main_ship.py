from kivy.graphics import Triangle, Color, Line

def build_main_ship(self):
    with self.canvas:
        Color(1, .4, .4)
        self.main_ship.append(Triangle())
    
def update_main_ship(self):
    x_multiply = int((self.NB_lines/2)-1)
    padding = self.padding*self.width
    center_x = self.width*self.V_SPACING_LINES/2
    offset = center_x * .1
    center_y = (self.height*self.H_SPACING_LINES)*.9
    center_ship = x_multiply*(self.width*self.V_SPACING_LINES)
    self.x1 = center_ship + padding + offset + self.current_x_offset
    self.x2, self.y2 = self.x1 + center_x - offset, center_y
    self.x3 = self.x2 + center_x - offset
    self.main_ship[0].points =  [self.x1, self.y1, self.x2, self.y2, self.x3, self.y3]

def move_main_ship(self, time_factor):
    self.move_speed_x = self.default_speed_x*(self.width/self.default_width)
    self.difference_x = self.move_ship_to - self.x2
    # move right
    if self.move_ship_to > self.x2 and self.difference_x + self.move_speed_x > 0:
        if self.difference_x <= self.move_speed_x:
            self.x1 += self.difference_x
            self.x2 += self.difference_x
            self.x3 += self.difference_x
            # self.current_x_offset += self.difference_x
        else:
            self.current_x_offset += self.move_speed_x*time_factor
    # move left
    if self.move_ship_to < self.x2 and self.difference_x - self.move_speed_x < 0:
        if self.difference_x >= self.move_speed_x:
            self.x1 -= self.difference_x
            self.x2 -= self.difference_x
            self.x3 -= self.difference_x
            # self.current_x_offset -= self.difference_x
        else:
            self.current_x_offset -= self.move_speed_x*time_factor
    self.difference_x = self.move_ship_to-self.x2

def lowest_enemy_x(self):
    difference_x_final = self.width
    difference_y_final = self.height
    difference_x_y_final = self.width+self.height
    for i in self.enemy_ship_coordinates:
        if self.enemy_ship_coordinates[i]["status"] == "online":
            if self.enemy_ship_coordinates[i]["y2"] > self.height*.15:
                difference_x = self.x2 - self.enemy_ship_coordinates[i]["x2"]
                if difference_x < 0:
                    difference_x *= -1
                difference_y = self.y2 - self.enemy_ship_coordinates[i]["y2"]
                if difference_y < 0:
                    difference_y *= -1

                difference_x_y = difference_x + difference_y
                if difference_x_y < difference_x_y_final:
                    self.cross_lock_to = i
                    self.move_ship_to = self.enemy_ship_coordinates[i]["x2"]
                    difference_x_final = self.enemy_ship_coordinates[i]["x2"]
                    difference_y_final = self.enemy_ship_coordinates[i]["y2"]
                    difference_x_y_final = difference_x_y


def build_cross(self):
    with self.canvas.after:
        Color(1, 0, 0)
        for i in range(0, 4):
            self.cross.append(Line())
            self.cross[i].width = (self.width_cross)
        self.circle.append(Line())

def cross_get_to_coordinates(self):
    center_y = self.move_ship_to_y_pos + self.center_cross
    self.cross_get_to = {"x": self.move_ship_to, "y": center_y}

def update_cross_coordinates(self, time_factor):
    speed = (self.default_speed_x + 1)  * time_factor
    difference_x = self.cross_get_to["x"] - self.cross_coordinates["x"]
    difference_y = self.cross_get_to["y"] - self.cross_coordinates["y"]
    # x axes
    
    if difference_x < speed and difference_x > -1*speed:
        self.cross_coordinates["x"] = self.cross_get_to["x"]
    # move x left
    elif self.cross_get_to["x"] <= self.cross_coordinates["x"]:
        self.cross_coordinates["x"] -= speed
    # move x right
    elif self.cross_get_to["x"] >= self.cross_coordinates["x"]:
        self.cross_coordinates["x"] += speed

    # y axes
    if difference_y < speed  and difference_y > -1*speed:
        self.cross_coordinates["y"] = self.cross_get_to["y"]
    # move y down
    elif self.cross_get_to["y"] <= self.cross_coordinates["y"]:
        self.cross_coordinates["y"] -= speed
    # move y up
    elif self.cross_get_to["y"] >= self.cross_coordinates["y"]:
        self.cross_coordinates["y"] += speed

    center_x = self.cross_coordinates["x"]
    center_y = self.cross_coordinates["y"]
    add_points = self.length_cross
    center_empty_points = add_points * .2

    # right
    x1, y1 = center_x + center_empty_points, center_y
    x2, y2 = center_x + add_points, center_y
    self.cross[0].points = [x1, y1, x2, y2]

    # left
    x1, y1 = center_x - center_empty_points, center_y
    x2, y2 = center_x - add_points, center_y
    self.cross[1].points = [x1, y1, x2, y2]

    # up
    x1, y1 = center_x, center_y + center_empty_points
    x2, y2 = center_x, center_y + add_points
    self.cross[2].points = [x1, y1, x2, y2]

    # down
    x1, y1 = center_x, center_y - center_empty_points
    x2, y2 = center_x, center_y - add_points
    self.cross[3].points = [x1, y1, x2, y2]

    # circle in cross
    self.circle[0].circle = [center_x, center_y, add_points/2]