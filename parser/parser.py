import json

filename = "games/frogger/frogger.c"

text = open(filename, 'r').readAll()

keyword = "ALLEGRO_KEY_"

print(text)