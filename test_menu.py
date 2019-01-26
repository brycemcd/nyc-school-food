import menu as m

def test_breakfast():
    bfast = m.BREAKFAST

    assert type(bfast) == dict
    for dt, bfast_items in bfast.items():
        assert dt # is not empty
        if len(bfast_items) == 1:
            assert bfast_items[0] == m.NO_SCHOOL_STRING
            continue

        assert len(bfast_items) == 2, ("%s does not have two entries" % dt)

def test_lunch():
    lunch = m.LUNCH

    assert type(lunch) == dict
    for dt, lunch_item in lunch.items():
        assert type(lunch_item) == str
        assert lunch_item
        assert dt # is not empty
