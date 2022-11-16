from collections import defaultdict
import random
from flask import Flask, render_template, request
from ga_algorithm_utils.GA import GeneticAlgorithm, Event, Schedule, Slot
from ga_algorithm_utils.dummy_data import events as dummy_events, slots as dummy_slots

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/timetable')
def timetable():
    slot_names = request.args.getlist("slot_names")
    slot_start_times = request.args.getlist("slot_start_times")
    slot_end_times = request.args.getlist("slot_end_times")
    slot_capacities = request.args.getlist("slot_capacities")
    slot_days = request.args.getlist("slot_days")

    event_names = request.args.getlist("event_names")
    event_durations = request.args.getlist("event_durations")
    event_capacities = request.args.getlist("event_capacities")
    event_codes = request.args.getlist("event_codes")

    slots = [
        Slot(name,
             (int(start_time.split(":")[0]), int(start_time.split(":")[1])),
             (int(end_time.split(":")[0]), int(end_time.split(":")[1])),
             int(capacity), day)
        for name, start_time, end_time, capacity, day in zip(
            slot_names, slot_start_times, slot_end_times, slot_capacities,
            slot_days)
    ]

    events = lambda: [
        Event(int(duration), int(capacity), name, code)
        for name, duration, capacity, code in zip(
            event_names, event_durations, event_capacities, event_codes)
    ]
    events = lambda: dummy_events
    slots = dummy_slots

    population = []
    population_size = 200
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

    days = defaultdict(list)
    for event in fittest.events:
        days[event.slot.day].append(event)

    for event in fittest.events:
        days[event.slot.day].sort(key=lambda e: e.start)

    context = {
        "days": days,
        "fitness": fittest.fitness(),
    }
    return render_template('timetable.html', **context)


if __name__ == '__main__':
    app.run(debug=True)
