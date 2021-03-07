# -*- coding: utf-8 -*-

import PySimpleGUI as sg
import threading
import time


W = 30 # name width

def open_leaderboard():
    while True:
        event, value = leaderboard.read()
        if event == sg.WIN_CLOSED:
            break

    leaderboard.close()

def update_leaderboard(players, last):
    i = 1
    for (k,v) in sorted(players.items(), key=lambda x: -x[1]):
        entry = f"{i}. {k.ljust(W-10)} {str(v).rjust(3)}"
        leaderboard[i].update(entry)
        i+=1
        if i > 5:
            break
    if last:
        leaderboard[0].update(f"{last} ({players[last] if last != 'beginnergo' else '-∞'})".ljust(W))
        
    leaderboard.refresh()

sg.theme('DarkPurple')   # Add a touch of color
font = {'font': 'Courier 16', 'text_color': 'white'}
font2 = {'font': 'Sans-Serif 20', 'text_color': 'white'}

layout = [
            [sg.Text(''.ljust(W+10), key=1, **font)],
            [sg.Text(''.ljust(W+10), key=2, **font)],
            [sg.Text(''.ljust(W+10), key=3, **font)],
            [sg.Text(''.ljust(W+10), key=4, **font)],
            [sg.Text(''.ljust(W+10), key=5, **font)],
            [sg.Text(' ', **font)],
            [sg.Text('Last correct answer:', **font2)],
            [sg.Text(''.ljust(W+10), key=0, **font2)], ]

leaderboard = sg.Window('Top Players', layout, alpha_channel=0.7)

t = threading.Thread(target=open_leaderboard)
t.start()
time.sleep(1)

