import copy
import random
import requests
import discord
from discord.ext import commands

client = commands.Bot(command_prefix=".", intents=discord.Intents.all())


@client.event
async def on_ready():
    print("im up!")


@client.command(aliases=["Hi", "hey", "Hey", "hello", "Hello"])
async def hi(ctx):
    l = ["Hi!", "Hey!", "Hello!", "Hello wassup!"]
    await ctx.send(random.choice(l))


@client.command()
async def calculate(ctx, *, eq):
    try:
        await ctx.send("Answer for the above is: " + str(eval(eq)))
    except:
        await ctx.send("Invalid equation.")


@client.command()
async def show(ctx, *, val):
    title = val
    val = val.replace(" ", "+")
    response = requests.get(
        "https://pixabay.com/api/?key=31876472-e4df35a71df0d46708a04d8eb&q={}&image_type=photo&pretty=true".format(val))
    json = response.json()
    if len(json["hits"]) > 0:
        imgUrl = random.choice(json["hits"])["largeImageURL"]
        embed = discord.Embed(title=title.capitalize(), colour=discord.Colour.green())
        embed.set_image(url=imgUrl)
        await ctx.send(embed=embed)
    else:
        await ctx.send("No image found.")

@client.command()
async def tictactoe(ctx):
    import random
    import copy
    class Point:
        def __init__(self, x):
            self.x = x

        def isCorner(self):
            return self.x % 2 != 0 and self.x != 5

        def isMiddle(self):
            return self.x % 2 == 0

        def isCenter(self):
            return self.x == 5

        def isFilled(self):
            return board[d[self.x][0]][d[self.x][1]] == "X" or board[d[self.x][0]][d[self.x][1]] == "O"

        def oppesite(self):
            opp = {1: 9, 2: 8, 3: 7, 4: 6, 5: 5, 6: 4, 7: 3, 8: 2, 9: 1}
            return opp[self.x]

    placesFiled = []
    board = [["-", "-", "-"], ["-", "-", "-"], ["-", "-", "-"]]
    d = {1: [0, 0], 2: [0, 1], 3: [0, 2], 4: [1, 0], 5: [1, 1], 6: [1, 2], 7: [2, 0], 8: [2, 1], 9: [2, 2]}
    # X -> ai
    # O -> human
    ai = ["X", "X"]
    human = ["O", "O"]

    def makeBoardEmpty():
        for i in range(3):
            for j in range(3):
                board[i][j] = "-"
        placesFiled.clear()

    def boardFull():
        for i in range(1, 10):
            if (not Point(i).isFilled()):
                return False
        return True

    def winning(L):
        pos = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        winningPos = [pos[0], pos[1], pos[2],
                      [pos[0][0], pos[1][0], pos[2][0]],
                      [pos[0][1], pos[1][1], pos[2][1]],
                      [pos[0][2], pos[1][2], pos[2][2]],
                      [pos[0][0], pos[1][1], pos[2][2]],
                      [pos[0][2], pos[1][1], pos[2][0]]]
        winningWays = [board[0], board[1], board[2],
                       [board[0][0], board[1][0], board[2][0]],
                       [board[0][1], board[1][1], board[2][1]],
                       [board[0][2], board[1][2], board[2][2]],
                       [board[0][0], board[1][1], board[2][2]],
                       [board[0][2], board[1][1], board[2][0]]]

        def win(l1, l2):
            original = copy.copy(l1)

            def removeCommonEle(l1, l2):
                for i in l2:
                    if (i in l1):
                        l1.remove(i)

            removeCommonEle(l1, l2)
            if (len(l1) == 1 and (l1[0] != "X" and l1[0] != "O")):
                return original.index(l1[0])
            else:
                return -1

        for i in winningWays:
            i2 = copy.copy(i)
            i3 = copy.copy(i)
            x = win(i2, L)
            # print(x)
            if (x != -1):
                return (winningPos[winningWays.index(i3)][x])

    async def setInput(x, XorO):
        if (Point(x).isFilled()):
            # print("Invalid Input", str(x), board, placesFiled)
            await ctx.send("That place is already filled. Choose another position.")
            await takeInput()
        else:
            board[d[x][0]][d[x][1]] = XorO
            placesFiled.append(x)

    async def printBoard():
        embed = discord.Embed(
            description="{}\u2001|\u2001{}\u2001|\u2001{}\n{}\u2001|\u2001{}\u2001|\u2001{}\n{}\u2001|\u2001{}\u2001|\u2001{}".format(
                str(board[0][0]), str(board[0][1]), str(board[0][2]), str(board[1][0]), str(board[1][1]),
                str(board[1][2]), str(board[2][0]), str(board[2][1]), str(board[2][2])), colour=discord.Colour.green())
        await ctx.send(embed=embed)

    async def takeInput():
        # x = int(input("Enter number: "))
        def check(m):
            return m.author.id == ctx.author.id
        await ctx.send("Enter position where u wanna perform ur move")
        msg = await client.wait_for("message", check=check)
        x = int(msg.content)
        if(x<1 or x>9):
            await ctx.send("Invalid Input.")
            await takeInput()
        else:
            await setInput(x, "O")
            return Point(x)

    def removeCommonEle(l1, l2):
        for i in l2:
            if (i in l1):
                l1.remove(i)

    async def aiInput(s):
        i = 0
        if (s == "mid"):
            useable = [2, 4, 6, 8]
            removeCommonEle(useable, placesFiled)
            i = random.randint(0, len(useable) - 1)
            await setInput(useable[i], "X")
            return Point(useable[i])
        elif (s == "cor"):
            useable = [1, 3, 7, 9]
            removeCommonEle(useable, placesFiled)
            i = random.randint(0, len(useable) - 1)
            await setInput(useable[i], "X")
            return Point(useable[i])
        elif (s == "ran"):
            for i in range(1, 10):
                if (not Point(i).isFilled()):
                    await setInput(i, "X")
                    return Point(i)
        elif (s == "cen"):
            i = 5
            if (not Point(i).isFilled()):
                await setInput(i, "X")
                return Point(i)
            else:
                print("center filled, ai cant input there")
        return Point(i)

    async def aiManualInput(x):
        await setInput(x, "X")

    async def aiAdjecentFill(x):
        adjecents = {2: [1, 3], 4: [1, 7], 6: [3, 9], 8: [7, 9], 1: [2, 4], 3: [2, 6], 7: [4, 8], 9: [8, 6]}
        i = random.randint(0, 1)
        while adjecents[x][i] in placesFiled:
            i = random.randint(0, 1)
        await aiManualInput(adjecents[x][i])

    def canWin(somebody):
        return winning(somebody) != None and winning(somebody) != -1

    def aiWon():
        winningWays = [board[0], board[1], board[2],
                       [board[0][0], board[1][0], board[2][0]],
                       [board[0][1], board[1][1], board[2][1]],
                       [board[0][2], board[1][2], board[2][2]],
                       [board[0][0], board[1][1], board[2][2]],
                       [board[0][2], board[1][1], board[2][0]]]
        return ["X", "X", "X"] in winningWays

    def humanWon():
        winningWays = [board[0], board[1], board[2],
                       [board[0][0], board[1][0], board[2][0]],
                       [board[0][1], board[1][1], board[2][1]],
                       [board[0][2], board[1][2], board[2][2]],
                       [board[0][0], board[1][1], board[2][2]],
                       [board[0][2], board[1][1], board[2][0]]]
        return ["O", "O", "O"] in winningWays

    async def fillBoard():
        async def again():
            await ctx.send("Wanna play again? (y/n) ")

            def check(m):
                return m.author.id == ctx.author.id

            yesOrNo = await client.wait_for("message", check=check)
            if (yesOrNo.content.lower() == "y"):
                makeBoardEmpty()
                await ctx.send("do u wanna go first? (y/n) ")

                def check(m):
                    return m.author.id == ctx.author.id

                yesOrNo = await client.wait_for("message", check=check)
                await play(yesOrNo.content)
            elif (yesOrNo.content.lower() == "n"):
                await ctx.send("Okay np!😊")
            else:
                await ctx.send("Invalid input.")
                await again()

        while (not boardFull()) and (not aiWon()) and (not humanWon()):
            await ctx.send("My turn:")
            if (canWin(ai)):
                await aiManualInput(winning(ai))
            elif (canWin(human)):
                await aiManualInput(winning(human))
            elif (not Point(1).isFilled() or not Point(3).isFilled() or not Point(7).isFilled() or not Point(
                    9).isFilled()):
                await aiInput("cor")
            else:
                await aiInput("ran")
            await printBoard()
            if (boardFull() or aiWon() or humanWon()):
                break
            await takeInput()
            await printBoard()
        if (boardFull() and (not aiWon()) and (not humanWon())):
            await ctx.send("Its a DRAW!")
            await again()
        elif aiWon():
            await ctx.send("U played well but Im better😉")
            await again()
        elif humanWon():
            await ctx.send("WOW! well played👍")
            await again()

    async def play(yn):
        if (yn in {"n", "N"}):
            await ctx.send("Empty board:")
            await printBoard()
            await ctx.send("My turn:")
            a1 = await aiInput("cor")
            await printBoard()
            p1 = await takeInput()
            await printBoard()
            if (p1.isMiddle()):
                await ctx.send("My turn:")
                a2 = await aiInput("cen")
                await printBoard()
                p2 = await takeInput()
                await printBoard()
                await fillBoard()
            elif (p1.isCorner()):
                await fillBoard()
            elif (p1.isCenter()):
                await ctx.send("My turn:")
                await aiManualInput(a1.oppesite())
                await printBoard()
                p2 = await takeInput()
                await printBoard()
                await fillBoard()
        elif (yn in {"y", "Y"}):
            await ctx.send("Empty board:")
            await printBoard()
            p1 = await takeInput()
            await printBoard()
            if (not p1.isCenter()):
                await ctx.send("My turn:")
                await aiInput("cen")
                await printBoard()
                p2 = await takeInput()
                await printBoard()
                await ctx.send("My turn:")
                await aiAdjecentFill(p2.x)
                await printBoard()
                await takeInput()
                await printBoard()
                await fillBoard()
            else:
                await fillBoard()

        else:
            # print("invalid input")
            await ctx.send("Ur inpur is invalid.")

            # play(input("do u wanna go first? (y/n) "))
            def check(m):
                return m.author.id == ctx.author.id

            await ctx.send("do u wanna go first? (y/n) ")
            msg = await client.wait_for("message", check=check)
            await play(msg.content)

    embed = discord.Embed(description="""{}\u2001|\u2001{}\u2001|\u2001{}
                {}\u2001|\u2001{}\u2001|\u2001{}
                {}\u2001|\u2001{}\u2001|\u2001{}
                These are the numbers for each position on the board which you will have to enter to perform your turn there.""".format(
        1, 2, 3, 4, 5, 6, 7, 8, 9),
                          colour=discord.Colour.green())
    await ctx.send(embed=embed)
    await ctx.send("do u wanna go first? (y/n) ")

    def check(m):
        return m.author.id == ctx.author.id

    yesOrNo = await client.wait_for("message", check=check)
    await play(yesOrNo.content)

