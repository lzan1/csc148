"""
Assignment 2: Trees for Treemap

=== CSC148 Winter 2024 ===
This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) 2024 Bogdan Simion, David Liu, Diane Horton,
                   Haocheng Hu, Jacqueline Smith

=== Module Description ===
This module contains the basic tree interface required by the treemap
visualiser. You will both add to the abstract class, and complete a
concrete implementation of a subclass to represent files and folders on your
computer's file system.
"""
from __future__ import annotations

import math
import os
from random import randint
from typing import List, Tuple, Optional


class TMTree:
    """A TreeMappableTree: a tree that is compatible with the treemap
    visualiser.

    This is an abstract class that should not be instantiated directly.

    You may NOT add any attributes, public or private, to this class.
    However, part of this assignment will involve you implementing new public
    *methods* for this interface.
    You should not add any new public methods other than those required by
    the client code.
    You can, however, freely add private methods as needed.

    === Public Attributes ===
    rect:
        The pygame rectangle representing this node in the treemap
        visualization.
    data_size:
        The size of the data represented by this tree.

    === Private Attributes ===
    _colour:
        The RGB colour value of the root of this tree.
    _name:
        The root value of this tree, or None if this tree is empty.
    _subtrees:
        The subtrees of this tree.
    _parent_tree:
        The parent tree of this tree; i.e., the tree that contains this tree
        as a subtree, or None if this tree is not part of a larger tree.
    _expanded:
        Whether or not this tree is considered expanded for visualization.

    === Representation Invariants ===
    - data_size >= 0
    - If _subtrees is not empty, then data_size is equal to the sum of the
      data_size of each subtree.

    - _colour's elements are each in the range 0-255.

    - If _name is None, then _subtrees is empty, _parent_tree is None, and
      data_size is 0.
      This setting of attributes represents an empty tree.

    - if _parent_tree is not None, then self is in _parent_tree._subtrees

    - if _expanded is True, then _parent_tree._expanded is True
    - if _expanded is False, then _expanded is False for every tree
      in _subtrees
    - if _subtrees is empty, then _expanded is False
    """

    rect: Tuple[int, int, int, int]
    data_size: int
    _colour: Tuple[int, int, int]
    _name: str
    _subtrees: List[TMTree]
    _parent_tree: Optional[TMTree]
    _expanded: bool

    def __init__(self, name: str, subtrees: List[TMTree],
                 data_size: int = 0) -> None:
        """Initialize a new TMTree with a random colour and the provided <name>.

        If <subtrees> is empty, use <data_size> to initialize this tree's
        data_size.

        If <subtrees> is not empty, ignore the parameter <data_size>,
        and calculate this tree's data_size instead.

        Set this tree as the parent for each of its subtrees.

        Precondition: if <name> is None, then <subtrees> is empty.
        """
        self.rect = (0, 0, 0, 0)
        self._name = name
        self._subtrees = subtrees[:]
        self._parent_tree = None
        self._expanded = False

        # You will change this in Task 5
        # if len(self._subtrees) > 0:
        #     for sub in self._subtrees:
        #         sub._expanded = False

        # TODO: (Task 1) Complete this initializer by doing two things:
        # 1. Initialize self._colour and self.data_size, according to the
        # docstring.
        if not self._subtrees:
            self.data_size = data_size
        else:
            self.data_size = sum([sub.data_size for sub in self._subtrees])
            # self._expanded = False

        # Initialize self._colour
        r, g, b = randint(0, 225), randint(0, 225), randint(0, 225)
        self._colour = (r, g, b)

        # 2. Set this tree as the parent for each of its subtrees.
        for sub in self._subtrees:
            sub._parent_tree = self


    def is_empty(self) -> bool:
        """Return True iff this tree is empty.
        """
        return self._name is None

    def get_parent(self) -> Optional[TMTree]:
        """Returns the parent of this tree.
        """
        return self._parent_tree

    def update_rectangles(self, rect: Tuple[int, int, int, int]) -> None:
        """Update the rectangles in this tree and its descendents using the
        treemap algorithm to fill the area defined by pygame rectangle <rect>.
        """
        # TODO: (Task 2) Complete the body of this method.
        x, y, width, height = rect
        if self.data_size == 0:
            self.rect = (0, 0, 0, 0)
        elif width > height:
            self.rect = rect
            #One var for updating start details
            pushx = x
            for i in range(len(self._subtrees)):
                if i == len(self._subtrees) - 1:
                    # The last one must make up take up all remaining space
                    updateW = width + x - pushx
                else:
                    percent_total = self._subtrees[i].data_size / self.data_size
                    updateW = math.floor(width * percent_total)
                self._subtrees[i].update_rectangles((pushx, y, updateW, height))
                pushx += updateW
        else:
            self.rect = rect
            pushy = y
            for i in range(len(self._subtrees)):
                if i == len(self._subtrees) - 1:
                    # The last one must make up take up all remaining space
                    updateH = height + y - pushy
                else:
                    percent_total = self._subtrees[i].data_size / self.data_size
                    updateH = math.floor(height * percent_total)
                self._subtrees[i].update_rectangles((x, pushy, width, updateH))
                pushy += updateH
        # Read the handout carefully to help get started identifying base cases,
        # then write the outline of a recursive step.
        #
        # Programming tip: use "tuple unpacking assignment" to easily extract
        # elements of a rectangle, as follows.
        # x, y, width, height = rect
        # if self._expanded:
        # ////
        # x, y, width, height = rect
        # #If self is not expanded
        # if self.data_size == 0:
        #     self.rect = 0, 0, 0, 0
        # #Elif self isn't expanded, or is a leaf
        # elif not self._expanded or not self._subtrees:
        #     self.rect = rect
        # else:
        #     #If self is expanded and has leaves
        #     total_size = sum([sub.data_size for sub in self._subtrees])
        #     pushx, actualx, pushy, actualy = 0, 0, 0, 0
        #     for i in range(len(self._subtrees)):
        #         percent_total = self._subtrees[i].data_size/total_size
        #         if width < height:
        #             if i == len(self._subtrees) - 1:
        #                 self._subtrees[i].update_rectangles((x + pushx, y + pushy, width, math.ceil(height * percent_total)-y))
        #                 actualy += height * percent_total - y
        #                 pushy = math.ceil(actualy)
        #             else:
        #                 #Vertical rectangle
        #                 self._subtrees[i].update_rectangles((x + pushx, y + pushy, width, math.floor(height * percent_total)))
        #                 actualy += height * percent_total
        #                 pushy = math.floor(actualy)
        #         else:
        #             if i == len(self._subtrees) - 1:
        #                 self._subtrees[i].update_rectangles((x + pushx, y + pushy, math.ceil(width * percent_total)-x, height))
        #                 actualx += width * percent_total - x
        #                 pushx = math.ceil(actualx)
        #             else:
        #                 self._subtrees[i].update_rectangles((x + pushx, y + pushy, math.floor(width * percent_total), height))
        #                 actualx += width * percent_total
        #                 pushx = math.floor(actualx)

    #Used in for rect, color in self.tree.get_rectangles()
    def get_rectangles(self) -> List[Tuple[Tuple[int, int, int, int],
                                           Tuple[int, int, int]]]:
        """Return a list with tuples for every leaf in the displayed-tree
        rooted at this tree. Each tuple consists of a tuple that defines the
        appropriate pygame rectangle to display for a leaf, and the colour
        to fill it with.
        """
        green = (0, 255, 51)
        madeItMauve = (97, 26, 79)
        #Returns the actual rectangles (color)
        #If you want to show self's subtrees
        # self._expanded = True
        if self._expanded and self._subtrees:
            # return [((0,0,100,200), green)]
            # if self._parent_tree and self._parent_tree._expanded:
            #     return [(self.rect, self._colour)]
            # else:
            # return [((0,0,100,200), (green))]
            result = []
            startx, starty = 0, 0
            self.update_rectangles(self.rect)
            for sub in self._subtrees:
                #sub.rect is (0,0,0,0) and not None. self.data size is fine though.
                # if sub.rect is not None:
                #     return [((0,0,200,200), sub._colour)]
                #Just returns self.rect
                # result.append((sub.rect, sub._colour))
                # result.append((sub.rect, sub._colour))
                result.extend(sub.get_rectangles())
            return result
        return [(self.rect, self._colour)]

    def get_tree_at_position(self, pos: Tuple[int, int]) -> Optional[TMTree]:
        """Return the leaf in the displayed-tree rooted at this tree whose
        rectangle contains position <pos>, or None if <pos> is outside of this
        tree's rectangle.

        If <pos> is on the shared edge between two or more rectangles,
        always return the leftmost and topmost rectangle (wherever applicable).
        """
        x, y, width, height = self.rect

        if not(x <= pos[0] <= x + width) or not(y <= pos[1] <= y + height):
            return None
        elif not self._expanded:
            return self
        else:
            for sub in self._subtrees:
                selected = sub.get_tree_at_position(pos)
                if selected:
                    return selected
            return self
        # if not self._subtrees:
        #     print('hoho')
        # if (self._parent_tree and self._parent_tree._expanded
        #         and not self._expanded):
        #     if (x <= pos[0] <= x + width) and (y <= pos[1] <= y + height):
        #         #When visualising
        #         # print('eee')
        #         return self
        # for sub in self._subtrees:
        #     selected  = sub.get_tree_at_position(pos)
        #     if selected:
        #         return selected
        # return None


    def update_data_sizes(self) -> int:
        """Update the data_size for this tree and its subtrees, based on the
        size of their leaves, and return the new size.

        If this tree is a leaf, return its size unchanged.
        """
        # TODO: (Task 4) Complete the body of this method.
        if self._subtrees is None or self._subtrees == []:
            return self.data_size
        else:
            return sum([sub.update_data_sizes() for sub in self._subtrees])


    def move(self, destination: TMTree) -> None:
        """If this tree is a leaf, and <destination> is not a leaf, move this
        tree to be the last subtree of <destination>. Otherwise, do nothing.
        """
        # TODO: (Task 4) Complete the body of this method.
        if self._subtrees is None or self._subtrees == []:
            if destination._subtrees is not None and destination._subtrees != []:
                destination._subtrees.append(self)
                destination.data_size += self.data_size
                if self._parent_tree:
                    self._parent_tree._subtrees.remove(self)


    def change_size(self, factor: float) -> None:
        """Change the value of this tree's data_size attribute by <factor>.

        Always round up the amount to change, so that it's an int, and
        some change is made.

        Do nothing if this tree is not a leaf.
        """
        if not self._subtrees:
            if self.data_size == 0:
                if factor > 0:
                    self.data_size = 0
                else:
                    self.data_size = 1
            else:
                if factor > 0:
                    amnt = math.ceil(self.data_size * (1 + factor))
                else:
                    amnt = math.floor(self.data_size * (1 + factor))
                self.data_size = amnt

    def delete_self(self) -> bool:
        """Removes the current node from the visualization and
        returns whether the deletion was successful.

        Only do this if this node has a parent tree.

        Do not set self._parent_tree to None, because it might be used
        by the visualiser to go back to the parent folder.
        """
        # TODO: (Task 4) Complete the body of this method
        if self._parent_tree is None:
            return False
        else:
            self._parent_tree._subtrees.remove(self)
            return True


    # TODO: (Task 5) Write the methods expand, expand_all, collapse, and
    def expand(self) -> None:
        if self._subtrees:
            self._expanded = True
        # for s in self._subtrees:
        #     s.expand()

    def expand_all(self) -> None:
        # if self._subtrees:
        #     self._expanded = True
        #     for s in self._subtrees:
        #         if s._subtrees:
        #             s.expand_all()
        if self._subtrees:
            self._expanded = True
            self.update_rectangles(self.rect)
            # Accessding any of self's subtrees gives a black screen
            # self._subtrees[0]._expanded = True
            for s in self._subtrees:
                s.expand_all()
                #s.rect = 0,0,0,0
                # s.rect = s.get_rectangles()[0]
                # s.update_rectangles(self.rect)

    def collapse(self) -> None:
        # self._expanded = False
        if not self._parent_tree:
            self._expanded = False
        else:
            self._expanded = False
            self._parent_tree._expanded = False

    def collapse_all(self) -> None:
        #If this node has no parent trees
        self.collapse()
        if self._parent_tree:
            self.update_rectangles(self.rect)
            self._parent_tree.collapse_all()

        # if self._subtrees == [] or self._subtrees is None:
        #     self._expanded = False
        # else:
        #     for s in self._subtrees:
        #         s.collapse_all()

    # TODO: collapse_all, and add the displayed-tree functionality to the
    # TODO: methods from Tasks 2 and 3

    # Methods for the string representation
    def get_path_string(self) -> str:
        """
        Return a string representing the path containing this tree
        and its ancestors, using the separator for this OS between each
        tree's name.
        """
        if self._parent_tree is None:
            return self._name
        else:
            return self._parent_tree.get_path_string() + \
                self.get_separator() + self._name

    def get_separator(self) -> str:
        """Return the string used to separate names in the string
        representation of a path from the tree root to this tree.
        """
        return ':'

    def get_suffix(self) -> str:
        """Return the string used at the end of the string representation of
        a path from the tree root to this tree.
        """
        if not self._subtrees:
            return ' (Paper)'
        else:
            return ' (Category)'


