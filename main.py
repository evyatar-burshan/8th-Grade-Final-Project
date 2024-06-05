##############################################
### * * * * * Table of Contents: * * * * * ###
### 1. Imports                             ###
### 2. File Readers                        ###
### 3. Variable Setting                    ###
### 4. Typing Animation Function           ###
### 5. Input Function                      ###
### 6. Weather Randomizer                  ###
### 7. Beginning of day processes          ###
### 8. Main Game Code                      ###
### 9. End of Day Summary                  ###
### 10. Shop Setup                         ###
### 11. Buying Mechanism                   ###
### 12. Lemonade Cup Value Estimator       ###
### 13. Recipe Builder                     ###
### 14. Max Amount of Lemonade Calculator  ###
### 15. Tutorial                           ###
### 16. Header Animation                   ###
### 17. Game Startup                       ###
### 18. Developer Test Mode                ###
### 19. Running the Game                   ###
### 20. File Closers                       ###
##############################################


################
### Imports: ###
################
import os
import time
import random
import sys
import math
from termcolor import colored

#####################
### File Readers: ###
#####################
welcomeFile = open('titles/welcome.txt', 'r')
welcomeMessage = welcomeFile.read()
shopFile = open('titles/shop.txt', 'r')
shopTitle = shopFile.read()
recipeFile = open('titles/recipeBuilder.txt', 'r')
recipeTitle = recipeFile.read()
standFile = open('titles/stand.txt', 'r')
standTitle = standFile.read()
summaryFile = open('titles/summary.txt', 'r')
summaryTitle = summaryFile.read()

#########################
### Variable Setting: ###
#########################
welcomeLoad = []
reverseWelcomeLoad = []
day = 0
customerCount = 15
global balance
balance = 50.0
starLength = 85
lemonDict = {
    "Price": 0.8,
    "Stock": 0,
    "AmountPerPurchase": 10,
    "PerfectAmount": 1
}
waterDict = {
    "Price": 0.6,
    "Stock": 0,
    "AmountPerPurchase": 70,
    "PerfectAmount": 8
}
sugarDict = {
    "Price": 1.5,
    "Stock": 0,
    "AmountPerPurchase": 8,
    "PerfectAmount": 4
}
iceDict = {
    "Price": 1.0,
    "Stock": 0,
    "AmountPerPurchase": 16,
    "PerfectAmount": 2
}
lemonadePrice = 0.0
lemonadeStock = 0
recipeForTheDay = {"Lemon": 0, "Water": 0, "Sugar": 0, "Ice": 0}

for i in range(0, starLength + 2):
    reverseWelcomeLoad.append(" ")


##################################
### Typing Animation Function: ###
##################################
def Type(text):
    words = text
    for char in words:
        time.sleep(0.06)
        sys.stdout.write(char)
        sys.stdout.flush()
    print()


#######################
### Input Function: ###
#######################
def Input(questionType, question, *options, actionsList):
    if questionType == "multipleChoice":
        answered = False
        Type(colored(question, 'cyan'))
        answer = input()
        answer = answer.lower()
        while answered == False:
            for i in options:
                if i.lower() == answer or i.lower() + "s" == answer or i.lower() + "S" == answer:
                    answered = True
                    action = actionsList[options.index(i)]
                    if answer[-1] == "s" or answer[-1] == "S":
                        answer = answer[:-1]
                    time.sleep(0.25)
                    return answer, eval(action)
            else:
                if answered == False:
                    print(colored("\n\tThat's not a valid answer!", 'red'))
                    print(colored(question, 'cyan'))
                    answer = input()
                    answer = answer.lower()
    elif questionType == "anyChoice":
        Type(colored(question, 'cyan'))
        answer = input()
        action = actionsList[0]
        time.sleep(0.25)
        return eval(action)
    elif questionType == "numberRange":
        answered = False
        Type(colored(question, 'cyan'))
        if actionsList[0] == "int":
            while answered == False:
                try:
                    answer = int(input())
                    answered = True
                    time.sleep(0.25)
                    return answer
                except ValueError:
                    print(colored("\n\tThat's not a valid answer!", 'red'))
                    print(colored(question, 'cyan'))
                    answered = False
        elif actionsList[0] == "float":
            while answered == False:
                try:
                    answer = float(input())
                    answered = True
                    time.sleep(0.25)
                    return answer
                except ValueError:
                    print(colored("\n\tThat's not a valid answer!", 'red'))
                    print(colored(question, 'cyan'))
                    answered = False


