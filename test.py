

""" XInput Game Controller APIs
Pure Python implementation for reading Xbox controller inputs without extra libs
Copyright (C) 2020 by Arti Zirk <arti.zirk@gmail.com>
Permission to use, copy, modify, and/or distribute this software for any purpose
with or without fee is hereby granted.
THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT,
INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS
OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER
TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF
THIS SOFTWARE.
"""

from ctypes import WinDLL, WinError, Structure, POINTER, byref, c_ubyte
from ctypes.util import find_library
from ctypes.wintypes import DWORD, WORD, SHORT
import keyboard

# keyboard.write("Python is an amazing programming language.")
# keyboard.press_and_release("enter")
# keyboard.press_and_release("fn+p")
# keyboard.press_and_release("y")
# keyboard.press_and_release("t")
# keyboard.press_and_release("h")
# keyboard.press_and_release("o")
# keyboard.press_and_release("n")

# for some reason wintypes.BYTE is defined as signed c_byte and as c_ubyte
BYTE = c_ubyte


# Max number of controllers supported
XUSER_MAX_COUNT = 4

state = [0 for i in range(200)]


class XINPUT_BUTTONS(Structure):
	"""Bit-fields of XINPUT_GAMEPAD wButtons"""

	_fields_ = [
		("P_U", WORD, 1),
		("P_D", WORD, 1),
		("P_L", WORD, 1),
		("P_R", WORD, 1),
		("S", WORD, 1),
		("B", WORD, 1),
		("L_T", WORD, 1),
		("R_T", WORD, 1),
		("L_S", WORD, 1),
		("R_S", WORD, 1),
		("_r_1_", WORD, 1),
		("_r_1_", WORD, 1),
		("A", WORD, 1),
		("B", WORD, 1),
		("X", WORD, 1),
		("Y", WORD, 1)
	]
	
	def __repr__(self):
		r = []
		for name, type, size in self._fields_:
			if "reserved" in name:
				continue
			r.append("{}={}".format(name, getattr(self, name)))
		args = ', '.join(r)
		return f"XINPUT_GAMEPAD({args})"
	

class XINPUT_GAMEPAD(Structure):
	"""Describes the current state of the Xbox 360 Controller.
	
	https://docs.microsoft.com/en-us/windows/win32/api/xinput/ns-xinput-xinput_gamepad
	
	wButtons is a bitfield describing currently pressed buttons
	"""
	_fields_ = [
		("B", XINPUT_BUTTONS),
		("LT", BYTE),
		("RT", BYTE),
		("TLX", SHORT),
		("TLY", SHORT),
		("TRX", SHORT),
		("TRY", SHORT),
	]
	
	def __repr__(self):
		r = []
		for name, type in self._fields_:
			r.append("{}={}".format(name, getattr(self, name)))
		args = ', '.join(r)
		return f"XINPUT_GAMEPAD({args})"


class XINPUT_STATE(Structure):
	"""Represents the state of a controller.
	
	https://docs.microsoft.com/en-us/windows/win32/api/xinput/ns-xinput-xinput_state
	
	dwPacketNumber: State packet number. The packet number indicates whether
		there have been any changes in the state of the controller. If the
		dwPacketNumber member is the same in sequentially returned XINPUT_STATE
		structures, the controller state has not changed.
	"""
	_fields_ = [
		("dwPacketNumber", DWORD),
		("Gamepad", XINPUT_GAMEPAD)
	]
	
	def __repr__(self):
		return f"XINPUT_STATE(dwPacketNumber={self.dwPacketNumber}, Gamepad={self.Gamepad})"


def writeCorrectInput(noFn, fn1, fn2):
	if state[190] == 1:
		keyboard.write(fn1)
	elif state[192] == 1:
		keyboard.write(fn2)
	else:
		keyboard.write(noFn)


def PressCorrectInput(noFn, fn1, fn2):
	if state[190] == 1:
		if fn1 == "":
			return
		keyboard.press(fn1)
	elif state[192] == 1:
		if fn2 == "":
			return
		keyboard.press(fn2)
	else:
		if noFn == "":
			return
		keyboard.press(noFn)

class XInput:
	"""Minimal XInput API wrapper"""

	def __init__(self):
		# https://docs.microsoft.com/en-us/windows/win32/xinput/xinput-versions
		# XInput 1.4 is available only on Windows 8+.
		# Older Windows versions are End Of Life anyway.
		lib_name = "XInput1_4.dll"  
		lib_path = find_library(lib_name)
		if not lib_path:
			raise Exception(f"Couldn't find {lib_name}")
		self._XInput_ = WinDLL(lib_path)
		self._XInput_.XInputGetState.argtypes = [DWORD, POINTER(XINPUT_STATE)]
		self._XInput_.XInputGetState.restype = DWORD

	def GetState(self, dwUserIndex):
		
		state = XINPUT_STATE()
		ret = self._XInput_.XInputGetState(dwUserIndex, byref(state))
		if ret:
			raise WinError(ret)

		return state.dwPacketNumber, state.Gamepad


