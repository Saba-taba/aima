from abc import ABC, abstractmethod
from collections import deque
import heapq

class State(ABC):
    pass

class HanoiState(State):
    def __init__(self, pegs):
        self.pegs = pegs

    def __eq__(self, other):
        return isinstance(other, HanoiState) and self.pegs == other.pegs

    def __hash__(self):
        return hash(tuple(tuple(p) for p in self.pegs))

    def __repr__(self):
        return f"HanoiState({self.pegs})"

    def __lt__(self, other):
        return False

class Node:
    def __init__(self, state, parent=None, action=None, path_cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.depth = 0
        if parent:
            self.depth = parent.depth + 1

    def expand(self, problem):
        return [self.child_node(problem, action) for action in problem.successor_function(self.state)]

    def child_node(self, problem, action):
        next_state = problem.result_function(self.state, action)
        cost = problem.path_cost(self.path_cost, self.state, action, next_state)
        return Node(next_state, self, action, cost)

    def path(self):
        node, path_back = self, []
        while node:
            path_back.append(node)
            node = node.parent
        return list(reversed(path_back))

class Problem(ABC):
    def __init__(self, initial_state):
        self.initial_state = initial_state

    @abstractmethod
    def goal_test(self, state): 
        pass

    @abstractmethod
    def successor_function(self, state):
        pass

    @abstractmethod
    def result_function(self, state, action):
        pass

    def path_cost(self, cost, state1, action, state2):
        return cost + 1

class HanoiProblem(Problem):
    def __init__(self, initial_state):
        super().__init__(initial_state)
        self.num_pegs = len(initial_state.pegs)
        self.num_disks = sum(len(p) for p in initial_state.pegs)

    def goal_test(self, state):
        return state.pegs[-1] == list(range(self.num_disks, 0, -1))

    def successor_function(self, state):
        actions = []
        for i in range(self.num_pegs):
            if not state.pegs[i]: continue
            disk = state.pegs[i][-1]
            for j in range(self.num_pegs):
                if i == j: continue
                if not state.pegs[j] or state.pegs[j][-1] > disk:
                    actions.append((i, j))
        return actions

    def result_function(self, state, action):
        i, j = action
        new_pegs = [peg.copy() for peg in state.pegs]
        disk = new_pegs[i].pop()
        new_pegs[j].append(disk)
        return HanoiState(new_pegs)

    def h(self, node):
        return self.num_disks - len(node.state.pegs[-1])

class PriorityQueue:
    def __init__(self, f):
        self.heap = []
        self.f = f
        self.count = 0
    def append(self, node):
        heapq.heappush(self.heap, (self.f(node), self.count, node))
        self.count += 1
    def pop(self):
        return heapq.heappop(self.heap)[2]
    def __len__(self):
        return len(self.heap)

def BFS(problem):
    node = Node(problem.initial_state)
    if problem.goal_test(node.state): return node
    frontier = deque([node])
    explored = {problem.initial_state}
    while frontier:
        node = frontier.popleft()
        for child in node.expand(problem):
            if child.state not in explored:
                if problem.goal_test(child.state): return child
                frontier.append(child)
                explored.add(child.state)
    return None

def DFS(problem):
    frontier = [Node(problem.initial_state)]
    explored = set()
    while frontier:
        node = frontier.pop()
        if problem.goal_test(node.state): return node
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored:
                frontier.append(child)
    return None

def IDS(problem):
    for depth in range(50):
        result = DLS(problem, depth)
        if result != 'cutoff' and result is not None: return result
    return None

def DLS(problem, limit):
    def recursive_dls(node, problem, limit):
        if problem.goal_test(node.state): return node
        elif limit == 0: return 'cutoff'
        else:
            cutoff_occurred = False
            for child in node.expand(problem):
                result = recursive_dls(child, problem, limit - 1)
                if result == 'cutoff': cutoff_occurred = True
                elif result is not None: return result
            return 'cutoff' if cutoff_occurred else None
    return recursive_dls(Node(problem.initial_state), problem, limit)

def best_first_search(problem, f):
    node = Node(problem.initial_state)
    frontier = PriorityQueue(f)
    frontier.append(node)
    explored = set()
    while frontier:
        node = frontier.pop()
        if problem.goal_test(node.state): return node
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored:
                frontier.append(child)
    return None

def UCS(problem):
    return best_first_search(problem, lambda n: n.path_cost)

def greedy_best_first_search(problem):
    return best_first_search(problem, lambda n: problem.h(n))

def a_star(problem):
    return best_first_search(problem, lambda n: n.path_cost + problem.h(n))

def print_hanoi(state):
    pegs = state.pegs
    max_h = max(len(p) for p in pegs) if any(pegs) else 0
    for level in range(max_h - 1, -1, -1):
        line = ""
        for p in pegs:
            line += f"  {p[level]}  " if len(p) > level else "  |  "
        print(line)
    print("  P0   P1   P2\n")

if __name__ == "__main__":
    init_state = HanoiState([[5,4,3, 2, 1], [], []])
    problem = HanoiProblem(init_state)
    
    algorithms = [
        (BFS, "BFS"),
        (DFS, "DFS"),
        (IDS, "IDS"),
        (UCS, "UCS"),
        (greedy_best_first_search, "Greedy"),
        (a_star, "A*")
    ]
    
    for alg, name in algorithms:
        print(f"--- Running {name} ---")
        res = alg(problem)
        if res:
            path = res.path()
            for i, n in enumerate(path):
                print(f"Step {i}:")
                print_hanoi(n.state)
            print(f"{name} moves: {len(path)-1}\n")
