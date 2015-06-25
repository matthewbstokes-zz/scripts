from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import InvalidElementStateException
from time import sleep

w = webdriver.Firefox()
w.get('http://play.typeracer.com/')
play_game = w.find_element_by_class_name('gwt-Anchor')
play_game.send_keys(Keys.CONTROL, Keys.ALT, 'i')

word = w.find_element_by_class_name('nonHideableWords')
span = word.find_elements_by_tag_name('span')[1]

txt_box = w.find_element_by_class_name('txtInput')

while 1:
  try:
    txt_box.send_keys(span.text + ' ')
    sleep(0.07) 
  except InvalidElementStateException as e:
    sleep(1)
