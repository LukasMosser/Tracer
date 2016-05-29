import pygame
import character, trace
from screen import ScoreDisplay, MessageDisplay, RandomMessageDisplay
from level import Level
import numpy as np
from collections import deque
from random import choice

class EventLoop:
    def __init__(self, screen):
        self.step = 0
        self.speed = 100
        peak_num = 1
        self.screen = screen

        self.level = Level(1, self.screen)
        self.level.initial_trace()

        self.last_trace_positions = deque()
        self.last_trace_positions_x = deque()
        self.last_trace_positions_y = deque()

        self.character = character.Character(screen)

        self.reference_trace = self.level.current_trace
        self.comparison_trace = self.level.reference_trace

        self.score_disp = ScoreDisplay(self.screen)
        self.total_score_disp = ScoreDisplay(self.screen)
        self.normalized_score_disp = ScoreDisplay(self.screen)

        self.positions = [(300, 500), (200, 400), (100, 400), (200, 300)]
        self.placed = [False, False, False, False]

        self.messages = deque()

        self.perfect_disp = MessageDisplay("PERFECT!", self.screen, 400)
        self.bad_disp = MessageDisplay("Bad! :(", self.screen, 400)

        self.awesome_disp = MessageDisplay("Awesome!", self.screen, 400)
        self.on_a_roll_disp = MessageDisplay("You're on a roll!", self.screen, 400)
        self.geogod_disp = MessageDisplay("GEOGOD", self.screen, 400)

        self.random_great_disp = RandomMessageDisplay(["Great!, Awesome!", "AMAZING", "WOW", "Much Seismic", "So Geologist"], self.screen, 400)
        self.random_hype_disp = RandomMessageDisplay(["Hype!, WOAHHHH!", "ON FIAAA", "BLAZING", "GODLIKE","Much Seismic","So Geologist"], self.screen, 400)

        self.total_score = 0
        self.record_score = True
        self.normalized_score = 0.
        self.number_of_traces = 0

        self.last_scores = []

        self.new_trace_pos = -screen.height / 2
        self.trace_position = self.new_trace_pos # vertical position relative to center

        self.clock = pygame.time.Clock()

        self.done = False
        self.doge = pygame.image.load("doge.bmp")
        self.doge_rect = self.doge.get_rect()

        self.step = 1 # the number of pixels to move the comparison trace per iteration

    def start(self):
        while not self.done:
            self.run()

        pygame.quit()

    def run(self):

        self.clock.tick(self.speed)

        score = np.abs(self.trace_position)#self.reference_trace.peaks[0]
        #score = self.comparison_trace.peaks[0]-self.trace_position-self.reference_trace.peaks[0]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.level.save_json()
                self.done = True
            elif event.type == pygame.KEYDOWN and event.key in [pygame.K_q, pygame.K_ESCAPE]:
                self.done = True
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.level.interpreted_traces.append([self.level.current_trace.data, self.trace_position])

                self.last_trace_positions.append(self.trace_position)
                self.last_trace_positions_x.append(self.trace_position)
                self.last_trace_positions_y.append(self.trace_position)

                self.trace_position = self.new_trace_pos

                self.number_of_traces += 1
                self.total_score += score
                self.normalized_score = self.total_score/float(self.number_of_traces)
                self.last_scores.append(score)
                if 10 < np.mean(self.last_scores) < 20 and len(self.last_scores) == 3:
                    self.awesome_disp = RandomMessageDisplay(["Great!, Awesome!", "AMAZING", "WOW", "Much Seismic", "So Geologist"], self.screen, 400)
                    self.awesome_disp.timeout = 400*self.step
                    self.messages.append(self.awesome_disp)
                    self.step += 1
                elif 5 < np.mean(self.last_scores) < 10 and len(self.last_scores) == 3:
                    #print "increased speed", self.speed
                    self.step += 2
                    self.on_a_roll_disp = RandomMessageDisplay(["Hype!, WOAHHHH!", "ON FIAAA", "BLAZING", "GODLIKE", "Much Seismic", "So Geologist"], self.screen, 400)
                    self.on_a_roll_disp .timeout = 400*self.step
                    self.messages.append(self.on_a_roll_disp )

                elif 0 < np.mean(self.last_scores) < 5 and len(self.last_scores) == 3:
                    #print "increased speed", self.speed
                    self.step += 3
                    #self.geogod_disp.draw_message(choice(self.positions))
                    self.geogod_disp.timeout = 500*self.step
                    self.messages.append(self.geogod_disp)
                elif np.mean(self.last_scores) > 20 and len(self.last_scores) == 3:
                    self.step -= 2
                    self.bad_disp = RandomMessageDisplay(["Horrible!", "Shame *Ding*", "Have a kitten."], self.screen, 400)
                    self.bad_disp.timeout = 300*self.step
                    self.messages.append(self.bad_disp)

                    if self.step < 1:
                        self.step = 1
                else:
                    pass

                if score == 0:
                    #self.perfect_disp.position((300, 200))
                    self.perfect_disp.timeout = 300*self.step
                    self.messages.append(self.perfect_disp)

                if len(self.last_scores) == 4:
                    self.last_scores = []

                #self.level.push_next_trace()
                self.level.previous_traces.append(self.level.current_trace)
                if len(self.level.previous_traces) > 3:
                    self.level.previous_traces.popleft()
                    self.last_trace_positions_x.popleft()
                    self.last_trace_positions_y.popleft()
                    self.last_trace_positions.popleft()

        self.screen.clear()

        for message in self.messages:
            if message.timeout > 0:
                message.timeout -= self.step
                if message.position is None:
                    message.position = self.place_message()
                message.draw_message()
            else:
                pass

        self.comparison_trace.draw(0, x_offset=100, y_offset=0, color=(0, 0, 0))
        self.level.current_trace = self.level.get_next_trace()
        self.reference_trace.draw(self.trace_position, y_offset=self.trace_position, x_offset=500-self.trace_position, color=(0, 255, 0))

        if len(self.level.previous_traces) is not 0:
            for prev_trace, last_trace_x, last_trace_y, last_trace_pos in zip(self.level.previous_traces, self.last_trace_positions_x, self.last_trace_positions_y, self.last_trace_positions):
                prev_trace.draw(last_trace_x, y_offset=last_trace_y, x_offset=500-last_trace_pos, color=(0, 0, 0))
        #self.score_disp.draw_score("Current Score", score, (100, 0))
        self.total_score_disp.draw_score("Total Score", self.total_score, (100, 50))
        #self.normalized_score_disp.draw_score("Normed Score", self.normalized_score, (100, 100))
        self.character.draw()
        pygame.display.flip()
        self.trace_position += self.step
        #self.last_trace_position += self.step
        self.last_trace_positions = deque([last_pos+self.step for last_pos in self.last_trace_positions])

    def place_message(self):
        chosen = choice(self.positions)
        print chosen
        return chosen
