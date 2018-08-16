# coding:utf-8
#
# Python 2.7
# thermistor.py
#
# Created 01/08/2018
# Kohei Motoya, University of Glasgow

"""
Module for processing the output of the thermistor.
"""
import numpy as np

class ThermProc(object):
    """
    Thermistor processor class.

    The instance of this class reads the output of A/D converter 
    which is connected to the thermistor.
    After that, this instance calculates the temperature
    via "Steinhart–Hart equation".

    In addition, this class can be called from wastebot.heatbed module. 
    (Please see the "Examples" section for details.)

    Parameters
    ----------
    init_adc_outputs: numpy.ndarray[float]
        Initial A/D converter outputs which are stored in the 1D numpy array.
        The number of elements in this array corresponds to the length of moving averaging filter.
        In addition, this class is assuming that the range of these value is 0~1024(10bit, unit: arbitrary).

    rt: int ot float
        The resistance of the thermistor at 25°C (unit: ohm).

    sh_params: dictionary
        The parameters of "Steinhart–Hart" equation for the thermistor.
        This dictionary must contain the keys: "A", "B", "C" and values corresponding to these keys.
    
    rd: int or float
        The resistance of the resistor in the voltage divider (unit: ohm).

    tc: int of float
        The correction value of temperature (unit: °C, optional). Default value is 0.

    Note
    ----
    **Steinhart–Hart equation**
    (John S. Steinhart and Stanley R. Hart, 1968)

    .. math::
        \\frac{1}{T} = A + B  * \\ln{R_{therm}} + C * \\left[ \\ln{R_{therm}} \\right] ^{3}

    * :math:`T` is the thermodynamic temperature of the thermistor.

    * :math:`R_{therm}` is the resistance of the thermistor.

    * :math:`A, B, C` are the parameters of the Steinhart–Hart equation.
    
    """
    def __init__(self, init_adc_outputs, rt, sh_params, rd, tc=0.0):

        # check init_adc_outputs
        assert isinstance(init_adc_outputs, np.ndarray), "init_adc_outputs must be a numpy.ndarray."
        assert init_adc_outputs.ndim == 1, "Number of dimension of init_adc_outputs must be 1."
        assert init_adc_outputs.size != 0, "init_adc_outputs must have at least one element."
        assert init_adc_outputs.dtype == float, "type of init_adc_outputs must be a numpy.ndarray[float]."

        self._buffer = init_adc_outputs

        # check rt
        assert rt > 0, "rt must be a positive value."
        self._rt = float(rt)

        # parse sh_params
        self._therm_a = sh_params["A"]
        self._therm_b = sh_params["B"]
        self._therm_c = sh_params["C"]

        # check rd
        assert rd > 0, "rd must be a positive value."
        self._rd = float(rd)

        # check tc
        self._tc = float(tc)

    def read_adc_output(self, adc_output):
        """
        This function reads the new output of A/D converter (unit: arbitrary).
        This function is assuming that the range of this value is 0~1024.

        Parameters
        ----------
        adc_outputs : float
            Output of A/D converter. (10bit value: 0~1024)
        """
        assert isinstance(adc_output, float), "type of adc_output must be float."
        self._buffer = np.roll(self._buffer, -1)
        self._buffer[-1] = adc_output

    @property
    def adc_output(self):
        """
        Filtered output of A/D converter (unit: arbitrary).
        Currently, we're using the moving average filter.
        """
        return np.mean(self._buffer)
        
    @property
    def therm_rss(self):
        """
        Present resistance of thermistor (unit: ohm).
        """
        return self.adc_output / (1024.0 - self.adc_output) * self._rd

    @property
    def temperature(self):
        """
        Calculated temperature from outputs of A/D converter (unit: °C).
        This class uses "Steinhart–Hart equation".
        """
        return 1.0 / (self._therm_a + self._therm_b * np.log(self.therm_rss) + self._therm_c * np.log(self.therm_rss)**3) - 273.15 + self._tc

