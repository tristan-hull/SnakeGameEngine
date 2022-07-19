import threading
from time import sleep
from SnakeGame import SnakeGame
import os


game = SnakeGame('medium', 'medium')
def moves():
    while True:
        sleep(2)


thread1 = threading.Thread(target=game.run_game)
thread1.daemon = True
thread2 = threading.Thread(target=moves)
thread2.daemon = True
thread1.start()
thread2.start()
while True:
    os.system('cls' if os.name == 'nt' else 'clear')
    game.print_game_state()
    sleep(1)
