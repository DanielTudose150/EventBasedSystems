import numpy as np
import PublicationItem as PI
import json
import time
import multiprocessing as mp
import Operators as O
import math

EPS = 10e-6


def generatePublication():
    publication = {}
    for fld in PI.PublicationItem:
        publication[fld] = PI.PublicationItem[fld]()
    return publication


def generateSubscription(constraints, allowed):
    fields = np.random.choice(allowed, np.random.randint(0, len(allowed)), replace=False)
    subscription = {}
    for fld in fields:
        subscription[fld] = {
            'operator': None,
            'value': PI.PublicationItem[fld]()
        }
    for cons in constraints:
        subscription[cons['field']] = {
            'operator': cons['operator'],
            'value': PI.PublicationItem[cons['field']]()
        }
    return subscription


def updateSubscription(subscription, constraints, allowed):
    for cons in constraints:
        subscription[cons['field']]['operator'] = cons['operator']
    for fld in subscription:
        if subscription[fld]['operator'] is None:
            subscription[fld]['operator'] = str(np.random.choice(allowed[fld]))
    return subscription


def frequencyGenerator(q_in, q_out, results, allowed):
    while not q_in.empty():
        item = q_in.get()
        if item['type'] == 'pub':
            q_out.put((item['index'], generatePublication()))
        else:
            q_out.put((item['index'], generateSubscription(item['constraints'], allowed)))
        q_in.task_done()


def operatorGenerator(q_in, q_out, results, allowed):
    while not q_in.empty():
        item = q_in.get()
        if item['type'] == 'sub':
            print(item['index'])
            q_out.put((item['index'], updateSubscription(results[item['index']], item['constraints'], allowed)))
        q_in.task_done()


def generate(q_in, q_out, generator, results, allowed):
    threads = []
    for i in range(config['threads']):
        thread = mp.Process(target=generator, args=(q_in, q_out, results, allowed))
        threads.append(thread)
        thread.start()

    q_in.join()

    while not q_out.empty():
        item = q_out.get()
        results[item[0]] = item[1]


if __name__ == "__main__":
    startTime = time.time()
    """
    publications: number
    subscriptions: number
    constraints: [
        type: x \in {frequency, operator}, 
        field: x \in {publication fields},
        operator: x \in {<, <=, >, >=, =, !=},
        percent: int \in (0, 100)
    ]
    threads: number
    """
    with open('config.json') as fd:
        config = json.load(fd)

    # list of items to generate
    toGenerate = [{} for _ in range(config['publications'] + config['subscriptions'])]
    # list of the generated results
    results = [{} for _ in range(config['publications'] + config['subscriptions'])]
    # indices of the publications in regard to the above
    publicationIndices = [i for i in range(config['publications'])]
    # indices of the subscriptions in regard to the above
    subscriptionIndices = [i for i in range(config['publications'], config['publications'] + config['subscriptions'])]

    for index in publicationIndices:
        toGenerate[index]['index'] = index
        toGenerate[index]['type'] = 'pub'

    for index in subscriptionIndices:
        toGenerate[index]['index'] = index
        toGenerate[index]['type'] = 'sub'
        toGenerate[index]['constraints'] = []

    allowedFields = list(PI.PublicationItem.keys())

    # Will traverse the constraints array twice: the first time to evaluate the "frequency" type constraints
    for constraint in config['constraints']:
        if constraint['type'] == 'operator':
            continue

        percent = constraint['percent']

        if constraint['operator'] == "<":
            percent = np.random.uniform(EPS, percent)
        elif constraint['operator'] == "<=":
            percent = np.random.uniform(EPS, percent + EPS)
        elif constraint['operator'] == ">":
            percent = np.random.uniform(percent + EPS, 100)
        elif constraint['operator'] == ">=":
            percent = np.random.uniform(percent, 100)
        elif constraint['operator'] == "!=":
            rd = np.random.uniform(0, 100)
            while abs(percent - rd) < EPS:
                rd = np.random.uniform(0, 100)

        indices = np.random.choice(subscriptionIndices, math.ceil(percent * len(subscriptionIndices) / 100), replace=False)

        queueConstraint = {
            'field': constraint['field'],
            'operator': None
        }

        if constraint['field'] in allowedFields:
            allowedFields.remove(constraint['field'])

        for index in indices:
            toGenerate[index]['constraints'].append(queueConstraint)

    Queue = mp.JoinableQueue()
    Out = mp.Manager().Queue()

    for element in toGenerate:
        Queue.put(element)
    print("Starting to generate frequency related")
    generate(Queue, Out, frequencyGenerator, results, allowedFields)
    print("finished generating")

    fieldIndices = {}
    allowedOperators = {}
    for field in PI.PublicationItem.keys():
        fieldIndices[field] = []
        allowedOperators[field] = O.AllowedOperators[field]()

    for index in subscriptionIndices:
        for field in results[index]:
            fieldIndices[field].append(index)
        toGenerate[index]['constraints'] = []

    for constraint in config['constraints']:
        if constraint['type'] == "frequency":
            continue

        percent = constraint['percent']

        indices = np.random.choice(fieldIndices[constraint['field']],
                                   math.ceil(percent * len(fieldIndices[constraint['field']]) / 100), replace=False)

        queueConstraint = {
            'field': constraint['field'],
            'operator': constraint['operator']
        }

        if constraint['operator'] in allowedOperators[constraint['field']]:
            allowedOperators[constraint['field']].remove(constraint['operator'])

        for index in indices:
            toGenerate[index]['constraints'].append(queueConstraint)

    Queue = mp.JoinableQueue()
    Out = mp.Manager().Queue()

    for index in subscriptionIndices:
        Queue.put(toGenerate[index])

    print("Starting to update")
    generate(Queue, Out, operatorGenerator, results, allowedOperators)
    print("finished uptading")
    finalResults = {
        "publications": results[:config['publications']],
        "subscriptions": results[config['publications']:]
    }

    endTime = time.time()

    print(f"Time taken = {endTime - startTime}")

    with open(f"{config['threads']}.txt", 'w') as fd:
        fd.write(f"{config['threads']},{endTime - startTime}")

    with open('results.json', 'w') as fd:
        json.dump(finalResults, fd, indent=4)
