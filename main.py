from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.uix.label import Label
from kivy.core.window import Window
import random

Window.size = (400, 700)


class Game(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # ---------------- CAR ----------------
        self.car_x = 180
        self.car_y = 50
        self.car = Image(source='car.png', size=(60, 90))
        self.add_widget(self.car)

        # ---------------- BULLETS ----------------
        self.bullets = []

        # ---------------- ENEMIES ----------------
        self.enemies = []

        # ---------------- SCORE ----------------
        self.score = 0
        self.label = Label(text="Score: 0", pos=(10, 650))
        self.add_widget(self.label)

        # ---------------- SOUND ----------------
        self.shoot_sound = SoundLoader.load('shoot.wav')

        # Spawn enemies
        for i in range(3):
            self.spawn_enemy()

        # Game loop
        Clock.schedule_interval(self.update, 1 / 60)

    # ---------------- SPAWN ENEMY ----------------
    def spawn_enemy(self):
        x = random.randint(0, 340)
        y = random.randint(700, 1000)

        enemy = Image(source='enemy.png', size=(60, 90), pos=(x, y))
        self.add_widget(enemy)

        self.enemies.append([x, y, enemy])

    # ---------------- TOUCH CONTROL ----------------
    def on_touch_move(self, touch):
        self.car_x = touch.x - 30

    def on_touch_down(self, touch):
        # Shoot bullet
        bullet = Image(source='bullet.png', size=(15, 30),
                       pos=(self.car_x + 20, self.car_y + 80))
        self.add_widget(bullet)

        self.bullets.append([self.car_x + 20, self.car_y + 80, bullet])

        if self.shoot_sound:
            self.shoot_sound.play()

    # ---------------- GAME LOOP ----------------
    def update(self, dt):

        # Move car
        self.car.pos = (self.car_x, self.car_y)

        # Move bullets
        for b in self.bullets[:]:
            b[1] += 10
            b[2].pos = (b[0], b[1])

            if b[1] > Window.height:
                self.remove_widget(b[2])
                self.bullets.remove(b)

        # Move enemies
        for e in self.enemies[:]:
            e[1] -= 5
            e[2].pos = (e[0], e[1])

            if e[1] < 0:
                self.remove_widget(e[2])
                self.enemies.remove(e)
                self.spawn_enemy()

        # Collision
        for b in self.bullets[:]:
            for e in self.enemies[:]:
                if abs(b[0] - e[0]) < 40 and abs(b[1] - e[1]) < 60:
                    self.remove_widget(b[2])
                    self.remove_widget(e[2])

                    self.bullets.remove(b)
                    self.enemies.remove(e)

                    self.spawn_enemy()

                    self.score += 1
                    self.label.text = f"Score: {self.score}"
                    break


class CarGameApp(App):
    def build(self):
        return Game()


if __name__ == "__main__":
    CarGameApp().run()