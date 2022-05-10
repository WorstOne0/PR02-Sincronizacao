from threading import Thread, Lock
from time import sleep, perf_counter
import os
from random import randint

lock = Lock()


class State:
    teams = []
    running = []
    totalTimes = {}

    def __init__(self) -> None:
        pass

    def startTraining(self):
        for i in range(6):
            team = Team(i + 1, self)

            self.teams.append(team)


class Team:
    cars = []
    isRunning = False

    def __init__(self, id, state) -> None:
        self.teamId = id

        carsThreads = []

        for i in range(2):
            car = Car(i + 1)

            self.cars.append(car)

            carThread = Thread(target=car.training, args=(self, state))
            carsThreads.append(carThread)

        for carThread in carsThreads:
            carThread.start()

        sleep(10)

        print("Tempo max")

        os._exit(1)


class Car:
    numLaps = 0
    isRunning = False

    def __init__(self, id) -> None:
        self.carId = id

    def training(self, team, state):
        while self.numLaps < 2:
            sleep(randint(1, 5))

            lock.acquire()
            if len(state.running) < 5 and not team.isRunning:
                self.isRunning = True
                team.isRunning = True
                state.running.append(f"E{team.teamId}C{self.carId}")

                print(f"Começou a correr E{team.teamId}C{self.carId}")

                print(
                    f"Atualmente correndo {state.running} - E{team.teamId}C{self.carId}"
                )
            else:
                print(f"E{team.teamId}C{self.carId} is waiting")

            lock.release()

            if self.isRunning:
                sleep(2)

                self.numLaps += 1
                self.isRunning = False

                lock.acquire()
                team.isRunning = False
                state.running.remove(f"E{team.teamId}C{self.carId}")

                print(
                    f"Terminou a correr E{team.teamId}C{self.carId}. Volta {self.numLaps}"
                )
                lock.release()
