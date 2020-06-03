from __future__ import print_function, unicode_literals, division

from states import InProgressState, DetectedState, StateData

class Signature():
    construction_complete = False
    def __init__(self):
        self.construction_complete = True
    def __setattr__(self,name,value):
        if not self.construction_complete:
            object.__setattr__(self,name,value)
        else:
            raise Exception('Signature objects are immutable. Attribute assignment not supported.')

    def __add__(self,other):
        ...
    def __and__(self,other):
        ...
    def __or__(self,other):
        ...
    def __mul__(self,operand):
        ...
    def __hash__(self):
        return hash((self.__class__,) + self.__getstate__())
    def __eq__(self,other):
        if isinstance(other,Signature):
            return (self.__class__,)+self.__getstate__() == (other.__class__,) + other.__getstate__()
        else:
            return False
    def __ne__(self,other):
        return not (self == other)


class LetterSignature(Signature):
    def alphabet(self):
        yield self.letter

class PatternSignature(Signature): 
    def alphabet(self):
        for element in self.elements:
            yield from element.alphabet()

class OBS(LetterSignature):
    def __init__(self,name,tag=None):
        self.name = name
        self.letter = (name,frozenset())
        self.tag = tag
        self.construction_complete = True
    def __getstate__(self):
        return (self.name,self.tag)
    def __setstate__(self,state):
        object.__setattr__(self,'construction_complete',False)
        self.name,self.tag = state
        self.construction_complete = True

    def update(self,state,timestamp,name,attrs):
        return DetectedState(self,timestamp,timestamp,None)


class CON(LetterSignature):
    def __init__(self,name,*constraints,tag=None):
        self.name = name
        self.constraints = frozenset(tuple(constraint) for constraint in constraints)
        self.letter = (name,constraints)
        self.tag = tag
        self.construction_complete = True
    def __getstate__(self):
        return (self.name,self.constraints,self.tag)
    def __setstate__(self,state):
        object.__setattr__(self,'construction_complete',False)
        self.name,self.constraints,self.tag = state
        self.construction_complete = True
    def update(self,state,timestamp,name,attrs):
        return DetectedState(self,timestamp,timestamp,None)

class ALL(PatternSignature):
    def __init__(self,*elements):
        accepted_elements = set()
        for element in elements:
            if isinstance(element,ALL):
                for sub_element in element.elements:
                    accepted_elements.add(sub_element)
            elif isinstance(element,str):
                accepted_elements.add(OBS(element))
            else:
                accepted_elements.add(element)
        self.elements = frozenset(accepted_elements)
    def __getstate__(self):
        return (self.elements,)
    def __setstate__(self,state):
        object.__setattr__(self,'construction_complete',False)
        self.elements, = state
        self.construction_complete = True
    def update(self,state,timestamp,name,attrs):
        if state is None:
            state = InProgressState(self,timestamp,timestamp,StateData(in_progress={},detected={}))
        for element in self.elements:
            ...

class ANY(PatternSignature):
    ...
class SEQ(PatternSignature):
    ...
class REPMIN(PatternSignature):
    ...
class REPMAX(PatternSignature):
    ...
