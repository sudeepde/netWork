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
        self.name = name
        self.root_id = None
        self.current_node_id = 0
        self.nodes = []

    def add_node(self, name, parent_node_id=None):
        added_node = Node(name=name, id=self.current_node_id, parent_node_id=parent_node_id)
        self.nodes.append(added_node)
        if parent_node_id != None:
            parent_node = self.get_node_by_id(parent_node_id)
            added_node.set_parent_node(parent_node)
            parent_node.append_child(child=added_node)
        self.current_node_id = self.current_node_id + 1

    def get_node_by_name(self, name):
        return_val = None
        for node in self.nodes:
            if node.name == name:
                return_val = node
        return return_val

    def get_node_by_id(self, id):
        return_val = None
        for node in self.nodes:
            if node.id == id:
                return_val = node
        return return_val


    # Builds a tree from an indented WBS text file
    # Returns a built tree
    def build_tree(self):
        for i in range(len(self.file_lines)):
            current_line = self.file_lines[i]
            num_indents = current_line.count(indentation_character)
            task_name = current_line.replace(indentation_character,"")
            if i == 0: # Root node
                self.add_node(name=current_line) # initializes tree with root task
            else: # all other nodes
                # Find parent node
                j = i - 1
                parent_node_name = None
                while j >= 0:
                    parent_candidate = self.file_lines[j]
                    parent_candidate_indents = parent_candidate.count(indentation_character)
                    if parent_candidate_indents == num_indents - 1:
                        parent_node_name = parent_candidate
                        break
                    else:
                        j = j - 1
                parent_node_id = self.get_node_by_name(parent_node_name).id
                self.add_node(name=current_line, parent_node_id=parent_node_id)

    # Return a list of leaf nodes
    def get_leaves(self):
        leaves = []
        for node in self.nodes:
            if len(node.children) == 0:
                leaves.append(node)
        return leaves

    def send_leaves_to_file(self, filename):
        f = open(filename, 'w')
        leaves = self.get_leaves()
        file_data = []
        for i in range(len(leaves)):
            file_line = str(i) + " " + leaves[i].task_name
            file_data.append(file_line)
        file_data
        file_data = '\n'.join(str(x) for x in file_data)
        file_data = file_data + "\n#\n"
        f.write(file_data)
        f.close()

    def create_node_path_names(self):
        for node in self.nodes:
            if node.parent_node_id is not None:
                break


class Node():

    # instance variables
    id = None
    parent_node = None
    parent_node_id = None
    children = []
    name = None # the task name including indents
    num_indents = 0
    task_name = None # the task name not including indents

    def __init__(self, name, id, parent_node_id=None, num_indents=None):
        if not isinstance(parent_node_id, int) and parent_node_id is not None:
            raise TreeError("parent_node_id is not an integer: %s" % parent_node_id)
        else:
            self.name = name
            self.task_name = name.replace('\t','')
            self.parent_node_id = parent_node_id
            self.id = id
            self.children = []
            self.parent_node = None
            self.num_indents = num_indents

    def set_parent_node(self, parent_node):
        self.parent_node = parent_node

    def append_child(self, child):
        print self.name
        print child
        self.children.append(child)


# Testing

filepath = "C:\\Users\\Sudeep\\Documents\\GitHub\\netWork\\wbs_working.txt"
data = open(filepath, 'r')
data = data.read()

# tree = Tree(name="Reelio Product Development", file_data=data)
# tree.build_tree()
# leaves = tree.get_leaves()
# print"Number of leaves: ", len(leaves)

tree = Tree(name="Reelio Product Development", file_data=data)
tree.build_tree()
tree.send_leaves_to_file("C:\\Users\\Sudeep\\Desktop\\test.tgf")
# tree.add_node("master")
# print tree.current_node_id
# tree.add_node("child node 1", parent_node_id=tree.get_node_by_name("master").id)
# print tree.current_node_id
# tree.add_node("child node 2", parent_node_id=tree.get_node_by_name("master").id)
# print tree.current_node_id