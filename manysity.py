import pygame
import random
import numpy as np
import matplotlib.pyplot as plt
import time
import sys
import pygame.freetype

pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('arial', 20)

# size
SIZE_DISTRICT_X = 500
SIZE_DISTRICT_Y = 400
LEFT_INDENT = 20
RIGHT_INDENT = 20
UP_INDENT = 20
DOWN_INDENT = 20
HORIZONTAL_INDENT = 40
VERTICAL_INDENT = 40

# границы
l1 = LEFT_INDENT
r1 = LEFT_INDENT + SIZE_DISTRICT_X
u1 = UP_INDENT
d1 = UP_INDENT + SIZE_DISTRICT_Y
l2 = LEFT_INDENT + SIZE_DISTRICT_X + HORIZONTAL_INDENT
r2 = LEFT_INDENT + 2 * SIZE_DISTRICT_X + HORIZONTAL_INDENT
u2 = UP_INDENT
d2 = UP_INDENT + SIZE_DISTRICT_Y
l3 = LEFT_INDENT
r3 = LEFT_INDENT + SIZE_DISTRICT_X
u3 = UP_INDENT + SIZE_DISTRICT_Y + VERTICAL_INDENT
d3 = UP_INDENT + 2 * SIZE_DISTRICT_Y + VERTICAL_INDENT
l4 = LEFT_INDENT + SIZE_DISTRICT_X + HORIZONTAL_INDENT
r4 = LEFT_INDENT + 2 * SIZE_DISTRICT_X + HORIZONTAL_INDENT
u4 = UP_INDENT + SIZE_DISTRICT_Y + VERTICAL_INDENT
d4 = UP_INDENT + 2 * SIZE_DISTRICT_Y + VERTICAL_INDENT

displayw = 2 * SIZE_DISTRICT_X + LEFT_INDENT + RIGHT_INDENT + HORIZONTAL_INDENT
displayh = 2 * SIZE_DISTRICT_Y + UP_INDENT + DOWN_INDENT + VERTICAL_INDENT
# point sqvad
pr1 = pygame.Rect((l1, u1, SIZE_DISTRICT_X, SIZE_DISTRICT_Y))
pr2 = pygame.Rect((l2, u2, SIZE_DISTRICT_X, SIZE_DISTRICT_Y))
pr3 = pygame.Rect((l3, u3, SIZE_DISTRICT_X, SIZE_DISTRICT_Y))
pr4 = pygame.Rect((l4, u4, SIZE_DISTRICT_X, SIZE_DISTRICT_Y))

window = pygame.display.set_mode((displayw, displayh))

# model param
fpsClock = pygame.time.Clock()
FPS = 30

max_speed = 2
Num_people = 800
radius = 2
care_range = 3
percent_transfer = 100
percent_chanse_transfer = 20
percent_live = 99.5
day_cure = 28
frame_clear = day_cure * FPS
day_second_disease = 40
timer_second_disease = day_second_disease * FPS
social_distance = int(care_range * 2)
social_jump = 2


def take_color_point(disease, cure, live):
    if live == False:
        return (255, 192, 203)
    if disease:
        return (255, 0, 0)
    if cure:
        return (0, 255, 0)
    return (0, 0, 255)


district1_dict = {'l': l1, 'r': r1, 'u': u1, 'd': d1}
district2_dict = {'l': l2, 'r': r2, 'u': u2, 'd': d2}
district3_dict = {'l': l3, 'r': r3, 'u': u3, 'd': d3}
district4_dict = {'l': l4, 'r': r4, 'u': u4, 'd': d4}
dist_district = {'1': district1_dict, '2': district2_dict, '3': district3_dict, '4': district4_dict}


def take_poind_pos(x, y, i):
    if i == 0:
        return x + dist_district['1']['l'], y + dist_district['1']['u']
    if i == 1:
        return x + dist_district['2']['l'], y + dist_district['2']['u']
    if i == 2:
        return x + dist_district['3']['l'], y + dist_district['3']['u']
    if i == 3:
        return x + dist_district['4']['l'], y + dist_district['4']['u']



