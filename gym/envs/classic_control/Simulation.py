import pygame
import maps
from pygame.locals import *
import math
import numpy as np
from random import randint
import camera
import roborange
import holes
import path
import sensors
import gym
from gym import spaces

PATH = False



class Simulation(gym.Env):
    def __init__(self):
        metadata = {'render.modes': ['human']}
        pygame.init()

        self.action_space = spaces.Discrete(5)
        low = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        high = np.array([4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000,
                         4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000,
                         4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000,
                         4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000,
                         4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000,
                         4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000,
                         4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000,
                         4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000,
                         4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000,
                         4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000,
                         4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000,
                         4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000])

        self.observation_space = spaces.Box(low, high, dtype=np.float32)

        self.score = 0
        self.stepscore = 0
        self.stepcount = 0
        self.holescore = 10

        self.map_s = pygame.sprite.Group()
        if PATH:
            self.path_s = pygame.sprite.Group()
        self.hole_s = pygame.sprite.Group()
        self.range_s = pygame.sprite.Group()
        self.sensor_s = pygame.sprite.Group()
        self.drill = 0

        self.screen = pygame.display.set_mode((1800, 1000))


        self.clock = pygame.time.Clock()
        self.CENTER_X = int(pygame.display.Info().current_w / 2)
        self.CENTER_Y = int(pygame.display.Info().current_h / 2)
        self.running = True

        self.cam = camera.Camera()
        self.robrange = roborange.RoRange()
        self.current_map = maps.Map()
        if PATH:
            self.path = path.Path()
        self.delta = 10

        # create new holes
        # create new holes
        hole0 = holes.Holes(927, 664)
        hole0.add(self.hole_s)
        hole1 = holes.Holes(1755, 706)
        hole1.add(self.hole_s)
        hole2 = holes.Holes(2431, 377)
        hole2.add(self.hole_s)
        hole3 = holes.Holes(3614, 829)
        hole3.add(self.hole_s)
        hole4 = holes.Holes(1849, 937)
        hole4.add(self.hole_s)
        hole5 = holes.Holes(2092, 1047)
        hole5.add(self.hole_s)
        hole6 = holes.Holes(1432, 1189)
        hole6.add(self.hole_s)
        hole7 = holes.Holes(1775, 986)
        hole7.add(self.hole_s)
        hole8 = holes.Holes(2977, 693)
        hole8.add(self.hole_s)
        hole9 = holes.Holes(885, 554)
        hole9.add(self.hole_s)
        hole10 = holes.Holes(3123, 1100)
        hole10.add(self.hole_s)
        hole11 = holes.Holes(1306, 1293)
        hole11.add(self.hole_s)
        hole12 = holes.Holes(2610, 518)
        hole12.add(self.hole_s)
        hole13 = holes.Holes(3448, 588)
        hole13.add(self.hole_s)
        hole14 = holes.Holes(3235, 1104)
        hole14.add(self.hole_s)
        hole15 = holes.Holes(3307, 1277)
        hole15.add(self.hole_s)
        hole16 = holes.Holes(1853, 881)
        hole16.add(self.hole_s)
        hole17 = holes.Holes(3375, 1260)
        hole17.add(self.hole_s)
        hole18 = holes.Holes(1576, 304)
        hole18.add(self.hole_s)
        hole19 = holes.Holes(1448, 1019)
        hole19.add(self.hole_s)
        hole20 = holes.Holes(2452, 517)
        hole20.add(self.hole_s)
        hole21 = holes.Holes(1066, 1226)
        hole21.add(self.hole_s)
        hole22 = holes.Holes(2484, 1329)
        hole22.add(self.hole_s)
        hole23 = holes.Holes(1109, 1169)
        hole23.add(self.hole_s)
        hole24 = holes.Holes(3345, 1343)
        hole24.add(self.hole_s)
        hole25 = holes.Holes(1224, 381)
        hole25.add(self.hole_s)
        hole26 = holes.Holes(3255, 336)
        hole26.add(self.hole_s)
        hole27 = holes.Holes(2389, 831)
        hole27.add(self.hole_s)
        hole28 = holes.Holes(3071, 212)
        hole28.add(self.hole_s)
        hole29 = holes.Holes(2185, 626)
        hole29.add(self.hole_s)
        hole30 = holes.Holes(3620, 332)
        hole30.add(self.hole_s)
        hole31 = holes.Holes(3669, 1063)
        hole31.add(self.hole_s)
        hole32 = holes.Holes(3381, 394)
        hole32.add(self.hole_s)
        hole33 = holes.Holes(3081, 924)
        hole33.add(self.hole_s)
        hole34 = holes.Holes(2373, 657)
        hole34.add(self.hole_s)
        hole35 = holes.Holes(995, 1490)
        hole35.add(self.hole_s)
        hole36 = holes.Holes(2516, 1225)
        hole36.add(self.hole_s)
        hole37 = holes.Holes(2154, 579)
        hole37.add(self.hole_s)
        hole38 = holes.Holes(2435, 562)
        hole38.add(self.hole_s)
        hole39 = holes.Holes(1207, 476)
        hole39.add(self.hole_s)

        # create list of hole coordinates and IR´s
        self.holestate = []
        for hole in self.hole_s:
            dist_x = hole.x - self.robrange.x
            dist_y = hole.y - self.robrange.y
            self.holestate.append(dist_x)
            self.holestate.append(dist_y)
            self.holestate.append(hole.IR)

        # create observation state array
        self.state = np.array(self.holestate)

        self.map_s.add(self.current_map)
        self.range_s.add(self.robrange)
        if PATH:
            self.path_s.add(self.path)
        pygame.display.set_caption('RoboSimAI')
        pygame.mouse.set_visible(True)
        self.font = pygame.font.Font(None, 24)

        self.background = pygame.Surface(self.screen.get_size())

        self.background.fill((210, 210, 250))

    def step(self, action):
        # action[0] in range -1, 1: speed
        # action[1] in range -1, 1: steering
        # action[2] in range -1, 1: drill

        self.stepscore = 0
        self.stepcount += 1
        self.holestate = []

        holes_in_range = self.check_collision(self.robrange, self.hole_s, False)
        if holes_in_range:
            for hole in self.hole_s.sprites():
                for hole_IR in holes_in_range:
                    if hole == hole_IR:
                        hole.IR = 4000
                    else:
                        hole.IR = 0
                dist_x = hole.x - self.robrange.x
                dist_y = hole.y - self.robrange.y
                self.holestate.append(dist_x)
                self.holestate.append(dist_y)
                self.holestate.append(hole.IR)
        else:
            for hole in self.hole_s.sprites():
                dist_x = hole.x - self.robrange.x
                dist_y = hole.y - self.robrange.y
                self.holestate.append(dist_x)
                self.holestate.append(dist_y)
                self.holestate.append(0)

        len_holelist = len(self.holestate)
        append_length = 120 - len_holelist

        if action == 0:
            #up
            self.robrange.update(0, -self.delta)
            self.stepscore -= 0.1
        elif action == 1:
            # down
            self.robrange.update(0, self.delta)
            self.stepscore -= 0.1
        elif action == 2:
            # left
            self.delta_x = -10
            self.delta_y = 0
            self.robrange.update(-self.delta, 0)
            self.stepscore -= 0.1
        elif action == 3:
            # right
            self.delta_x = 10
            self.delta_y = 0
            self.robrange.update(self.delta, 0)
            self.stepscore -= 0.1
        elif action == 4:
            # drill
            for hole in holes_in_range:
                self.hole_s.remove(hole)
            self.stepscore += len(holes_in_range) * self.holescore
            self.stepscore -= 3

        if PATH:
            self.path_s.update(self.cam.x, self.cam.y)
        self.hole_s.update(self.cam.x, self.cam.y)
        self.map_s.update(self.cam.x, self.cam.y)
        self.cam.set_pos(self.robrange.x, self.robrange.y)

        self.score += self.stepscore
        append_length = int(append_length / 3)

        if append_length == 0:
            self.state = np.array(self.holestate)
        else:
            listof0 = [0, 0, 0] * append_length
            holearray = np.array(self.holestate)
            zeroarray = np.array(listof0)
            self.state = np.array(holearray)
            self.state = np.append(self.state, zeroarray)

        #render #######################################################
        pygame.event.pump()
        # Show text data.
        text_fps = self.font.render('FPS: ' + str(int(self.clock.get_fps())), 1, (255, 127, 0))
        textpos_fps = text_fps.get_rect(centery=25, centerx=60)
        text_score = self.font.render("Score: " + str(self.score), 1, (255, 127, 0))
        textpos_score = text_score.get_rect(centery=50, centerx=160)

        self.screen.blit(self.background, (0, 0))
        if PATH:
            self.path.image.fill((255, 127, 0), Rect(self.robrange.x, self.robrange.y, 5, 5))
            self.path_s.draw(self.screen)

        self.range_s.draw(self.screen)
        self.map_s.draw(self.screen)
        self.hole_s.draw(self.screen)

        self.screen.blit(text_fps, textpos_fps)
        self.screen.blit(text_score, textpos_score)

        pygame.display.update()
        self.clock.tick(120)
        ###end render #################################
        done = 0
        if self.score < -500:
            done = 1
        if self.stepcount > 1500:
            done = 1
        if not self.hole_s.sprites():
            done = 1

        return self.state, self.stepscore, done, {}

    def reset(self):
        self.stepscore = 0
        self.score = 0
        self.stepcount = 0
        self.holestate = []


        if PATH:
            self.path.reset()
        self.score = 0
        self.robrange.reset()
        # reset sensor values
        for r in self.sensor_s:
            r.delta = 700
        # create new holes
        self.hole_s.empty()
        # create new holes
        hole0 = holes.Holes(527, 364)
        hole0.add(self.hole_s)
        hole1 = holes.Holes(1755, 706)
        hole1.add(self.hole_s)
        hole2 = holes.Holes(2431, 377)
        hole2.add(self.hole_s)
        hole3 = holes.Holes(3614, 829)
        hole3.add(self.hole_s)
        hole4 = holes.Holes(1849, 437)
        hole4.add(self.hole_s)
        hole5 = holes.Holes(2092, 1047)
        hole5.add(self.hole_s)
        hole6 = holes.Holes(1432, 1189)
        hole6.add(self.hole_s)
        hole7 = holes.Holes(1775, 986)
        hole7.add(self.hole_s)
        hole8 = holes.Holes(2977, 393)
        hole8.add(self.hole_s)
        hole9 = holes.Holes(885, 554)
        hole9.add(self.hole_s)
        hole10 = holes.Holes(3123, 1100)
        hole10.add(self.hole_s)
        hole11 = holes.Holes(1306, 1293)
        hole11.add(self.hole_s)
        hole12 = holes.Holes(2610, 218)
        hole12.add(self.hole_s)
        hole13 = holes.Holes(3448, 588)
        hole13.add(self.hole_s)
        hole14 = holes.Holes(3635, 1104)
        hole14.add(self.hole_s)
        hole15 = holes.Holes(3307, 1277)
        hole15.add(self.hole_s)
        hole16 = holes.Holes(1853, 881)
        hole16.add(self.hole_s)
        hole17 = holes.Holes(3375, 1260)
        hole17.add(self.hole_s)
        hole18 = holes.Holes(1576, 304)
        hole18.add(self.hole_s)
        hole19 = holes.Holes(1448, 1019)
        hole19.add(self.hole_s)
        hole20 = holes.Holes(2452, 517)
        hole20.add(self.hole_s)
        hole21 = holes.Holes(1066, 1226)
        hole21.add(self.hole_s)
        hole22 = holes.Holes(2484, 1329)
        hole22.add(self.hole_s)
        hole23 = holes.Holes(1109, 1169)
        hole23.add(self.hole_s)
        hole24 = holes.Holes(3345, 1343)
        hole24.add(self.hole_s)
        hole25 = holes.Holes(1224, 381)
        hole25.add(self.hole_s)
        hole26 = holes.Holes(3455, 336)
        hole26.add(self.hole_s)
        hole27 = holes.Holes(2389, 831)
        hole27.add(self.hole_s)
        hole28 = holes.Holes(3071, 212)
        hole28.add(self.hole_s)
        hole29 = holes.Holes(2185, 626)
        hole29.add(self.hole_s)
        hole30 = holes.Holes(3620, 332)
        hole30.add(self.hole_s)
        hole31 = holes.Holes(3669, 1063)
        hole31.add(self.hole_s)
        hole32 = holes.Holes(3381, 394)
        hole32.add(self.hole_s)
        hole33 = holes.Holes(3081, 924)
        hole33.add(self.hole_s)
        hole34 = holes.Holes(2373, 657)
        hole34.add(self.hole_s)
        hole35 = holes.Holes(995, 1490)
        hole35.add(self.hole_s)
        hole36 = holes.Holes(2516, 1225)
        hole36.add(self.hole_s)
        hole37 = holes.Holes(2154, 579)
        hole37.add(self.hole_s)
        hole38 = holes.Holes(2435, 562)
        hole38.add(self.hole_s)
        hole39 = holes.Holes(1207, 476)
        hole39.add(self.hole_s)

        # create list of hole coordinates and IR´s

        for hole in self.hole_s:
            dist_x = hole.x - self.robrange.x
            dist_y = hole.y - self.robrange.y
            self.holestate.append(dist_x)
            self.holestate.append(dist_y)
            self.holestate.append(hole.IR)

        # create observation state array
        self.state = np.array(self.holestate)

        return self.state

    def render(self, mode='human'):
        pass

    def check_collision(self, sprite, sprite_group, dokill=False):
        spritelist = pygame.sprite.spritecollide(sprite, sprite_group, dokill, pygame.sprite.collide_mask)
        if spritelist:
            return spritelist
        else:
            return []
