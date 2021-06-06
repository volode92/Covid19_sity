import pygame
import random
import numpy as np
import matplotlib.pyplot as plt
import time
import sys
import pygame.freetype

pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('arial',20)
#size
SIZE_DISTRICT_X = 500
SIZE_DISTRICT_Y = 400
LEFT_INDENT = 20
RIGHT_INDENT = 20
UP_INDENT = 20
DOWN_INDENT = 20
HORIZONTAL_INDENT = 40
VERTICAL_INDENT = 40

#границы
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


displayw = 2*SIZE_DISTRICT_X + LEFT_INDENT + RIGHT_INDENT + HORIZONTAL_INDENT
displayh = 2*SIZE_DISTRICT_Y + UP_INDENT + DOWN_INDENT + VERTICAL_INDENT
#point sqvad
pr1 = pygame.Rect((l1, u1, SIZE_DISTRICT_X, SIZE_DISTRICT_Y))
pr2 = pygame.Rect((l2, u2, SIZE_DISTRICT_X, SIZE_DISTRICT_Y))
pr3 = pygame.Rect((l3, u3, SIZE_DISTRICT_X, SIZE_DISTRICT_Y))
pr4 = pygame.Rect((l4, u4, SIZE_DISTRICT_X, SIZE_DISTRICT_Y))

window = pygame.display.set_mode((displayw,displayh))

#model param
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
social_distance = int(care_range*2)
social_jump = 2


def take_color_point(disease,cure,live):
    if live == False:
        return (255,192,203)
    if disease:
        return (255, 0, 0)
    if cure:
        return (0, 255, 0)
    return (0, 0, 255)

district1_dict = {'l':l1,'r':r1,'u':u1,'d':d1}
district2_dict = {'l':l2,'r':r2,'u':u2,'d':d2}
district3_dict = {'l':l3,'r':r3,'u':u3,'d':d3}
district4_dict = {'l':l4,'r':r4,'u':u4,'d':d4}
dist_district = {'1':district1_dict,'2':district2_dict,'3':district3_dict,'4':district4_dict}

def take_poind_pos(x,y,i):
    if i == 0:
        return x+dist_district['1']['l'],y+dist_district['1']['u']
    if i == 1:
        return x+dist_district['2']['l'],y+dist_district['2']['u']
    if i == 2:
        return x+dist_district['3']['l'],y+dist_district['3']['u']
    if i == 3:
        return x+dist_district['4']['l'],y+dist_district['4']['u']

