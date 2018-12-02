import math


def softmax_row(row):
    """Given a row of things, softmax em,"""
    # You obtain all values between (0,1), and also all values sum to 1.
    summer = 0  # obtain the sum of all exponentials
    return_list = []
    for obtain in row:
        summer += math.exp(obtain)
        print(math.exp(obtain))
    for i in range(len(row)):  # here's to hoping my implementation isn't boggled
        return_list.append(math.exp(row[i])/summer)
        # append back in the exact order they are obtained
    return return_list
