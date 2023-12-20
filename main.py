import pygame
import math
from sys import exit
import os


os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()  # starts and prep pygame
# VARIABLES
WIDTH = 600
HEIGHT = 600

# Givens
L1 = 60*5
L2 = 40*5
START_L1X = 0
START_L1Y = HEIGHT
SLOPE = -1
#############################################


def draw_line():  # draw the line that should be tracked
    start_x = 0
    start_y = SLOPE * start_x + (L1+L2)
    end_y = 0
    end_x = (end_y - (L1+L2)) / SLOPE
    return start_x, start_y, end_x, end_y


def get_points():  # get points on the line to be tracked (step = 0.25)

    lst = []
    i = 0
    d = 0
    x = 0
    y = 10
    while d <= 10:
        lst.append((x, y))
        x += 0.25
        y = SLOPE * x + 10
        d = math.sqrt(math.pow(x, 2)+math.pow(y, 2))
        if y < 0:
            break
    return lst


def get_angles(x, y):  # get the angles of the elbow down solution

    target = (x, y)
    l1 = 6
    l2 = 4
    d_sqr = math.pow(target[0], 2) + math.pow(target[1], 2) # X^2 + Y^2
    eqn1 = d_sqr - math.pow(l1, 2)-math.pow(l2, 2)
    eqn2 = 2*l1*l2
    sol1_q2 = math.degrees(math.acos(eqn1/eqn2))
    left = (l2*math.sin(sol1_q2 * math.pi/180))
    right = (l1+l2 * math.cos(sol1_q2 * math.pi/180))
    beta = math.atan2(left, right)
    beta = math.degrees(beta)
    if target[0] == 0:
        tan1 = 90
    else:
        tan1 = math.degrees(math.atan2(target[1], target[0]))
    sol1_q1 = tan1 - beta

    return sol1_q1, sol1_q2


def get_angles_sol2(x, y):  # get the angles of the elbow up solution

    target = (x, y)
    l1 = 6
    l2 = 4
    d_sqr = math.pow(target[0], 2) + math.pow(target[1], 2)  # X^2 + Y^2
    eqn1 = d_sqr - math.pow(l1, 2) - math.pow(l2, 2)
    eqn2 = 2 * l1 * l2
    sol1_q2 = -1 * math.degrees(math.acos(eqn1 / eqn2))
    left = (l2 * math.sin(sol1_q2 * math.pi / 180))
    right = (l1 + l2 * math.cos(sol1_q2 * math.pi / 180))
    beta = math.atan(left/right)
    beta = math.degrees(beta)
    if target[0] == 0:
        tan1 = 90
    else:
        tan1 = math.degrees(math.atan(target[1]/target[0]))
    sol1_q1 = tan1 - beta
    return sol1_q1, sol1_q2


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('IK')
Clock = pygame.time.Clock()
bg = pygame.image.load('media/bakcground3.jpg')  # insert image
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))


def main():
    i = 0
    index = 0
    line = draw_line()
    while True:

        lst = get_points()
        if i % 10 == 0 and index < len(lst):
            theta1, theta2 = get_angles(lst[index][0], lst[index][1])
            # print(theta1, theta2)
            if theta1 <= 0:
                # print(theta1, theta2)
                theta1, theta2 = get_angles_sol2(lst[index][0], lst[index][1])
                # print(theta1, theta2)
            index += 1
        Clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        line1_end = (
            START_L1X + L1 * math.cos(theta1 * math.pi / 180),
            START_L1Y - L1 * math.sin(theta1 * math.pi / 180)
        )
        line2_end = (
            line1_end[0] + L2 * math.cos((theta1 + theta2) * math.pi / 180),
            line1_end[1] - L2 * math.sin((theta1 + theta2) * math.pi / 180)
        )
        # draw
        screen.blit(bg, (0, 0))
        pygame.draw.line(screen, (255, 255, 255), (line[0], HEIGHT-line[1]), (line[2], HEIGHT-line[3]), 2)
        pygame.draw.line(screen, (153, 51, 255), (START_L1X, START_L1Y), line1_end, 4)
        pygame.draw.line(screen, (51, 51, 255), line1_end, line2_end, 4)
        pygame.draw.circle(screen, (255, 255, 255), line1_end, 15, 0)
        pygame.draw.circle(screen, (255, 255, 255), (START_L1X, START_L1Y), 25, 0)
        pygame.draw.circle(screen, (128, 128, 128), line1_end, 10, 0)
        pygame.draw.circle(screen, (128, 128, 128), (START_L1X, START_L1Y), 20, 0)
        pygame.display.update()
        #############################################
        i += 1


if __name__ == "__main__":

    main()