###########################
### Weather Randomizer: ###
###########################
def Weather():
    global weather
    weatherList = ["Sunny", "Hot", "Cloudy", "Rainy"]
    weatherRandomizer = random.choice(weatherList)
    if weatherRandomizer == "Cloudy":
        isMeatballs = random.randint(1, 10)
        if isMeatballs == 7:
            weather = "CLOUDY WITH A CHANCE OF MEATBALLS"
        else:
            weather = weatherRandomizer
    else:
        weather = weatherRandomizer
    return weather


###################################
### Beginning of day processes: ###
###################################
def StartDay():
    global weatherToday, day, balance
    day += 1
    balance = round(balance, 2)
    lemonDict["Stock"] = round(lemonDict["Stock"], 2)
    waterDict["Stock"] = round(waterDict["Stock"], 2)
    sugarDict["Stock"] = round(sugarDict["Stock"], 2)
    iceDict["Stock"] = round(iceDict["Stock"], 2)
    if day == 1:
        weatherToday = "Sunny"
    else:
        weatherToday = Weather()
    os.system('clear')
    Type(F"Day {day} in {name}'s Lemonade stand:")
    Type(colored(F"\nYour current balance is: {balance}🌕", 'green'))
    Type(F"The weather today is: {weatherToday}")
    Shop()


#######################
### Main Game Code: ###
#######################
def RunDay():
    global lemonadePayment, sourCustomers, blandCustomers, bitterCustomers, warmCustomers, expensiveCustomers, outOfStockCustomers, totalLostCustomers, totalBadEffectCustomers, totalCustomerMoneyLost, originalcustomerCount, tipCustomers, totalTipMoney
    sourCustomers, blandCustomers, bitterCustomers, warmCustomers, expensiveCustomers, outOfStockCustomers, totalLostCustomers, totalBadEffectCustomers, totalCustomerMoneyLost, tipCustomers = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    estimatedLemonadePrice = EstLemonadeValue()
    def BadLemonadeRandomizer():
        global lemonadePayment, sourCustomers, blandCustomers, bitterCustomers, warmCustomers, expensiveCustomers, tipCustomers
        lemonadePayment = lemonadePrice
        lemonDifference = abs(lemonDict["PerfectAmount"] -
                              recipeForTheDay["Lemon"])
        waterDifference = abs(waterDict["PerfectAmount"] -
                              recipeForTheDay["Water"])
        sugarDifference = abs(sugarDict["PerfectAmount"] -
                              recipeForTheDay["Sugar"])
        iceDifference = abs(iceDict["PerfectAmount"] - recipeForTheDay["Ice"])
        moneyDiffernce = estimatedLemonadePrice - lemonadePrice
        isExpensive = round(random.uniform(0, -2), 2)
        if moneyDiffernce < isExpensive:
            expensiveCustomers += 1
            return "Too Expensive"
        isDifferent = round(random.uniform(-5, 1.5),2)
        if isDifferent < lemonDifference:
            lemonadePayment = round(lemonadePayment * 0.9, 2)
            sourCustomers += 1
            return "Sour"
        elif isDifferent < waterDifference:
            lemonadePayment = round(lemonadePayment * 0.9, 2)
            blandCustomers += 1
            return "Bland"
        elif isDifferent < sugarDifference:
            bitterCustomers += 1
            lemonadePayment = round(lemonadePayment * 0.9, 2)
            return "Bitter"
        elif isDifferent < iceDifference:
            warmCustomers += 1
            lemonadePayment = round(lemonadePayment * 0.9, 2)
            return "Warm"
        isTip = round(random.uniform(-0.5, 1.3), 2)
        if moneyDiffernce < isTip:
            tipCustomers += 1
            lemonadePayment = round(lemonadePayment * 1.1, 2)
            return "Tip"
        else:
            return None

    global lemonadeStock, balance, lemonadePrice, originalBalance
    originalBalance = balance
    lemonadePayment = lemonadePrice
    customerCount = 15
    if weatherToday == "Hot":
        changeValueBy = round(random.uniform(1.45, 1.86), 2)
    elif weatherToday == "Rainy":
        changeValueBy = round(random.uniform(0.5, 0.8), 2)
    elif weatherToday == "Cloudy":
        changeValueBy = round(random.uniform(0.7, 1), 2)
    elif weatherToday == "Sunny":
        changeValueBy = round(random.uniform(0.95, 1.4), 2)
    elif weatherToday == "CLOUDY WITH A CHANCE OF MEATBALLS":
        changeValueBy = 3
    customerCount *= changeValueBy
    customerCount = round(customerCount)
    originalcustomerCount = customerCount
    for i in range(1, customerCount + 1):
        os.system('clear')
        print(standTitle)
        if lemonadeStock <= 0:
            outOfStockCustomers += 1
            print(F"\n\nCustomer Number {i}: Out of stock!")
        elif lemonadeStock > 0:
            effect = BadLemonadeRandomizer()
            if effect == "Sour" or effect == "Bland" or effect == "Bitter" or effect == "Warm":
                print(
                    F"\n\nCustomer Number {i}: Bought Lemonade!, The lemonade was {effect} (+{lemonadePayment}🌕)"
                )
                balance += lemonadePayment
                lemonadeStock -= 1
            elif effect == "Tip":
                print(
                    F"\n\nCustomer Number {i}: Bought Lemonade!, The lemonade was AMAZING (+ {lemonadePayment}🌕 +Tip!)"
                )
                balance += lemonadePayment
                lemonadeStock -= 1
            elif effect == "Too Expensive":
                print(F"\n\nCustomer Number {i}: Too Expensive!")
            else:
                print(
                    F"\n\nCustomer Number {i}: Bought Lemonade!, The lemonade was Good (+ {lemonadePayment}🌕)"
                )
                balance += lemonadePayment
                lemonadeStock -= 1
            time.sleep(0.5)
    totalLostCustomers = expensiveCustomers + outOfStockCustomers
    totalBadEffectCustomers = sourCustomers + blandCustomers + bitterCustomers + warmCustomers
    totalCustomerMoneyLost = round(
        totalBadEffectCustomers * (lemonadePrice * 0.1), 2)
    totalTipMoney = round(tipCustomers * lemonadePayment * 0.1, 2)
    Summary()


