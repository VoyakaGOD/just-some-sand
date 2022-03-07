import pygame as pg

class App:
    def __init__(self):
        self.screen = pg.display.set_mode((512, 512))
        self.clock = pg.time.Clock()
        pg.display.set_caption('just some sand')

    def run(self):
        isRunning = True
        while isRunning:
            for i in pg.event.get():
                if i.type == pg.QUIT:
                    isRunning = False
            self.clock.tick(60)
        pg.quit()
            

if __name__ == '__main__':
    app = App()
    app.run()
