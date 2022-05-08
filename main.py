from threading import Thread
from time import sleep, perf_counter

from state import State

state = State()

if __name__ == "__main__":
    state.startTraining()

    # print(len(state.teams))