def show_info():
    pygame.draw.rect(window, (255, 255, 255), pr1, 2)
    pygame.draw.rect(window, (255, 255, 255), pr2, 2)
    pygame.draw.rect(window, (255, 255, 255), pr3, 2)
    pygame.draw.rect(window, (255, 255, 255), pr4, 2)
    window.blit(myfont.render('Город1', True, (200, 200, 200)), (LEFT_INDENT, 0))
    window.blit(myfont.render('Город2', False, (200, 200, 200)), (LEFT_INDENT + SIZE_DISTRICT_X + HORIZONTAL_INDENT, 0))
    window.blit(myfont.render('Город3', True, (200, 200, 200)), (LEFT_INDENT, SIZE_DISTRICT_Y + VERTICAL_INDENT))
    window.blit(myfont.render('Город4', False, (200, 200, 200)),
                (LEFT_INDENT + SIZE_DISTRICT_X + HORIZONTAL_INDENT, SIZE_DISTRICT_Y + VERTICAL_INDENT))


class People():
    def __init__(self, x, y, district):
        self.district = district
        self.posx, self.posy = take_poind_pos(x, y, district)
        self.disease = False
        self.cure = False
        self.live = True
        self.ill = False
        self.speedx = random.randint(-max_speed, max_speed)
        self.speedy = random.randint(-max_speed, max_speed)
        self.color = take_color_point(self.disease, self.cure, self.live)
        self.timedisease = 0
        self.timeafterdisease = 0

    def update(self):
        if self.live:
            self.posx += self.speedx
            self.posy += self.speedy
            if self.posx <= dist_district[str(self.district + 1)]['l'] + 4 or self.posx >= \
                    dist_district[str(self.district + 1)]['r'] - 4:
                self.speedx = -self.speedx
                if self.posx < dist_district[str(self.district + 1)]['l'] + 4:
                    self.posx = dist_district[str(self.district + 1)]['l'] + 4
                if self.posx > dist_district[str(self.district + 1)]['r'] - 4:
                    self.posx = dist_district[str(self.district + 1)]['l'] + 4
            if self.posy <= dist_district[str(self.district + 1)]['u'] + 4 or self.posy >= \
                    dist_district[str(self.district + 1)]['d'] - 4:
                self.speedy = -self.speedy
                self.posy += self.speedy * 2
            if self.disease:
                self.timedisease += 1
            if self.timeafterdisease > 0:
                self.timeafterdisease += 1
            if self.timedisease >= frame_clear:
                self.disease = False
                if random.randint(0, 100) > percent_live:
                    self.cure = True
                    self.live = False
                    self.color = (255, 192, 203)
                else:
                    self.cure = True
                    self.timedisease = 0
                    self.timeafterdisease += 1
                    self.color = (0, 255, 0)
            if self.timeafterdisease != 0:
                self.timeafterdisease += 1
            if self.timeafterdisease > timer_second_disease:
                self.disease = False
                self.color = (0, 0, 255)
                self.cure = False
                self.ill = True
                self.timeafterdisease = 0


class Sity():
    def __init__(self, district, num_people):
        self.people_list = []
        for peop in range(num_people):
            new_people = People(random.randint(5, SIZE_DISTRICT_X - 5), random.randint(5, SIZE_DISTRICT_Y - 5), district)
            self.people_list.append(new_people)

    def chahgestat(self, People1, People2):
        if People1.disease:
            if People2.disease == False and People2.cure == False:
                People2.disease = True if random.randint(0, 100) < percent_transfer else False
                People2.color = (255, 0, 0) if People2.disease else (0, 0, 255)
        if People2.disease:
            if People1.disease == False and People1.cure == False:
                People1.disease = True if random.randint(0, 100) < percent_transfer else False
                People1.color = (255, 0, 0) if People1.disease else (0, 0, 255)

class Hospital():
    def __init__(self):
        pass


class Cemetery():
    def __init__(self):
        pass

