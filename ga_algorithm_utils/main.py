from collections import defaultdict
import random
from GA import GeneticAlgorithm
from population import Schedule, Event
from slot import Slot


def main():
    slots = [
        Slot("Slot 1", (8, 0), (9, 0), 20, "Monday"),
        Slot("Slot 2", (9, 0), (10, 0), 30, "Monday"),
        Slot("Slot 3", (10, 0), (11, 0), 40, "Thursday"),
        Slot("Slot 4", (10, 0), (12, 0), 40, "Tuesday"),
        Slot("Slot 5", (10, 0), (12, 0), 30, "Tuesday"),
        Slot("Slot 6", (9, 0), (11, 0), 40, "Friday"),
        Slot("Slot 7", (9, 0), (11, 0), 40, "Friday"),
        # Slot("Slot 7", (9, 0), (12, 0), 40),
        # Slot("Slot 7", (9, 0), (12, 0), 40),
        # Slot("Slot 7", (9, 0), (12, 0), 40),
        # Slot("Slot 7", (9, 0), (12, 0), 40),
    ]

    events = lambda: [
        Event(60, 15, "123", "123"),
        Event(60, 10, "223", "223"),
        Event(60, 15, "323", "323"),
        Event(120, 10, "123", "123"),
        Event(60, 5, "313", "313"),
        Event(120, 4, "323", "323"),
        Event(120, 10, "313", "313"),
        Event(60, 10, "413", "413"),
    ]

    slots = [
        Slot("NNB2", (7, 30), (9, 30), 100, "Monday"),
        Slot("JQB14", (11, 30), (13, 30), 100, "Tuesday"),
        Slot("LT3", (15, 30), (17, 30), 100, "Tuesday"),
        Slot("JQB19", (17, 30), (19, 30), 100, "Tuesday"),
        Slot("KAB", (9, 30), (11, 30), 100, "Wednesday"),
        Slot("JQB09", (15, 30), (17, 30), 100, "Wednesday"),
        Slot("N1", (17, 30), (19, 30), 100, "Wednesday"),
        Slot("JQB24", (18, 30), (19, 30), 100, "Wednesday"),
        Slot("NNB3", (7, 30), (9, 30), 100, "Thursday"),
        Slot("NNB3", (15, 30), (17, 30), 100, "Thursday"),
        Slot("JQB24", (17, 30), (19, 30), 100, "Thursday"),
        Slot("JQB09", (9, 30), (11, 30), 100, "Friday"),
        Slot("NNB2", (11, 30), (13, 30), 100, "Friday"),
        Slot("NNB3", (17, 30), (19, 30), 100, "Friday"),
    ]

    events = lambda: [
        Event(120, 50, "DCIT316", "DCIT316"),
        Event(120, 50, "DCIT314", "DCIT314"),
        Event(120, 50, "DCIT322", "DCIT322"),
        Event(120, 50, "DCIT302", "DCIT302"),
        Event(120, 50, "DCIT308", "DCIT308"),
        Event(120, 50, "DCIT304", "DCIT304"),
        Event(60, 50, "DCIT314", "DCIT314"),
        Event(60, 50, "DCIT322", "DCIT322"),
        Event(60, 50, "DCIT312", "DCIT312"),
        Event(60, 50, "DCIT304", "DCIT304"),
        Event(60, 50, "DCIT308", "DCIT308"),
        Event(120, 50, "DCIT318", "DCIT318"),
        Event(120, 50, "DCIT306", "DCIT306"),
        Event(60, 50, "DCIT302", "DCIT302"),
        Event(60, 50, "DCIT316", "DCIT316"),
        Event(120, 50, "DCIT312", "DCIT312"),
        Event(60, 50, "DCIT306", "DCIT306"),
        Event(60, 50, "DCIT318", "DCIT318"),
    ]

    population = []
    population_size = 500
    for i in range(population_size):
        pop_events = []
        waiting_list = events()
        while waiting_list:
            event = waiting_list.pop()
            index = random.randint(0, len(slots) - 1)
            event.slot = slots[index]
            pop_events.append(event)
        schedule = Schedule(f"Schedule {i}", pop_events)
        population.append(schedule)

    GA = GeneticAlgorithm(population)
    fittest = GA.run(200)
    fittest.allocate_time()
    print(fittest, fittest.fitness())

    days = defaultdict(list)
    for event in fittest.events:
        days[event.slot.day].append(event)

    for event in fittest.events:
        days[event.slot.day].sort(key=lambda e: e.start)

    print("fittest.events", days)

    for day, events in days.items():
        print(day.upper())
        for event in events:
            print(event.summary())


if __name__ == "__main__":
    main()
