#-------------------------------------------------------------------------------
# Name:        netWork
# Purpose:     Tools for network-based project management
#
# Author:      Sudeep De
#
# Created:     06/08/2014
# Copyright:   (c) Sudeep 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

indentation_character = "\t"

class TreeError(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

class Tree():

	file_data = None
	file_lines = None
	name = None
	nodes = [] # List of nodes in the tree
	root_id = None # Root node ID
	current_node_id = 0

	def __init__(self, file_data, name=None):
		self.file_data = file_data
		self.file_lines = file_data.split("\n")
		if len(self.file_lines) <= 0:
			raise TreeError("No task lines in the document")
		if name is not None:
			self.name = name
		else:
			self.name = file_lines[0].replace("\t", "")

	def add_node(self, name, id, parent_node=None):
		current_id = self.current_node_id
		self.nodes.append(Node(name=name, id=current_id, parent_node=parent_node))
		self.current_node_id = self.current_node_id + 1

	def get_node_by_name(self, name):
		for node in self.nodes:
			if node.name == name:
				return node
		return None

	# Builds a tree from an indented WBS text file
	# Returns a built tree
	def build_tree(self):
	    for i in range(len(self.file_lines)):
	    	current_line = self.file_lines[i]
	    	num_indents = current_line.count(indentation_character)
	    	task_name = current_line.replace(indentation_character,"")
	        if i == 0: # Root node
	            self.add_node(name=task_name, id=self.current_node_id) # initializes tree with root task
	       	else: # all other nodes
	       		# Find parent node
	       		j = i
	       		parent_node_name = None
	       		while j >= 0:
	       			parent_candidate = self.file_lines[j]
	       			parent_candidate_indents = parent_candidate.count(indentation_character)
	       			if parent_candidate_indents == num_indents - 1:
	       				parent_node_name = self.file_lines[j]
	       				break
       				else:
       					j = j - 1
       			parent_node = self.get_node_by_name(parent_node_name)
       			self.add_node(name=task_name, id=self.current_node_id, parent_node=parent_node)
		print "Done building tree!"


class Node():
	# instance variables
	id = None
	parent = None
	parent_node = None
	child_ids = []
	name = None
	num_indents = 0

	def __init__(self, name, id, parent_node, num_indents=None):
		self.name = name
		self.parent_node = parent_node
		self.id = id
		if num_indents is not None:
			self.num_indents = num_indents


# Testing

filepath = "C:\\Users\\Sudeep\\Documents\\GitHub\\netWork\\wbs_working.txt"
data = open(filepath, 'r')
data = data.read()

tree = Tree(name="Reelio Product Development", file_data=data)
tree.build_tree()
