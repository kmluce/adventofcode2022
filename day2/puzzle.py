class Puzzle:
    fileName: str

    def __init__(self, file_name, puzzle_part):
        self.fileName = file_name
        self.puzzle_part = puzzle_part
        self.total_shape_score = 0
        self.total_win_score = 0

    def parse(self):
        with open(self.fileName) as file:
            game = []
            for line in file:
                game = [ord(x)-64 if ord(x) < 70 else ord(x)-87 for x in line.rstrip().split(" ")]
                #print(line.rstrip(), game)
                #print("  Adding", game[1], "to shape score and", self.gameScore(game), "to win score" )
                self.total_shape_score += self.shapeScore(game)
                self.total_win_score += self.gameScore(game)

    def gameScore(self, my_game):
        if (self.puzzle_part == "a"):
            if my_game[0] == my_game[1]:
                return 3
            elif ((my_game[0] == 1 and my_game[1] == 2)
                    or (my_game[0] == 2 and my_game[1] == 3)
                  or (my_game[0] == 3 and my_game[1] == 1)) :
                return 6
            else:
                return 0
        elif (self.puzzle_part == "b"):
            if(my_game[1] == 1):
                return 0
            elif(my_game[1] == 2):
                return 3
            elif(my_game[1] == 3):
                return 6


    def shapeScore(self, my_game):
        if (self.puzzle_part == "a"):
            return my_game[1]
        elif (self.puzzle_part == "b"):
            if (my_game[1] == 2):
                return my_game[0]
            elif (my_game[1] == 1):
                if(my_game[0] == 1):
                    return 3
                elif(my_game[0] == 2):
                    return 1
                elif(my_game[0] == 3):
                    return 2
            elif (my_game[1] == 3):
                if(my_game[0] == 1):
                    return 2
                elif(my_game[0] == 2):
                    return 3
                elif(my_game[0] == 3):
                    return 1


    def print(self):
        pass

    def solve(self):
        self.print()
        print("~~~~~~~~~~~~~~~")
        return self.total_win_score + self.total_shape_score
