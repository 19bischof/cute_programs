
def myfunction():
    yield 5*555
    yield 4*444
def thisfunction():
    for index,bullet in enumerate(myfunction()):
        if index == 0:
            assert bullet == 2775
        else:
            assert bullet == 1776
thisfunction()