import pygame
import random
import time

class Game:
    width = 800
    height = 500

    init_button = language_button = again_button = None

    language = "en"
    fields_en = {
            "language": "en",
            "title": "Speed typing test",
            "init_button": "Click here to start",
            "language_button": "Change language",
            "statistics": "Statistics",
            "time": "Time",
            "average": "Hit average",
            "again": "Play again",
        }
    fields_br = {
            "language": "br", 
            "title": "Teste de digitação",
            "init_button": "Clique para iniciar",
            "language_button": "Trocar idioma",
            "statistics": "Estatísticas",
            "time": "Tempo",
            "average": "Média",
            "again": "Jogar novamente",
        }
    fields = fields_en

    stage = "init"

    def __init__(self):
        self.window = pygame.display.set_mode((self.width, self.height))
        self.font = pygame.font.SysFont("arial", 50)
        self.phrase_font = pygame.font.SysFont("arial", 40)

        self.main()

    def main(self):
        while True:
            self.window.fill((0, 0, 0))

            for event in pygame.event.get():
                match event.type:
                    case pygame.QUIT:
                        pygame.quit()
                        quit()

                    case pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            if self.stage == "init":
                                if self.init_button and self.init_button.collidepoint(event.pos):
                                    self.stage = "countdown"
                                    self.countdown_i = 3

                                    self.phrase = self.selectPhrase(self.language)
                                    self.user_entry = ""

                                    self.initial_time = time.time() + 3
                                
                                if self.language_button and self.language_button.collidepoint(event.pos):
                                    if self.language == "en":
                                        self.language = "br"

                                        self.fields = self.fields_br

                                    else:
                                        self.language = "en"

                                        self.fields = self.fields_en
                                    
                                    self.fields

                            if self.again_button and self.again_button.collidepoint(event.pos) and self.stage == "finish":
                                self.stage = "init"

                    case pygame.KEYDOWN:
                        if self.stage == "play":
                            match event.key:
                                case pygame.K_BACKSPACE:
                                    self.user_entry = self.user_entry[:-1]

                                case pygame.K_RETURN | pygame.K_KP_ENTER:
                                    self.stage = "finish"
                                    self.total_time = round(time.time() - self.initial_time, 2)
                                    self.average = round(self.calcAverage(self.phrase, self.user_entry), 2)

                                case pygame.K_ESCAPE | 126:
                                    pass

                                case _:
                                    self.user_entry += event.unicode

            self.text(self.fields.get('title'), (255, 255, 255), "center", 10, 70)

            match self.stage:
                case "init":
                    self.init_button = self.button(self.fields.get('init_button'), (255, 255, 255), "center", 155)

                    self.text("English" if self.language == "en" else "Português", (255, 255, 255), "right", 350, 50)
                    self.language_button = self.button(self.fields.get('language_button'), (255, 255, 255), "right", 420)

                case "countdown":
                    self.text(str(self.countdown_i), (255, 255, 255), "center", 175, 100)

                    time.sleep(1) if self.countdown_i != 3 else None

                    if self.countdown_i == 0:
                        self.stage = "play"

                    self.countdown_i -= 1

                case "play":
                    phrases = self.formatPhrase(self.phrase)

                    phrase_n = 0
                    for p in phrases:
                        self.text(p, (255, 255, 0), "center", 155 + phrase_n * 50, 40)

                        phrase_n += 1

                    entry_formatted = self.formatPhrase(self.user_entry)

                    entry_n = phrase_n + 1
                    for entry in entry_formatted:
                        self.text(entry, (0, 0, 255), "center", 155 + entry_n * 50, 40)

                        entry_n += 1

                case "finish":
                    self.text(self.fields.get('statistics'), (255, 0, 255), "center", 140, 60)

                    self.text(f"{self.fields.get('time')}: {self.total_time}", (50, 50, 255), "left", 255, 50)
                    
                    self.text(f"{self.fields.get('average')}: {self.average}%", ((255, 0, 0) if self.average < 80 else (0, 255, 0)), "right", 255, 50)

                    self.again_button = self.button(self.fields.get('again'), (255, 255, 255), "center", 350)

            pygame.display.update()

    getCenter = lambda self, x: (self.width - x) / 2

    getFourth = lambda self, x: (self.width / 2 - x) / 2

    def formatPhrase(self, p: str):
        """
        Format phrase width to show

        params:
        p: phrase
        """
        words = p.split()

        phrases = []
        n = 0
        width_used = 0
        for word in words:
            word_size = self.phrase_font.size(f"{word} ")[0]
            if word_size + width_used < self.width:
                if width_used == 0:
                    phrases.append(word)
                else:
                    phrases[n] += f" {word}"
                width_used += word_size
            else:
                phrases.append(word)
                n += 1
                width_used = word_size
        
        return phrases

    def selectPhrase(self, l: str = "en"):
        """
        Select random phrase

        params:
        l: language
        """
        with open(f"phrases-{l}.txt", "r", encoding="utf-8") as f:
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

    def definePosition(self, x: int | str, w: int):
        """
        Define position in X 
        
        params:
        x: x axis = int | "center" | "left" | "right"
        w: width
        """
        match x:
            case "center":
                return self.getCenter(w)
            case "left":
                return self.getFourth(w)
            case "right":
                return self.getFourth(w) + self.width / 2
            case _:
                return x

    def button(self, t: str, c: tuple, x: int | str, y: int):
        """
        Make a button

        params:
        t: text
        c: color
        x: x axis = int | "center" | "left" | "right"
        y: y axis
        s: size = "small" | "large"
        """
        button_text = self.font.render(f"  {t}  ", True, c)

        button_width, button_height = button_text.get_size()
        
        x = self.definePosition(x, button_width)
        
        button_rect = pygame.draw.rect(self.window, (150, 150, 150), (x, y, button_width, button_height + 5), border_radius = 7)

        self.window.blit(button_text, (x, y))

        return button_rect

    def text(self, t: str, c: tuple, x: int | str, y: int, f: int):
        """
        Make a text

        params:
        t: text
        c: color
        x: x axis = int | "center" | "left" | "right"
        y: y axis
        f: font size
        """
        text_font = pygame.font.SysFont("arial", f)

        text = text_font.render(t, True, c)

        x = self.definePosition(x, text.get_rect().width)

        self.window.blit(text, (x, y))

        return text

if __name__ == "__main__":
    pygame.init()

    Game()
