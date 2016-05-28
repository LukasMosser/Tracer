import pygame
import screen, event_loop

def main():
    pygame.init()

    canvas = screen.Screen()

    loop = event_loop.EventLoop(canvas)

    loop.start()

if __name__ == "__main__":
    main()



