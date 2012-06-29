"""A package"""

def status():
    import random
    msgs = ['Resting peacefully',
            'Listening to the angels',
            "Can't a spirit get any peace around here?"]
    return random.choice(msgs)
