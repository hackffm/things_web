import helper_test

from things import *

ts1 = 'ts1'
ts2 = 'ts2'
debug = True
id_thing1 = 'door1'
id_thing2 = 'door2'
t1 = Thing(id_thing1)
t2 = Thing(id_thing2)
things = [t1]

NS1 = NodeSerial(ts1, debug)
NS2 = NodeSerial(ts2)
print(NS1.thing_add(t1))


# -- Logic --------------------------------------------------------------------------


def test_thing_exists():
    print('>test_thing_exists')
    assert NS1.thing_exists(id_thing1) == True, 'Failed finding thing'
    assert NS1.thing_exists('nono1') == False, 'failed checking non existing thing'


def test_thing_not_empty():
    print('>test_thing_not_empty')
    _things = NS1.things
    assert len(_things) > 0, 'Failed counting things'
    for t in _things:
        print(t.id)


def test_all_thing_properties():
    print('>test_all_thing_properties')
    NS1.thing_add(t2)
    print('serial thing ' + str(NS1.id) + ' has properties')
    print('debug    ' + str(NS1.debug))
    print('message  ' + NS1.message)
    print('result   ' + NS1.result)
    print('verified ' + str(NS1.verified))
    print('list of things')
    for t in NS1.things:
        print(str(t.id))


test_thing_exists()
test_thing_not_empty()
test_all_thing_properties()
