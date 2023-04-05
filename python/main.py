import numpy as np
import PublicationItem as PI
import json
import time

if __name__ == "__main__":

    startTime = time.time()

    """
    publications: number
    subscriptions: number
    constraints: [
        type: x \in {frequency, operator}, 
        field: x \in {publication fields},
        operator: x \in {<, <=, >, >=, =},
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

    endTime = time.time()

    print(f"Time taken = {endTime - startTime}")

