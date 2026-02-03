balance=0
output=" "
while True:
    print("[Welcome to OwlBanking] ")
    print("1 – Deposit \n 2 – Withdraw \n 3 – Check Balance \n 4 – Check Transaction History \n Q – Quit ")

    choice=input("")

    if choice == "1":
        deposit=float(input("How much do you want to deposit: "))
        balance+=deposit
        output+=f"${deposit} was deposited, balance went from $0.00 to ${deposit}\n"

    elif choice == "2":
        if balance == 0:
            print("Error: Cannot Withdraw with balance of zero ")
        else:
            wihtdraw=float(input("How much do you want to withdraw: "))
            if wihtdraw > balance:
                print("Error")
            else:
                balance-=wihtdraw
                output += f"${Withdraw} was withdrawn, balance went from $0.00 to ${Withdraw}\n"
    elif choice == "3":
        print(balance)
    elif choice == "4":
        break
    elif choice=="Q":
        break



