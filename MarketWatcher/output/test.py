# -*- coding: utf-8 -*-
"""
Created on Fri Oct 27 21:57:15 2023

@author: tani

"""
from scipy import interpolate
import numpy as np
import copy
from numba import jit, int32, float64, void, int_, double
from numba.experimental import jitclass

spec = [
    ('x', float64[:]),
    ('y', float64[:])
]

@jitclass(spec)
class Mesh(object):
    def __init__(self):
        pass

    def setValue(self, x, y):
        self.x = x
        self.y = y
        # self.interp1d = interpolate.interp1d(x, y, fill_value=(y[0], y[-1]))

    def interp(self, x):
        return np.interp(x, self.x, self.y)
        # return self.interp1d(x)

    def copy(self):
        mesh = Mesh()
        mesh.setValue(self.x, self.y)
        return mesh

@jit
def test(x, mesh):
    return mesh.interp(x)


spec = [
    ('mesh', Mesh.class_type.instance_type)
]
# @jitclass(spec)
class testClass():
    def __init__(self):
        self.mesh = Mesh()

    def __deepcopy__(self, memodict={}):
        cls = self.__class__
        result = cls.__new__(cls)
        memodict[id(self)] = result
        for k, v in self.__dict__.items():
            if hasattr(v, "_numba_type_"):
                if hasattr(v, "copy"):
                    setattr(result, k, v.copy())
                else:
                    raise ValueError(f"Can not deepcopy {k} of type <{type(v)}>: numba classes need 'copy' method defined to be copyable")
            else:
                setattr(result, k, copy.deepcopy(v, memodict))
        return result

    def deepcopy(self, memodict={}):
        return self.__deepcopy__(memodict)




if __name__  ==  '__main__':
    x = np.array([1, 2, 3, 4], dtype=float)
    y = np.array([2, 3, 4, 5], dtype=float)
    # mesh = Mesh(x, y)
    mesh = Mesh()
    mesh.setValue(x, y)
    a = test(np.array([0, 1, 1.1, 2, 3.3, 5, 6]), mesh)
    print(a)


    a = testClass()
    a.mesh.setValue(x, y)
    b = copy.deepcopy(a)

    @jit
    class Shrubbery(object):
        @void(int_, int_)
        def __init__(self, w, h):
            # All instance attributes must be defined in the initializer
            self.width = w
            self.height = h

            # Types can be explicitly specified through casts
            self.some_attr = double(1.0)

        @int_()
        def area(self):
            return self.width * self.height

        @void()
        def describe(self):
            print("This shrubbery is ", self.width,
                  "by", self.height, "cubits.")

    shrub = Shrubbery(10, 20)
    print(shrub.area())
    shrub.describe()
    print(shrub.width, shrub.height)
    shrub.width = 30
    print(shrub.area())
    print(shrub._numba_attrs._fields_) # This is an internal attribute subject to change!

    class MyClass(Shrubbery):
        def newmethod(self):
            print("This is a new method.")

    shrub2 = MyClass(30,40)
    shrub2.describe()
    shrub2.newmethod()
    print(shrub._numba_attrs._fields_)