###########################
### End of Day Summary: ###
###########################
def Summary():
    global lemonadeStock
    os.system('clear')
    print(summaryTitle)
    profit = round(balance - originalBalance, 2)
    print(F"\n\n{originalcustomerCount} customers came to your stand today!")
    if profit >= 0:
        print(colored(F"You profited {profit}🌕", 'green'))
    elif profit < 0:
        print(colored(F"\n\nYou lost {profit}🌕", 'red'))
    if lemonadeStock > 0:
        print(
            colored(
                F"You threw away {lemonadeStock} lemonades (buy less lemonade)",
                'red'))
    else:
        print(colored("You didn't throw away any lemonades today!", 'green'))
    lemonadeStock = 0
    print(
        colored(
            F"{tipCustomers} customers tipped you! ({totalTipMoney}🌕 in total)",
            'green'))
    if totalLostCustomers > 0:
        print(
            colored(F"\nYou lost {totalLostCustomers} customers in total:",
                    'red'))
        print(
            F"\n{expensiveCustomers} customers thought your lemonade was too expensive! (reduce the price your lemonade)"
        )
        print(
            F"{outOfStockCustomers} customers didn't get lemonade because it was out of stock! (buy more lemonade)"
        )
    else:
        print(
            colored(F"\nYou lost {totalLostCustomers} customers in total",
                    'green'))
    if totalCustomerMoneyLost > 0:
        print(
            colored(
                F"\nYou lost {totalCustomerMoneyLost}🌕 from customers in total ({totalBadEffectCustomers} customers):",
                'red'))
        print(
            F"\n{sourCustomers} customers thought your lemonade was too sour! (change the amount of lemons in each cup)"
        )
        print(
            F"{blandCustomers} customers thought your lemonade was too bland! (change the amount of water in each cup)"
        )
        print(
            F"{bitterCustomers} customers thought your lemonade was too bitter! (change the amount of sugar in each cup)"
        )
        print(
            F"{warmCustomers} customers thought your lemonade was too warm! (change the amount of ice in each cup)"
        )
    else:
        print(
            colored(
                F"\nYou lost {totalCustomerMoneyLost}🌕 from customers in total ({totalBadEffectCustomers} customers)",
                'green'))
    Input("anyChoice",
          "\n\nType anything when you're ready to continue!",
          'start',
          actionsList=["StartDay()"])


