from kivy.properties import NumericProperty, StringProperty
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
from kivy.core.window import Window

class MenuScreen(Screen):
    # Menu text
    greeting_text = "W  e  l  c  o  m  e    t  o    t  h  e    p  r  o  g  r  a  m"
    greeting_size = NumericProperty(0)
    greeting_opacity = NumericProperty(0)
    menu_font_size = NumericProperty(0)

    default_width = 1024
    current_width = default_width
    default_height = 780

    fps = 60
    game_start = 0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_interval(self.update, 1/self.fps)

    def greetings_update(self, time_factor):
        # greetings opacity
        if self.greeting_opacity < 1:
            self.greeting_opacity += .002*time_factor
        # greetings font size
        if self.current_width > self.width and self.greeting_size > 15:
            self.greeting_size -= self.default_width/self.width-1

        elif self.current_width < self.width and self.greeting_size < 20:
            self.greeting_size += self.default_width/self.width-1

    def menu_update(self):
        # menu font size
        if self.current_width > self.width and self.menu_font_size > 10:
            self.menu_font_size -= self.default_width/self.width-1
        elif self.current_width < self.width and self.menu_font_size < 15:
            self.menu_font_size += self.default_width/self.width-1
        self.current_width = self.width

    def user_exit(self):
        exit
    
    def start(self):
        #GameWidget().reset()
        pass

    def update(self, dt):
        time_factor = dt*self.fps
        self.greetings_update(time_factor)
        self.menu_update()
        if self.width == 100:
            self.greeting_size = 20
            self.greeting_opacity = .1
            self.menu_font_size = 15

class Settings(Screen):
    resolution_opt = ["640 x 480", "1280 x 720", "1920 x 1080"]
    display = 1
    display_resolution_text = StringProperty(resolution_opt[display])
    fps = 60

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def left_resolution_text(self):
        if self.display == 0:
            self.display = 2
        else:
            self.display -= 1
        self.update_resolution()
    
    def right_resolution_text(self):
        if self.display == 2:
            self.display = 0
        else: 
            self.display += 1
        self.update_resolution()
        
    def update_resolution(self):
        self.display_resolution_text = str(self.resolution_opt[self.display])
        split_resolution = self.resolution_opt[self.display].split(" ")
        x = int(split_resolution[0])
        y = int(split_resolution[2])
        Window.size = (x, y)
