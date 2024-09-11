import tkinter as tk
import random
# import time

class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("贪吃蛇游戏")
        self.canvas = tk.Canvas(root, width=400, height=400, bg="black")
        self.canvas.pack()
        self.snake = [(100, 100), (90, 100), (80, 100)]
        self.food = self.create_food()
        self.direction = "Right"
        self.bind_keys()
        self.speed = 200  # 降低速度
        self.update()

    def create_food(self):
        x = random.randint(0, 39) * 10
        y = random.randint(0, 39) * 10
        return x, y

    def bind_keys(self):
        self.root.bind("<Left>", lambda _: self.change_direction("Left"))
        self.root.bind("<Right>", lambda _: self.change_direction("Right"))
        self.root.bind("<Up>", lambda _: self.change_direction("Up"))
        self.root.bind("<Down>", lambda _: self.change_direction("Down"))

    def change_direction(self, direction):
        if direction == "Left" and self.direction != "Right":
            self.direction = direction
        elif direction == "Right" and self.direction != "Left":
            self.direction = direction
        elif direction == "Up" and self.direction != "Down":
            self.direction = direction
        elif direction == "Down" and self.direction != "Up":
            self.direction = direction

    def move(self):
        head_x, head_y = self.snake[0]
        if self.direction == "Left":
            head_x -= 10
        elif self.direction == "Right":
            head_x += 10
        elif self.direction == "Up":
            head_y -= 10
        elif self.direction == "Down":
            head_y += 10

        self.snake.insert(0, (head_x, head_y))

        if head_x == self.food[0] and head_y == self.food[1]:
            self.food = self.create_food()
        else:
            self.snake.pop()

        if (head_x < 0 or head_x >= 400 or head_y < 0 or head_y >= 400 or
                (head_x, head_y) in self.snake[1:]):
            self.game_over()

    def update(self):
        self.canvas.delete("all")
        self.move()
        for x, y in self.snake:
            self.canvas.create_rectangle(x, y, x + 10, y + 10, fill="green")
        self.canvas.create_oval(self.food[0], self.food[1], self.food[0] + 10, self.food[1] + 10, fill="red")
        self.root.after(self.speed, self.update)

    def game_over(self):
        self.canvas.create_text(200, 200, text="游戏结束", fill="white", font=("Arial", 20))
        self.show_options()

    def show_options(self):
        self.canvas.create_text(200, 250, text="继续游戏(C) / 退出(Q)", fill="white", font=("Arial", 16))
        self.root.bind("<Key>", self.handle_options)

    def handle_options(self, event):
        if event.char.lower() == 'c':
            self.reset_game()
        elif event.char.lower() == 'q':
            self.root.destroy()

    def reset_game(self):
        self.snake = [(100, 100), (90, 100), (80, 100)]
        self.food = self.create_food()
        self.direction = "Right"
        self.update()

if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()
