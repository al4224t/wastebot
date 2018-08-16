# coding:utf-8
#
# Python 2.7
# controller.py
#
# Created 30/07/2018
# Kohei Motoya, University of Glasgow

"""
Module for the controller of the heatbed which use the PID control method.
"""
import numpy as np

class Controller(object):
    """
    Controller class which use the PID controlling method.

    The instance of this class reads the prosess variable and try to 
    control the manipulative variable.

    In addition, this class can be called from wastebot.heatbed module. 
    (Please see the "Examples" section for details.)

    Parameters
    ----------
        params: dictionary
            The parameters of this controller class.
            This dictionary must contain the following keys and values corresponding to these keys.
            
            * sv: float
                The set variable. In other words, target value of the manipulative variable (unit: arbitrary).
                This value must be within the pv_range.
            
            * pv_range: numpy.ndarray[float]
                The range of the process variable (unit: arbitrary).
                This range is stored in the 1D numpy array of which storing format is [min, max].
            
            * mv_max: float
                The max value of the manipulative variable (unit: arbitrary). 
                Note that this class is assuming that the min value of the manipulative variable is 0.
            
            * prop_band: float
                The proportional band (unit: %). This class is assuiming that the range of prop_band must be (0, 100].
            
            * integral_time: float
                The integral time (unit: sampling points). This value must be a positive value.
            
            * derivative_time: float
                The derivative time (unit: sampling points). This value must be a positive value.

            * initial_pv: float
                The initial value of the process variable (unit: arbitrary). This value must be within the pv_range.

    Note
    ----
    **PID control**

    * **P** is the initial of "Proportional".

    * **I** is the initial of "Integral".

    * **D** is the initial of "Derivative".

    Following formula represents the PID control.

    .. math::
        e(t) = sv(t) - pv(t)

    .. math::    
        mv(t) = \\frac{100}{PB} \\left[ e(t) + \\frac{1}{T_{I}} \\int e(t) dt + T_{D} \\frac{d}{dt} e(t)  \\right]

    Note that :math:`t` represents the time.
     
    * :math:`sv(t)` is the set variable. In other words, target value of the manipulative variable.

    * :math:`pv(t)` is the process variable. For example, temperature and degree etc. 

    * :math:`e(t)` is the error between sv and pv.

    * :math:`mv(t)` is the manipulative variable. For example, power and torque etc. 

    * :math:`PB` is the proportional band (unit: %).

    * :math:`T_{I}` is the integral time.

    * :math:`T_{D}` is the derivative time.
    """

    def __init__(self, params):

        keys = ["sv", "pv_range", "mv_max", "prop_band", "integral_time", "derivative_time"]

        for key in keys:
            if not key in params:
                raise KeyError(key)
            setattr(self, "_" + key, params[key])

        # check sv
        assert isinstance(self._sv, float), "type of sv must be float"

        # check pv_range
        assert isinstance(self._pv_range, np.ndarray), "pv_range must be a numpy.ndarray."
        assert self._pv_range.shape == (2,), "The shape of pv_range must be (2,)."
        assert self._pv_range.dtype == float, "type of pv_range must be a numpy.ndarray[float]."
        assert self._pv_range[1] > self._pv_range[0], "pv_range must be monotonically increasing array."

        # check "sv is in pv_range"
        assert self._sv >= self._pv_range[0], "sv must be higher than pv_range[0]."
        assert self._sv <= self._pv_range[1], "sv must be lower than pv_range[1]."

        # check mv_max
        assert isinstance(self._mv_max, float), "type of mv_max must be float."
        assert self._mv_max > 0, "mv_max must be positive value."

        # check prop_band
        assert isinstance(self._prop_band, float), "type of prop_band must be float."
        assert self._prop_band > 0, "prop_band must be positive value."
        assert self._prop_band <= 100, "max value of prop_band is 100."

        # check integral_time
        assert isinstance(self._integral_time, float), "type of integral_time must be float."
        assert self._integral_time > 0, "integral_time must be positive value."

        # check derivative_time
        assert isinstance(self._derivative_time, float), "type of derivative_time must be float."
        assert self._derivative_time > 0, "derivative_time must be positive value."

        # check initial_pv
        assert isinstance(params["initial_pv"], float), "type of initial_pv must be float."
        assert params["initial_pv"] >= self._pv_range[0], "initial_pv must be higher than pv_range[0]."
        assert params["initial_pv"] <= self._pv_range[1], "initial_pv must be lower than pv_range[1]."
        self._pv = params["initial_pv"] # current pv

        self._integrated_error = 0.0 # integrated error

        self.__update_mv() # initialize mv and so on. 

    @property
    def sv(self):
        """
        Present set variable (unit: arbitrary). Note that if you change the sv, 
        the integrated error is reseted and the mv is updated.
        """

        return self._sv

    @sv.setter
    def sv(self, new_sv):
        """
        This setter updates the set variable. Note that if you use this function, 
        the integrated error is reseted and the mv is updated.
        """

        self._integrated_error = 0.0 # reset integrated_error
        assert isinstance(new_sv, float), "type of sv must be float."
        assert new_sv >= self._pv_range[0], "sv must be higher than pv_range[0]."
        assert new_sv <= self._pv_range[1], "sv must be lower than pv_range[1]."
        self._sv = new_sv
        self.__update_mv() # update mv

    @property
    def pv(self):
        """
        Present process variable (unit: arbitrary). Note that if you change the present pv, 
        the mv is updated.
        """
        
        return self._pv

    @pv.setter
    def pv(self, new_pv):
        """
        This setter updates the current process variable. Note that if you use this function, 
        the mv is updated.
        """
        assert isinstance(new_pv, float), "type of pv must be float."
        assert new_pv >= self._pv_range[0], "pv must be higher than pv_range[0]."
        assert new_pv <= self._pv_range[1], "pv must be lower than pv_range[1]."

        self._pv = new_pv
        self.__update_mv() # updates mv

    def __update_mv(self):
        """
        This function updates the current manipulative variable.
        """

        pv_range_width = self._pv_range[1] - self._pv_range[0]

        # calculate proportional band limits
        prop_band_width = pv_range_width * self._prop_band / 100.0
        prop_band_lim = np.array([self._sv-prop_band_width/2, self._sv + prop_band_width/2])

        # Calculate normalized error (Proportional action)
        error = (self._sv - self._pv) / pv_range_width # normalized error

        # Integral action
        if (self._pv >= prop_band_lim[0]) and (self._pv <= prop_band_lim[1]):
            # inside of proportional band
            # Now, we're using "Anti Reset Windup"
            self._integrated_error = self._integrated_error + error

        integral_term = self._integrated_error / self._integral_time

        # Derivative action
        if hasattr(self, "_past_error") == False:
            self._past_error = error # -> error_gradinet = 0 -> no derivative action

        error_gradinet = (error - self._past_error) # normalized error gradinet
        derivative_term = error_gradinet * self._derivative_time
        self._past_error = error # update past error

        # Calculate mv_rate (PID control)
        prop_sens = 100.0 / self._prop_band # proportional sensitivity, Kp
        mv_rate = np.clip(prop_sens * (error + integral_term + derivative_term), 0.0, 1.0)

        # Calculate mv
        self._mv = self._mv_max * mv_rate

    @property
    def mv(self):
        """
        Present manipulative variable (unit: arbitrary).
        """

        return self._mv
