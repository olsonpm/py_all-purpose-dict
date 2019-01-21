# ------- #
# Imports #
# ------- #

from simple_chalk import green, red
from all_purpose_dict import ApDict
from all_purpose_dict.fns import isLaden, joinWith, map_, passThrough
import os


# ---- #
# Init #
# ---- #

x = red("✘")
o = green("✔")


# ---- #
# Main #
# ---- #


def runTests():
    errors = []

    # validate list of pairs
    try:
        code = "ApDict(1)"
        ApDict(1)
    except Exception as e:
        expected = "listOfpairs is not an instance of list"
        if expected not in str(e):
            errors.append(code)

    try:
        code = "ApDict([1])"
        ApDict([1])
    except Exception as e:
        expected = "listOfPairs has 1 element which isn't a list or tuple"
        if expected not in str(e):
            errors.append(code)

    # ensure an empty dict works and test `len`
    code = "ApDict()"
    result = ApDict()
    passed = len(result) == 0
    if not passed:
        errors.append(code)

    # get -> key error
    code = "result.get('doesnt exist')"
    try:
        result.get("doesnt exist")
        errors.append(code)
    except KeyError:
        pass
    except:
        errors.append(code)

    # delete -> key error
    code = "result.delete('doesnt exist')"
    try:
        result.delete("doesnt exist")
        errors.append(code)
    except KeyError:
        pass
    except:
        errors.append(code)

    # del -> key error
    code = "del result['doesnt exist']"
    try:
        del result["doesnt exist"]
        errors.append(code)
    except KeyError:
        pass
    except:
        errors.append(code)

    # _hashableData is populated
    pair = ("a key", "a val")
    code = "ApDict([('a key', 'a val')])"
    result = ApDict([pair])
    passed = (
        len(result._hashableData) == 1
        and result._hashableData["a key"] == "a val"
    )
    if not passed:
        errors.append(code)

    # _nonHashableData is populated
    key = {}
    pair = (key, "a val")
    code = "ApDict([(<ref to {}>, 'a val')])"
    result = ApDict([pair])
    passed = (
        len(result._nonHashableData) == 1
        and result._nonHashableData[id(key)] == pair
    )
    if not passed:
        errors.append(code)

    # set _hashableData
    code = "result.set('a key', 'a different val')"
    result = ApDict([("a key", "a val")])
    result.set("a key", "a different val")
    passed = (
        len(result._hashableData) == 1
        and result._hashableData["a key"] == "a different val"
    )
    if not passed:
        errors.append(code)

    # set _hashableData
    code = "result['a key'] = 'a different val'"
    result = ApDict([("a key", "a val")])
    result["a key"] = "a different val"
    passed = (
        len(result._hashableData) == 1
        and result._hashableData["a key"] == "a different val"
    )
    if not passed:
        errors.append(code)

    # set _nonHashableData
    key = {}
    code = "result.set(<ref to {}>, 'a different val')"
    result = ApDict([(key, "a val")])
    result.set(key, "a different val")
    passed = len(result._nonHashableData) == 1 and result._nonHashableData[
        id(key)
    ] == (key, "a different val")
    if not passed:
        errors.append(code)

    # set _nonHashableData
    key = {}
    code = "result.set(<ref to {}>, 'a different val')"
    result = ApDict([(key, "a val")])
    result[key] = "a different val"
    passed = len(result._nonHashableData) == 1 and result._nonHashableData[
        id(key)
    ] == (key, "a different val")
    if not passed:
        errors.append(code)

    # get _hashableData
    code = "result.get('a key')"
    result = ApDict([("a key", "a val")])
    passed = result.get("a key") == "a val" and result["a key"] == "a val"
    if not passed:
        errors.append(code)

    # get _nonHashableData
    key = {}
    code = "result.get(<ref to {}>)"
    result = ApDict([(key, "a val")])
    passed = result.get(key) == "a val" and result[key] == "a val"
    if not passed:
        errors.append(code)

    # delete _hashableData
    code = "result.delete('a key')"
    result = ApDict([("a key", "a val")])
    result.delete("a key")
    passed = len(result._hashableData) == 0
    if not passed:
        errors.append(code)

    # del _hashableData
    code = "del result['a key']"
    result = ApDict([("a key", "a val")])
    del result["a key"]
    passed = len(result._hashableData) == 0
    if not passed:
        errors.append(code)

    # delete _nonHashableData
    key = {}
    code = "result.delete(<ref to {}>)"
    result = ApDict([(key, "a val")])
    result.delete(key)
    passed = len(result._nonHashableData) == 0
    if not passed:
        errors.append(code)

    # del _nonHashableData
    key = {}
    code = "del result[<ref to {}>]"
    result = ApDict([(key, "a val")])
    del result[key]
    passed = len(result._nonHashableData) == 0
    if not passed:
        errors.append(code)

    # has and 'in' _hashableData
    code = "result.has('a key')"
    result = ApDict([("a key", "a val")])
    passed = result.has("a key") and "a key" in result
    if not passed:
        errors.append(code)

    # has and 'in' _nonHashableData
    key = {}
    code = "result.has(<ref to {}>)"
    result = ApDict([(key, "a val")])
    passed = result.has(key) and key in result
    if not passed:
        errors.append(code)

    # clear all data
    key = {}
    code = "result.clear()"
    result = ApDict([(key, "a val"), ("a key", "another val")])
    result.clear()
    passed = len(result) == 0
    if not passed:
        errors.append(code)

    # get all keys
    key = {}
    code = "result.keysIterator()"
    result = ApDict([(key, "a val"), ("a key", "another val")])
    allKeys = list(result.keysIterator())
    passed = allKeys == [key, "a key"]
    if not passed:
        errors.append(code)

    # get all values
    key = {}
    code = "result.valuesIterator()"
    result = ApDict([(key, "a val"), ("a key", "another val")])
    values = list(result.valuesIterator())
    passed = values == ["a val", "another val"]
    if not passed:
        errors.append(code)

    # iterate dict
    key = {}
    code = "for key, val in aDict:"
    result = ApDict([(key, "a val"), ("a key", "another val")])
    pairs = list(result)
    passed = pairs == [(key, "a val"), ("a key", "another val")]
    if not passed:
        errors.append(code)

    if isLaden(errors):
        errorOutput = passThrough(
            errors, [map_(prepend(f"{x} ")), joinWith(os.linesep)]
        )
        print(errorOutput)
    else:
        print(f"{o} all tests")


# ------- #
# Helpers #
# ------- #


def prepend(leftStr):
    def prepend_inner(rightStr):
        return leftStr + rightStr

    return prepend_inner
