import time
import random
import os


class Game:
    language_strings = {
        "en": {
            "title": "Speed typing test ",
            "start": "Press enter to start",
            "time": "Time",
            "average": "Average",
        },
        "br": {
            "title": "Teste de digitação",
            "start": "Aperte enter para iniciar",
            "time": "Tempo",
            "average": "Média de acertos",
        },
    }

    def __init__(self, language):
        phrase = self.selectPhrase(language)

        if language == "br":
            language = self.language_strings.get("br")
        else:
            language = self.language_strings.get("en")

        print(
            "=====================================================",
            "||                                                 ||",
            f"||                 {language.get('title')}              ||",
            "||                                                 ||",
            "=====================================================",
            sep="\n",
        )

        input(language.get("start"))

        print(phrase)

        start_time = time.time()

        res = input()

        end_time = time.time()

        print(
            f"{language.get('time')}: {round(end_time - start_time, 2)}, {language.get('average')}: {self.calcAverage(phrase, res)}%"
        )

    def selectPhrase(self, l: str):
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

    def calcAverage(self, p: str, u: str):
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


if __name__ == "__main__":
    language = input("Select language(en/br):")

    loop = True
    while loop:
        os.system("cls")

        Game(language)

        again = input("Play again?(y/n)")

        loop = False if again != "y" else loop
