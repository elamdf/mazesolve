import numpy as np 
import matplotlib.pyplot as plt
class GridWorld(object):
    def __init__(self,m,n):
        self.grid = np.zeros((m,n))
        self.m = m
        self.n = n
        self.stateSpace = [i for i in range(self.m*self.n)]
        self.stateSpace.remove(self.m*self.n-1)
        self.stateSpacePlus = [i for i in range(self.m*self.n)]
        self.actionSpace = {'Up': self.m, 'Down': self.m, 
                'Left': -1, 'Right': 1}
        self.possibleActions = ['Up', 'Down', 'Left', 'Right']
        self.agentPosition = 0
    def isTerminalState(self, state):
        return(state in self.stateSpacePlus and state not in self.stateSpace)
    def getAgentRowAndColumn(self):
        x = self.agentPosition // self.m
        y = self.agentPosition % self.n
        return x,y
    def setState(self,state):
        x, y = self.getAgentRowAndColumn()
        self.grid[x][y] = 0
        self.agentPosition = state
        x, y = self.getAgentRowAndColumn()
        self.grid[x][y] = 1
    def offGridMove(self, newState, oldState):
        if newState not in self.stateSpacePlus:
            return True
        elif oldState % self.m == 0 and newState % self.m == self.m - 1:
            return True
        elif oldState % self.m == self.m - 1 and newState % self.m == 0:
            return True
        else:
            return False
    def step(self, action):
        x, y = self.getAgentRowAndColumn()
        resultingState = self.agentPosition + self.actionSpace[action]
        reward = -1 if not self.isTerminalState(resultingState) else 0
        if not self.offGridMove(resultingState, self.agentPosition):
            self.setState(resultingState)
            return resultingState, reward, self.isTerminalState(self.agentPosition), None
        else:
            return self.agentPosition, reward, self.isTerminalState(self.agentPosition), None
    def reset(self):
        self.agentPosition = 0
        self.grid = np.zeros((self.m, self.n))
        return self.agentPosition
    def render(self):
        print('-------------------------------')
        for row in self.grid:
            for col in row:
                if col == 0:
                    print('-', end='\t')
                elif col == 1:
                    print('X', end='\t')
                else:
                    print("?", end='\t')
            print('\n')
        print('-------------------------------')
    def actionSpaceSample(self):
        return np.random.choice(self.possibleActions)
def maxAction(Q, state, actions):
    values = np.array([Q[state,a] for a in actions])
    action = np.argmax(values)
    return actions[action]
def renderPolicy(Q,env):
    actionz = []
    policy = []
    qlen = env.m * env.n #* len(env.possibleActions)
    for index in range(qlen):
        if index == 0 or index == 81:
            continue
        for action in env.possibleActions:
           actionz.append([Q[index, action],action])
        print(max(actionz)[1])
        policy.append(max(actionz)[1])
        actionz = []
    count = 0
    print('-------------------------------')
    for choice in policy:
        if count == env.m:
            print('\n')
            count = 0
        count += 1
        print(choice, end="\t")
    print("X")
    print('\n')
    print('-------------------------------')
if __name__ == '__main__':
    env = GridWorld(9,9)
    ALPHA = 0.1
    discount = 1 # infinitley farsighted
    eps = 1 # greedy
    Q = {}
    for state in env.stateSpacePlus:
        for action in env.possibleActions:
            Q[state,action] = 0
    numGames = 50000
    totalRewards = np.zeros(numGames)
    for i in range(numGames):
        if i % 5000 == 0:
            print('starting game', i)
            env.render()
        done = False
        epRewards = 0
        observation = env.reset()
        while not done:
            rand = np.random.random()
            action = maxAction(Q, observation, env.possibleActions) if rand < (1-eps) \
                    else env.actionSpaceSample()
            observation_, reward, done, info = env.step(action)
            epRewards += reward
            action_ = maxAction(Q, observation_, env.possibleActions)
            Q[observation, action] = Q[observation, action] + ALPHA*(reward + \
                    discount*Q[observation_, action_] - Q[observation, action])
            observation = observation_ 
        if eps - 2 / numGames > 0: # linear decrease in eps twoards pure greed about halfway through 
            eps -= 2 / numGames
        else:
            eps = 0
        totalRewards[i] = epRewards
    renderPolicy(Q,env)
