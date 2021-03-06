from . controller import *
from core.event_manager import *
import os
import pygame

class PlayerController(Controller):

	#Note: Since gameplay is not asymetric, two objects of the same PlayerController class can be used to
	#control both players.
	TRIGGER_THRESHOLD = 0.5

	def __init__(self,player_id = 0):
		super(PlayerController,self).__init__()
		self.__player_id = player_id

		self.__key_delta = [
			0,0,0,0 # U D L R
		]
		self.__joy_delta = [0,0] # x y

		self.__joystick = None

		try:
			self.__joystick = pygame.joystick.Joystick(player_id) # should be a 1 or 0
			self.__joystick.init()
			self.__buttons = self.__joystick.get_button(3) #TODO - find out what this does
		except:
			print("ERROR IN PLAYER CONTROLLER JOYSTICK INITIALIZATION")

	def key_press(self,event):
		if event.key == pygame.K_w:
			self.__key_delta[0] = 1
		elif event.key == pygame.K_s:
			self.__key_delta[1] = 1
		if event.key == pygame.K_a:
			self.key_delta[2] = 1
		elif event.key == pygame.K_d:
			self.key_delta[3] = 1
		if event.key == (pygame.K_ESCAPE):
			pass

	def key_release(self,event):
		if event.key == pygame.K_w:
			self.__key_delta[0] = 0
		elif event.key == pygame.K_s:
			self.__key_delta[1] = 0
		if event.key == pygame.K_a:
			self.key_delta[2] = 0
		elif event.key == pygame.K_d:
			self.key_delta[3] = 0


	def update(self, dt):
		if self.__joystick != None:
			analog_data = self.receive_joy()
			EventManager.get_instance().send(f"joystick{self.__player_id}_update", analog_data)
			if os.name == 'posix':
				trigger_data = (self.__joystick.get_axis(5) - self.__joystick.get_axis(2)) / 2
			else:
				trigger_data = self.__joystick.get_axis(2)
			if trigger_data > PlayerController.TRIGGER_THRESHOLD:
				EventManager.get_instance().send("fire", self.__player_id)

	def receive_joy(self):
		move_x = self.__joystick.get_axis(0)
		move_y = self.__joystick.get_axis(1)
		rot_x = self.__joystick.get_axis(3)
		rot_y = self.__joystick.get_axis(4)
		if os.name == "posix":
			return move_x, move_y, rot_x, rot_y
		else:
			return move_x, move_y, rot_y, rot_x
