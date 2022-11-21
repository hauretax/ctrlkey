

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
# keyboard.press_and_release("shift+p")
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
		print(xi.GetState(0)[1], end="     \r")
		sleep(0.001)






	# SHIFT
		if xi.GetState(0)[1].B.R_T and state[190] == 0:
			keyboard.press("shift")
			state[190] = 1
		if xi.GetState(0)[1].B.R_T == 0 and state[190] == 1:
			keyboard.release("shift")
			state[190] = 0
	# DEL
		if xi.GetState(0)[1].B.B and state[195] == 0:
			keyboard.press("backspace")
			state[195] = 1
		if xi.GetState(0)[1].B.B == 0 and state[195] == 1:
			state[195] = 0
	# DEL
		if xi.GetState(0)[1].B.A and state[191] == 0:
			keyboard.press("space")
			state[191] = 1
		if xi.GetState(0)[1].B.A == 0 and state[191] == 1:
			state[191] = 0

	#  abcde uvwx
		if xi.GetState(0)[1].B.L_S and state[0] == 0:
			if xi.GetState(0)[1].TRY > 20000:
				keyboard.press("b")
			elif xi.GetState(0)[1].TRY < -20000:
				keyboard.press("c")
			elif xi.GetState(0)[1].TRX > 20000:
				keyboard.press("d")
			elif xi.GetState(0)[1].TRX < -20000:
				keyboard.press("e")
			elif xi.GetState(0)[1].TLY > 20000:
				keyboard.press("u")
			elif xi.GetState(0)[1].TLY < -20000:
				keyboard.press("v")
			elif xi.GetState(0)[1].TLX > 20000:
				keyboard.press("w")
			elif xi.GetState(0)[1].TLX < -20000:
				keyboard.press("x")
			else:
				keyboard.press("a")
			state[0] = 1
		if xi.GetState(0)[1].B.L_S == 0 and state[0] == 1:
			state[0] = 0
	# fghij yz
		if xi.GetState(0)[1].B.R_S and state[1] == 0:
			if xi.GetState(0)[1].TRY > 20000:
				keyboard.press("g")
			elif xi.GetState(0)[1].TRY < -20000:
				keyboard.press("h")
			elif xi.GetState(0)[1].TRX > 20000:
				keyboard.press("i")
			elif xi.GetState(0)[1].TRX < -20000:
				keyboard.press("j")
			elif xi.GetState(0)[1].TLY > 20000:
				keyboard.press("y")
			elif xi.GetState(0)[1].TLY < -20000:
				keyboard.press("z")
			else:
				keyboard.press("f")
			state[1] = 1
		if xi.GetState(0)[1].B.R_S == 0 and state[1] == 1:
			state[1] = 0
	# klmno
		if xi.GetState(0)[1].RT > 100 and state[2] == 0:
			if xi.GetState(0)[1].TRY > 20000:
				keyboard.press("l")
			elif xi.GetState(0)[1].TRY < -20000:
				keyboard.press("m")
			elif xi.GetState(0)[1].TRX > 20000:
				keyboard.press("n")
			elif xi.GetState(0)[1].TRX < -20000:
				keyboard.press("o")
			else:
				keyboard.press("k")
			state[2] = 1
		if xi.GetState(0)[1].RT == 0 and state[2] == 1:
			state[2] = 0
	# pqrst
		if xi.GetState(0)[1].LT > 100 and state[3] == 0:
			if xi.GetState(0)[1].TRY > 20000:
				keyboard.press("q")
			elif xi.GetState(0)[1].TRY < -20000:
				keyboard.press("r")
			elif xi.GetState(0)[1].TRX > 20000:
				keyboard.press("s")
			elif xi.GetState(0)[1].TRX < -20000:
				keyboard.press("t")
			else:
				keyboard.press("p")
			state[3] = 1
		if xi.GetState(0)[1].LT == 0 and state[3] == 1:
			state[3] = 0


