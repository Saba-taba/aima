from abc import ABC, abstractmethod

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
        return (
            len(state.pegs[-1]) == self.num_disks and
            state.pegs[-1] == list(range(self.num_disks, 0, -1))
        )

    def successor_function(self, state):
        actions = []

        for i in range(self.num_pegs):
            if not state.pegs[i]:
                continue

            disk = state.pegs[i][-1]

            for j in range(self.num_pegs):
                if i == j:
                    continue

                if not state.pegs[j] or state.pegs[j][-1] > disk:
                    actions.append((i, j)) 

        return actions

    def result_function(self, state, action):
        i, j = action
        new_pegs = [peg.copy() for peg in state.pegs]

        disk = new_pegs[i].pop()
        new_pegs[j].append(disk)

        return HanoiState(new_pegs)
