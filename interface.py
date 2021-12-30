import pygame


class Game:
    width = 800
    height = 500

    def __init__(self):
        self.window = pygame.display.set_mode((self.width, self.height))
        self.font = pygame.font.SysFont('arial', 50)

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
                            if button_rect.collidepoint(event.pos):
                                print('Start game')

            title = self.font.render('Speed typing test', True, (255, 255, 255))
            self.window.blit(title, (self.getCenter(title.get_rect().width), 20))

            button_rect = pygame.draw.rect(self.window, (150, 150, 150), (self.getCenter(350), 150, 350, 70))

            button_text = self.font.render(' Click here to start ', True, (255, 255, 255))
            self.window.blit(button_text, (self.getCenter(button_text.get_rect().width), 155))

            pygame.display.update()

    getCenter = lambda self, x: (self.width - x) / 2


if __name__ == "__main__":
    pygame.init()
    Game()