def Fastcheck():
    for arr_i in range(4):
        tmp_arr = []
        for i,peop in enumerate(arr_people[arr_i]):
            tmp_arr.append({'i':i,'x':peop.posx,'y':peop.posy,'xy':peop.posx+peop.posy, 'disease':peop.disease})
        tmp_arr.sort(key=lambda x:x['xy'])
        for k in range(len(tmp_arr)-1):
            l=1
            while abs(tmp_arr[k]['xy'] - tmp_arr[k+l]['xy']) < care_range:
                if ((tmp_arr[k]['x'] - tmp_arr[k+l]['x']) < 2*radius) and ((tmp_arr[k]['y'] - tmp_arr[k+l]['y']) < 2*radius):
                    if tmp_arr[k]['disease']^tmp_arr[k+l]['disease']:
                        Chahgestat(arr_people[arr_i][tmp_arr[k]['i']], arr_people[arr_i][tmp_arr[k+l]['i']])
                if l>(len(tmp_arr)-k-1):
                    l+=1
                else:
                    break
            # l=1
            # while abs(tmp_arr[k]['xy'] - tmp_arr[k+l]['xy']) < social_distance:
            #     if ((tmp_arr[k]['x'] - tmp_arr[k+l]['x']) < social_distance) and ((tmp_arr[k]['y'] - tmp_arr[k+l]['y'])< social_distance):
            #         if tmp_arr[k]['x'] - tmp_arr[k+l]['x'] <= 0:
            #             if arr_people[arr_i][tmp_arr[k]['i']].posx  > \
            #                     dist_district[str(arr_people[arr_i][tmp_arr[k]['i']].district + 1)]['l']:
            #                 arr_people[arr_i][tmp_arr[k]['i']].posx -= 1
            #             else:
            #                 arr_people[arr_i][tmp_arr[k]['i']].posx = \
            #                 dist_district[str(arr_people[arr_i][tmp_arr[k]['i']].district + 1)]['l'] + 1
            #         else:
            #             if arr_people[arr_i][tmp_arr[k]['i']].posx  < \
            #                     dist_district[str(arr_people[arr_i][tmp_arr[k]['i']].district + 1)]['r']:
            #                 arr_people[arr_i][tmp_arr[k]['i']].posx += 1
            #             else:
            #                 arr_people[arr_i][tmp_arr[k]['i']].posx = \
            #                 dist_district[str(arr_people[arr_i][tmp_arr[k]['i']].district + 1)]['r'] - 1
            #         if tmp_arr[k]['y'] - tmp_arr[k+l]['y'] <= 0:
            #             if arr_people[arr_i][tmp_arr[k]['i']].posy  > \
            #                     dist_district[str(arr_people[arr_i][tmp_arr[k]['i']].district + 1)]['u']:
            #                 arr_people[arr_i][tmp_arr[k]['i']].posy -= 1
            #             else:
            #                 arr_people[arr_i][tmp_arr[k]['i']].posy = \
            #                 dist_district[str(arr_people[arr_i][tmp_arr[k]['i']].district + 1)]['u'] + 1
            #         else:
            #             if arr_people[arr_i][tmp_arr[k]['i']].posy  < \
            #                     dist_district[str(arr_people[arr_i][tmp_arr[k]['i']].district + 1)]['d']:
            #                 arr_people[arr_i][tmp_arr[k]['i']].posy += 1
            #             else:
            #                 arr_people[arr_i][tmp_arr[k]['i']].posy = \
            #                 dist_district[str(arr_people[arr_i][tmp_arr[k]['i']].district + 1)]['d'] - 1
            #     if l>(len(tmp_arr)-k-1):
            #         l+=1
            #     else:
            #         break


def Chahgestat(People1,People2):
    if People1.disease:
        if People2.disease == False and People2.cure == False:
            People2.disease = True if random.randint(0, 100) < percent_transfer else False
            People2.color = (255, 0, 0) if People2.disease else (0, 0, 255)
    if People2.disease:
        if People1.disease == False and People1.cure == False:
            People1.disease = True if random.randint(0, 100) < percent_transfer else False
            People1.color = (255, 0, 0) if People1.disease else (0, 0, 255)

def Checkdeth():
    for arr_dis in arr_people:
        for el in arr_dis:
            if el.disease:
                if random.random()*100 > percent_live:
                    el.disease = False
                    el.live = False
                    el.cure = True
                    el.color = (255, 192, 203)

def Transfer(arr_people):
    if random.randint(0,100) < percent_chanse_transfer:
        rand_distr = random.randint(0,3)
        rand_distr2 = random.randint(0,3)
        while rand_distr==rand_distr2:
            rand_distr2 = random.randint(0, 3)
        rand_peop = random.randint(0, len(arr_people[rand_distr])-1)
        while arr_people[rand_distr][rand_peop].live == False:
            rand_peop = random.randint(0, len(arr_people[rand_distr])-1)
        tmp_peop = arr_people[rand_distr].pop(rand_peop)
        tmp_peop.district = rand_distr2
        tmp_peop.posx, tmp_peop.posy = take_poind_pos(random.randint(5, SIZE_DISTRICT_X-5), random.randint(5, SIZE_DISTRICT_Y-5), rand_distr2)
        arr_people[rand_distr2].append(tmp_peop)
    return arr_people

