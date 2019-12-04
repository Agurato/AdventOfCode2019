# https://adventofcode.com/2019/day/4


def check_double_digits(number):
    prev_digit = -1
    while number:
        digit = number % 10
        number //= 10
        if digit == prev_digit:
            return True
        prev_digit = digit
    return False


def check_never_decrease(number):
    prev_digit = -1
    while number:
        digit = number % 10
        number //= 10
        if digit > prev_digit and prev_digit != -1:
            return False
        prev_digit = digit
    return True


def check_two_max(number):
    number_s = str(number)
    for d in number_s:
        if number_s.count(d) == 2:
            return True
    return False


def puzzle1(limits):
    count = 0
    for num in range(limits[0], limits[1]):
        if check_double_digits(num) and check_never_decrease(num):
            count += 1
    return count


def puzzle2(limits):
    count = 0
    for num in range(limits[0], limits[1]):
        if (
            check_double_digits(num)
            and check_never_decrease(num)
            and check_two_max(num)
        ):
            count += 1
    return count


if __name__ == "__main__":
    with open("res/day4.txt", "r") as input_f:
        limits = [int(n) for n in input_f.read().split("-")]
        print(puzzle1(limits))
        print(puzzle2(limits))
