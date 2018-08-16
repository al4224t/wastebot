# coding:utf-8
#
# Python 2.7
# heatbed.py
#
# Created 27/07/2018
# Kohei Motoya, University of Glasgow

"""
Module for imprementing the virtual heatbed.
"""

class Heatbed(object):
    """
    Virtual heatbed class.

    The instance of this class represents a virtual heatbed.
    This instance reads the input power and calculated the temperature every time.
    In this calculation, this class uses the Newton's law of cooling to estimate the heat loss amount.

    In addition, this class can be called from wastebot.heatbed.simulation module. 
    (Please see the "Examples" section for details.)
    
    Parameters
    ----------
    init_tmp: int or float
        The initial temperature of the virtual heatbed (unit: °C).
    
    capacity: int or float
        The heat capacity of the virtual heatbed (unit: J/K).

    surf_area: int ot float
        The surface area of the virtual heatbed (unit: m^2).

    init_power: int ot float
        The initail input power of the virtual heatbed (unit: W). You must set the value within the range (0, max_power].
        Otherwise, this class throw ValueError.

    max_power: int ot float
        The max input power of the virtual heatbed (unit: W).

    Examples
    --------
    >>> from wastebot.heatbed.simulation import Heatbed
    
    
    Note
    ----
    **Newton's law of cooling**

    .. math::
        -\\frac{dQ}{dt} = \\alpha S \\left( T - T_{m} \\right)

    Note that :math:`t` represents the time.

    * :math:`Q` is the thermal energy in the solid (unit: joule).
     
    * :math:`\\alpha` is the heat transfer coefficient of the medium (unit: W/(m^2 * K).

    * :math:`S` is the surface area of the solid. 

    * :math:`T` is the temperature of the the solid (unit: K).

    * :math:`T_{m}` is the temperature of the medium (unit: K).
    """

    def __init__(self, init_tmp, capacity, surf_area, init_power, max_power):
        self._tmp = float(init_tmp)
        self._capacity = float(capacity)
        self._surf_area = float(surf_area)

        if self.judge_power(init_power, max_power) == False:
            raise ValueError("power must be in the range from 0 to max_power.")

        self._power = float(init_power)
        self._max_power = float(max_power)

    @property
    def tmp(self):
        """
        Present temperature of the virtual heatbed (unit: °C).
        """

        return self._tmp

    def __get_tmp_diff(self, q):
        """
        This function estimates the amount of change of temperature
        using the input thermal energy and heat capacity of this virtual heatbed.

        Parameters
        ----------
        q: float
            The amount of input thermal energy. 

        Returns
        -------
        dt: float
            The amount of change of temperature (unit: °C).
        """
        dt = float(q) / self._capacity
        return dt

    def update_tmp(self, duration, medium_tmp, medium_htc):
        """
        This function updates the temprature of the virtual heatbed.
        This function uses the Newton's law of cooling to estimate the heat loss amount.

        Parameters
        ----------
        duration: int or float
            The reciprocal of the sampling frequency. (unit: sec)

        medium_tmp: int or float
            The temperature of the medium. (ex. the air in the room, unit: °C)

        medium_htc: int or float
            Heat transfer coefficient of the medium. (ex. the air in the room, unit: W/(m^2 * K))

        """

        q1 = self._power * float(duration) # input heat

        # Calculate the heat loss using "Newton's law of cooling"
        q2 = float(medium_htc) * (self._tmp - float(medium_tmp)) * self._surf_area * float(duration) # heat loss

        # Warning!!
        # Currently, we don't calculate the heat loss by the radiation expressly.
        # If you want to calculate he heat loss by the radiation, you must use "Stefan–Boltzmann law".

        # update the temperature of this heatbed.
        self._tmp = self._tmp + self.__get_tmp_diff(q1 - q2)

    @property
    def surf_area(self):
        """
        The surf area of the virtual heatbed. (unit: m^2)
        """
        return self._surf_area

    @property
    def capacity(self):
        """
        The heat capacity of the virtual heatbed. (unit: J/K) 
        """
        return self._capacity

    @classmethod
    def judge_power(self, power, max_power):
        """
        This function judge which the "power" is within the range (0, max_power] or not.
        If the "power" is within this range, this function returns True.
        If the "power" isn't within this range, this function returns False.

        Returns
        -------
        result: bool
            The result of the judgement.
        """
        result = True
        
        if power < 0 or power > max_power:
            return False

        return result

    @property
    def power(self):
        """
        Present input power of ths virtual heatbed. (unit: W)

        If you want to change this value, you must set the value within the range (0, max_power].
        Otherwise, this instance throw ValueError.
        """
        return self._power

    @power.setter
    def power(self, new_power):
        """
        This setter updates the input power of the virtual heatbed. Note that if you want to update the power, 
        you must set the value within the range (0, max_power]. Otherwise, this setter throw ValueError.
        """
        if self.judge_power(new_power, self._max_power) == False:
            raise ValueError("power must be in the range from 0 to max_power.")

        self._power = float(new_power)

    @property
    def max_power(self):
        """
        The max input power of heatbed. (unit: W)
        """
        return self._max_power
