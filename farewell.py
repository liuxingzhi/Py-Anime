import pygame
import random
from typing import List, Tuple
from enum import Enum
from musicUtils import BackgroundMusic
import os
import signal
from os import path
from time import sleep
import sys

src_dir = "src"
frame_rate = 60
speed_unit = 60 / frame_rate


class Stage(Enum):
    INITIALIZING = 0
    ENTERING = 1
    STAYING = 2
    LEAVING = 3
    COMPLETED = 4
    REINITIALIZING = 5


class Section(Enum):
    PROLOGUE = 1
    BODY = 2
    EPILOGUE = 3


# SCREEN_WIDTH = 1920
# SCREEN_HEIGHT = 1080
# SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

pygame.init()
screen = pygame.display.set_mode()
pygame.display.toggle_fullscreen()
SCREEN_WIDTH, SCREEN_HEIGHT = pygame.display.get_surface().get_size()
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)


# font = pygame.font.Font('my_font.ttf', 16)
# font_size = 28
# # for s in pygame.sysfont.get_fonts():
# #     print(s)
# font_over = pygame.font.Font("XinYeYingTi.otf", font_size)
# # font_over.set_bold(True)
# line_space = font_size * 1

class Snowflake:
    def __init__(self):
        self.x = random.randrange(0, SCREEN_SIZE[0])
        self.y = random.randrange(0, SCREEN_SIZE[1])
        self.sx = random.uniform(-1 * speed_unit, 1 * speed_unit)  # x speed
        self.sy = random.uniform(2 * speed_unit, 4 * speed_unit)  # y speed
        self.r = random.randint(1, 4)

    def fly(self):
        self.x += self.sx
        self.y += self.sy
        if self.y > SCREEN_SIZE[1]:
            self.x = random.randrange(0, SCREEN_SIZE[0])
            self.y = random.randrange(-50, -10)


class SnowflakeBackground:
    def __init__(self, snowflake_num: int):
        self.snowflake_list = [Snowflake() for _ in range(snowflake_num)]

    def update(self):
        for snowflake in self.snowflake_list:
            snowflake.fly()
            pygame.draw.circle(screen, (255, 255, 255), (round(snowflake.x), round(snowflake.y)), snowflake.r)


class Poem:
    def __init__(self, filename: str, font: str, font_size: int, bold: bool, line_space_coefficient: float,
                 color: Tuple[int, int, int] = (0, 0, 0), speed: float = 2.0, stay_time: float = 10.0,
                 speed_change_rate: float = 1.0,
                 boundary_left: int = 0,
                 boundary_right: int = SCREEN_WIDTH, hanging_height = -1):
        self.font_size = font_size
        self.font_over = pygame.font.Font(font, font_size)
        self.font_over.set_bold(bold)
        self.line_space = font_size * line_space_coefficient
        self.start_pixel = SCREEN_HEIGHT
        self.fall_speed = speed * speed_unit
        self.speed_change_rate = speed_change_rate
        self.max_width = 0  # find the longest text width within a poem
        self.stage = Stage.INITIALIZING
        self.staying_time = frame_rate * stay_time
        self.boundary_left = boundary_left
        self.boundary_right = boundary_right
        self.section_width = self.boundary_right - self.boundary_left
        self.leaving_threshold = - 0.2 * SCREEN_HEIGHT
        with open(filename) as f:
            self.lyrics = [self.PoemRow(line, index, self, color) for index, line in enumerate(f.readlines(), start=1)]
        self.lines_count = len(self.lyrics)

        right_align_start = self.boundary_right - self.max_width - self.line_space
        center_align_start = self.boundary_left + (self.section_width - self.max_width) / 2
        self.start_align = right_align_start if right_align_start < center_align_start else center_align_start

        self.section_height = (self.lines_count - 1) * self.line_space + self.font_size
        if hanging_height == -1:
            if self.section_height > SCREEN_HEIGHT:
                self.hanging_height = self.line_space
            else:
                self.hanging_height = (SCREEN_HEIGHT - self.section_height) / 2 + self.font_size
        else:
            self.hanging_height = hanging_height

        self.stage = Stage.ENTERING

    def update(self):
        if self.stage == Stage.REINITIALIZING:
            for lyric in self.lyrics:
                lyric.y = self.start_pixel + lyric.rank * self.line_space
            self.staying_time = frame_rate * 10
            self.stage = Stage.ENTERING
        elif self.stage == Stage.ENTERING or self.stage == Stage.LEAVING:
            for lyric in self.lyrics:
                lyric.move()
                lyric.show()
        elif self.stage == Stage.STAYING:
            for lyric in self.lyrics:
                lyric.show()
            self.staying_time -= 1
            if self.staying_time <= 0:
                self.stage = Stage.LEAVING
        elif self.stage == Stage.COMPLETED:
            pass

    class PoemRow:
        def __init__(self, line: str, index: int, poem, color: Tuple[int, int, int]):
            self.poem = poem
            self.color = color
            self.content = line
            self.rank = index  # start from 1
            self.y = self.poem.start_pixel + self.rank * self.poem.line_space
            self.rendered = self.poem.font_over.render(self.content.replace("\n", ""), True, self.color)
            if self.rendered.get_width() > self.poem.max_width:
                self.poem.max_width = self.rendered.get_width()

        def move(self):
            assert self.poem.stage != Stage.INITIALIZING
            assert self.poem.stage != Stage.STAYING
            assert self.poem.stage != Stage.COMPLETED
            self.y -= self.poem.fall_speed

            if self.rank == self.poem.lines_count:
                # when last row appears leave the screen change to completed stage
                if self.poem.stage == Stage.LEAVING and self.y < self.poem.leaving_threshold:
                    self.poem.stage = Stage.COMPLETED
                # when last row appears on the screen change to staying stage
                elif self.poem.stage == Stage.ENTERING and self.y < SCREEN_HEIGHT - self.poem.hanging_height:
                    self.poem.stage = Stage.STAYING
                    self.poem.fall_speed *= self.poem.speed_change_rate

        def show(self):
            screen.blit(self.rendered, (self.poem.start_align, self.y))


