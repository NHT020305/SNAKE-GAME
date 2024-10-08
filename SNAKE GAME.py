import random
import string
import time
import math
import enchant
import threading
import contextlib
import nltk
from nltk.corpus import words, names
nltk.download('words', quiet=True)
nltk.download('names', quiet=True)



class NullIO:
    def write(self, s):
        pass
with contextlib.redirect_stdout(NullIO()):
    import pygame



RESET = "\033[0m"
BOLD = "\033[1m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"



def clear_screen():
    
    print("\033c", end="")



def play_sound(sound_file):
    
    pygame.mixer.music.load(sound_file)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)



def play_sound_list(sound_file_list):
    
    for song in sound_file_list:
        play_sound(song)



def time_in_parts(time_in_second):

    time_in_second = int(time_in_second)
    hours = str(time_in_second // 3600) + ' HOURS '
    minutes = str((time_in_second % 3600) // 60) + ' MINUTES '
    seconds = str(time_in_second % 3600 % 60) + ' SECONDS'
    time_list = [hours, minutes, seconds]
    time_in_parts = ''
    for part in time_list:
        if part[0] != '0':
            time_in_parts += part
    return time_in_parts



def print_in_frame(message, color):

    message1 = list(map(lambda x: len(x), message))
    length = max(message1)
    border = '*' * (length + 4)
    time.sleep(0.08)
    print(color + border + RESET)
    for line in message:
        time.sleep(0.08)
        print(color + '| ' + ' '*length + ' |')
        print(color + '| ' + " "*math.ceil((length-len(line))/2) + line +
               " "*math.floor((length-len(line))/2) + ' |')
    time.sleep(0.08)
    print(color + '| ' + ' '*length + ' |' + RESET)
    time.sleep(0.08)
    print(color + border + RESET)



def animation(message, color):
    
    for i in message:
        print(color + i + RESET, end = '', flush = True)
        time.sleep(0.015)



def split(word_list, n):

    a = len(word_list) // n
    parts = []
    for i in range(n):
        word = word_list[i*a : (i+1)*a]
        parts.append(word)
    return parts



print()
animation('SETTING UP......', GREEN)
time.sleep(1)
print(), print()
animation('WAIT A FEW SECONDS......', GREEN)
print()



male_names = set(names.words('male.txt'))
female_names = set(names.words('female.txt'))
name = list(male_names.union(female_names))
for i in range(len(name)):
    name[i] = name[i].lower()
dictionary = words.words()
for i in range(len(dictionary)):
    dictionary[i] = dictionary[i].lower()
dictionary = list(filter(lambda x: x not in name, dictionary))



def word_generator(char, n):

    char = char.lower()
    snake = list(filter(lambda x: x[0] == char and len(x) > 1 
                        and x[0] == x[-1], dictionary))
    not_snake = list(filter(lambda x: x[0] == char and len(x) > 1 
                            and x[0] != x[-1], dictionary))
    helper = split(not_snake, n)
    d = {}
    for i in range(1, n+1):
        d[i] = helper[i-2]
    random_word = random.choice(d[random.choice(range(1,n+1))])
    if snake:
        d[n+1] = snake
        random_word = random.choice(d[random.choice(range(1,n+2))])
    return random_word



def is_english_word(word):

    english_dict = enchant.Dict("en_US")
    return len(word) > 1 and english_dict.check(word)



def is_valid_word(word):

    word = word.lower()
    if not is_english_word(word) or word in name:
        return False
    return True



class SnakeGame:


    def __init__(self):

        self.name = None
        self.players = []
        self.word_history = []
        self.level = 0
        self.snake = 10
        self.time_player = 0
        self.computer_turn = ''
        self.player_turn = ''
        self.player_turn_valid = True
        self.play_turn = None
        self.start = True
        self.start_time = 0
        self.end_time = 0



    def is_in_word_history(self, word):

        return word in self.word_history
    


    def add_word_to_history(self, word):
        
        for player in self.players + [self]:
            player.word_history.append(word)



    def can_start(self):

        return self.start



    def start_game(self):

        print(), print_in_frame(['WELCOME TO SNAKE GAME'], GREEN)
        time.sleep(1)
        print(), print_in_frame([' THE COMPUTER WILL GENERATE THE FIRST WORD, THEN IT WILL BE YOUR TURN ',
                                      'IN THE BEGINNING, BOTH PLAYER AND COMPUTER WILL HAVE 10 SNAKES',
                                      'THE GAME WILL END IMMEDIATELY WHEN YOU WIN OR LOSE'], YELLOW)
        print()
        time.sleep(1)
        while True:
            animation('DO YOU WANT TO START THE GAME NOW (START / QUIT): ', BLUE)
            play = input().upper()
            if play == 'START' or play == 'QUIT':
                break
            print(RED + 'INVALID! PLEASE TRY AGAIN' + RESET), print()
        if play == 'QUIT':
            self.start = False
            return
        clear_screen()
        print()
        player_lst = ['TOM', 'MARRY', 'JOHN', 'PETER', 'KATE', 'THOMAS']
        while True:
            animation('CHOOSE YOUR NICKNAME: ', BLUE)
            name = input().upper()
            if name not in player_lst:
                break
            print(RED + 'THIS NICKNAME HAS BEEN CHOSEN! PLEASE CHOOSE ANOTHER ONE'), print()
        self.name = name
        print()
        difficulty_levels = {1: [7, 15], 2: [4, 10], 3: [1, 5]}
        while True:
            try:
                animation('PLEASE CHOOSE THE DIFFICULTY LEVEL (1 - 3): ', BLUE)
                choose_level = int(input())
                if choose_level in difficulty_levels:
                    break
                print(RED + 'INVALID! PLEASE TRY AGAIN'), print()
            except ValueError:
                print(RED + 'INVALID! PLEASE TRY AGAIN'), print()
        print()
        while True:
            try:
                animation('PLEASE CHOOSE THE NUMBER OF PLAYERS (2 - 7): ', BLUE)
                num_player = int(input()) - 1
                if 1 <= num_player <= len(player_lst):
                    break
                print(RED + 'INVALID! PLEASE TRY AGAIN'), print()
            except ValueError:
                print(RED + 'INVALID! PLEASE TRY AGAIN'), print()
        for i in range(num_player):
            name = random.choice(player_lst)
            new_player = Computer(name)
            player_lst.remove(name)
            self.players.append(new_player)
        for player in self.players:
            player.players = self.players.copy()
            player.players.remove(player)
            player.players.append(self)
        self.original_players = self.players.copy()
        self.level = difficulty_levels[choose_level][0]
        self.time_player = difficulty_levels[choose_level][1]
        print()
        print_in_frame(['YOU WILL HAVE ' + str(self.time_player) + 
                        ' SECONDS TO THINK OF A WORD IN EACH TURN',
                    'OTHER PLAYERS WILL HAVE 5 SECONDS TO THINK OF A WORD IN EACH TURN',], GREEN), 
        print()
        player_list = [self.name]
        for player in self.players:
            player_list.append(player.name)
        print_in_frame(['LIST OF PLAYERS:'] + player_list, YELLOW)
        print()



    def player_turn_generator(self):

        if self.snake <= 0:
            print_in_frame(['PLAYER LOST ALL SNAKES', 'GAME OVER'], RED), print()
            self.player_turn_valid = False
            return 
        start_time = time.time()
        turns = 0
        while True:
            if turns == 5:
                break
            animation('Enter your word starting with "' + self.computer_turn[-1] + '": ', BLUE)
            self.player_turn = input().upper()
            if not is_valid_word(self.player_turn):
                turns += 1
                if turns < 5:
                    print(RED + 'INVALID WORD! PLEASE TRY AGAIN' + RESET), print()
                continue
            if  self.player_turn[0] != self.computer_turn[-1]:
                turns += 1
                if turns < 5:
                    print(RED + 'YOUR WORD MUST START WITH LETTER "'
                          + self.computer_turn[-1] + '"! PLEASE TRY AGAIN' + RESET), print()
                continue
            if self.is_in_word_history(self.player_turn):
                turns += 1
                if turns < 5:
                    print(RED + 'THIS WORD HAS BEEN CHOSEN BEFORE! PLEASE TRY ANOTHER WORD' 
                                                                            + RESET), print()
                continue
            break
        if turns == 5:
            print(), print_in_frame(['GAME OVER'], RED)
            self.player_turn_valid = False
            return 
        end_time = time.time()
        if end_time - start_time >= self.time_player:
            print(), print_in_frame(['TIME OVER'], RED)
            self.player_turn_valid = False
            return
        if self.player_turn[-1] == self.player_turn[0]:
            self.snake += 1
            if self.play_turn.name != 'START':
                self.play_turn.snake -= 1
                print(), print_in_frame(['SNAKE FOR YOU! YOU STEAL 1 SNAKE FROM ' 
                                                    + self.play_turn.name], GREEN)



    def bonus_generator(self):

        have_bonus = {1: None, 2: None, 3: 'YOU HAVE A GIFT', 4: None, 5: None}
        output = have_bonus[random.choice(range(1,6))]
        if not output:
            return
        print_in_frame([output, 'YOU HAVE 3 OPTIONS'], GREEN), print()
        animal = ['CAT', 'DOG', 'MOUSE', 'ELEPHANT', 'BEAR', 'DINOSAUR', 'BIRD', 'FISH']
        option1 = random.choice(animal)
        print_in_frame([option1], BLUE), print()
        animal.remove(option1)
        option2 = random.choice(animal)
        print_in_frame([option2], YELLOW), print()
        animal.remove(option2)
        option3 = random.choice(animal)
        print_in_frame([option3], RED), print()
        while True:
            animation('CHOOSE YOUR GIFT: ', BLUE)
            choose = input().upper()
            if choose in [option1, option2, option3]:
                break
            print(RED + 'INVALID! PLEASE TRY AGAIN' + RESET), print()
        random_player = random.choice(self.players)
        bonus = random.choice(range(1,5))
        bonus_list = ['BONUS ' + str(bonus) + ' SECONDS FOR EACH TURN', 
                 'LOSE ' + str(bonus) + ' SECONDS FOR EACH TURN',
                 'STEAL ' + str(bonus) + ' SNAKES FROM ' + random_player.name,
                 random_player.name + ' STEALS ' + str(bonus) + ' SNAKES FROM YOU']
        bonus_type = random.choice(bonus_list)
        if bonus_type == bonus_list[0]:
            self.time_player += bonus
            print(), print_in_frame([bonus_type], GREEN), print()
        if bonus_type == bonus_list[1]:
            self.time_player -= bonus
            print(), print_in_frame([bonus_type], RED), print()
        if bonus_type == bonus_list[2]:
            random_player.snake -= bonus
            self.snake += bonus
            print(), print_in_frame([bonus_type], GREEN), print()
        if bonus_type == bonus_list[3]:
            random_player.snake += bonus
            self.snake -= bonus
            print(), print_in_frame([bonus_type], RED), print()
        


    def play_game(self): 
        self.start_time = time.time()
        first = Computer('START')
        self.play_turn = first
        self.computer_turn = first.computer_turn_generator(
                            random.choice(string.ascii_letters), None, self.level)
        self.add_word_to_history(self.computer_turn)
        time.sleep(1)
        while True:
            self.player_turn_generator()
            print()
            if not self.player_turn_valid:
                break
            self.add_word_to_history(self.player_turn)
            self.play_turn = self
            self.bonus_generator()
            for player in self.players:
                time.sleep(1)
                if self.play_turn == self:
                    self.computer_turn = player.computer_turn_generator(self.player_turn[-1], 
                                                                        self, self.level)
                else: 
                    self.computer_turn = player.computer_turn_generator(self.computer_turn[-1], 
                                                                        self.play_turn, self.level)
                if not player.computer_turn_valid: 
                    self.players.remove(player)
                    for enemy in self.players:
                        enemy.players.remove(player)
                    if self.players:
                        print_in_frame(['RESET GAME'], GREEN), print()
                        first = Computer('START')
                        self.computer_turn = first.computer_turn_generator(random.
                                            choice(string.ascii_letters), None, self.level)
                        self.play_turn = first
                        continue
                    break
                if player.computer_turn_valid:
                    player.bonus_generator()
                    self.play_turn = player
                self.add_word_to_history(self.computer_turn)
            lst = []
            for player in self.players:
                if player.snake < 0:
                    player.snake = 0
                lst.append(player.name + ' SNAKE: ' + str(player.snake))
            time.sleep(1)
            print_in_frame([self.name + ' SNAKE: ' + str(self.snake)] + lst, GREEN)
            print()
            if not self.players:
                print_in_frame(['YOU WIN THE GAME'], GREEN), print()
                break
            time.sleep(1)
        self.end_time = time.time()
        play_time = time_in_parts(self.end_time - self.start_time)
        lst = []
        for player in self.original_players:
            if player.snake < 0:
                player.snake = 0
            lst.append(player.name + ' SNAKE: ' + str(player.snake))
        print_in_frame([self.name + ' SNAKE: ' + str(self.snake)] + lst +
                             ['NUMBER OF WORDS PLAYED: ' + str(len(self.word_history)), 
                              'TIME PLAYED: ' + play_time], YELLOW), print()



class Computer(SnakeGame):


    def __init__(self, name):

        super().__init__()
        self.name = name
        self.turn = ''
        self.snake = 10
        self.time_computer = 4
        self.computer_turn_valid = True
    


    def computer_turn_generator(self, char, player, level):

        if self.snake <= 0:
            print_in_frame([self.name + ' LOST ALL SNAKES',
                                 self.name + ' LOSES THE GAME'], RED), print()
            self.computer_turn_valid = False
            return 
        start_time = time.time()
        while True:
            self.turn = word_generator(char, level).upper()
            if is_valid_word(self.turn) and not self.is_in_word_history(self.turn):
                end_time = time.time()
                if end_time - start_time >= self.time_computer:
                    self.computer_turn_valid = False
                    return print_in_frame([self.name + ' CANNOT GENERATE A NEW WORD', 
                                                self.name + ' LOSE THE GAME'], RED), print()
                break
        if self.name == 'START':
            print_in_frame([str(self.name) + ': ' + self.turn], GREEN), print()
        else:
            print_in_frame([str(self.name) + ': ' + self.turn], YELLOW), print()
        if self.turn[-1] == self.turn[0]:
            self.snake += 1
            if player:
                player.snake -= 1
                print_in_frame(['SNAKE FOR ' + self.name + '! ' + 
                                 self.name + ' STEALS 1 SNAKE FROM ' + player.name], RED), print()
        return self.turn
    


    def bonus_generator(self):

        have_bonus = {1: None, 2: None, 3: 'YOU HAVE A GIFT', 4: None, 5: None}
        output = have_bonus[random.choice(range(1,6))]
        if not output:
            return 
        random_player = random.choice(self.players)
        bonus = random.choice(range(2,6))
        bonus_list = ['BONUS ' + str(bonus) + ' SECONDS FOR ' + self.name + "'S TURN", 
                 self.name + ' LOSES ' + str(bonus) + ' SECONDS FOR EACH TURN',
                 self.name + ' STEALS ' + str(bonus) + ' SNAKES FROM ' + random_player.name,
                 self.name + ' LOSES ' + str(bonus) + ' SNAKES FOR ' + random_player.name]
        bonus_type = random.choice(bonus_list)
        if bonus_type == bonus_list[0]:
            self.time_player += bonus
        if bonus_type == bonus_list[1]:
            self.time_player -= bonus
        if bonus_type == bonus_list[2]:
            random_player.snake -= bonus
            self.snake += bonus
        if bonus_type == bonus_list[3]:
            random_player.snake += bonus
            self.snake -= bonus
        time.sleep(1)
        print_in_frame(['GIFT FOR ' + self.name + ':', bonus_type], GREEN), print()
    


if __name__ == "__main__":

    play_turn = 0
    while True:
        snake_game = SnakeGame()
        snake_game.start_game()
        if not snake_game.can_start():
            break
        time.sleep(2)
        if play_turn == 0:
            pygame.mixer.init()
            sound_file_list = ['Alan Walker Greatest Hits Full Album 2023.MP3']
            random.shuffle(sound_file_list)
            sound_thread = threading.Thread(target=play_sound_list, args=(sound_file_list,))
            sound_thread.start()
        clear_screen()
        snake_game.play_game()
        while True:
            animation('DO YOU WANT TO RESTART THE GAME (YES / NO): ', BLUE)
            play_again = input().upper()
            if play_again == 'YES' or play_again == 'NO':
                break
            print(RED + 'INVALID! PLEASE TRY AGAIN' + RESET), print()
        if play_again == 'NO':
            break
        clear_screen()
        play_turn += 1
    print()
    animation('QUITING THE GAME......', GREEN)
    print()
    time.sleep(3)
    pygame.mixer.quit()