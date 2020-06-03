from __future__ import print_function, unicode_literals, division

def expand_alphabet(alphabet):
    ea = {}
    for name,constraints in alphabet:
        if len(constraints) == 0:
            ea[name] = True
        elif name in ea:
            if ea[name] is not True:
                ea[name].add(constraints)
        else:
            ea[name] = set()
            ea[name].add(constraints)
    return ea

class State():
    def __init__(self,signature,first_timestamp,last_timestamp,data):
        self.signature = signature
        self.first_timestamp = first_timestamp
        self.last_timestamp = last_timestamp
        self.data = data

class InProgressState(State): pass

class DetectedState(State): pass

class StateData():
    def __init__(self,**kwargs):
        for kw,value in kwargs.items():
            setattr(self,kw,value)
