import numpy as np
import PublicationItem as PI
import json
import time
import queue
import threading

EPS = 10e-6


def generatePublication():
    publication = {}
    for field in PI.PublicationItem:
        publication[field] = PI.PublicationItem[field]()
    return publication


def generateSubscription(constraints, allowed):
    fields = np.random.choice(allowed, np.random.randint(0, len(allowed)), replace=False)
    subscriptions = {}
    for field in fields:
        subscriptions[field] = {
            'operator': None,
            'value': PI.PublicationItem[field]()
        }
    for cons in constraints:
        subscriptions[cons['field']] = {
            'operator': cons['operator'],
            'value': PI.PublicationItem[cons['field']]()
        }
    return subscriptions


def updateSubscription(subscription, constraints, operators):
    for cons in constraints:
        subscription[cons['field']]['operator'] = cons['operator']
    for field in subscription:
        if subscription[field]['operator'] is None:
            subscription[field]['operator'] = 0
    return subscription


def frequencyGenerator():
    while not Queue.empty():
        item = Queue.get()
        if item['type'] == 'pub':
            results[item['index']] = generatePublication()
        else:
            results[item['index']] = generateSubscription(item['constraints'], allowedFields)


def generate(generator):
    threads = []
    for i in range(config['threads']):
        thread = threading.Thread(target=generator)
        threads.append(thread)
        threads[-1].start()

    for thread in threads:
        thread.join()


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

        indices = np.random.choice(subscriptionIndices, round(percent * len(subscriptionIndices) / 100), replace=False)

        queueConstraint = {
            'field': constraint['field'],
            'operator': None
        }

        if constraint['field'] in allowedFields:
            allowedFields.remove(constraint['field'])

        for index in indices:
            toGenerate[index]['constraints'].append(queueConstraint)

    Queue = queue.Queue()
    for element in toGenerate:
        Queue.put(element)

    generate(frequencyGenerator)

    finalResults = {
        "publications": results[:config['publications']],
        "subscriptions": results[config['publications']:]
    }

    endTime = time.time()

    print(f"Time taken = {endTime - startTime}")

    with open('results.json', 'w') as fd:
        json.dump(finalResults, fd, indent=2)
