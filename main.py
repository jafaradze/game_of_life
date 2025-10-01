from tkinter import ttk
import tkinter as tk
import random
from shapes import shapes

black = '#000000'
green = '#09d940'


class Game:
    """Основной класс игры 'Жизнь' Конвея с графическим интерфейсом.

        Attributes:
            width (int): Ширина игрового поля в клетках.
            height (int): Высота игрового поля в клетках.
            cell_size (int): Размер одной клетки в пикселях.
            mode (str): Текущий режим редактирования (тип фигуры).
            board (List[List[int]]): Игровое поле (0 - мертвая, 1 - живая клетка).
            running (bool): Флаг активности симуляции.
            alive_n (int): Количество живых клеток.
            dead_n (int): Количество мертвых клеток.
            gen_n (int): Номер текущего поколения.
            speed (int): Скорость симуляции в миллисекундах.
    """

    def __init__(self, width: int = 50, height: int = 50, cell_size: int = 10):
        """Инициализация игры с заданными параметрами.
            Args:
                width: Ширина поля (количество клеток). По умолчанию 50.
                height: Высота поля (количество клеток). По умолчанию 50.
                cell_size: Размер клетки в пикселях. По умолчанию 10.
        """
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.mode = 'cell'
        self.board = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.running = False
        self.alive_n = 0
        self.dead_n = 0
        self.gen_n = 0
        self.speed = 100
        self.init_window()
        self.window.mainloop()
        self.randomize_board()


    def init_window(self) -> None:
        """Инициализация графического интерфейса игры."""
        self.window = tk.Tk()
        self.window.title('???? "?????"')
        self.window.geometry(f'{self.width * self.cell_size + 300}x{self.height * self.cell_size + 200}+200+200')
        self.window.resizable(False, False)
        self.window.config(bg=black)

        self.frame_board = tk.Frame(self.window, width=self.width * self.cell_size,
                                    height=self.height * self.cell_size, bg=black)
        self.frame_board.place(x=10, y=10)

        self.canvas = tk.Canvas(self.frame_board, bg=black, width=self.width * self.cell_size,
                                height=self.height * self.cell_size)
        self.canvas.bind('<Button-1>', self.toggle_cell)
        self.canvas.place(x=0, y=0)
        self.update_canvas()

        self.frame_btns = tk.Frame(self.window, width=self.width * self.cell_size,
                                   height=170, bg=black)
        self.frame_btns.place(x=10, y=20 + self.height * self.cell_size)

        self.btn_start = tk.Button(self.frame_btns, text='START', font='System 24',
                                   height=1, fg=green, bg=black, command=self.start_simulation)
        self.btn_start.grid(row=0, column=0)

        self.btn_stop = tk.Button(self.frame_btns, text='STOP', font='System 24',
                                  height=1, fg=green, bg=black, command=self.stop_simulation)
        self.btn_stop.grid(row=0, column=1)

        self.btn_random = tk.Button(self.frame_btns, text='RANDOM', font='System 24',
                                    height=1, width=9, fg=green, bg=black, command=self.randomize_board)
        self.btn_random.grid(row=0, column=2)

        self.btn_clear = tk.Button(self.frame_btns, text='CLEAR', font='System 24',
                                   height=1, width=7, fg=green, bg=black, command=self.clear_board)
        self.btn_clear.grid(row=0, column=4)

        self.label_info = tk.Label(self.frame_btns,
                                   text=f'Alive: {self.alive_n}\nDead: {self.dead_n}\nGener: {self.gen_n}\nMode: {self.mode}',
                                   font='Consolas 16', fg=green, bg=black, justify=tk.LEFT)
        self.label_info.grid(row=1, column=2, columnspan=2, sticky=tk.NSEW)

        self.speed_scale = tk.Scale(self.frame_btns, from_=10, to=1000, orient=tk.HORIZONTAL,
                                    command=self.update_speed, label='Speed (ms)', font='System 18', fg=green, bg=black)
        self.speed_scale.set(self.speed)
        self.speed_scale.grid(row=1, columns=1, columnspan=2)

        self.notebook = ttk.Notebook(self.window, width=270, height=600)
        self.notebook.place(x=520, y=10)

        self.frame_planers = tk.Frame(self.notebook, bg=black)
        self.frame_planers.pack(fill=tk.BOTH, expand=True)
        self.notebook.add(self.frame_planers, text='Planers')

        self.btn_glider = tk.Button(self.frame_planers, text='Glider', font='System 24',
                                    fg=green, bg=black, command=lambda: self.change_mode('glider'), width=15)
        self.btn_glider.pack()

        self.btn_LWSS = tk.Button(self.frame_planers, text='LWSS', font='System 24',
                                  fg=green, bg=black, command=lambda: self.change_mode('LWSS'), width=15)
        self.btn_LWSS.pack()

        self.btn_MWSS = tk.Button(self.frame_planers, text='MWSS', font='System 24',
                                  fg=green, bg=black, command=lambda: self.change_mode('MWSS'), width=15)
        self.btn_MWSS.pack()

        self.btn_HWSS = tk.Button(self.frame_planers, text='HWSS', font='System 24',
                                  fg=green, bg=black, command=lambda: self.change_mode('HWSS'), width=15)
        self.btn_HWSS.pack()

        self.frame_guns = tk.Frame(self.notebook, bg=black)
        self.frame_guns.pack(fill=tk.BOTH, expand=True)
        self.notebook.add(self.frame_guns, text='Guns')

        self.btn_Gosper = tk.Button(self.frame_guns, text='Gosper gun', font='System 24',
                                    fg=green, bg=black, command=lambda: self.change_mode('Gosper'), width=15)
        self.btn_Gosper.pack()

        self.frame_oscillators = tk.Frame(self.notebook, bg=black)
        self.frame_oscillators.pack(fill=tk.BOTH, expand=True)
        self.notebook.add(self.frame_oscillators, text='Oscillators')

        self.btn_blinker = tk.Button(self.frame_oscillators, text='Blinker', font='System 24',
                                     fg=green, bg=black, command=lambda: self.change_mode('blinker'), width=15)
        self.btn_blinker.pack()

        self.btn_toad = tk.Button(self.frame_oscillators, text='Toad', font='System 24',
                                  fg=green, bg=black, command=lambda: self.change_mode('toad'), width=15)
        self.btn_toad.pack()

        self.btn_beacon = tk.Button(self.frame_oscillators, text='Beacon', font='System 24',
                                    fg=green, bg=black, command=lambda: self.change_mode('beacon'), width=15)
        self.btn_beacon.pack()

        self.btn_pulsar = tk.Button(self.frame_oscillators, text='Pulsar', font='System 24',
                                    fg=green, bg=black, command=lambda: self.change_mode('pulsar'), width=15)
        self.btn_pulsar.pack()

        self.btn_penta = tk.Button(self.frame_oscillators, text='Penta-D', font='System 24',
                                   fg=green, bg=black, command=lambda: self.change_mode('penta'), width=15)
        self.btn_penta.pack()

        self.frame_stable = tk.Frame(self.notebook, bg=black)
        self.frame_stable.pack(fill=tk.BOTH, expand=True)
        self.notebook.add(self.frame_stable, text='Stable')

        self.btn_cell = tk.Button(self.frame_stable, text='Cell', font='System 24',
                                  fg=green, bg=black, command=lambda: self.change_mode('cell'), width=15)
        self.btn_cell.pack()

        self.btn_block = tk.Button(self.frame_stable, text='Block', font='System 24',
                                   fg=green, bg=black, command=lambda: self.change_mode('block'), width=15)
        self.btn_block.pack()

        self.btn_hive = tk.Button(self.frame_stable, text='Hive', font='System 24',
                                  fg=green, bg=black, command=lambda: self.change_mode('hive'), width=15)
        self.btn_hive.pack()

        self.btn_loaf = tk.Button(self.frame_stable, text='Loaf', font='System 24',
                                  fg=green, bg=black, command=lambda: self.change_mode('loaf'), width=15)
        self.btn_loaf.pack()

        self.btn_box = tk.Button(self.frame_stable, text='Box', font='System 24',
                                 fg=green, bg=black, command=lambda: self.change_mode('box'), width=15)
        self.btn_box.pack()

        self.btn_boat = tk.Button(self.frame_stable, text='Boat', font='System 24',
                                  fg=green, bg=black, command=lambda: self.change_mode('boat'), width=15)
        self.btn_boat.pack()

        self.btn_ship = tk.Button(self.frame_stable, text='Ship', font='System 24',
                                  fg=green, bg=black, command=lambda: self.change_mode('ship'), width=15)
        self.btn_ship.pack()


    def change_mode(self, new_mode: str) -> None:
        """Изменение текущего режима редактирования

        Args:
            new_mode: Новый режим (тип фигуры из shapes.py)
        """
        self.mode = new_mode
        self.update_info()


    def update_info(self) -> None:
        """Обновление информации о состоянии игры на UI"""
        self.label_info.config(
            text=f'Alive: {self.alive_n}\nDead: {self.dead_n}\nGener: {self.gen_n}\nMode: {self.mode}')


    def calculate_alive(self) -> int:
        """Подсчет количества живых клеток на поле.

            Returns:
                Количество живых клеток.
        """
        result = 0
        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                result += self.board[y][x]
        return result


    def update_canvas(self) -> None:
        """Обновление отображения игрового поля в Canvas"""
        self.canvas.delete('all')
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] == 1:
                    self.canvas.create_rectangle(self.cell_size * j, self.cell_size * i,
                                                 self.cell_size * j + self.cell_size,
                                                 self.cell_size * i + self.cell_size, fill=green, outline='gray')


    def toggle_cell(self, event) -> None:
        """Обработчик клика оп игровому полю для размещения фигур.

            Args:
                event: Событие мыши, содержит координаты клика.
        """
        x = event.x // self.cell_size
        y = event.y // self.cell_size
        shape = shapes[self.mode]
        for dy in range(len(shape)):
            for dx in range(len(shape[dy])):
                new_x, new_y = x + dx, y + dy
                self.board[new_y % self.height][new_x % self.width] = shape[dy][dx]
        self.alive_n = self.calculate_alive()
        self.dead_n = self.width * self.height - self.alive_n
        self.update_info()
        self.update_canvas()


    def randomize_board(self) -> None:
        """Случайное заполнение игрового поля."""

        for i in range(self.height):
            for j in range(self.width):
                self.board[i][j] = random.randint(0, 1)
        self.alive_n = self.calculate_alive()
        self.dead_n = self.width * self.height - self.alive_n
        self.update_info()
        self.update_canvas()


    def start_simulation(self) -> None:
        """Запуск симуляции"""
        if not self.running:
            self.running = True
            self.simulate()


    def stop_simulation(self) -> None:
        """Остановка симуляции"""
        self.running = False


    def clear_board(self) -> None:
        """Очистка игрового поля"""
        self.board = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.alive_n = 0
        self.dead_n = self.width * self.height
        self.gen_n = 0
        self.update_info()
        self.update_canvas()


    def update_speed(self, value: int) -> None:
        """Обновление скорости симуляции

        Args:
            value: Новое значение скорости (в миллисекундах)
        """
        self.speed = round(float(value))


    def simulate(self):
        if self.running:
            self.next_generation()
            self.window.after(self.speed, self.simulate)


    def next_generation(self):
        new_board = [[0 for _ in range(self.width)] for _ in range(self.height)]
        for y in range(self.height):
            for x in range(self.width):
                count = self.count_neighbour(x, y)
                if self.board[y][x] == 1:
                    if 2 <= count <= 3:
                        new_board[y][x] = 1
                    else:
                        new_board[y][x] = 0
                else:
                    if count == 3:
                        new_board[y][x] = 1
                    else:
                        new_board[y][x] = 0
        self.board = new_board
        self.alive_n = self.calculate_alive()
        self.dead_n = self.width * self.height - self.alive_n
        self.gen_n += 1
        self.update_info()
        self.update_canvas()


    def count_neighbour(self, x, y):
        result = 0
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)]
        for dx, dy in directions:
            nx, ny = (x + dx) % self.width, (y + dy) % self.height
            result += self.board[ny][nx]
        return result


# Game(width=60, height=70, cell_size=8)
Game()
