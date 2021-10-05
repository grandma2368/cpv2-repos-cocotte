def guess_close_nbr(nbr):
    guess = round(nbr / 2)
    while guess * guess > nbr:
        guess -= 1
    return guess if guess != 0 else 1


def better_approx(nbr, approx):
    return (approx + nbr/approx)/2


def ft_sqrt(nbr):
    approx = guess_close_nbr(nbr)
    for i in range(3):
        approx = better_approx(nbr, approx)
        i += 1
    return round(approx, 3)
