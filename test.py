

def decorador(func):
    def wrapper(*args, **kwargs):
        kwargs['arg2'] = 'valor'
        return func(*args, **kwargs)
    return wrapper

@decorador
def funcao_test(arg1=None, **kwargs):
    print(locals())

funcao_test()