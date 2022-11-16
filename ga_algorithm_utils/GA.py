from collections import defaultdict
import random


class Slot:

    def __init__(self,
                 name,
                 start: tuple[int, int],
                 end: tuple[int, int],
                 capacity: int,
                 day: str = "",
                 description: str = "") -> None:
        self.name = name
        self.start = start
        self.end = end
        self.day = day
        self.capacity = capacity
        self.description = description

    def duration(self) -> int:
        total_minutes = self.end[0] * 60 + self.end[1]
        total_minutes -= self.start[0] * 60 + self.start[1]
        return total_minutes

    def get_id(self):
        return self.name + self.day + str(self.start) + str(self.end)


class Event:
    """An event is an individual in the population."""

    def __init__(
        self,
        duration_in_minutes: int,
        capacity: int,
        name: str = "",
        code: str = "",
        slot: Slot = None,
        description: str = "",
    ):
        self.name = name
        self.duration_in_minutes = duration_in_minutes
        self.capacity = capacity
        self.slot = slot
        self.code = code
        self.start = None
        self.end = None
        self.description = description

    def __str__(self) -> str:
        return str(self.slot)

    def summary(self):
        if self.start and self.end:
            return self.code + f" {self.start[0]}:{self.start[1]}-{self.end[0]}:{self.end[1]}"
        return self.code


class Schedule:
    """A population contains a list of events and a fitness function."""

    def __init__(self, name, events: list[Event]):
        self.name = name
        self.events = events
        self.slots = [event.slot for event in events]

    def __str__(self):
        return repr(self)

    def __repr__(self) -> str:
        days = {
            "Monday": 1,
            "Tuesday": 2,
            "Wednesday": 3,
            "Thursday": 4,
            "Friday": 5
        }
        names = ["\n", '"', self.name, ": \n"]
        self.events.sort(key=lambda event: days[event.slot.day])
        for event in self.events:
            names.append(event.summary() + " in " + event.slot.name + " on " + event.slot.day + " for " + str(round(event.slot.duration()/60,2)) + "\n") #yapf: disable

        return "".join(names + ['"'])

    def fitness(self):
        """Return the fitness of the population."""
        valid_points = 0
        total_points = 0

        slot_events = defaultdict(list)
        day_events = defaultdict(list)
        for event in self.events:
            slot_events[event.slot].append(event)
            day_events[event.slot.day].append(event)

        # Check if events are overlapping
        for slot, events in slot_events.items():
            total_event_duration = sum(
                [event.duration_in_minutes for event in events])
            if total_event_duration <= slot.duration():
                valid_points += 1

            # Check if all events are within the slot's capacity
            valid_points += all(
                [event.capacity <= slot.capacity for event in events])

            total_points += 2

        # Check if events with same code are not are not in the same day
        for day, events in day_events.items():
            codes = [event.code for event in events]
            valid_points += len(set(codes))
            total_points += len(codes)

        return round(valid_points / max(1, total_points) * 100)

    def mutate(self):
        """Mutate the population."""
        random.choice(self.events).slot = random.choice(self.slots)

    def allocate_time(self):
        """Allocate time to events."""
        slot_events = defaultdict(list)
        self.events.sort(key=lambda event: -event.duration_in_minutes)
        for event in self.events:
            slot_events[event.slot].append(event)

        for slot, events in slot_events.items():
            start = slot.start
            for event in events:
                event.start = start
                event.end = (start[0] + event.duration_in_minutes // 60,
                             start[1] + event.duration_in_minutes % 60)
                start = event.end


class GeneticAlgorithm:

    def __init__(self, population):
        self.population = population

    def select(self):
        new_population = []
        # Randomly select two parents from the population and cross over
        # them to create a new population. Select with probability based on fitness.
        selection_weights = [
            schedule.fitness() for schedule in self.population
        ]
        for _ in range(len(self.population)):
            parent1 = random.choices(self.population,
                                     weights=selection_weights)[0]
            parent2 = random.choices(self.population,
                                     weights=selection_weights)[0]
            new_population.append(self.cross_over(parent1, parent2))

        self.population = new_population

    def cross_over(self, parent1, parent2):
        # Randomly select a crossover point and swap the genes after the
        # crossover point.
        crossover_point = random.randint(0, len(parent1.events) - 1)
        child_events = parent1.events[:crossover_point]
        child_events.extend(parent2.events[crossover_point:])
        return Schedule("Child", child_events)

    def mutate(self):
        # For each individual in the population, randomly mutate it.
        schedule = random.choice(self.population)
        if random.random() * 100 < 1:
            print("Mutating")
            schedule.mutate()

    def get_fittest(self):
        return max(self.population, key=lambda x: x.fitness())

    def run(self, iterations):
        fittest = self.get_fittest()
        for _ in range(iterations):
            if fittest.fitness() == 100:
                break
            self.select()
            self.mutate()
            fittest = max(self.get_fittest(),
                          fittest,
                          key=lambda x: x.fitness())
        return fittest
