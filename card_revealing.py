import random
import os
import time




def main():
    card_revealing_game()

def card_revealing_game(rows=2, cols=4, seed=5):
    clear = "clear"
    game = Game(rows=rows, cols=cols, seed=seed)
    os.system(clear) #clear the screen
    while game.pairs != 0:
        game.board_print()
        f_reveal = input("First Reveal: ")
        if f_reveal == "111":  # Cheat code
            os.system(clear)
            break
        while f_reveal not in game.pos_lst or f_reveal == "":
            os.system(clear)
            print("Invalid input, try again")
            game.board_print()
            f_reveal = input("First Reveal: ")
        os.system(clear)
        game.first_reveal(f_reveal)
        s_reveal = input("Next Reveal:")
        while s_reveal not in game.pos_lst or s_reveal == "" or s_reveal == f_reveal:
            os.system(clear)
            print("Invalid input, try again")
            game.first_reveal(f_reveal)
            s_reveal = input("Next Reveal: ")

        os.system(clear)
        if game.second_reveal(f_reveal, s_reveal):
            game.tornado_condition()
            _ = input("Press Enter to Continue")
        else:
            if not game.tornado_condition():
                game.switch_condition(2)
            _ = input("Finish memorizing?(Press Enter to Continue)")
        os.system(clear)

        y_n = ""
        if game.hint_check():
            y_n = input("It seems like you are in trouble, do you want some hints?[y/n]")
            game.hint(y_n)
    game.reveal_all()
    print(f"Total turns: {game.turns}")
    print("Congratulation!")


