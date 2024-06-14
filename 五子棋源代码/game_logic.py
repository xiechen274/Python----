class GameLogic:
    def __init__(self, board_size=15):
        self.board_size = board_size
        self.board = [[0] * board_size for _ in range(board_size)]  # 初始化棋盘，0表示空格
        self.current_player = 1  # 当前玩家，1表示先手，-1表示后手
        self.winner = None  # 获胜玩家，None表示无获胜玩家
        self.game_over = False  # 游戏结束标志

    def make_move(self, row, col):
        if not self.game_over and self.is_valid_move(row, col):
            self.board[row][col] = self.current_player
            if self.check_winner(row, col):
                self.winner = self.current_player
                self.game_over = True
            else:
                self.current_player = -self.current_player  # 切换到下一个玩家

    def is_valid_move(self, row, col):
        # 检查落子是否有效
        if 0 <= row < self.board_size and 0 <= col < self.board_size and self.board[row][col] == 0:
            return True
        return False

    def check_winner(self, row, col):
        # 检查是否有玩家获胜
        def count_stones(row, col, d_row, d_col):
            count = 0
            r, c = row, col
            while 0 <= r < self.board_size and 0 <= c < self.board_size and self.board[r][c] == self.current_player:
                count += 1
                r += d_row
                c += d_col
            return count

        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]  # 横、竖、正斜、反斜
        for d_row, d_col in directions:
            # 计算两个方向的总棋子数
            total_count = count_stones(row, col, d_row, d_col) + count_stones(row, col, -d_row, -d_col) - 1
            if total_count >= 5:
                return True
        return False