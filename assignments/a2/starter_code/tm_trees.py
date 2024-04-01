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
        if len(self._subtrees) > 0:
            self._expanded = True
        else:
            self._expanded = False

        # TODO: (Task 1) Complete this initializer by doing two things:
        # 1. Initialize self._colour and self.data_size, according to the
        # docstring.
        if self._subtrees == []:
            self.data_size = data_size
        else:
            # calculate this tree's data_size
            # data_size is equal to the sum of the
            # data_size of each subtree
            self.data_size = 0
            self._expanded = False
            for sub in self._subtrees:
                self.data_size += sub.data_size

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
        # Read the handout carefully to help get started identifying base cases,
        # then write the outline of a recursive step.
        #
        # Programming tip: use "tuple unpacking assignment" to easily extract
        # elements of a rectangle, as follows.
        # x, y, width, height = rect
        if self._expanded:
            x, y, width, height = rect
            if self.data_size == 0:
                self.rect = 0, 0, 0, 0
            elif self._subtrees == [] or self._subtrees is None:
                self.rect = rect
            else:
                total_size = sum([sub.data_size for sub in self._subtrees])
                pushx, actualx, pushy, actualy = 0, 0, 0, 0
                for i in range(len(self._subtrees)):
                    percent_total = self._subtrees[i].data_size/total_size
                    if width < height:
                        if i == len(self._subtrees) - 1:
                            self._subtrees[i].update_rectangles((x + pushx, y + pushy, width, math.ceil(height * percent_total)-y))
                            actualy += height * percent_total - y
                            pushy = math.ceil(actualy)
                        else:
                            #Vertical rectangle
                            self._subtrees[i].update_rectangles((x + pushx, y + pushy, width, math.floor(height * percent_total)))
                            actualy += height * percent_total
                            pushy = math.floor(actualy)
                            # if sub._subtrees or sub._subtrees is None:
                            #     sub.update_rectangles((x + pushx, y + pushy, width, height * percent_total))
                            #     pushy += height * percent_total
                            # else:
                            #     sub.update_rectangles((x + pushx, y + pushy, width, math.floor(height * percent_total)))
                            #     pushy += math.floor(height * percent_total)

                    else:
                        if i == len(self._subtrees) - 1:
                            self._subtrees[i].update_rectangles((x + pushx, y + pushy, math.ceil(width * percent_total)-x, height))
                            actualx += width * percent_total - x
                            pushx = math.ceil(actualx)
                        else:
                            self._subtrees[i].update_rectangles((x + pushx, y + pushy, math.floor(width * percent_total), height))
                            actualx += width * percent_total
                            pushx = math.floor(actualx)
                            # if sub._subtrees or sub._subtrees is None:
                            #     sub.update_rectangles((x + pushx, y + pushy, width * percent_total, height))
                            #     pushx += width * percent_total
                            # else:
                            #     sub.update_rectangles((x + pushx, y + pushy, math.floor(width * percent_total), height))
                            #     pushx += math.floor(width * percent_total)


    def get_rectangles(self) -> List[Tuple[Tuple[int, int, int, int],
                                           Tuple[int, int, int]]]:
        """Return a list with tuples for every leaf in the displayed-tree
        rooted at this tree. Each tuple consists of a tuple that defines the
        appropriate pygame rectangle to display for a leaf, and the colour
        to fill it with.
        """
        if self._expanded:
            if not self._subtrees or self._subtrees == []:
                return [(self.rect, self._colour)]
            else:
                result = []
                for sub in self._subtrees:
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
        if self._expanded:
            x, y, width, height = self.rect
            if not self._subtrees or self._subtrees == []:
                if (x <= pos[0] <= x + width) and (y <= pos[1] <= y + height):
                    return self
                else:
                    return None
            else:
                for sub in self._subtrees:
                    if sub.get_tree_at_position(pos):
                        return sub.get_tree_at_position(pos)
                return None


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
                self._parent_tree._subtrees.remove(self)


    def change_size(self, factor: float) -> None:
        """Change the value of this tree's data_size attribute by <factor>.

        Always round up the amount to change, so that it's an int, and
        some change is made.

        Do nothing if this tree is not a leaf.
        """
        if self._subtrees is None or self._subtrees == []:
            amnt = math.ceil(self.data_size * factor)
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
        self._expanded = True

    def expand_all(self) -> None:
        self._expanded = True
        if self._subtrees == [] or self._subtrees is None:
            self._expanded = True
        else:
            for s in self._subtrees:
                s.expand_all()

    def collapse(self) -> None:
        self._expanded = False

    def collapse_all(self) -> None:
        self._expanded = False
        if self._subtrees == [] or self._subtrees is None:
            self._expanded = False
        else:
            for s in self._subtrees:
                s.collapse_all()

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
        raise NotImplementedError

    def get_suffix(self) -> str:
        """Return the string used at the end of the string representation of
        a path from the tree root to this tree.
        """
        raise NotImplementedError

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
