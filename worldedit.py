import pygame
import os
import json
from tkinter.simpledialog import askstring

from src.rooms import Room

pygame.init()

FONT = pygame.font.SysFont("courier", 24)

WIDTH, HEIGHT = 640, 480
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

if os.path.exists(os.path.join('data', 'locations', 'yaatr.json')):
    rooms = [
        Room(None, r['name'], r['description'], r['items'], r['entities'], {
            'north': r['north'],
            'south': r['south'],
            'east': r['east'],
            'west': r['west']
        }, r['drawing'])
        for r in json.load(open(os.path.join('data', 'yaatr.json')))["rooms"]
    ]
else:
    rooms = []

def generate_drawing(room):
    drawing = [
        ["+", "-", "-", "-", "-", "-", "+"],
        ["|", " ", " ", " ", " ", " ", "|"],
        ["|", " ", " ", " ", " ", " ", "|"],
        ["|", " ", " ", " ", " ", " ", "|"],
        ["|", " ", " ", " ", " ", " ", "|"],
        ["|", " ", " ", " ", " ", " ", "|"],
        ["+", "-", "-", "-", "-", "-", "+"],
    ]

    directions = {
        "north": [(-1, 0, '|'), (-2, 0, 'r')],
        "south": [(1, 0, '|'), (2, 0, 'r')],
        "west":  [(0, -1, '-'), (0, -2, 'r')],
        "east":  [(0, 1, '-'), (0, 2, 'r')],
    }

    x, y = 3, 3

    def draw_neighbors(x, y, room, depth = 1):
        if depth > 4:
            return
        
        for direction, updates in directions.items():
            neighbor_id = room.neighbors[direction]
            if neighbor_id:
                for dy, dx, char in updates:
                    if 1 <= x + dx < len(drawing[0]) - 1 and 1 <= y + dy < len(drawing) - 1:
                        drawing[y + dy][x + dx] = char
                    else:
                        return
                draw_neighbors(x + dx, y + dy, get_room(neighbor_id), depth + 1)

    draw_neighbors(x, y, room)

    drawing[y][x] = 'X'

    return "\n".join("".join(row) for row in drawing)

def get_room(name):
    for r in rooms:
        if r.name == name:
            return r
    
    return None

def main():
    run = True
    current_room = rooms[0]
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if pygame.key.get_pressed()[pygame.K_LCTRL]:
                    if event.key == pygame.K_s:
                        data = {"rooms": []}
                        for r in rooms:
                            data["rooms"].append({
                                "name": r.name,
                                "description": r.description,
                                "items": r.items,
                                "entities": r.entities,
                                "north": r.neighbors['north'],
                                "south": r.neighbors['south'],
                                "east": r.neighbors['east'],
                                "west": r.neighbors['west'],
                                "drawing": generate_drawing(r)
                            })
                        
                        json.dump(data, open(os.path.join('data', 'yaatr.json'), 'w'), indent='\t')

                    if event.key == pygame.K_UP and not current_room.neighbors['north']:
                        rooms.append(Room(None, askstring("room name", "room name"), askstring("room description", "room description"), [], [], {
                            "north": None,
                            "south": current_room.name,
                            "east": None,
                            "west": None
                        }, ""))
                        current_room.neighbors['north'] = rooms[-1].name
                        current_room = rooms[-1]
                    if event.key == pygame.K_DOWN and not current_room.neighbors['south']:
                        rooms.append(Room(None, askstring("room name", "room name"), askstring("room description", "room description"), [], [], {
                            "north": current_room.name,
                            "south": None,
                            "east": None,
                            "west": None
                        }, ""))
                        current_room.neighbors['south'] = rooms[-1].name
                        current_room = rooms[-1]
                    if event.key == pygame.K_RIGHT and not current_room.neighbors['east']:
                        rooms.append(Room(None, askstring("room name", "room name"), askstring("room description", "room description"), [], [], {
                            "north": None,
                            "south": None,
                            "east": None,
                            "west": current_room.name
                        }, ""))
                        current_room.neighbors['east'] = rooms[-1].name
                        current_room = rooms[-1]
                    if event.key == pygame.K_LEFT and not current_room.neighbors['west']:
                        rooms.append(Room(None, askstring("room name", "room name"), askstring("room description", "room description"), [], [], {
                            "north": None,
                            "south": None,
                            "east": current_room.name,
                            "west": None
                        }, ""))
                        current_room.neighbors['west'] = rooms[-1].name
                        current_room = rooms[-1]
                else:
                    if event.key == pygame.K_UP and current_room.neighbors['north']: current_room = get_room(current_room.neighbors['north'])
                    if event.key == pygame.K_DOWN and current_room.neighbors['south']: current_room = get_room(current_room.neighbors['south'])
                    if event.key == pygame.K_RIGHT and current_room.neighbors['east']: current_room = get_room(current_room.neighbors['east'])
                    if event.key == pygame.K_LEFT and current_room.neighbors['west']: current_room = get_room(current_room.neighbors['west'])

                    if event.key == pygame.K_n:
                        a = askstring("connected room", "connected room")
                        if get_room(a) or a == None:
                            current_room.neighbors['north'] = a
                    if event.key == pygame.K_e:
                        a = askstring("connected room", "connected room")
                        if get_room(a) or a == None:
                            current_room.neighbors['east'] = a
                    if event.key == pygame.K_s:
                        a = askstring("connected room", "connected room")
                        if get_room(a) or a == None:
                            current_room.neighbors['south'] = a
                    if event.key == pygame.K_w:
                        a = askstring("connected room", "connected room")
                        if get_room(a) or a == None:
                            current_room.neighbors['west'] = a

                    if event.key == pygame.K_a:
                        a = askstring("room name", "room name")
                        for room in rooms:
                            if room.neighbors['north'] == current_room.name:
                                room.neighbors['north'] = a
                            if room.neighbors['east'] == current_room.name:
                                room.neighbors['east'] = a
                            if room.neighbors['south'] == current_room.name:
                                room.neighbors['south'] = a
                            if room.neighbors['west'] == current_room.name:
                                room.neighbors['west'] = a
                        current_room.name = a

                    if event.key == pygame.K_i:
                        a = askstring("items", "items")
                        current_room.items = [b.lower().strip() for b in a.split(',')]

                    if event.key == pygame.K_t:
                        a = askstring("entities", "entities")
                        current_room.entities = [b.lower().strip() for b in a.split(',')]

        WIN.fill('#080020')

        y = 0
        for line in [
            f"n]orth: {current_room.neighbors['north']}",
            f"s]outh: {current_room.neighbors['south']}",
            f"e]ast : {current_room.neighbors['east']}",
            f"w]est : {current_room.neighbors['west']}",
        ]:
            WIN.blit(t := FONT.render(line, True, 'white'), (0, y))
            y += t.get_height()

        y = 0
        for line in [
            f"n[a]me: {current_room.name}",
            f"i]tems: {', '.join([a for a in current_room.items])}",
            f"en[t]ities: {', '.join([a for a in current_room.entities])}",
        ]:
            WIN.blit(t := FONT.render(line, True, 'white'), (WIDTH - t.get_width(), y))
            y += t.get_height()

        for room in rooms:
            if room != current_room:
                continue
            
            x, y = WIDTH // 2, HEIGHT // 2

            for line in generate_drawing(room).splitlines():
                WIN.blit(t := FONT.render(line, True, 'white'), (x - t.get_width() // 2, y - t.get_height() // 2))
                y += t.get_height()

        pygame.display.flip()
    
    pygame.quit()

main()