class FileSystemTree(TMTree):
    """A tree representation of files and folders in a file system.

    The internal nodes represent folders, and the leaves represent regular
    files (e.g., PDF documents, movie files, Python source code files, etc.).

    The _name attribute stores the *name* of the folder or file, not its full
    path. E.g., store 'assignments', not '/Users/Diane/csc148/assignments'

    The data_size attribute for regular files is simply the size of the file,
    as reported by os.path.getsize.
    """
    def __init__(self, path: str) -> None:
        """Store the file tree structure contained in the given file or folder.

        Precondition: <path> is a valid path for this computer.
        """
        # Remember that you should recursively go through the file system
        # and create new FileSystemTree objects for each file and folder
        # encountered.
        #
        # Also remember to make good use of the superclass constructor!
        # TODO: (Task 1) Implement the initializer
        # if not os.path.isdir(path):
        #     super().__init__(os.path.basename(path), [], os.path.getsize(path))
        # else:
        #     sub = [FileSystemTree(os.path.join(path, filepath))
        #                           for filepath in os.listdir(path)]
        #     super().__init__(os.path.basename(path), sub, os.path.getsize(path))

        if os.path.isdir(path):
            sub = []
            for filename in os.listdir(path):
                # filename = directory in list of directories
                # Joins all other dirs/files under the current path
                next_path = os.path.join(path, filename)
                sub.append(FileSystemTree(next_path))
            super().__init__(os.path.basename(path), sub, os.path.getsize(path))
        else:
            super().__init__(os.path.basename(path), [], os.path.getsize(path))


        # result = FileSystemTree(path)
        # if os.path.isdir(path):
        #     direct = os.listdir(path)
        #     super().__init__(direct[0], [])
        #     for filename in direct:
        #         subitem = os.path.join(path, filename)
        #         if os.path.isdir(subitem):
        #             nextpath = ''.join(direct[1:])
        #             self._subtrees.append(super().__init__(
        #                 os.path.basename(nextpath), [], os.path.getsize(nextpath)))
        # else:
        #     super().__init__(os.path.basename(path), [], os.path.getsize(path))

        # direct = os.listdir(path)
        # # If is file (leaf): create new FileSystemTree objects for each file
        # if len(direct) == 1:
        #      a = FileSystemTree(path)
        # else:
        #     # If folder, create new FileSystemTree object for each folder
        #     if os.path.isdir(direct[0]):
        #         a = FileSystemTree(path)
        #         a._subtrees.append(FileSystemTree(''.join(direct[1:])))
        #     else:
        #         pass



    def get_separator(self) -> str:
        """Return the file separator for this OS.
        """
        return os.sep

    def get_suffix(self) -> str:
        """Return the final descriptor of this tree.
        """

        def convert_size(data_size: float, suffix: str = 'B') -> str:
            suffixes = {'B': 'kB', 'kB': 'MB', 'MB': 'GB', 'GB': 'TB'}
            if data_size < 1024 or suffix == 'TB':
                return f'{data_size:.2f}{suffix}'
            return convert_size(data_size / 1024, suffixes[suffix])

        components = []
        if len(self._subtrees) == 0:
            components.append('file')
        else:
            components.append('folder')
            components.append(f'{len(self._subtrees)} items')
        components.append(convert_size(self.data_size))
        return f' ({", ".join(components)})'


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'allowed-import-modules': [
            'python_ta', 'typing', 'math', 'random', 'os', '__future__'
        ]
    })
