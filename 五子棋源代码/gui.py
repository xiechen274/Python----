import tkinter as tk
from tkinter import messagebox
from game_logic import GameLogic
from PIL import Image, ImageTk


class GameGUI:
    def __init__(self, root, game_logic):

        self.root = root
        self.root.title("五子棋游戏")
        self.game_logic = game_logic
        self.num_games = 0  # 记录已经进行的游戏数
        self.num_wins = {1: 0, -1: 0}  # 记录各玩家的胜利次数
        self.root.geometry("350x650")  # 增加窗口的高度
        self.create_start_menu()  # 创建开始菜单
        # 添加消息标签
        self.message_label = tk.Label(root, text="玩的爽可以考虑请Edward喝杯咖啡.jpg", font=("Helvetica", 15),
                                      fg="blue", bg="white")
        self.message_label.pack()

        # 创建棋盘
        self.canvas = tk.Canvas(root, width=350, height=500)
        self.canvas.pack()

        # 绘制背景图片
        self.draw_background()  # 确保在绘制棋盘之前调用

        # 绘制棋盘线条
        self.draw_board()

        self.canvas.bind("<Button-1>", self.on_canvas_click)

        self.restart_button = tk.Button(root, text="重新开始", command=self.restart_game)
        self.restart_button.pack()

        self.score_label = tk.Label(root, text="比分：黑棋(0) - 白棋(0)", font=("Helvetica", 20,), fg="red", bg="white")
        self.score_label.pack()

    def draw_background(self):
        image_path = '/Users/xiechen/Library/Mobile Documents/com~apple~CloudDocs/QLU/计科/python/五子棋源代码/IMG_0627.JPG'

        image = Image.open(image_path)
        image = image.resize((200, 225), Image.Resampling.LANCZOS)
        self.background_image = ImageTk.PhotoImage(image)
        # 在棋盘上添加图片作为背景
        self.canvas.create_image(
            175,  # X坐标，画布宽度的一半
            325,  # Y坐标，画布高度的一半
            image=self.background_image,
            anchor='n'  # 确保图片的中心位于指定坐标
        )

    def draw_board(self):
        # 绘制棋盘
        board_size = self.game_logic.board_size
        delta = 20
        edge = delta * (board_size - 1) + 20  # 计算棋盘边缘位置
        for i in range(board_size):
            self.canvas.create_line(20 + i * delta, 20, 20 + i * delta, edge)
            self.canvas.create_line(20, 20 + i * delta, edge, 20 + i * delta)

    def create_start_menu(self):
        self.start_frame = tk.Frame(self.root)
        self.start_frame.pack(padx=10, pady=10)

        tk.Label(self.start_frame, text="五子棋游戏", font=("Helvetica", 20)).pack(side="top", pady=10)
        tk.Button(self.start_frame, text="开始游戏", command=self.start_game).pack(side="top")

    def start_game(self):
        # 隐藏开始菜单
        self.start_frame.pack_forget()
        # 现在询问用户先手棋子颜色
        color = messagebox.askquestion("先手选择", "是否选择黑棋为先手?")
        if color == 'yes':
            self.game_logic.current_player = 1  # 黑棋为先手
        else:
            self.game_logic.current_player = -1  # 白棋为先手

        # 设置棋盘
        self.setup_game_board()

    def on_canvas_click(self, event):
        # 处理玩家的点击事件
        if not self.game_logic.game_over:
            col = (event.x - 20) // 20
            row = (event.y - 20) // 20
            if self.game_logic.is_valid_move(row, col):
                self.game_logic.make_move(row, col)
                self.draw_piece(row, col)
                if self.game_logic.game_over:
                    self.num_games += 1
                    winner = self.game_logic.winner
                    winner_name = "白棋" if winner == 1 else "黑棋"
                    if winner in self.num_wins:
                        self.num_wins[winner] += 1
                    self.update_score_label()
                    messagebox.showinfo("游戏结束",
                                        f"获胜玩家是：{winner_name}\n已经进行了{self.num_games}局\n当前比分：白棋({self.num_wins.get(1, 0)}) - 黑棋({self.num_wins.get(-1, 0)})")

    def draw_piece(self, row, col):
        # 绘制棋子
        x = 20 + col * 20
        y = 20 + row * 20
        color = "black" if self.game_logic.current_player == 1 else "white"
        self.canvas.create_oval(x - 8, y - 8, x + 8, y + 8, fill=color)

    def restart_game(self):
        # 重新开始游戏
        self.game_logic.__init__(self.game_logic.board_size)  # 重新初始化游戏逻辑
        self.canvas.delete("all")  # 清空棋盘
        self.draw_background()  # 重新绘制背景图片
        self.draw_board()  # 重新绘制棋盘
        self.update_score_label()  # 更新得分显示

    def update_score_label(self):
        # 更新比分显示
        black_score = self.num_wins.get(1, 0)
        white_score = self.num_wins.get(-1, 0)
        color = "red" if black_score > white_score else "black" if white_score > black_score else "black"
        self.score_label.config(text=f"比分：白棋({black_score}) - 黑棋({white_score})", fg=color)


if __name__ == "__main__":
    root = tk.Tk()
    game_logic = GameLogic()
    gui = GameGUI(root, game_logic)
    root.mainloop()