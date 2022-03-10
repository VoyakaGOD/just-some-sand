from game import *

class App:
    def __init__(self):
        self.screen = pg.display.set_mode((GAME_SCALE*GAME_WIDTH, GAME_SCALE*GAME_HEIGHT))
        self.clock = pg.time.Clock()
        pg.display.set_caption('just some sand')

    def run(self):
        isRunning = True
        isMBPressed = False
        game = Game(self.screen)
        brushId = 1
        brushSize = 3
        while isRunning:
            pg.display.set_caption('just some sand' + str(self.clock.get_fps())) ##########
            game.Update()
            if isMBPressed:
                mp = pg.mouse.get_pos()
                game.UseBrush(mp[0] // GAME_SCALE, mp[1] // GAME_SCALE, brushId, brushSize)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    isRunning = False
                elif event.type == pg.MOUSEBUTTONDOWN:
                    isMBPressed = True
                elif event.type == pg.MOUSEBUTTONUP:
                    isMBPressed = False
                elif event.type == pg.KEYDOWN:
                    if event.key >= pg.K_0 and event.key <= pg.K_4:
                        brushId = event.key - pg.K_0
                        print(ELEMENTS[brushId].name)
                elif event.type == pg.MOUSEWHEEL:
                    brushSize += event.y
                    if brushSize < 0:
                        brushSize = 0
                    elif brushSize > MAX_BRUSH_SIZE:
                        brushSize = MAX_BRUSH_SIZE
            self.clock.tick(60)
        pg.quit()

if __name__ == '__main__':
    app = App()
    app.run()
