# -*- encoding: utf-8 -*-
from collections import defaultdict
RADIUS = 9
RANGE = range(-RADIUS, RADIUS + 1)
DIAMETER = RADIUS * 2 + 1

def sub(v1, v2):
    return (v1[0] - v2[0], v1[1] - v2[1])

def add(v1, v2):
    return (v1[0] + v2[0], v1[1] + v2[1])

def rot90(v):
    return (-v[1], v[0])

def debugprint_map(vecs):
    map_ = [['.'] * DIAMETER for _ in RANGE]
    for x, y in vecs:
        map_[y + RADIUS][x + RADIUS] = '*'
    print
    print '\n'.join(''.join(line) for line in map_)
    print

baika_list = []
for center_x in RANGE:
    for nw_corner_x in RANGE:
        if center_x < nw_corner_x: break
        for center_y in RANGE:
            for nw_corner_y in RANGE:
                if center_y <= nw_corner_y: break
                center = (center_x, center_y)
                nw = (nw_corner_x, nw_corner_y)
                diff = sub(nw, center)
                r90diff = rot90(diff)
                ne = add(center, r90diff)
                if ne[0] > RADIUS: continue
                if ne[1] < -RADIUS: continue
                r180diff = rot90(r90diff)
                se = add(center, r180diff)
                if se[0] > RADIUS: continue
                if se[1] > RADIUS: continue
                r270diff = rot90(r180diff)
                sw = add(center, r270diff)
                if sw[0] < -RADIUS: continue
                if sw[1] > RADIUS: continue

                baika_list.append([center, nw, ne, se, sw])

#print '\n'.join(','.join('%3d' % count[(x, y)] for x in RANGE) for y in RANGE)

BLACK = 'o'
WHITE = 'x'
map_ = [['.'] * DIAMETER for _ in RANGE]

def set((x, y), v):
    map_[y + RADIUS][x + RADIUS] = v

def get((x, y)):
    return map_[y + RADIUS][x + RADIUS]

def print_map(map_):
    print
    print '  ' + ''.join('%2d' % x for x in RANGE) + ' x'
    print '\n'.join('%2d ' % y + ' '.join(map_[y + RADIUS]) for y in RANGE)
    print ' y'

def add_score((x, y), score):
    score_map[y + RADIUS][x + RADIUS] += score

def print_score():
    print '\n'.join(','.join(
            '%5d' % score_map[y + RADIUS][x + RADIUS]
            for x in RANGE) for y in RANGE)
    print

def calc_score(me=BLACK):
    global score_map
    score_map = [[0] * DIAMETER for _ in RANGE]
    if me == BLACK:
        op = WHITE
    else:
        op = BLACK

    for baika in baika_list:
        num_me = 0
        num_op = 0
        for p in baika:
            v = get(p)
            if v == me: num_me += 1
            if v == op: num_op += 1

        if num_op == 0:
            if num_me == 4:
                score = 960
            elif num_me == 3:
                score = 120
            elif num_me == 2:
                score = 4
            elif num_me == 1:
                score = 2
            elif num_me == 0:
                score = 1
            else:
                continue
        elif num_me == 0:
            if num_op == 4:
                score = 480
            elif num_op == 3:
                score = 120
            elif num_op == 2:
                score = 4
            elif num_op == 1:
                score = 2
            elif num_op == 0:
                score = 1
        else:
            continue

        for p in baika:
            v = get(p)
            if v != BLACK and v != WHITE:
                add_score(p, score)

    print_score()

    max_score = max(max(line) for line in score_map)
    from copy import deepcopy
    map2 = deepcopy(map_)
    best = []
    for x in RANGE:
        for y in RANGE:
            if score_map[y + RADIUS][x + RADIUS] == max_score:
                map2[y + RADIUS][x + RADIUS] = "*"
                best.append((x, y))
    print_map(map2)
    return best

from random import choice
while True:
    best = calc_score(BLACK)
    pos = raw_input("black>")
    if not pos:
        set(choice(best), BLACK)
    else:
        set(eval(pos), BLACK)
    print_map(map_)

    best = calc_score(WHITE)
    pos = raw_input("white>")
    if not pos:
        set(choice(best), WHITE)
    else:
        set(eval(pos), WHITE)
    print_map(map_)
