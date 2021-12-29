from time import time, sleep
from random import randint, choice

operations = ('+', '-', '*', '/')

def givechal():
    challenge = str(randint(1, 999)) + ' ' + choice(operations) + ' ' + str(randint(1, 999)) + ' ' + choice(operations) + ' ' + str(randint(1, 999))
    result = int(eval(challenge))
    return challenge, result

def main():
    print('Can You Math It?')
    sleep(1)
    print('You have 5 seconds to answer each question')
    print('You have 100 questions to solve')
    print('Please give all answers to nearest integer')
    print('Good luck')
    sleep(1)
    for i in range(100):
        challenge, result = givechal()
        print('Solve ', challenge, ' :')
        start = time()
        answer = input()
        timetaken = time() - start
        if timetaken < 5 and answer == str(result):
            print('Correct!')
            print('Next question')
        elif timetaken > 5:
            print('Took longer than 5 seconds')
            exit()
        else:
            print('Wrong answer')
            exit()
    print('Congratulations! You CAN math it')
    print('The flag is IRS{4f2cd85d0a9f32f4}')

if __name__ == '__main__':
    main()