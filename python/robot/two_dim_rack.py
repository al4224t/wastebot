"""
    coding: UTF-8
    Python 2.7

    two_dim_rack.py

    Created 18/06/2016
    Kevin Donkers, The Cronin Group, University of Glasgow

    Two dimensional rack of positions with set dimensions, origin and spacing
    xy - number of positions in x and y
    xyz0 - xyz coordinates of origin position
    dxyz - xyz spacings between positions
    labels - dictionary of label:[coordinates] of rack positions
    cycle - if True index reset after reaching end of rack
"""

class TwoDimRack(object):

    def __init__(self, xy, xyz0, dxyz, labels={}, cycle=True):
        self.dimensions = xy
        self.origin = xyz0
        self.spacing = dxyz
        self.labels = labels
        self.cycle = cycle
        self.current_index = [1,1]

    def get_index(self):
        return self.current_index

    def set_index(self, new_index):
        self.current_index = new_index
        return self.current_index

    def reset_index(self):
        self.current_index = [1,1]
        return self.current_index

    def next_index(self):
        '''Increment index to run through all y positions (columns) before changing x position (row)'''
        # End of rack = return to start/print message
        if self.current_index == self.dimensions:
            if self.cycle == False:
                print 'End of rack'
                return self.current_index
            self.reset_index()
        # End of row = next row
        elif self.current_index[1] == self.dimensions[1]:
            self.current_index[0] += 1
            self.current_index[1] = 0
        # Next vial in row
        else:
            self.current_index[1] += 1
        return self.current_index

    def is_label_in_labels(self, label):
        '''Returns bool if label is in labels'''
        if type(label)==str:
            if label in self.labels:
                return True
        else:
            return False

    def get_coordinates(self, index=None):
        '''Calculates coordinates of position at index'''
        if index == None:
            index = self.current_index
        elif type(index)==str:
            if self.is_label_in_labels(index):
                index = self.labels[index]
            else:
                raise Exception("{} is not a recognised label".format(index))
        if index[0]<=self.dimensions[0] or index[1]<=self.dimensions[1]:
            coord = [0,0,0]
            coord[0] = self.origin[0] + self.spacing[0] * index[0]
            coord[1] = self.origin[1] + self.spacing[1] * index[1]
            coord[2] = self.origin[2] + self.spacing[2]
            return coord
        else:
            raise Exception("Index outwith defined boundaries: {}".format(self.dimensions))