class ChainComand():
    def __init__(self, num_people):
        self.sitylist = []
        for i in range(4):
            new_sity = Sity(i, num_people)
            self.sitylist.append(new_sity)

    def start_inf(self):
        inf_distr = random.randint(0, len(self.sitylist)-1)
        zero_pacient = random.randint(0, len(self.sitylist[inf_distr].people_list))
        self.sitylist[inf_distr].people_list[zero_pacient].disease = True
        self.sitylist[inf_distr].people_list[zero_pacient].color = (255, 0, 0)

    def drow_poin(self):
        for sity in self.sitylist:
            for people in sity.people_list:
                pygame.draw.circle(window, people.color, (people.posx, people.posy), radius)
                people.update()

    def fast_check(self):
        for sites in self.sitylist:
            tmp_arr = []
            for i, peop in enumerate(sites.people_list):
                tmp_arr.append(
                    {'i': i, 'x': peop.posx, 'y': peop.posy, 'xy': peop.posx + peop.posy, 'disease': peop.disease})
            tmp_arr.sort(key=lambda x: x['xy'])
            for k in range(len(tmp_arr) - 1):
                l = 1
                while abs(tmp_arr[k]['xy'] - tmp_arr[k + l]['xy']) < care_range:
                    if ((tmp_arr[k]['x'] - tmp_arr[k + l]['x']) < 2 * radius) and (
                            (tmp_arr[k]['y'] - tmp_arr[k + l]['y']) < 2 * radius):
                        if tmp_arr[k]['disease'] ^ tmp_arr[k + l]['disease']:
                            sites.chahgestat(sites.people_list[tmp_arr[k]['i']], sites.people_list[tmp_arr[k + l]['i']])
                    if l > (len(tmp_arr) - k - 1):
                        l += 1
                    else:
                        break

    def transfer(self):
        if random.randint(0, 100) < percent_chanse_transfer:
            rand_distr = random.randint(0, 3)
            rand_distr2 = random.randint(0, 3)
            while rand_distr == rand_distr2:
                rand_distr2 = random.randint(0, 3)
            rand_peop = random.randint(0, len(self.sitylist[rand_distr].people_list) - 1)
            while self.sitylist[rand_distr].people_list[rand_peop].live == False:
                rand_peop = random.randint(0, len(self.sitylist[rand_distr].people_list) - 1)
            tmp_peop = self.sitylist[rand_distr].people_list.pop(rand_peop)
            tmp_peop.district = rand_distr2
            tmp_peop.posx, tmp_peop.posy = take_poind_pos(random.randint(5, SIZE_DISTRICT_X - 5),
                                                          random.randint(5, SIZE_DISTRICT_Y - 5), rand_distr2)
            self.sitylist[rand_distr2].people_list.append(tmp_peop)

class Log():
    def __init__(self):
        self.live_people = []
        self.die_people = []
        self.ill_people = []
        self.cure_people = []
        self.disease_people = []
        self.day = 0
        self.day_array = []

    def update_data(self, sitieslist):
        self.day += 1
        tmp_live = 0
        tmp_die = 0
        tmp_ill = 0
        tmp_cure = 0
        tmp_disease = 0
        for sity in sitieslist:
            for ppl in sity.people_list:
                if ppl.live == False:
                    tmp_die += 1
                    continue
                if ppl.disease:
                    tmp_disease += 1
                    continue
                if ppl.ill:
                    tmp_ill += 1
                    continue
                if ppl.cure:
                    tmp_cure += 1
                    continue
                tmp_live += 1
        self.live_people.append(tmp_live)
        self.die_people.append(tmp_die)
        self.ill_people.append(tmp_ill)
        self.cure_people.append(tmp_cure)
        self.disease_people.append(tmp_disease)
        self.day_array.append(self.day)
        if tmp_disease == 0:
            return False
        return True

    def show_graph(self):
        data = {
            'live_people': self.live_people,
            'die_people': self.die_people,
            'ill_people': self.ill_people,
            'cure_people': self.cure_people,
            'disease_people': self.disease_people,
        }
        fig, ax = plt.subplots()
        ax.stackplot(self.day_array, data.values(),
                     labels=data.keys())
        ax.legend(loc='upper left')
        ax.set_title('World population')
        ax.set_xlabel('Year')
        ax.set_ylabel('Number of people (millions)')

        plt.show()




CoR = ChainComand(1000) #создаем города с людьми
CoR.start_inf()
log = Log()

frame = 0
start_time = time.time()
END = True
while END:
    frame += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    fpsClock.tick(FPS)
    window.fill((0, 0, 0))
    show_info()
    CoR.drow_poin()
    pygame.display.update()
    CoR.fast_check()
    CoR.transfer()
    if frame % FPS == 0:
        END = log.update_data(CoR.sitylist)
        #print(frame, '%.07f' % (time.time() - start_time))
        start_time = time.time()

log.show_graph()

pygame.quit()