# TODO add background for screen
background = pygame.transform.scale(pygame.image.load(path.join(src_dir, 'bg.jpg')).convert(), SCREEN_SIZE)
if __name__ == "__main__":
    # phase = Section.PROLOGUE
    clock = pygame.time.Clock()
    snowflake_background = SnowflakeBackground(250)
    chinese_poem = Poem(path.join(src_dir, "诗词.txt"), path.join(src_dir, "XinYeYingTi.otf"), 28, False, 1, speed=1.2,
                        speed_change_rate=0.7,
                        stay_time=12, boundary_left=SCREEN_WIDTH * 0.6)
    english_poem = Poem(path.join(src_dir, "lyrics.txt"), path.join(src_dir, "my_font.ttf"), 24, False, 1.2, speed=1.2,
                        speed_change_rate=0.7,
                        stay_time=8, boundary_left=SCREEN_WIDTH * 0.6)
    ack = Poem(path.join(src_dir, "author十八年.txt"), path.join(src_dir, "XinYeYingTi.otf"), 66, False, 1,
               speed_change_rate=1.0,
               stay_time=0, color=(255, 255, 255), speed=4)
    code = Poem("farewell.py", path.join(src_dir, "Courier_New_Bold.ttf"), 24, False, 1, speed_change_rate=1.0,
                stay_time=0, color=(255, 255, 255), speed=8)
    finale_background = pygame.Surface(SCREEN_SIZE)
    finale_background.fill((0, 0, 0))
    with BackgroundMusic(path.join(src_dir, "卷珠帘琵琶吉他.mp3"), loop=1, forever=False):
        phase = Section.BODY
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                        # pygame.quit()
                        os.kill(os.getpid(), signal.SIGKILL)
                        exit(0)
                    if event.key == pygame.K_r:
                        chinese_poem.stage = Stage.REINITIALIZING
                        english_poem.stage = Stage.REINITIALIZING
                if event.type == pygame.QUIT:
                    pygame.quit()
                    os.kill(os.getpid(), signal.SIGKILL)
                    exit(0)
            # TODO show background
            if phase == Section.BODY:
                screen.blit(background, (0, 0))
                snowflake_background.update()
                if chinese_poem.stage != Stage.COMPLETED:
                    chinese_poem.update()
                elif english_poem.stage != Stage.COMPLETED:
                    english_poem.update()
                else:
                    phase = Section.EPILOGUE

            elif phase == Section.EPILOGUE:
                screen.blit(finale_background, (0, 0))
                if ack.stage != Stage.COMPLETED:
                    ack.update()
                elif code.stage != Stage.COMPLETED:
                    code.update()
                else:
                    font_size = 60
                    font_over = pygame.font.Font(path.join(src_dir, "Calafia-Regular.otf"), 128)
                    thank_you = font_over.render("END", 1, (255, 255, 255))
                    score_text_length = thank_you.get_width()
                    screen.blit(thank_you,
                                ((SCREEN_WIDTH - score_text_length) / 2, SCREEN_HEIGHT / 2 - 0.5 * font_size))

            pygame.display.flip()
            clock.tick(frame_rate)

        # sleep(3)
        # pygame.quit()
        # exit(0)