###################
### Shop Setup: ###
###################
def Shop():
    time.sleep(1)
    os.system('clear')
    print(shopTitle)
    print(colored(F"\n\nYour current balance is: {balance}🌕", 'green'))
    print(F"The weather today is: {weatherToday}")
    print(
        "\n\n8 Spoon = 100 Grams,\n70 Spoons = 1 Liter,\n1 Ice Tray = 16 Ice Cubes,\n1 Lemon Bag = 10 Lemons.\n\n"
    )
    print("You Have:\n🍋" + str(lemonDict["Stock"]) + " Lemons\n💧" +
          str(waterDict["Stock"]) + " sp Water\n🍚" + str(sugarDict["Stock"]) +
          " sp Sugar\n🧊" + str(iceDict["Stock"]) + " Ice Cubes")

    print(F"\n🍋Lemons Bag (10 Lemons) = " + str(lemonDict["Price"]) +
          "🌕\n💧Water Bottle (1L) = " + str(waterDict["Price"]) +
          "🌕\n🍚Sugar Bag (100g) = " + str(sugarDict["Price"]) +
          "🌕\n🧊Ice Tray (16 Cubes) = " + str(iceDict["Price"]) + "🌕")
    requestedItem = Input("multipleChoice",
                          "\n\nWhat would you like to buy?",
                          "lemon",
                          "water",
                          "sugar",
                          "ice",
                          actionsList=["None", "None", "None", "None"])[0]
    amountToBuy = Input(
        "numberRange",
        "How much of it would you like to buy (Bags/Bottles/Trays)?",
        '1',
        actionsList=["int"])
    Buy(requestedItem, amountToBuy, eval(requestedItem + "Dict[\"Price\"]"))


#########################
### Buying Mechanism: ###
#########################
def Buy(item, amount, price):
    global balance
    stock = eval(item + "Dict[\"Stock\"]")
    if balance >= price * amount:
        balance -= eval(item + "Dict[\"Price\"]") * amount
        balance = round(balance, 2)
        stock += eval(item + "Dict[\"AmountPerPurchase\"]") * amount
        eval(item + "Dict" + ".update({\"Stock\": stock})")
        Input("multipleChoice",
              "Would you like to buy more items (ANY items)? (y/n)",
              'y',
              'n',
              actionsList=["Shop()", "RecipeBuilder()"])
    else:
        print(colored("You don't have enough money to buy that!", 'red'))
        Shop()


#####################################
### Lemonade Cup Value Estimator: ###
#####################################
def EstLemonadeValue():
    estLemonadePrice = 4
    if weatherToday == "Hot":
        changeValueBy = round(random.uniform(1.45, 1.86), 2)
    elif weatherToday == "Rainy":
        changeValueBy = round(random.uniform(0.5, 0.8), 2)
    elif weatherToday == "Cloudy":
        changeValueBy = round(random.uniform(0.7, 1), 2)
    elif weatherToday == "Sunny":
        changeValueBy = round(random.uniform(0.95, 1.4), 2)
    elif weatherToday == "CLOUDY WITH A CHANCE OF MEATBALLS":
        changeValueBy = 3
    estLemonadePrice *= changeValueBy
    estLemonadePrice = round(estLemonadePrice, 1)
    return estLemonadePrice


