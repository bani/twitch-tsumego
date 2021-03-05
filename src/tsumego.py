# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
import time
import re
import rank
import threading
import pickle

GOOD = 1
BAD = 0
CONTINUE = 2
OTHER = 3

class Tsumego(object):

    def __init__(self):
        self.url = 'https://blacktoplay.com/?p=1000'
        self.driver = webdriver.Chrome()
        self.driver.get(self.url)
        self.players = pickle.load( open( "leaderboard.p", "rb" ) )
        self.time = time.localtime()
        self.wait = False
        rank.update(self.players, None)
        time.sleep(1)
        self.update_rank('12 kyu')
        self.load_next(0)

    def fancy_click(self, id):
        self.driver.execute_script("arguments[0].click();", self.driver.find_element_by_id(id))

    def next(self):
        time_elapsed = time.mktime(time.localtime()) - time.mktime(self.time)
        if time_elapsed > 120:
            self.fancy_click('solutionButton')
            t = threading.Thread(target=self.load_next, args=(0,))
            t.start()
            return 0
        else:
            return 120 - time_elapsed

    def load_next(self, pause):
        self.wait = True
        time.sleep(pause)
        self.fancy_click('loadButton')
        time.sleep(1)
        self.wait = False

    def coordinates(self):
        for i in range(1,20):
            for j in range (1,20):
                id = f"{chr(ord('a') - 1 + i)}{chr(ord('a') - 1 + j)}"
                label = f"{(chr(ord('a') - 1 + j)).upper()}{i}"
                div = self.driver.find_elements_by_id(id)
                if len(div) > 0:
                    self.driver.execute_script(f"arguments[0].innerText = '{label}'", div[0])
                    self.driver.execute_script("arguments[0].setAttribute('style', 'text-align: center; padding: 15px 15px; font-size: 1.2em')", div[0])
                else:
                    break

    def solution_check(self):
        solution_check = self.driver.find_element_by_id('solutionContainer')
        if solution_check.text == 'Completed!':
            t = threading.Thread(target=self.load_next, args=(5,))
            t.start()
            return GOOD
        elif solution_check.text == 'Wrong. Keep trying.':
            self.driver.execute_script("stepBeginning()")
            return BAD
        elif solution_check.text == 'Right, go on...':
            return CONTINUE
        else:
            return OTHER

    def place_stone(self, x, y, u):
        if self.wait:
            return "Please wait for the next problem to load."
        self.time = time.localtime()
        xc = x.lower()
        yc = chr(ord('a') - 1 + int(y))
        try:
            self.fancy_click(yc+xc)
        except:
            print(f"invalid coordinates: {yc+xc}")
            return f"{x}{y}?! WutFace"
        
        time.sleep(1)
        result = self.solution_check()
        last = None

        if u not in self.players:
            self.players[u] = 0
        
        if result == GOOD:
            self.players[u]+= 1
            last = u
            self.url = self.driver.current_url
            p = re.search(r'p=([0-9]+)', self.url)
            message = f"HSWP {x}{y} was correct for problem {p.group(1)}! SeemsGood"
        elif result == BAD:
            if self.players[u] > 0:
                self.players[u]-= 1
            message = f"{x}{y}? Try again! NotLikeThis"
        elif result == CONTINUE:
            message = f"{x}{y}? Keep going... O_o"
        else:
            message = f"{x}{y}?! WutFace"
        
        pickle.dump( self.players, open( "leaderboard.p", "wb" ) )
        rank.update(self.players, last)
        
        return message

    def update_rank(self, rank):
        self.driver.find_element_by_id('userText').click()
        
        select = Select(self.driver.find_element_by_id('userRankSelector'))
        try:
            select.select_by_visible_text(rank)
            updated = True
        except:
            updated = False

        self.driver.find_element_by_id('userText').click()
        return updated
