from test_tools import Account, logger, World

def test_comment(world):
    init_node = world.create_init_node()
    init_node.run()

    wallet = init_node.attach_wallet()

    #**************************************************************
    response = wallet.api.create_account('initminer', 'alice', '{}')
    assert 'result' in response

    #**************************************************************
    response = wallet.api.transfer('initminer', 'alice', '200.000 TESTS', 'avocado')
    assert 'result' in response

    #**************************************************************
    response = wallet.api.transfer('initminer', 'alice', '100.000 TBD', 'banana')
    assert 'result' in response

    #**************************************************************
    response = wallet.api.transfer_to_vesting('initminer', 'alice', '50.000 TESTS')
    assert 'result' in response

    #**************************************************************
    response = wallet.api.create_account('alice', 'bob', '{}')
    assert 'result' in response

    #**************************************************************
    response = wallet.api.transfer('alice', 'bob', '50.000 TESTS', 'lemon')
    assert 'result' in response

    #**************************************************************
    response = wallet.api.transfer_to_vesting('alice', 'bob', '25.000 TESTS')
    assert 'result' in response

    #**************************************************************
    response = wallet.api.post_comment('alice', 'test-permlink', '', 'xyz', 'śćą', 'DEBUG    test_tools.wallet.World.InitNodeWallet0:wallet.py:462 Closed with 0 return code', '{}')
    _result = response['result']

    _ops = _result['operations']
    _op = _ops[0]

    assert _op[0] == 'comment'

    _value = _op[1]

    assert _value['author'] == 'alice'
    assert _value['title'] == 'u015bu0107u0105'
    assert _value['body'] == 'DEBUG    test_tools.wallet.World.InitNodeWallet0:wallet.py:462 Closed with 0 return code'

    #**************************************************************
    response = wallet.api.post_comment('alice', 'test-permlink', '', 'xyz', 'TITLE NR 2', 'BODY NR 2', '{}')
    _result = response['result']

    _ops = _result['operations']
    _op = _ops[0]

    assert _op[0] == 'comment'

    _value = _op[1]

    assert _value['author'] == 'alice'
    assert _value['title'] == 'TITLE NR 2'
    assert _value['body'] == 'BODY NR 2'

    #**************************************************************
    response = wallet.api.post_comment('bob', 'bob-permlink', 'alice', 'test-permlink', 'TITLE NR 3', 'BODY NR 3', '{}')
    _result = response['result']

    _ops = _result['operations']
    _op = _ops[0]

    assert _op[0] == 'comment'

    _value = _op[1]

    assert _value['author'] == 'bob'
    assert _value['parent_author'] == 'alice'
    assert _value['title'] == 'TITLE NR 3'
    assert _value['body'] == 'BODY NR 3'

    #**************************************************************
    response = wallet.api.vote('bob', 'bob', 'bob-permlink', 100)
    _result = response['result']

    _ops = _result['operations']
    _op = _ops[0]

    _op[0] == 'vote'

    _value = _op[1]

    assert _value['voter'] == 'bob'
    assert _value['author'] == 'bob'
    assert _value['permlink'] == 'bob-permlink'
    assert _value['weight'] == 10000

    #**************************************************************
    response = wallet.api.decline_voting_rights('alice', True)
    _result = response['result']

    _ops = _result['operations']
    _op = _ops[0]

    assert _op[0] == 'decline_voting_rights'

    _value = _op[1]

    assert _value['account'] == 'alice'