import tkinter as tk
from PIL import Image, ImageTk
import time

class Bullet:
    def __init__(self, canvas, x, y):
        self.canvas = canvas
        self.bullet = self.canvas.create_rectangle(x-2, y-10, x+2, y, fill="yellow")
        self.damage = 50
        self.speed = 10

    def move(self):
        self.canvas.move(self.bullet, 0, -self.speed)
        if self.canvas.coords(self.bullet)[1] <= 0:
            self.canvas.delete(self.bullet)

class Laser:
    def __init__(self, canvas, x, y):
        self.canvas = canvas
        self.laser = self.canvas.create_rectangle(x-1, y-30, x+1, y, fill="red")
        self.damage = 500

    def stop(self):
        pass  # Laser now remains stationary

class SpaceGame:
    def __init__(self, master):
        self.master = master
        self.master.title("太空大战")
        self.master.geometry("800x600")
        self.master.resizable(False, False)

        # 游戏状态
        self.paused = False
        self.bullets = []
        self.last_bullet_time = time.time()

        # 创建画布
        self.canvas = tk.Canvas(self.master, width=800, height=600, bg="black")
        self.canvas.pack()

        # 加载飞船图片
        self.spaceship_image = Image.open("spaceship.png")
        self.spaceship_image = self.spaceship_image.resize((50, 50), Image.LANCZOS)
        self.spaceship_photo = ImageTk.PhotoImage(self.spaceship_image)

        # 创建飞船
        self.spaceship = self.canvas.create_image(400, 500, image=self.spaceship_photo)

        # 绑定事件
        self.canvas.bind("<Motion>", self.move_spaceship)
        self.master.bind("<space>", self.shoot_laser)
        self.master.bind("<Escape>", self.toggle_pause)
        self.master.bind("<Up>", self.menu_up)
        self.master.bind("<Down>", self.menu_down)
        self.master.bind("<Return>", self.menu_select)

        # 隐藏鼠标
        self.canvas.config(cursor="none")

        self.game_loop()

    def move_spaceship(self, event):
        if not self.paused:
            # 获取鼠标坐标
            x, y = event.x, event.y

            # 限制飞船在窗口内移动
            x = max(25, min(x, 775))
            y = max(25, min(y, 575))

            # 移动飞船
            self.canvas.coords(self.spaceship, x, y)

    def shoot_bullet(self):
        current_time = time.time()
        if current_time - self.last_bullet_time >= 0.33:  # 每秒3发
            x, y = self.canvas.coords(self.spaceship)
            bullet = Bullet(self.canvas, x, y)
            self.bullets.append(bullet)
            self.last_bullet_time = current_time

    def shoot_laser(self, event):
        if not self.paused:
            x, y = self.canvas.coords(self.spaceship)
            laser = Laser(self.canvas, x, y)

    def toggle_pause(self, event):
        self.paused = not self.paused
        if self.paused:
            self.show_menu()
        else:
            self.hide_menu()

    def show_menu(self):
        self.menu_state = 0
        self.menu_items = [
            self.canvas.create_text(400, 250, text="继续", font=("Arial", 20), fill="white"),
            self.canvas.create_text(400, 300, text="退出", font=("Arial", 20), fill="white")
        ]
        self.update_menu()

    def update_menu(self):
        for index, item in enumerate(self.menu_items):
            if index == self.menu_state:
                self.canvas.itemconfig(item, fill="red")
            else:
                self.canvas.itemconfig(item, fill="white")

    def hide_menu(self):
        for item in self.menu_items:
            self.canvas.delete(item)

    def menu_up(self, event):
        if self.paused:
            self.menu_state = (self.menu_state - 1) % 2
            self.update_menu()

    def menu_down(self, event):
        if self.paused:
            self.menu_state = (self.menu_state + 1) % 2
            self.update_menu()

    def menu_select(self, event):
        if self.paused:
            if self.menu_state == 0:
                self.toggle_pause(None)  # 继续游戏
            elif self.menu_state == 1:
                self.master.quit()  # 退出游戏

    def game_loop(self):
        if not self.paused:
            self.shoot_bullet()
            for bullet in self.bullets:
                bullet.move()
            self.bullets = [bullet for bullet in self.bullets if self.canvas.bbox(bullet.bullet)]
        
        self.master.after(33, self.game_loop)  # Updated delay

if __name__ == "__main__":
    root = tk.Tk()
    game = SpaceGame(root)
    root.mainloop()