class Game:
    def __init__(self, rows, cols, symbols = "☾◇♡⊚", seed=5, hint_req_turns=5):
        random.seed(seed)
        self.rev_board = None
        self.scores = 0
        self.turns = 0
        self.combo = 0
        self.rows = rows
        self.cols = cols
        pairs = (rows * cols) // 2
        self.pairs = pairs
        color_codes = range(31, 37)
        cards = []
        self.revealed = set()
        self.tornado_occur = False
        self.hint_counter = 0
        self.hint_req = hint_req_turns

        self.questions = {
            "what is colour of the sky?":"blue",
            "who is ENGG1330 Professor for part 1? ": "schiender dirk" ,
            "whats capital of france? " :"paris"}
        self.hints_left = len(self.questions)

        self.pos_lst = []
        for i in range(self.rows):
            for j in range(self.cols):
                char = chr(65 + j)
                self.pos_lst.append(f"{i + 1}{char}")
        
        self.pos_lst0 = self.pos_lst[:]

        self.pos_to_num = {}
        index = 0
        for pos in self.pos_lst:
            self.pos_to_num.update({pos: index})
            index += 1

        for c in color_codes:
            for symbol in symbols:
                cards.append(color(c, symbol))

        cards = cards[:pairs]
        self.pos = cards + cards
        random.shuffle(self.pos)
        self.board = ["x" for _ in range(pairs * 2)]

    def board_print(self, board=None):
        if not board:
            board = self.board

        print(f"Turns: {self.turns} | Pairs left: {self.pairs} | Scores: {self.scores}")
        print("      ", end="")

        for i in range(self.cols - 1):
            print(chr(65 + i), end="   ")
        print(chr(65 + self.cols - 1))

        for i in range(self.rows):
            print(f"{i + 1}  :  ", end='')
            for j in range(self.cols - 1):
                print(board[j + i * self.cols], end=" | ")
            print(board[self.cols - 1 + i * self.cols])


    def first_reveal(self, pos): #Reveal the first position
        rev_board = self.board[:]
        rev_board[self.pos_to_num[pos]] = self.pos[self.pos_to_num[pos]]
        self.board_print(rev_board)


    def second_reveal(self, pos1, pos2):
        self.turns += 1
        self.hint_check()

        rev_board = self.board[:]
        index1 = self.pos_to_num[pos1]
        index2 = self.pos_to_num[pos2]

        rev_board[index1] = self.pos[index1]
        rev_board[index2] = self.pos[index2]

        self.revealed.add(pos1)
        self.revealed.add(pos2)


        if rev_board[index1] == rev_board[index2]: #if two reveal are the same
            self.revealed.remove(pos1)
            self.revealed.remove(pos2)
            self.pairs -= 1 #pairs-1
            self.combo += 1 #combo+1
            inc = int((self.combo + 1) * self.combo / 2) * 100 #the increase in points
            self.scores += inc #increase the
            self.board_print(rev_board)
            print(f"Correct! Combo: {self.combo} -> +{inc} Score")
            self.board[index1] = "√"
            self.board[index2] = "√"
            self.pos_lst[index1] = ""
            self.pos_lst[index2] = ""
            self.hint_counter = 0
            return True
        else:
            self.combo = 0
            self.board_print(rev_board)
            return False
    
    def switch_condition(self, probability):
        if not (len(self.revealed) == 0 or self.pairs <= 1 or random.randrange(0, 10) > probability):
            self.switching()

    def switching(self):
        switch_pos1 = random.choice(list(self.revealed))
        lst = []
        lst.append(switch_pos1)
        switch_pos2 = random.choice(list(set(self.pos_lst0) - set(lst)))
        pos1 = self.pos_to_num[switch_pos1]
        pos2 = self.pos_to_num[switch_pos2]
        self.board[pos1], self.board[pos2] = self.board[pos2], self.board[pos1]
        self.pos[pos1], self.pos[pos2] = self.pos[pos2], self.pos[pos1]
        print('--------------------------------------------')
        print(f"A random switching occurs between {switch_pos1} and {switch_pos2}.")
        print('--------------------------------------------')
        self.pos_lst_update()

    def tornado_condition(self):
        if ((self.rows * self.cols) / 2 - self.pairs) == len(self.pos) // 4 and not self.tornado_occur:
            self.tornado()
            return True
        return False

    # def tornado(self):
    #     for i in range(0, len(self.pos), self.cols):
    #         end = self.pos[i + self.cols - 1]
    #         for j in range(self.cols - 1, 0, -1):
    #             self.pos[i + j] = self.pos[i + j - 1]
    #         self.pos[i] = end

    #     for i in range(0, len(self.board), self.cols):
    #         end = self.board[i + self.cols - 1]
    #         for j in range(self.cols - 1, 0, -1):
    #             self.board[i + j] = self.board[i + j - 1]
    #         self.board[i] = end

    #     self.tornado_occur = True
    #     print('-----------------------------------------------------------------------------------------------------------------------------')
    #     print(f"A tornado will happen after pressing Enter: each card moves one step backward and the last card in a row moves to the front.")
    #     print('-----------------------------------------------------------------------------------------------------------------------------')
    #     self.pos_lst_update()

    def tornado(self):
        print('-----------------------------------------------------------------------------------------------------------------------------')
        print(f"A tornado will happen after pressing Enter: each card moves one step backward and the last card in a row moves to the front.")
        print('-----------------------------------------------------------------------------------------------------------------------------')

        _ = input("Press Enter to Continue")
        os.system('clear')
        self.board_print()
        time.sleep(1)
        os.system('clear')

        modified_board = [self.board[i * self.cols:(i + 1) * self.cols] for i in range(self.rows)]

        for i in range(0, len(self.pos), self.cols):
            end = self.pos[i + self.cols - 1]
            for j in range(self.cols - 1, 0, -1):
                self.pos[i + j] = self.pos[i + j - 1]
            self.pos[i] = end

        for i in range(0, len(self.board), self.cols):
            end = self.board[i + self.cols - 1]
            for j in range(self.cols - 1, 0, -1):
                self.board[i + j] = self.board[i + j - 1]
            self.board[i] = end

        self.tornado_occur = True
        self.pos_lst_update()


        for blank_pos in range(self.cols - 1, -1, -1):
            print(f"Turns: {self.turns} | Pairs left: {self.pairs} | Scores: {self.scores}")
            print("      ", end="")

            for i in range(self.cols - 1):
                print(chr(65 + i), end="   ")
            print(chr(65 + self.cols - 1))

            for i in range(self.rows):
                print(f"{i + 1}  :  ", end='')
                modified_row = modified_board[i][:blank_pos] + [" "] + modified_board[i][blank_pos:]
                row_str = " | ".join(map(str, modified_row))
                print(row_str)

            time.sleep(1)
            os.system('clear')

        self.board_print()

    
    def pos_lst_update(self):
        self.pos_lst = self.pos_lst0[:]
        for i in range(len(self.board)):
            if self.board[i] == "√":
                self.pos_lst[i] = ""

    def reveal_all(self): #Reveal the whole code
        self.board_print(self.pos)

    def ask_question(self):
        question, answer = random.choice(list(self.questions.items()))
        user_answer = input(f"Answer this to get hint: {question}").strip().lower()
        del self.questions[question]
        return user_answer == answer

    def hint(self, y_n):
        self.hint_counter = 0
        if y_n.lower() == "y":
            positions = []
            for i, pos in enumerate(self.pos_lst):
                if pos != "":
                    positions.append(pos)
                    sym = self.pos[i]
                    index = i
                    break
            for i, syms in enumerate(self.pos):
                if syms == sym and self.pos_lst[i] not in positions:
                    positions.append(self.pos_lst[i])

            if self.ask_question():
                print(f"Hint: Try revealing {positions[0]} and {positions[1]}")
                self.hints_left -= 1
                return
    
    def hint_check(self):
        if self.hint_counter == self.hint_req*2 and self.hints_left != 0:
            return True
        else:
            self.hint_counter += 1
            return False

def color(code, char): #For coloring text, code is the color code and char is the character or string being colored
    return "\33[{code}m".format(code=code) + char + "\33[{code}m".format(code=39)


if __name__ == "__main__":
    main()
