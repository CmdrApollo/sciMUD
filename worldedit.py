import pygame
import os
import json
import tkinter as tk

from src.rooms import Room

pygame.init()

FONT = pygame.font.SysFont("courier", 24)

WIDTH, HEIGHT = 640, 480
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

if os.path.exists(os.path.join('data', 'rooms.json')):
    rooms = [
        Room(None, r['name'], r['description'], r['items'], r['entities'], {
            'north': r['north'],
            'south': r['south'],
            'east': r['east'],
            'west': r['west']
        }, r['drawing'])
        for r in json.load(open(os.path.join('data', 'rooms.json')))["rooms"]
    ]
else:
    rooms = []

def main():
    run = True
    current_room = rooms[0]
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
        WIN.fill('#080020')

        for room in rooms:
            if room != current_room:
                continue
            
            x, y = WIDTH // 2, HEIGHT // 2

            for line in room.drawing.splitlines():
                WIN.blit(t := FONT.render(line, True, 'white'), (x - t.get_width() // 2, y - t.get_height() // 2))
                y += t.get_height()

        pygame.display.flip()
    
    pygame.quit()

main()