if __name__ == "__main__":
	xi = XInput()
	from time import sleep
	for x in range(XUSER_MAX_COUNT):
		try:
			print(f"Reading input from controller {x}")
			print(xi.GetState(1))
		except Exception as e:
			print(f"Controller {x} not available: {e}")

	print("Reading all inputs from gamepad 0")
	while True:
		# print(xi.GetState(0)[1], end="     \r")
		sleep(0.001)


	# fn1
		if xi.GetState(0)[1].B.L_T and state[190] == 0:
			#keyboard.press()
			state[190] = 1
		if xi.GetState(0)[1].B.L_T == 0 and state[190] == 1:
			#keyboard.release("fn")
			state[190] = 0
	# fn2
		if xi.GetState(0)[1].B.R_T and state[192] == 0:
			#keyboard.press("fn")
			state[192] = 1
		if xi.GetState(0)[1].B.R_T == 0 and state[192] == 1:
			#keyboard.release("fn")
			state[192] = 0
	# DEL

	# DEL


	# screen it
	# 
		if xi.GetState(0)[1].TRY > 20000:
			print("L2: q Q -    R2: . ? ! L1: k K 2    R1: | ^ \\", end="     \r")
			# 
		if xi.GetState(0)[1].TRY > 20000:
			print("L2: q Q -    R2: . ? ! L1: k K 2    R1: | ^ \\", end="     \r")
				# 
		if xi.GetState(0)[1].TRY > 20000:
			print("L2: q Q -    R2: . ? ! L1: k K 2    R1: | ^ \\", end="     \r")
				# 
		if xi.GetState(0)[1].TRY > 20000:
			print("L2: q Q -    R2: . ? ! L1: k K 2    R1: | ^ \\", end="     \r")
				# 
		if xi.GetState(0)[1].TRY > 20000:
			print("L2: q Q -    R2: . ? ! L1: k K 2    R1: | ^ \\", end="     \r")
				# 
		if xi.GetState(0)[1].TRY > 20000:
			print("L2: q Q -    R2: . ? ! L1: k K 2    R1: | ^ \\", end="     \r")
				# 
		if xi.GetState(0)[1].TRY > 20000:
			print("L2: q Q -    R2: . ? ! L1: k K 2    R1: | ^ \\", end="     \r")
				# 
		if xi.GetState(0)[1].TRY > 20000:
			print("L2: q Q -    R2: . ? ! L1: k K 2    R1: | ^ \\", end="     \r")

	#  on L1
		if xi.GetState(0)[1].B.L_S and state[0] == 0:
			#Right Top
			if xi.GetState(0)[1].TRY > 20000:
				writeCorrectInput("k","K","2")
			#Right Bot
			elif xi.GetState(0)[1].TRY < -20000:
				writeCorrectInput("x","X","4")
			#Right Right
			elif xi.GetState(0)[1].TRX > 20000:
				writeCorrectInput("y","y","3")
			#Right Left
			elif xi.GetState(0)[1].TRX < -20000:
				writeCorrectInput("u","U","1")
			#Left Left
			elif xi.GetState(0)[1].TLX < -20000:
				writeCorrectInput("l","L","")
			#Left Up
			elif xi.GetState(0)[1].TLY > 20000:
				writeCorrectInput("(","@",")")
			#Left Down
			elif xi.GetState(0)[1].TLY < -20000:
				writeCorrectInput("w","W","#")
			#Left Right
			elif xi.GetState(0)[1].TLX > 20000:
				writeCorrectInput("<","",">")
			#neutral
			else:
				writeCorrectInput("a","A","0")
			state[0] = 1
		if xi.GetState(0)[1].B.L_S == 0 and state[0] == 1:
			state[0] = 0
	# on R1
		if xi.GetState(0)[1].B.R_S and state[1] == 0:
			#Right Top
			if xi.GetState(0)[1].TRY > 20000:
				writeCorrectInput("|","^","\\")
			#Right Bot
			elif xi.GetState(0)[1].TRY < -20000:
				writeCorrectInput("'","%","\"")
			#Right Right
			elif xi.GetState(0)[1].TRX > 20000:
				writeCorrectInput("z","Z","")
			#Right Left
			elif xi.GetState(0)[1].TRX < -20000:
				writeCorrectInput("v","V","")
			#Left Up
			elif xi.GetState(0)[1].TLY > 20000:
				writeCorrectInput("c","C","7")
			#Left Down
			elif xi.GetState(0)[1].TLY < -20000:
				writeCorrectInput("m","M","9")
			#Left Right
			elif xi.GetState(0)[1].TLX > 20000:
				writeCorrectInput("s","S","8")
			#Left Left
			elif xi.GetState(0)[1].TLX < -20000:
				writeCorrectInput("g","G","6")
			#neutral
			else:
				writeCorrectInput("d","D","5")
			state[1] = 1
		if xi.GetState(0)[1].B.R_S == 0 and state[1] == 1:
			state[1] = 0
	# on R2
		if xi.GetState(0)[1].RT > 100 and state[2] == 0:
			#Right Top
			if xi.GetState(0)[1].TRY > 20000:
				writeCorrectInput(".","?","!")
			#Right Bot
			elif xi.GetState(0)[1].TRY < -20000:
				writeCorrectInput(":",";","")
			#Right Right
			elif xi.GetState(0)[1].TRX > 20000:
				writeCorrectInput(",","","")
			#Right Left
			elif xi.GetState(0)[1].TRX < -20000:
				writeCorrectInput("r","R","")
			#Left Up
			elif xi.GetState(0)[1].TLY > 20000:
				writeCorrectInput("b","B","")
			#Left Down
			elif xi.GetState(0)[1].TLY < -20000:
				writeCorrectInput("j","J","")
			#Left Right
			elif xi.GetState(0)[1].TLX > 20000:
				writeCorrectInput("o","O","")
			#Left Left
			elif xi.GetState(0)[1].TLX < -20000:
				writeCorrectInput("f","F","")
			#neutral
			else:
				writeCorrectInput("e","E","")
			state[2] = 1
		if xi.GetState(0)[1].RT == 0 and state[2] == 1:
			state[2] = 0
	# on L2
		if xi.GetState(0)[1].LT > 100 and state[3] == 0:
			#Right Top
			if xi.GetState(0)[1].TRY > 20000:
				writeCorrectInput("q","Q","-")
			#Right Bot
			elif xi.GetState(0)[1].TRY < -20000:
				writeCorrectInput("n","N","*")
			#Right Right
			elif xi.GetState(0)[1].TRX > 20000:
				writeCorrectInput("t","T","/")
			#Right Left
			elif xi.GetState(0)[1].TRX < -20000:
				writeCorrectInput("h","H","+")
			#Left Up
			elif xi.GetState(0)[1].TLY > 20000:
				writeCorrectInput("[","`","]")
			#Left Down
			elif xi.GetState(0)[1].TLY < -20000:
				writeCorrectInput("=","","$")
			#Left Right
			elif xi.GetState(0)[1].TLX > 20000:
				writeCorrectInput("{","-","}")
			#Left Left
			elif xi.GetState(0)[1].TLX < -20000:
				writeCorrectInput("p","P","_")
			#neutral
			else:
				writeCorrectInput("i","I","&")
			state[3] = 1
		if xi.GetState(0)[1].LT == 0 and state[3] == 1:
			state[3] = 0

	# on up
		if xi.GetState(0)[1].B.P_U  and state[4] == 0:
			PressCorrectInput("up","","")
			state[4] = 1
		if xi.GetState(0)[1].B.P_U == 0 and state[4] == 1:
			state[4] = 0
	# on down
		if xi.GetState(0)[1].B.P_D  and state[5] == 0:
			PressCorrectInput("down","","control")
			state[5] = 1
		if xi.GetState(0)[1].B.P_D == 0 and state[5] == 1:
			state[5] = 0
	# on right
		if xi.GetState(0)[1].B.P_R  and state[6] == 0:
			PressCorrectInput("right","","home")
			state[6] = 1
		if xi.GetState(0)[1].B.P_R == 0 and state[6] == 1:
			state[6] = 0
	# on left
		if xi.GetState(0)[1].B.P_L and state[7] == 0:
			PressCorrectInput("left","","")
			state[7] = 1
		if xi.GetState(0)[1].B.P_L == 0 and state[7] == 1:
			state[7] = 0


	# on A
		if xi.GetState(0)[1].B.A and state[191] == 0:
			PressCorrectInput("space","return","tab")
			state[191] = 1
		if xi.GetState(0)[1].B.A == 0 and state[191] == 1:
			state[191] = 0
	# on B
		if xi.GetState(0)[1].B.B and state[195] == 0:
			PressCorrectInput("backspace","delete","")
			state[195] = 1
		if xi.GetState(0)[1].B.B == 0 and state[195] == 1:
			state[195] = 0
	# on X
		if xi.GetState(0)[1].B.X > 100 and state[10] == 0:
			PressCorrectInput("right option","","")
			state[10] = 1
		if xi.GetState(0)[1].B.X == 0 and state[10] == 1:
			state[10] = 0
	# on Y
		if xi.GetState(0)[1].B.Y > 100 and state[11] == 0:
			PressCorrectInput("escape","","")
			state[11] = 1
		if xi.GetState(0)[1].B.Y == 0 and state[11] == 1:
			state[11] = 0


