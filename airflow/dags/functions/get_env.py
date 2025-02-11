def test(env):
    print(env)
    add_x = env + "-1999"
    return add_x

def test1(env):
    x = test(env)
    y = "-01-01"
    z = x + y
    print(z)