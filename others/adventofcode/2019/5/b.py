#!/usr/bin/env python3

import sys

input_values = [5]

def read_input_value():
	if len(input_values) > 0:
		return input_values.pop(0)
	else:
		raise Exception("No more values in input")
	

def read_input():
	with open("input.txt", "r") as f:
		content = f.read()
		values = content.split(",")
		return list(map(int, values))
		
def op_sum(p, state, mp1=0, mp2=0, mp3=0):
	pos1 = state[p+1]
	pos2 = state[p+2]
	pos3 = state[p+3]
	
	val1 = state[pos1] if mp1 == 0 else state[p+1]
	val2 = state[pos2] if mp2 == 0 else state[p+2]
	
	id3 = pos3 if mp3 == 0 else p+3
	state[id3] = val1 + val2
	
	return (p+4, state)
	
def op_mult(p, state, mp1=0, mp2=0, mp3=0):
	
	pos1 = state[p+1]
	pos2 = state[p+2]
	pos3 = state[p+3]
	
	val1 = state[pos1] if mp1 == 0 else state[p+1]
	val2 = state[pos2] if mp2 == 0 else state[p+2]
	
	id3 = pos3 if mp3 == 0 else p+3
	state[id3] = val1 * val2
	
	return (p+4, state)
	
def op_input(p, state, mp1=None, mp2=None, mp3=None):
	input_value = read_input_value()
	
	pos1 = state[p+1]
	state[pos1] = input_value
	
	return (p+2, state)
	
def op_output(p, state, mp1=None, mp2=None, mp3=None):
	pos1 = state[p+1]
	value = state[pos1]
	print(">>>", value)
	return (p+2, state)
	
def op_jump_if_true(p, state, mp1=None, mp2=None, mp3=None):
	pos1 = state[p+1]
	pos2 = state[p+2]
	
	val1 = state[pos1] if mp1 == 0 else state[p+1]
	val2 = state[pos2] if mp2 == 0 else state[p+2]
	
	new_pos = p+3
	if int(val1) != 0:
		new_pos = int(val2)
	return (new_pos, state)
	
def op_jump_if_false(p, state, mp1=None, mp2=None, mp3=None):
	pos1 = state[p+1]
	pos2 = state[p+2]
	
	val1 = state[pos1] if mp1 == 0 else state[p+1]
	val2 = state[pos2] if mp2 == 0 else state[p+2]
	
	new_pos = p+3
	if int(val1) == 0:
		new_pos = int(val2)
	return (new_pos, state)
	
def op_less_than(p, state, mp1=None, mp2=None, mp3=None):
	pos1 = state[p+1]
	pos2 = state[p+2]
	pos3 = state[p+3]
	
	val1 = state[pos1] if mp1 == 0 else state[p+1]
	val2 = state[pos2] if mp2 == 0 else state[p+2]
	
	id3 = pos3 if mp3 == 0 else p+3
	
	if val1 < val2:
		state[id3] = 1
	else:
		state[id3] = 0
	
	return (p+4, state)
	
def op_equals(p, state, mp1=None, mp2=None, mp3=None):
	pos1 = state[p+1]
	pos2 = state[p+2]
	pos3 = state[p+3]
	
	val1 = state[pos1] if mp1 == 0 else state[p+1]
	val2 = state[pos2] if mp2 == 0 else state[p+2]
	
	id3 = pos3 if mp3 == 0 else p+3
	
	if val1 == val2:
		state[id3] = 1
	else:
		state[id3] = 0
	
	return (p+4, state)
	
def op_halt(p, state, mp1=None, mp2=None, mp3=None):
	return (-1, state)
	
def get_op_handler(op_code):
	if op_code == 1:
		return op_sum
	elif op_code == 2:
		return op_mult
	elif op_code == 3:
		return op_input
	elif op_code == 4:
		return op_output
	elif op_code == 5:
		return op_jump_if_true
	elif op_code == 6:
		return op_jump_if_false
	elif op_code == 7:
		return op_less_than
	elif op_code == 8:
		return op_equals
	elif op_code == 99:
		return op_halt
	else:
		raise NotImplementedError("op_code {} not implemeted".format(op_code))
		
def read_op_code(raw_op_code):
	s_i = "{}".format(raw_op_code)
	if len(s_i) == 1 or len(s_i) == 2:
		return (raw_op_code, 0, 0, 0)
	elif len(s_i) == 3:
		op_code = int(s_i[-2:])
		m1 = int(s_i[0])
		return (op_code, m1, 0, 0)
	elif len(s_i) == 4:
		op_code = int(s_i[-2:])
		m1 = int(s_i[1])
		m2 = int(s_i[0])
		return (op_code, m1, m2, 0)
	elif len(s_i) == 5:
		op_code = int(s_i[-2:])
		m1 = int(s_i[2])
		m2 = int(s_i[1])
		m3 = int(s_i[0])
		return (op_code, m1, m2, m3)
	else:
		raise Exception("Incorrect op_code: {}".format(raw_op_code))
		
def execute(machine_code):
	it = 0
	last_pos_code = len(machine_code)
	while it < last_pos_code:
		(op_code, mode_1, mode_2, mode_3) = read_op_code(machine_code[it])
		op_handler = get_op_handler(op_code)
		(new_it, new_state) = op_handler(it, machine_code, mode_1, mode_2, mode_3)
		
		if new_it < 0:
			return new_state
		else:
			it = new_it
			machine_code = new_state
		
	return machine_code
	
if __name__ == "__main__":
	machine_code = read_input()
	execute(machine_code)
	