@client.command(aliases=["stonepaperscissors"])
async def sps(ctx):
    await ctx.send("GO!")

    def check(m):
        return m.content.lower() in {"stone", "paper", "scissor"} and m.author.id == ctx.author.id

    userTurn = await client.wait_for("message", check=check)
    userTurn = userTurn.content.lower()
    compTurn = random.choice(["stone", "paper", "scissor"])
    await ctx.send(compTurn)
    if (compTurn == "stone"):
        if (userTurn == "stone"):
            await ctx.send("Its a TIE!😐")
        elif (userTurn == "paper"):
            await ctx.send("ah! u won☹")
        elif (userTurn == "scissor"):
            await ctx.send("yeahh! i won💪")
    elif (compTurn == "paper"):
        if (userTurn == "stone"):
            await ctx.send("yeahh! i won💪")
        elif (userTurn == "paper"):
            await ctx.send("Its a TIE!😐")
        elif (userTurn == "scissor"):
            await ctx.send("ah! u won☹")
    elif (compTurn == "scissor"):
        if (userTurn == "stone"):
            await ctx.send("ah! u won☹")
        elif (userTurn == "paper"):
            await ctx.send("yeahh! i won💪")
        elif (userTurn == "scissor"):
            await ctx.send("Its a TIE!😐")