#######################
### Recipe Builder: ###
#######################
def RecipeBuilder():
    def RecipeBuilderInput(question, item):
      asnweredUpdate = False
      updateRecipe = Input("numberRange", question, '1', actionsList=["float"])
      while asnweredUpdate == False:
        if updateRecipe > eval(item.lower() + "Dict[\"Stock\"]"):
          print(colored("\n\tThat's not a valid answer!", 'red'))
          updateRecipe = Input("numberRange",
                                 question,
                                 '1',
                                 actionsList=["float"])
        else:
           recipeForTheDay[item] = updateRecipe
           asnweredUpdate = True
    global lemonadeStock, lemonadePrice
    print(recipeTitle)
    currentItem = ["lemon", "water", "sugar", "ice"]
    if weatherToday == "Sunny":
        changeBy = random.uniform(1, 2)
    elif weatherToday == "Cloudy":
        changeBy = random.uniform(0.8, 1.2)
    elif weatherToday == "Rainy":
        changeBy = random.uniform(0.3, 0.7)
    elif weatherToday == "Hot":
        changeBy = random.uniform(1.5, 2.5)
    elif weatherToday == "CLOUDY WITH A CHANCE OF MEATBALLS":
        changeBy = 3
    for i in range(4):
        changedPerfect = eval(currentItem[i] +
                              "Dict[\"PerfectAmount\"]*changeBy")
        changedPerfect = round(changedPerfect, 1)
        eval(currentItem[i] + "Dict" +
             ".update({\"PerfectAmount\": changedPerfect})")
        i += 1

    os.system('clear')
    print(recipeTitle)
    print(
        "\n\n8 Spoon = 100 Grams,\n70 Spoons = 1 Liter,\n1 Ice Tray = 16 Ice Cubes,\n1 Lemon Bag = 10 Lemons."
    )
    print("\nYou Have:\n🍋" + str(lemonDict["Stock"]) + " Lemons\n💧" +
          str(waterDict["Stock"]) + " sp Water\n🍚" + str(sugarDict["Stock"]) +
          " sp Sugar\n🧊" + str(iceDict["Stock"]) + " Ice Cubes")

    RecipeBuilderInput("\n\nHow much lemons should be in each lemonade cup?",
                       "Lemon")
    RecipeBuilderInput(
        "How much spoons of water should be in each lemonade cup?", "Water")
    RecipeBuilderInput(
        "How much spoons of sugar should be in each lemonade cup?", "Sugar")
    RecipeBuilderInput("How much ice cubes should be in each lemonade cup?",
                       "Ice")
    asnweredUpdate = False
    print(
        colored("\n\n\tHow much would you like to charge per lemonade cup?",
                'cyan'))
    while asnweredUpdate == False:
        try:
            lemonadePrice = float(input("\t"))
            asnweredUpdate = True
            time.sleep(0.25)
        except ValueError:
            print(colored("\n\tThat's not a valid answer!", 'red'))
            print(
                colored(
                    "\nHow much would you like to charge per lemonade cup?",
                    'cyan'))
            asnweredUpdate = False
    maximumLemonadeAvailable = MaxAmountOfLemonade()
    asnweredUpdate = False
    print(
        colored(
            F"\n\n\tHow much cups of lemonade would you like to make? (maximum {maximumLemonadeAvailable})",
            'cyan'))
    while asnweredUpdate == False:
        try:
            lemonadeStock = int(input("\t"))
            if lemonadeStock > maximumLemonadeAvailable:
                print(colored("\n\tThat's not a valid answer!", 'red'))
                print(
                    colored(
                        F"\nHow much cups of lemonade would you like to make? (maximum {maximumLemonadeAvailable})",
                        'cyan'))
                asnweredUpdate = False
            else:
                lemonDict["Stock"] -= recipeForTheDay["Lemon"] * lemonadeStock
                waterDict["Stock"] -= recipeForTheDay["Water"] * lemonadeStock
                sugarDict["Stock"] -= recipeForTheDay["Sugar"] * lemonadeStock
                iceDict["Stock"] -= recipeForTheDay["Ice"] * lemonadeStock
                asnweredUpdate = True
                time.sleep(0.25)
        except ValueError:
            print(colored("\n\tThat's not a valid answer!", 'red'))
            print(
                colored(
                    F"\nHow much cups of lemonade would you like to make? (maximum {maximumLemonadeAvailable})",
                    'cyan'))
            asnweredUpdate = False
    RunDay()


##########################################
### Max Amount of Lemonade Calculator: ###
##########################################
def MaxAmountOfLemonade():
    global recipeForTheDay
    maxLemonadeList = []

    def ZeroCheck(item):
        try:
            updateMaxLemonadeList = eval(
                item.lower() + "Dict[\"Stock\"]") / recipeForTheDay[item]
        except ZeroDivisionError:
            updateMaxLemonadeList = 0
        maxLemonadeList.append(updateMaxLemonadeList)

    ZeroCheck("Lemon")
    ZeroCheck("Water")
    ZeroCheck("Sugar")
    ZeroCheck("Ice")
    maxLemonade = min(maxLemonadeList)
    maxLemonade = math.floor(maxLemonade)
    return maxLemonade


