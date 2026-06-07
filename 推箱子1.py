import tkinter as tk
from tkinter import messagebox

# 基础配置
CELL_SIZE = 45

# 多关卡地图
LEVELS = [
    # 第一关
    [
        "##########",
        "#□□□□□□□□#",
        "#□#★□#□□□#",
        "#□#□□□□箱□#",
        "#□□□箱□#□□#",
        "#□#□□□□人□#",
        "#□★□□#□□□#",
        "##########"
    ],
    # 第二关
    [
        "############",
        "#□□##□□□□□#",
        "#□□□□箱□#",
        "#□□##□□★□#",
        "#□□□□□□□人#",
        "#□箱□★□□□#",
        "############"
    ],
    # 第三关
    [
        "##############",
        "#□□□#□□□□□□#",
        "#□箱□#□箱□★#",
        "#□□□□□□□□#",
        "#□箱#□★□人#",
        "#□□□#□★□□□#",
        "##############"
    ]
]

# 地图符号定义
WALL = "#"
EMPTY = "□"
TARGET = "★"
BOX = "箱"
PLAYER = "人"

# 美化配色
COLOR_MAP = {
    WALL: "#3a3a3a",
    EMPTY: "#e8f4f8",
    TARGET: "#ff7875",
    BOX: "#faad14",
    PLAYER: "#2f54eb"
}