@client.command()
async def flipcoin(ctx):
    headsOrTails = random.choice(["HEADS", "TAILS"])
    embed = discord.Embed(title=headsOrTails, colour=discord.Colour.green())
    if (headsOrTails == "HEADS"):
        embed.set_image(url="https://media.tenor.com/nEu74vu_sT4AAAAM/heads-coinflip.gif")
    elif (headsOrTails == "TAILS"):
        embed.set_image(url="https://media.tenor.com/kK8D7hQXX5wAAAAC/coins-tails.gif")
    await ctx.send(embed=embed)


@client.command(aliases=["Pokemon"])
async def pokemon(ctx, name):
    title = copy.copy(name.capitalize())
    name = name.lower()
    response = requests.get("https://pokeapi.co/api/v2/pokemon/{}".format(name))
    try:
        json = response.json()
        img = json["sprites"]["other"]["official-artwork"]["front_default"]
        embed = discord.Embed(title=title, colour=discord.Colour.green(), description="""Height: {}
                    Weight: {}""".format(str(json["height"] / 10) + "m", str(json["weight"] / 10) + "kg"))
        embed.set_image(url=img)
        await ctx.send(embed=embed)
    except:
        await ctx.send("Wrong pokemon name.")


@client.command()
async def quiz(ctx):
    def check(m):
        return m.author.id == ctx.author.id

    l = ["artliterature", "language", "sciencenature", "general", "fooddrink", "peopleplaces", "geography",
         "historyholidays", "entertainment", "toysgames", "music", "mathematics", "religionmythology", "sportsleisure"]
    embed1 = discord.Embed(title="Quiz Topics", description="""1. ArtLiterature
2. Language
3. ScienceNature
4. General
5. FoodDrink
6. PeoplePlaces
7. Geography
8. HistoryHolidays
9. Entertainment
10. Toysgames
11. Music
12. Mathematics
13. ReligionMythology
14. SportsLeisure""", colour=discord.Colour.green())
    await ctx.send(embed=embed1)
    await ctx.send("Enter the name or the number of the type of quiz u wanna play.")

    async def getCategory():
        msg = await client.wait_for("message", check=check)
        msg = msg.content
        if (msg.isnumeric()):
            if (int(msg) <= len(l) and int(msg) >= 1):
                return l[int(msg) - 1]
            else:
                await ctx.send("Invalid Input. Enter a valid category name or number.")
                await getCategory()
        else:
            if (msg.lower() in l):
                return msg.lower()
            else:
                await ctx.send("Invalid Input. Enter a valid category name or number.")
                await getCategory()

    category = await getCategory()
    score = 0
    await ctx.send(
        "U will be asked 5 ques based on the category u selected, with 1 point each. Lets see how much u score.")
    for i in range(1, 6):
        reponse = requests.get("https://api.api-ninjas.com/v1/trivia?category={}".format(category),
                               headers={"X-Api-Key": "zOpw8h5MQykp3n3DzVpyzQ==GX0KAObLPTCuTYL0"})
        json = reponse.json()
        # print(json)
        embed2 = discord.Embed(title="{} Quiz: Ques {}".format(category.capitalize(), i),
                               description=json[0]["question"], colour=discord.Colour.green())
        await ctx.send(embed=embed2)
        ans = await client.wait_for("message", check=check)
        if (ans.content.lower() == json[0]["answer"].lower()):
            await ctx.send("CORRECT!👏👏")
            score += 1
        else:
            await ctx.send("Incorrect answer☹")
            await ctx.send("The correct answer is {}.".format(json[0]["answer"]))

    async def again():
        await ctx.send("Wanna play again? (y/n)")
        yesOrNo = await client.wait_for("message", check=check)
        if (yesOrNo.content.lower() == "y"):
            await quiz(ctx)
        elif (yesOrNo.content.lower() == "n"):
            await ctx.send("Okay np!😊")
        else:
            await ctx.send("Invalid input.")
            await again()

    if (score >= 4):
        await ctx.send("Well played! U scored {}/5".format(score))
    elif (score == 3):
        await ctx.send("Not bad. U scored 3/5")
    else:
        await ctx.send("Nice try. u scored {}/5".format(score))
    await again()


@client.command()
async def commands(ctx):
    embed = discord.Embed(title="All Commands", colour=discord.Colour.green())
    embed.add_field(name=".hi", value="Bot greets you!")
    embed.add_field(name=".calculate <equation>", value="Gives you the answer of the equation.")
    embed.add_field(name=".show <object>", value="Shows you an image for whatever u type.")
    embed.add_field(name=".tictactoe", value="Play a game of tictactoe with the Bot, Good luck beating him🤭")
    embed.add_field(name=".sps", value="Play stone paper scissors with the bot.")
    embed.add_field(name=".flipcoin", value="Bot will flip a coin for u.")
    embed.add_field(name=".pokemon <pokemon name>", value="Bot will show you image and details of the pokemon u type.")
    embed.add_field(name=".quiz", value="Play a quiz game.")
    await ctx.send(embed=embed)


client.run("<Your Bot's Token>")
