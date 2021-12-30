import pygame
import random
import time


class Game:
    width = 800
    height = 500

    stage = 'init'

    def __init__(self):
        self.window = pygame.display.set_mode((self.width, self.height))
        self.title_font = pygame.font.SysFont('arial', 75)
        self.font = pygame.font.SysFont('arial', 50)
        self.phrase_font = pygame.font.SysFont('arial', 40)

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
                            if button_rect.collidepoint(event.pos) and self.stage == 'init':
                                self.stage = 'play'
                                self.phrase = self.selectPhrase()
                                self.user_entry = ''
                                self.initial_time = time.time()
                    case pygame.KEYDOWN:
                        if self.stage == 'play':
                            match event.key:
                                case pygame.K_BACKSPACE:
                                    self.user_entry = self.user_entry[:-1]
                                case pygame.K_RETURN | pygame.K_KP_ENTER:
                                    self.stage = 'finish'
                                    self.total_time = round(time.time() - self.initial_time, 2)
                                    self.average = round(self.calcAverage(self.phrase, self.user_entry), 2)
                                case _:
                                    self.user_entry += event.unicode

            title = self.title_font.render('Speed typing test', True, (255, 255, 255))
            self.window.blit(title, (self.getCenter(title.get_rect().width), 10))

            match self.stage:
                case 'init':
                    button_rect = pygame.draw.rect(self.window, (150, 150, 150), (self.getCenter(350), 150, 350, 70))

                    button_text = self.font.render(' Click here to start ', True, (255, 255, 255))
                    self.window.blit(button_text, (self.getCenter(button_text.get_rect().width), 155))

                case 'play':
                    phrases = self.formatPhrase(self.phrase)

                    phrase_n = 0
                    for p in phrases:
                        text = self.phrase_font.render(p, True, (255, 255, 0))
                        self.window.blit(text, (self.getCenter(text.get_rect().width), 155 + phrase_n * 50))

                        phrase_n += 1

                    entry_formatted = self.formatPhrase(self.user_entry)

                    entry_n = phrase_n + 1
                    for entry in entry_formatted:
                        entry = self.phrase_font.render(entry, True, (0, 0, 255))
                        self.window.blit(entry, (self.getCenter(entry.get_rect().width), 155 + entry_n * 50))

                        entry_n += 1

                case 'finish':
                    statistics = self.font.render('Statistics', True, (255, 0, 255))
                    self.window.blit(statistics, (self.getCenter(statistics.get_rect().width), 155))

                    statistics_time = self.font.render(f'Time: {self.total_time}', True, (50, 50, 255))
                    self.window.blit(statistics_time, (self.getCenterOfMiddle(statistics_time.get_rect().width), 255))

                    average = self.font.render(f'Hit average: {self.average}%', True, ((255, 0, 0) if self.average < 80 else (0, 255, 0)))
                    self.window.blit(average, (self.getCenterOfMiddle(average.get_rect().width) + self.width / 2, 255))

            pygame.display.update()

    getCenter = lambda self, x: (self.width - x) / 2

    getCenterOfMiddle = lambda self, x: (self.width / 2 - x) / 2

    def formatPhrase(self, p: str):
        '''
        Format phrase width to show

        params:
        p: phrase
        '''
        words = p.split()

        phrases = []
        n = 0
        width_used = 0
        for word in words:
            word_size = self.phrase_font.size(f'{word} ')[0]
            if word_size + width_used < self.width:
                if width_used == 0:
                    phrases.append(word)
                else:
                    phrases[n] += f' {word}'
                width_used += word_size
            else:
                phrases.append(word)
                n += 1
                width_used = word_size
        
        return phrases

    def selectPhrase(self, l: str = 'en'):
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


if __name__ == "__main__":
    pygame.init()
    Game()
