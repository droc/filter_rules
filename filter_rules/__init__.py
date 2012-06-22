class CompositionalRule(object):
    def __and__(self, other):
        return And(self, other)

    def __invert__(self):
        return Not(self)

    def __or__(self, other):
        return Or(self, other)

    def __ne__(self, other):
        return Not(self.__eq__(other))

    def accepts(self, anObject):
        raise NotImplementedError


class CollectionAttributeIncludesFilter(CompositionalRule):
    def __init__(self, attribute, quantifier, filter):
        self.filter = filter
        self.attribute = attribute
        self.quantifier = quantifier

    def accepts(self, anObject):
        return self.quantifier(self.filter.accepts(x) for x in getattr(anObject, self.attribute))


class And(CompositionalRule):
    def __init__(self, l, r):
        self.r = r
        self.l = l

    def accepts(self, anObject):
        return self.l.accepts(anObject) and self.r.accepts(anObject)


class Or(CompositionalRule):
    def __init__(self, l, r):
        self.r = r
        self.l = l

    def accepts(self, anObject):
        return self.l.accepts(anObject) or self.r.accepts(anObject)


class AttributeEqualsFilter(CompositionalRule):
    def __init__(self, attribute, value):
        self.value = value
        self.attribute = attribute

    def accepts(self, anObject):
        return self.value == getattr(anObject, self.attribute)


class AttributeLambdaFilter(CompositionalRule):
    def __init__(self, attribute, l):
        self.l = l
        self.attribute = attribute

    def accepts(self, anObject):
        return self.l(getattr(anObject, self.attribute))


class ConditionOnCollectionAttribute(CompositionalRule):
    def __init__(self, collection_attribute):
        self.collection_attribute = collection_attribute

    def includes(self, quantifier, criteria):
        return CollectionAttributeIncludesFilter(self.collection_attribute, quantifier, criteria)


class ConditionOnAttribute(object):
    def __init__(self, attr_name):
        self.attr_name = attr_name

    def __eq__(self, other):
        return AttributeLambdaFilter(self.attr_name, lambda x: x == other)

    def includes(self, param):
        return AttributeLambdaFilter(self.attr_name, lambda x: param in x)


class ForAll(CompositionalRule):
    def __init__(self, attribute, condition):
        self.attribute = attribute
        self.condition = condition

    def accepts(self, anObject):
        return all([self.condition.accepts(x) for x in getattr(anObject, self.attribute)])


class Not(CompositionalRule):
    def __init__(self, inner):
        self.inner = inner

    def accepts(self, anObject):
        return not self.inner.accepts(anObject)


class Exists(CompositionalRule):
    def __init__(self, attribute, condition):
        self.attribute = attribute
        self.condition = condition

    def accepts(self, anObject):
        return any(self.condition.accepts(x) for x in getattr(anObject, self.attribute))


class IF(object):
    def __init__(self, precedent_condition, consequent_condition):
        self.consequent_condition = consequent_condition
        self.precedent_condition = precedent_condition

    def accepts(self, anObject):
        return Not(self.precedent_condition).accepts(anObject) or self.consequent_condition.accepts(anObject)


class AcceptAllFilter(CompositionalRule):
    def accepts(self, anObject):
        return True
