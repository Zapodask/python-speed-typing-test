import time
import random


def calcAverage(p: str, u: str):
    """
    Calculate average

    param:
    p: phrase
    r: user phrase
    """
    pl = len(p)

    correct = 0

    i = 0
    while i < pl and i < len(u):
        if p[i] == u[i]:
            correct += 1

        i += 1

    return (correct / pl) * 100


def selectPhrase(l: str):
    """
    Select random phrase

    params:
    l: language
    """
    lan = l if l == "br" else "en"

    with open(f"phrases-{lan}.txt", "r", encoding="utf-8") as f:
        phrases_list = f.read()

    phrase = random.choice(phrases_list.split("\n"))

    return phrase


language = input("Select language(en/br):")

phrase = selectPhrase(language)

input("Press enter to start")

print(phrase)

start_time = time.time()

res = input()

end_time = time.time()


print(f"Time: {round(end_time - start_time, 2)}, Average: {calcAverage(phrase, res)}%")
