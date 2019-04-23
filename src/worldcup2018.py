import pickle
import os
import csv

DEBUG = False

class Team():
    theTeams = {}
    filename = 'teams.pickle'
    @staticmethod
    def retrieve():
        if os.path.isfile(Team.filename):
            with open(Team.filename, 'rb') as f:
                Team.theTeams = pickle.load(f)
            if DEBUG:
                for x in Team.theTeams: print(x)
            return True
        else: return False
        
    def __init__(self, name):
        self.name = name
        self.games = []
        Team.theTeams[self.name] = self
        self.points=0
    def calculate_score(self):

        for game in self.games:
            
            team1 = game.team1
            team2 = game.team2
            score = game.score

            #print(self.points)

            #self is the first team
            if(team1.name == self.name):
                if(score[0] > score[1]):
                    self.points = self.points + 3
                elif(score[0] == score[1]):
                    self.points = self.points + 1
            elif(team2.name == self.name):
                if(score[1] > score[0]):
                    self.points = self.points + 3
                elif(score[1] == score[0]):
                    self.points = self.points + 1
            
                

            
            #print(self.points)
        
        # υπολογίσετε τους βαθμούς της ομάδας
        return 0
        
    def in_group(self):
        group = []
        for g in self.games:
            for t in [g.team1, g.team2]:
                if t != self: group.append(t.name)
        return group
            
    def __repr__(self):
        out = self.name+'\nΑγώνες:\n'
        for g in self.games:
            out += repr(g) + '\n'
        return out
            
class Game():
    theGames = []
    filename = 'games.pickle'
    @staticmethod
    def retrieve():
        if os.path.isfile(Game.filename):
            with open(Game.filename, 'rb') as f:
                Game.theGames = pickle.load(f)
            if DEBUG:
                for x in Game.theGames: print(x)
            return True
        else: return False
    def __init__(self, t1, t2):
        self.team1 = t1
        self.team2 = t2
        self.score = []
        Game.theGames.append(self)
    def __repr__(self):
        return self.team1.name+'-'+self.team2.name+":" + "{}-{}".format(*self.score)

class Persistant():
    ''' κλάση μόνιμης αποθήκευσης των αντικειμένων Team, Game'''
    def __init__(self):
        self.data = [[Team.theTeams, 'teams.pickle'], [Game.theGames,'games.pickle']]
    def store(self):
        for d in self.data:
            with open(d[1], 'wb') as f:
                pickle.dump(d[0], f)
        print('stored in pickle')
    def retrieve(self):
        for c in [Team, Game]:
            if not (c.retrieve()): return False
            print('retrieved from pickle')
        return True
    
class Main():
    def __init__(self):
        self.persist = Persistant()
        if not self.persist.retrieve():
            self.load_csv()
        ## menu
        while True:
            print(','.join([Team.theTeams[t].name for t in Team.theTeams]))
            sel = input('Country....')
            if not sel: break
            teams=[]
            for t in Team.theTeams.keys():
                if DEBUG: print(t)
                if sel.lower() in t.lower(): teams.append(Team.theTeams[t])
            if DEBUG: print([t.name for t in teams])
            self.select_show(teams)
    def select_show(self,teams):
        if len(teams)>1:
            to_show = ','.join([str(x[0]+1)+':'+x[1] for x in enumerate([t.name for t in teams])])
            while True:
                print(to_show)
                sel = input()
                if not sel: break
                if sel in ','.join([str(x+1) for x in range(len(teams))]).split(','):
                    self.show_country(teams[int(sel)-1])
        elif teams:
            self.show_country(teams[0])

    def show_country(self, t):
        print(50*'=', '\nΟμάδα:', t)
        t.calculate_score()
        print('Βαθμοί: {}'.format(t.points))
        print('\nΆλλες ομάδες στο ίδιο γκρουπ:', t.in_group(), '\n', 50*'=', '\n\n')
                
    def load_csv(self):       
        with open('worldcup2018.csv', 'r', encoding='utf-8') as wc:
            reader = csv.reader(wc, delimiter=";")
            for row in reader:
                teams = []
                for t in row[4:8:3]:
                    if t not in Team.theTeams:
                        teams.append(Team(t))
                        if DEBUG: print('new team')
                        if DEBUG: print(Team.theTeams[t])
                    else:
                        teams.append(Team.theTeams[t])
                score = [int(x) for x in row[5:7]]
                if DEBUG: print(score)
                g = Game(*teams)
                g.score = score
                if DEBUG:
                    print('new game')
                    print(g)
                for t in teams: t.games.append(g)
        self.persist.store()

if __name__ == '__main__': Main()
    
        