class Sokoban:
    def __init__(self, root):
        self.root = root
        self.root.title("多关卡推箱子游戏")
        self.cur_level = 0
        self.game_map = []
        self.player_x = 0
        self.player_y = 0
        self.targets = []
        self.rows = 0
        self.cols = 0
        self.step_count = 0  # 本局步数统计

        # 顶部信息栏
        self.info_frame = tk.Frame(root, bg="#f0f2f5", padx=10, pady=5)
        self.info_frame.pack(fill=tk.X)
        self.level_label = tk.Label(self.info_frame, text="当前关卡：1", font=("微软雅黑", 12))
        self.level_label.pack(side=tk.LEFT, padx=20)
        self.step_label = tk.Label(self.info_frame, text="移动步数：0", font=("微软雅黑", 12))
        self.step_label.pack(side=tk.LEFT, padx=20)

        # 功能按钮栏
        self.btn_frame = tk.Frame(root, bg="#f0f2f5", padx=10, pady=5)
        self.btn_frame.pack(fill=tk.X)
        self.restart_btn = tk.Button(self.btn_frame, text="重新开始本局", command=self.restart_level,
                                     font=("微软雅黑", 10))
        self.restart_btn.pack(side=tk.LEFT, padx=10)

        # 游戏画布
        self.canvas = tk.Canvas(root, bg="#f0f2f5")
        self.canvas.pack(padx=10, pady=10)

        # 加载初始关卡
        self.load_level(self.cur_level)
        # 绑定键盘事件
        self.root.bind("<Key>", self.key_event)
        self.draw_map()
        self.center_window()
        # 开局弹出操作说明
        self.show_game_tip()

    # 开局操作提示
    def show_game_tip(self):
        tip = "游戏操作说明\n↑↓←→ 方向键控制人物移动\n将所有箱子推到红色目标点即可通关\nQ键退出游戏\n点击按钮可重置当前关卡"
        messagebox.showinfo("游戏指引", tip)

    # 窗口居中
    def center_window(self):
        self.root.update()
        w = self.root.winfo_width()
        h = self.root.winfo_height()
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = (sw - w) // 2
        y = (sh - h) // 2
        self.root.geometry(f"{w}x{h}+{x}+{y}")

    # 重新开始当前关卡
    def restart_level(self):
        self.step_count = 0
        self.update_info()
        self.load_level(self.cur_level)
        self.draw_map()

    # 更新关卡、步数文字显示
    def update_info(self):
        self.level_label.config(text=f"当前关卡：{self.cur_level + 1}")
        self.step_label.config(text=f"移动步数：{self.step_count}")

    # 加载关卡数据
    def load_level(self, idx):
        if idx >= len(LEVELS):
            messagebox.showinfo("游戏结束", "🎉 恭喜通关所有关卡！")
            self.root.quit()
            return

        raw_map = LEVELS[idx]
        self.rows = len(raw_map)
        self.cols = max(len(row) for row in raw_map)
        self.game_map = []
        for row in raw_map:
            if len(row) < self.cols:
                row = row.ljust(self.cols, WALL)
            elif len(row) > self.cols:
                row = row[:self.cols]
            self.game_map.append(list(row))

        self.targets.clear()
        for y in range(self.rows):
            for x in range(self.cols):
                char = self.game_map[y][x]
                if char == PLAYER:
                    self.player_x = x
                    self.player_y = y
                    self.game_map[y][x] = EMPTY
                elif char == TARGET:
                    self.targets.append((x, y))

        self.canvas.config(width=self.cols * CELL_SIZE, height=self.rows * CELL_SIZE)
        self.update_info()

    # 绘制游戏画面
    def draw_map(self):
        self.canvas.delete("all")
        gap = 2
        for y in range(self.rows):
            for x in range(self.cols):
                cell = self.game_map[y][x]
                x1 = x * CELL_SIZE + gap
                y1 = y * CELL_SIZE + gap
                x2 = (x + 1) * CELL_SIZE - gap
                y2 = (y + 1) * CELL_SIZE - gap

                # 基础地面
                self.canvas.create_rectangle(x1, y1, x2, y2,
                                             fill=COLOR_MAP[EMPTY], outline="#cbd5e1", width=1)
                # 墙体
                if cell == WALL:
                    self.canvas.create_rectangle(x1, y1, x2, y2,
                                                 fill=COLOR_MAP[WALL], outline="#1a1a1a")
                # 目标点
                elif cell == TARGET:
                    self.canvas.create_oval(x1 + 6, y1 + 6, x2 - 6, y2 - 6,
                                            fill=COLOR_MAP[TARGET], outline="#d32f2f")
                # 箱子
                elif cell == BOX:
                    self.canvas.create_rectangle(x1 + 5, y1 + 5, x2 - 5, y2 - 5,
                                                 fill=COLOR_MAP[BOX], outline="#ad6800")

        # 绘制玩家小人
        px1 = self.player_x * CELL_SIZE + gap
        py1 = self.player_y * CELL_SIZE + gap
        px2 = (self.player_x + 1) * CELL_SIZE - gap
        py2 = (self.player_y + 1) * CELL_SIZE - gap
        self.canvas.create_oval(px1 + 7, py1 + 7, px2 - 7, py2 - 7,
                                fill=COLOR_MAP[PLAYER], outline="#10239e")
        # 眼睛装饰
        eye_r = 3
        self.canvas.create_oval(px1 + 12, py1 + 15, px1 + 12 + eye_r * 2, py1 + 15 + eye_r * 2, fill="white")
        self.canvas.create_oval(px2 - 15, py1 + 15, px2 - 15 + eye_r * 2, py1 + 15 + eye_r * 2, fill="white")

    # 人物移动逻辑
    def move(self, dx, dy):
        nx = self.player_x + dx
        ny = self.player_y + dy

        # 边界判断
        if nx < 0 or nx >= self.cols or ny < 0 or ny >= self.rows:
            return
        if self.game_map[ny][nx] == WALL:
            return

        # 推箱子逻辑
        if self.game_map[ny][nx] == BOX:
            box_nx = nx + dx
            box_ny = ny + dy
            if box_nx < 0 or box_nx >= self.cols or box_ny < 0 or box_ny >= self.rows:
                return
            if self.game_map[box_ny][box_nx] in (WALL, BOX):
                return
            self.game_map[ny][nx] = EMPTY
            self.game_map[box_ny][box_nx] = BOX

        # 更新位置与步数
        self.player_x = nx
        self.player_y = ny
        self.step_count += 1
        self.update_info()
        self.draw_map()

        # 通关判定
        if self.check_win():
            self.cur_level += 1
            messagebox.showinfo("关卡通关", f"✅ 成功通过第{self.cur_level}关！\n本局总共移动{self.step_count}步")
            self.step_count = 0
            self.load_level(self.cur_level)
            self.draw_map()
            self.center_window()

    # 胜利条件判断
    def check_win(self):
        for tx, ty in self.targets:
            if self.game_map[ty][tx] != BOX:
                return False
        return True

    # 键盘按键监听
    def key_event(self, event):
        key = event.keysym
        if key == "Up":
            self.move(0, -1)
        elif key == "Down":
            self.move(0, 1)
        elif key == "Left":
            self.move(-1, 0)
        elif key == "Right":
            self.move(1, 0)
        elif key.lower() == "q":
            self.root.quit()


if __name__ == "__main__":
    window = tk.Tk()
    game = Sokoban(window)
    window.mainloop()