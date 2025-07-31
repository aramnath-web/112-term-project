lbFile = 'leaderboard.txt'

def loadLeaderboard():
    leaderboard = []

    # chatgpt instructed me to use try/except in cases there is no lb file in order to avoid crashes.
    # the code to parse through each entry is my own
    try:
        with open(lbFile, 'r') as f:
            for line in f:
                parts = line.strip().split(',')
                if len(parts) == 2:
                    name, score = parts
                    leaderboard.append((name, int(score)))
    except FileNotFoundError:
        pass
    return sorted(leaderboard, key=lambda x: x[1], reverse=True)[:10]

def saveLeaderboard(leaderboard):
    with open(lbFile, 'w') as f:
        for name, score in leaderboard:
            f.write(f'{name},{score}\n')

def addScore(name, score):
    leaderboard = loadLeaderboard()
    
    # first check if the leaderboard has spots available or score is higher than the lowest one on the leaderboard
    if len(leaderboard) < 10 or score > leaderboard[-1][1]:
        
        # add the score to the board
        leaderboard.append((name, score))

        # sort it but leave out the bottom one
        leaderboard = sorted(leaderboard, key=lambda x: x[1], reverse=True)[:10]

        #save it
        saveLeaderboard(leaderboard)
    saveLeaderboard(leaderboard)