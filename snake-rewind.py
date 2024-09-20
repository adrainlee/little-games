import tkinter as tk
import random

class SnakeGame:
    def __init__(self, master):
        self.master = master
        self.master.title("贪吃蛇游戏")
        self.master.geometry("800x600")
        self.master.resizable(False, False)

        self.canvas = tk.Canvas(self.master, bg="black", width=790, height=590)
        self.canvas.pack(padx=5, pady=5)

        self.score = 0
        self.score_display = self.canvas.create_text(740, 20, text="得分: 00000", fill="white", font=("Arial", 14), anchor="e")

        self.snake = [(100, 100), (90, 100), (80, 100)]
        self.direction = "Right"
        self.food = self.create_food()

        self.paused = False
        self.game_over_flag = False
        self.pause_menu_selection = 0

        self.master.bind("<KeyPress>", self.handle_keypress)
        self.update()

    def create_food(self):
        x = random.randint(0, 78) * 10
        y = random.randint(0, 58) * 10
        self.food_obj = self.canvas.create_oval(x, y, x+10, y+10, fill="red")
        return (x, y)

    def move_snake(self):
        head = self.snake[0]
        if self.direction == "Right":
            new_head = (head[0] + 10, head[1])
        elif self.direction == "Left":
            new_head = (head[0] - 10, head[1])
        elif self.direction == "Up":
            new_head = (head[0], head[1] - 10)
        elif self.direction == "Down":
            new_head = (head[0], head[1] + 10)

        self.snake.insert(0, new_head)

        if new_head == self.food:
            self.score += 10
            self.canvas.delete(self.food_obj)
            self.food = self.create_food()
            self.update_score()
        else:
            self.snake.pop()

        self.check_collisions()

    def update_score(self):
        self.canvas.itemconfig(self.score_display, text=f"score: {self.score:05d}")

    def check_collisions(self):
        head = self.snake[0]
        if (head[0] < 0 or head[0] >= 790 or
            head[1] < 0 or head[1] >= 590 or
            head in self.snake[1:]):
            self.game_over()

    def game_over(self):
        self.game_over_flag = True
        self.canvas.create_text(395, 295, text="游戏结束", fill="white", font=("Arial", 24))

    def handle_keypress(self, event):
        key = event.keysym
        if not self.paused and not self.game_over_flag:
            if (key == "Right" and self.direction != "Left"):
                self.direction = key
            elif (key == "Left" and self.direction != "Right"):
                self.direction = key
            elif (key == "Up" and self.direction != "Down"):
                self.direction = key
            elif (key == "Down" and self.direction != "Up"):
                self.direction = key
            elif key == "Escape":
                self.pause_game()
        elif self.paused:
            if key == "Up" or key == "Down":
                self.pause_menu_selection = 1 - self.pause_menu_selection
                self.draw_pause_menu()
            elif key == "Return":
                if self.pause_menu_selection == 0:
                    self.resume_game()
                else:
                    self.master.quit()
        elif self.game_over_flag and key == "Return":
            self.master.quit()

    def pause_game(self):
        self.paused = True
        self.draw_pause_menu()

    def resume_game(self):
        self.paused = False
        self.canvas.delete("pause_menu")
        self.update()

    def draw_pause_menu(self):
        self.canvas.delete("pause_menu")
        self.canvas.create_rectangle(300, 200, 500, 400, fill="gray", tags="pause_menu")
        self.canvas.create_text(400, 250, text="继续", fill="white" if self.pause_menu_selection == 0 else "black", font=("Arial", 20), tags="pause_menu")
        self.canvas.create_text(400, 350, text="退出", fill="white" if self.pause_menu_selection == 1 else "black", font=("Arial", 20), tags="pause_menu")

    def draw_snake(self):
        self.canvas.delete("snake")
        for segment in self.snake:
            self.canvas.create_rectangle(segment[0], segment[1],
                                         segment[0]+10, segment[1]+10,
                                         fill="green", tags="snake")

    def update(self):
        if not self.paused and not self.game_over_flag:
            self.move_snake()
            self.draw_snake()
            self.master.after(150, self.update)  # 速度减慢，间隔增加到150毫秒

if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()
