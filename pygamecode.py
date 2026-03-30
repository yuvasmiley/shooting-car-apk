from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock

class Game(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            Color(1, 0, 0)
            self.rect = Rectangle(pos=(100, 100), size=(100, 100))

        Clock.schedule_interval(self.update, 1/60)

    def update(self, dt):
        x, y = self.rect.pos
        self.rect.pos = (x + 2, y)

class MyApp(App):
    def build(self):
        return Game()

MyApp().run()