#################
### Tutorial: ###
#################
def Tutorial():
    os.system('clear')
    print(
        "The goal of this game is to acquire as much money as possible in 7 days.\n\n"
    )
    time.sleep(4)
    print(
        "To acquire money (symbolized as 🌕) you'll need to sell lemonade to the people of Lem🍋nville.\n\n"
    )
    time.sleep(4)
    print(
        "Each day you'll need to buy lemons, water, ice & sugar to make your lemonade. Then, you will be tasked with making THE PERFECT lemonade recipe (You can use a decimal point), by adjusting the amounts of your lemons, water, ice & sugar.\n\n"
    )
    time.sleep(8)
    print(
        "The measurements are:\n8 Spoon = 100 Grams,\n70 Spoons = 1 Liter,\n1 Ice Tray = 16 Ice Cubes,\n1 Lemon Bag = 10 Lemons.\n\n"
    )
    time.sleep(3)
    print(
        "But that's not all, Lem🍋nville is known for it's CrAzY weather. So you'll need to adjust the recipe and the price accordingly.\n\n"
    )
    time.sleep(5)
    print(
        colored(
            "Tip: Default measurments for a lemonade cup are close to real life! 1 Lemon, 8 sp Water, 4 sp Sugar and 2 Ice cubes! (worth about 3🌕)\n\n",
            'green'))
    time.sleep(5)
    print(
        "So you've created you're recipe, watched today's forecast, now all you need is to name your price! When you set a price we reccomend you consider: The weather, the price of your stock, how much stock you have and what people will think of the price.\n\n"
    )
    time.sleep(10)
    print(
        "Then you'll need to make as much lemonade as you think customers will buy. Any lemonade left at the end of the day will be thrown away.\n\n"
    )
    time.sleep(7)
    print(
        "At the end of each day you'll get a summary of how the day went and will be able to buy upgrades.\n\n"
    )
    time.sleep(4)
    print(
        "\t\t⚠️ ⚠️ ⚠️  PLEASE NOTICE ⚠️ ⚠️ ⚠️ \nyou will NOT be able to buy more stock or change the recipe during the day. So make sure you don't give anyone diabetes and let's start!\n\n"
    )
    time.sleep(6)
    print(
       colored("Cyan text will indicate you to interact with the game.\n\n",
                'cyan'))
    time.sleep(1)
    Input("anyChoice",
          "Type anything when you're ready to start!",
          'start',
          actionsList=["StartDay()"])


#########################
### Header Animation: ###
#########################
def Header():
    for i in range(0, starLength + 1):
        reverseWelcomeLoad.pop(0)
        reverseWelcomeLoad.append("*")
        welcomeLoad.append("*")
        print(''.join(welcomeLoad))
        print(welcomeMessage)
        print(''.join(reverseWelcomeLoad))
        time.sleep(0.05)
        os.system('clear')
    index = 0
    for j in range(0, starLength + 1):
        welcomeLoad.pop(0)
        reverseWelcomeLoad[index] = " "
        index += 1
        print(''.join(welcomeLoad))
        print(welcomeMessage)
        print(''.join(reverseWelcomeLoad))
        time.sleep(0.05)
        os.system('clear')


#####################
### Game Startup: ###
#####################
def Intro():
    os.system('clear')
    Header()
    Type("This is Lemonade Stand Simulator™!")
    Type(
        "\nFor the next few days you will be selling lemonade to the people of Lem🍋nville, trying to get as much money as possible"
    )
    Type(colored("\n\nWhat's your name?", 'cyan'))
    global name
    name = input()
    Input("multipleChoice",
          "\nWould you like to see a tutorial? (y/n)",
          'y',
          'n',
          actionsList=["Tutorial()", "StartDay()"])


############################
### Developer Test Mode: ###
############################
def TestMode():
    global name, lemonDict, waterDict, sugarDict, iceDict, recipeForTheDay, lemonadeStock, lemonadePrice, weatherToday, day
    day = 1
    name = "tamar"
    weatherToday = "Sunny"
    lemonDict = {
        "Price": 0.8,
        "Stock": 40,
        "AmountPerPurchase": 10,
        "PerfectAmount": 1
    }
    waterDict = {
        "Price": 0.6,
        "Stock": 70,
        "AmountPerPurchase": 70,
        "PerfectAmount": 8
    }
    sugarDict = {
        "Price": 1.5,
        "Stock": 16,
        "AmountPerPurchase": 8,
        "PerfectAmount": 4
    }
    iceDict = {
        "Price": 1.0,
        "Stock": 96,
        "AmountPerPurchase": 16,
        "PerfectAmount": 2
    }
    lemonadePrice = 4
    lemonadeStock = 20
    recipeForTheDay = {"Lemon": 1.4, "Water": 7.5, "Sugar": 3.6, "Ice": 2}
    #Any part of the day goes here:
    RunDay()


#########################
### Running the Game: ###
#########################
Intro()

#####################
### File Closers: ###
#####################
welcomeFile.close()
shopFile.close()
recipeFile.close()
standFile.close()
summaryFile.close()