def Show_info():
    pygame.draw.rect(window, (255, 255, 255), pr1, 2)
    pygame.draw.rect(window, (255, 255, 255), pr2, 2)
    pygame.draw.rect(window, (255, 255, 255), pr3, 2)
    pygame.draw.rect(window, (255, 255, 255), pr4, 2)
    window.blit(myfont.render('Город1', True, (200, 200, 200)), (LEFT_INDENT, 0))
    window.blit(myfont.render('Город2', False, (200, 200, 200)), (LEFT_INDENT+SIZE_DISTRICT_X+HORIZONTAL_INDENT, 0))
    window.blit(myfont.render('Город3', True, (200, 200, 200)), (LEFT_INDENT, SIZE_DISTRICT_Y+VERTICAL_INDENT))
    window.blit(myfont.render('Город4', False, (200, 200, 200)), (LEFT_INDENT+SIZE_DISTRICT_X+HORIZONTAL_INDENT, SIZE_DISTRICT_Y+VERTICAL_INDENT))

class People():
    def __init__(self, x, y, district):
        self.district = district
        self.posx, self.posy = take_poind_pos(x,y,district)
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
            if self.posx <= dist_district[str(self.district+1)]['l']+4 or self.posx >= dist_district[str(self.district+1)]['r']-4:
                self.speedx = -self.speedx
                if self.posx < dist_district[str(self.district + 1)]['l'] + 4:
                    self.posx = dist_district[str(self.district + 1)]['l'] + 4
                if self.posx > dist_district[str(self.district+1)]['r']-4:
                    self.posx = dist_district[str(self.district + 1)]['l'] + 4
            if self.posy <= dist_district[str(self.district+1)]['u']+4 or self.posy >= dist_district[str(self.district+1)]['d']-4:
                self.speedy = -self.speedy
                self.posy += self.speedy*2
            if self.disease:
                self.timedisease +=1
            if self.timeafterdisease > 0:
                self.timeafterdisease += 1
            if self.timedisease >= frame_clear:
                self.disease = False
                if random.randint(0, 100) > percent_live:
                    self.cure = True
                    self.live = False
                    self.color = (255,192,203)
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


#создаем людей
arr_distr1, arr_distr2, arr_distr3, arr_distr4 = [], [], [], []
for peop in range(Num_people):
    New_people = People(random.randint(5, SIZE_DISTRICT_X - 5), random.randint(5, SIZE_DISTRICT_Y - 5), 0)
    arr_distr1.append(New_people)
for peop in range(Num_people):
    New_people = People(random.randint(5, SIZE_DISTRICT_X-5), random.randint(5, SIZE_DISTRICT_Y-5),1)
    arr_distr2.append(New_people)
for peop in range(Num_people):
    New_people = People(random.randint(5, SIZE_DISTRICT_X-5), random.randint(5, SIZE_DISTRICT_Y-5),2)
    arr_distr3.append(New_people)
for peop in range(Num_people):
    New_people = People(random.randint(5, SIZE_DISTRICT_X-5), random.randint(5, SIZE_DISTRICT_Y-5),3)
    arr_distr4.append(New_people)
arr_people = [arr_distr1, arr_distr2, arr_distr3, arr_distr4]

zero_pacient = random.randint(0,Num_people)
inf_distr = random.randint(0,3)
arr_people[inf_distr][zero_pacient].disease = True
arr_people[inf_distr][zero_pacient].color = (255, 0, 0)

frame = 0
start_time = time.time()
while True:
    frame += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    fpsClock.tick(FPS)
    window.fill((0, 0, 0))
    Show_info()
    for arr in arr_people:
        for peop in arr:
            pygame.draw.circle(window, peop.color, (peop.posx, peop.posy), radius)
            peop.update()
    pygame.display.update()
    arr_people = Transfer(arr_people)
    Fastcheck()
    if frame%FPS == 0:
        Checkdeth()
        print(frame, '%.07f' % (time.time() - start_time ))
        start_time = time.time()


pygame.quit()