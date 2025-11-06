from abc import ABC, abstractmethod

class State(ABC):
    @abstractmethod
    def goal(self) -> bool:
        pass
    
    @abstractmethod
    def succesor(self):
        pass

    def __repr__(self):
        return f"{self.__class__.__name__}()"


class Problem(ABC):
    def __init__(self, initial_state):
        self.initial_state = initial_state

    @abstractmethod 
    def goal_test(self, state) -> bool:
        pass
    
    @abstractmethod
    def succesor_function(self, state):
        pass
    
    @abstractmethod
    def result_function(self, state, action):
        pass

    @abstractmethod
    def goal_state(self):
        pass
        
    def path_cost(self, current_cost, state1, action, state2):
        return current_cost + 1


class Tower_of_hanoi(State):
    def __init__(self, pegs):
        self.pegs = pegs

    def goal(self):
        n = sum(len(p) for p in self.pegs)
        return len(self.pegs[-1]) == n and self.pegs[-1] == list(range(n, 0, -1))

    def succesor(self):
        successors = []
        n = len(self.pegs)
        for i in range(n):
            if not self.pegs[i]:
                continue
            disk = self.pegs[i][-1]
            for j in range(n):
                if i != j:
                    if not self.pegs[j] or self.pegs[j][-1] > disk:
                        new_pegs = [peg.copy() for peg in self.pegs]
                        new_pegs[i].pop()
                        new_pegs[j].append(disk)
                        successors.append((f"Move {disk} from peg {i} to {j}", Tower_of_hanoi(new_pegs)))
        return successors

    def __repr__(self):
        return f"HanoiState(pegs={self.pegs})"


class Hanoi_problem(Problem):
    def __init__(self, initial_state):
        super().__init__(initial_state)

    def goal_test(self, state):
        return state.goal()

    def succesor_function(self, state):
        return state.succesor()

    def result_function(self, state, action):
        for act, new_state in state.succesor():
            if act == action:
                return new_state
        return None

    def goal_state(self):
        n = sum(len(p) for p in self.initial_state.pegs)
        goal_pegs = [[], [], list(range(n, 0, -1))]
        return Tower_of_hanoi(goal_pegs)




