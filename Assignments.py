money = float(input("How much US Dollars are you sending? "))
conversion = int(money)*120
print(conversion)

grade = float(input('What is your grade? '))

if int(grade)>=90:
    print("Your Grade is an A")
elif 80 <= int(grade) <=89:
    print("Your Grade is a B")
elif 70 <= int(grade) <= 79:
    print("Your Grade is a C")
elif 60 <= int(grade) <= 69:
    print("Your Grade is a D")
elif int(grade) <= 59:
    print("your Grade is a F")

import random
user_action = input("Enter a choice of rock, paper, or scissors: ")
possible_action = ['rock', 'paper', 'scissors']
computer_action = random.choice(possible_action)
print("you chose " + user_action + ' computer chose ' + computer_action + ".")

if user_action.lower() == computer_action:
    print("Both Players Selected " + user_action + " it is a tie.")
elif user_action.lower() == 'rock':
    if computer_action == 'scissors':
        print('Rock Smashes Scissors. You win.')
    else:
        print("Paper Covers Rock. You lose.")
elif user_action.lower() == 'scissors':
    if computer_action == 'paper':
        print('Scissors Cuts the Paper. You win.')
    else:
        print("Rock Crushes Scissors. You lose.")
elif user_action.lower() == 'paper':
    if computer_action == 'rock':
        print('Paper Covers the Rock. You win.')
    else:
        print("Scissors Cuts Paper. You lose.")



