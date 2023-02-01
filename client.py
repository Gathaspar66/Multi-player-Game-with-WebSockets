from MultiGame import configuration
from network import Network
from player import *


def read_pos(data):
    data = eval(data)
    return data


def make_pos(x, y):
    data = str({'position': (x, y)})
    return data


def draw_ball(win, ball_position):
    pygame.draw.circle(win, (255, 0, 0), ball_position, 5)


def draw_points(win, points):
    pygame.font.init()
    my_font = pygame.font.SysFont('Comic Sans MS', 30)
    text_surface = my_font.render(str(points[1]), False, (255, 255, 255))
    win.blit(text_surface, (400, 0))

    text_surface = my_font.render(str(points[0]), False, (255, 255, 255))
    win.blit(text_surface, (600, 0))


def draw_window(win, player, player2, ball_position, points):
    win.fill((0, 0, 0))
    player2.draw(win)
    player.draw(win)
    draw_points(win, points)

    draw_ball(win, ball_position)
    pygame.display.update()


def close_window():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            return run
    return True


def main():
    pygame.display.set_caption("Player client.")
    win = pygame.display.set_mode((configuration.width, configuration.height))

    network = Network()
    data = read_pos(network.getPos())

    player1 = Player(data['playerPosition'][0], data['playerPosition'][1], 10, 100, (0, 255, 0))  # create player object
    player2 = Player(0, 0, 10, 100, (255, 0, 0))  # create player object

    clock = pygame.time.Clock()

    run = True
    while run:
        clock.tick(60)

        data_recv = read_pos(network.send(make_pos(player1.x, player1.y)))  # get information from the server

        player2.x = data_recv['playerPosition'][0]  # assign the received data to the player
        player2.y = data_recv['playerPosition'][1]  # assign the received data to the player

        player2.update()  # update player data

        run = close_window()  # check if the player wants to close the window

        player1.move()

        draw_window(win, player1, player2, data_recv['ballPosition'], data_recv['points'])


main()
