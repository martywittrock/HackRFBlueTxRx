#!/usr/bin/env python2
##################################################
# GNU Radio Python Flow Graph
# Title: SSB Receiver
# Author: OZ9AEC Respin by KN0CK
# Description: Simple SSB receiver prototype
# Generated: Wed Nov 18 10:58:02 2015
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from gnuradio import analog
from gnuradio import audio
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import wxgui
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from gnuradio.wxgui import fftsink2
from gnuradio.wxgui import forms
from gnuradio.wxgui import waterfallsink2
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import osmosdr
import time
import wx

class ssb_rx(grc_wxgui.top_block_gui):

    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title="SSB Receiver")
        _icon_path = "/usr/share/icons/hicolor/32x32/apps/gnuradio-grc.png"
        self.SetIcon(wx.Icon(_icon_path, wx.BITMAP_TYPE_ANY))

        ##################################################
        # Variables
        ##################################################
        self.width = width = 2600
        self.samp_rate = samp_rate = 64e6/256
        self.offset_fine = offset_fine = 1
        self.offset_coarse = offset_coarse = 1
        self.freq = freq = 4.0e6
        self.center = center = +1500
        self.LO = LO = 0
        self.xlate_filter_taps = xlate_filter_taps = firdes.low_pass(1, samp_rate, 125000, 25000, firdes.WIN_HAMMING, 6.76)
        self.trans = trans = 500
        self.rx_freq = rx_freq = LO+freq+(offset_coarse+offset_fine)
        self.rf_gain = rf_gain = 10
        self.low = low = center-width/2
        self.lo_freq = lo_freq = LO
        self.high = high = center+width/2
        self.display_selector = display_selector = 1
        self.agc_decay = agc_decay = 5e-5
        self.af_gain = af_gain = 0.18

        ##################################################
        # Blocks
        ##################################################
        _trans_sizer = wx.BoxSizer(wx.VERTICAL)
        self._trans_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_trans_sizer,
        	value=self.trans,
        	callback=self.set_trans,
        	label="Trans",
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._trans_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_trans_sizer,
        	value=self.trans,
        	callback=self.set_trans,
        	minimum=100,
        	maximum=2000,
        	num_steps=190,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.GridAdd(_trans_sizer, 9, 0, 1, 1)
        self._rx_freq_static_text = forms.static_text(
        	parent=self.GetWin(),
        	value=self.rx_freq,
        	callback=self.set_rx_freq,
        	label="Receive",
        	converter=forms.float_converter(),
        )
        self.GridAdd(self._rx_freq_static_text, 5, 3, 1, 1)
        _rf_gain_sizer = wx.BoxSizer(wx.VERTICAL)
        self._rf_gain_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_rf_gain_sizer,
        	value=self.rf_gain,
        	callback=self.set_rf_gain,
        	label="RF",
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._rf_gain_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_rf_gain_sizer,
        	value=self.rf_gain,
        	callback=self.set_rf_gain,
        	minimum=1,
        	maximum=50,
        	num_steps=50,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.GridAdd(_rf_gain_sizer, 7, 1, 1, 1)
        self._display_selector_chooser = forms.drop_down(
        	parent=self.GetWin(),
        	value=self.display_selector,
        	callback=self.set_display_selector,
        	label="Spectrum",
        	choices=[0, 1],
        	labels=['Baseband','USRP'],
        )
        self.GridAdd(self._display_selector_chooser, 5, 0, 1, 1)
        self._agc_decay_chooser = forms.drop_down(
        	parent=self.GetWin(),
        	value=self.agc_decay,
        	callback=self.set_agc_decay,
        	label="AGC",
        	choices=[1e-5, 5e-5, 1e-4],
        	labels=['Fast','Medium','Slow'],
        )
        self.GridAdd(self._agc_decay_chooser, 9, 1, 1, 1)
        _af_gain_sizer = wx.BoxSizer(wx.VERTICAL)
        self._af_gain_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_af_gain_sizer,
        	value=self.af_gain,
        	callback=self.set_af_gain,
        	label="VOL",
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._af_gain_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_af_gain_sizer,
        	value=self.af_gain,
        	callback=self.set_af_gain,
        	minimum=0,
        	maximum=1.0,
        	num_steps=500,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.GridAdd(_af_gain_sizer, 8, 1, 1, 1)
        self.wxgui_waterfallsink2_0 = waterfallsink2.waterfall_sink_c(
        	self.GetWin(),
        	baseband_freq=0,
        	dynamic_range=100,
        	ref_level=0,
        	ref_scale=2.0,
        	sample_rate=samp_rate,
        	fft_size=512,
        	fft_rate=15,
        	average=False,
        	avg_alpha=None,
        	title="Waterfall Plot",
        	size=(800,300),
        )
        self.Add(self.wxgui_waterfallsink2_0.win)
        _width_sizer = wx.BoxSizer(wx.VERTICAL)
        self._width_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_width_sizer,
        	value=self.width,
        	callback=self.set_width,
        	label="Filter",
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._width_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_width_sizer,
        	value=self.width,
        	callback=self.set_width,
        	minimum=100,
        	maximum=5000,
        	num_steps=490,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.GridAdd(_width_sizer, 7, 0, 1, 1)
        self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
                interpolation=1,
                decimation=1,
                taps=None,
                fractional_bw=0.25,
        )
        self.osmosdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + "" )
        self.osmosdr_source_0.set_sample_rate(samp_rate)
        self.osmosdr_source_0.set_center_freq(rx_freq, 0)
        self.osmosdr_source_0.set_freq_corr(0, 0)
        self.osmosdr_source_0.set_dc_offset_mode(2, 0)
        self.osmosdr_source_0.set_iq_balance_mode(0, 0)
        self.osmosdr_source_0.set_gain_mode(False, 0)
        self.osmosdr_source_0.set_gain(rf_gain, 0)
        self.osmosdr_source_0.set_if_gain(20, 0)
        self.osmosdr_source_0.set_bb_gain(20, 0)
        self.osmosdr_source_0.set_antenna("", 0)
        self.osmosdr_source_0.set_bandwidth(0, 0)
          
        _offset_fine_sizer = wx.BoxSizer(wx.VERTICAL)
        self._offset_fine_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_offset_fine_sizer,
        	value=self.offset_fine,
        	callback=self.set_offset_fine,
        	label="Fine tune",
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._offset_fine_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_offset_fine_sizer,
        	value=self.offset_fine,
        	callback=self.set_offset_fine,
        	minimum=-1000,
        	maximum=1000,
        	num_steps=400,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.GridAdd(_offset_fine_sizer, 6, 0, 1, 2)
        _offset_coarse_sizer = wx.BoxSizer(wx.VERTICAL)
        self._offset_coarse_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_offset_coarse_sizer,
        	value=self.offset_coarse,
        	callback=self.set_offset_coarse,
        	label="Coarse tune",
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._offset_coarse_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_offset_coarse_sizer,
        	value=self.offset_coarse,
        	callback=self.set_offset_coarse,
        	minimum=-120000,
        	maximum=120000,
        	num_steps=960,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.GridAdd(_offset_coarse_sizer, 6, 2, 1, 2)
        self._lo_freq_static_text = forms.static_text(
        	parent=self.GetWin(),
        	value=self.lo_freq,
        	callback=self.set_lo_freq,
        	label="LO",
        	converter=forms.float_converter(),
        )
        self.GridAdd(self._lo_freq_static_text, 5, 2, 1, 1)
        self.freq_xlating_fir_filter_xxx_0 = filter.freq_xlating_fir_filter_ccc(1, (xlate_filter_taps), 0, samp_rate)
        self._freq_text_box = forms.text_box(
        	parent=self.GetWin(),
        	value=self.freq,
        	callback=self.set_freq,
        	label="USRP",
        	converter=forms.float_converter(),
        )
        self.GridAdd(self._freq_text_box, 5, 1, 1, 1)
        self.fftsink = fftsink2.fft_sink_c(
        	self.GetWin(),
        	baseband_freq=rx_freq*display_selector,
        	y_per_div=10,
        	y_divs=10,
        	ref_level=1,
        	ref_scale=13490.0,
        	sample_rate=samp_rate,
        	fft_size=512,
        	fft_rate=15,
        	average=True,
        	avg_alpha=0.5,
        	title="",
        	peak_hold=False,
        	size=(800,300),
        )
        self.GridAdd(self.fftsink.win, 0, 0, 5, 4)
        _center_sizer = wx.BoxSizer(wx.VERTICAL)
        self._center_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_center_sizer,
        	value=self.center,
        	callback=self.set_center,
        	label="Center",
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._center_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_center_sizer,
        	value=self.center,
        	callback=self.set_center,
        	minimum=-5000,
        	maximum=5000,
        	num_steps=200,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.GridAdd(_center_sizer, 8, 0, 1, 1)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vff((af_gain, ))
        self.blocks_complex_to_real_0 = blocks.complex_to_real(1)
        self.band_pass_filter = filter.fir_filter_ccc(5, firdes.complex_band_pass(
        	1, samp_rate, -high, -low, trans, firdes.WIN_HAMMING, 6.76))
        self.audio_sink_0 = audio.sink(44100, "", True)
        self.analog_agc2_xx_0 = analog.agc2_cc(1e-1, agc_decay, 1.0, 1.0)
        self.analog_agc2_xx_0.set_max_gain(65536)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_agc2_xx_0, 0), (self.rational_resampler_xxx_0, 0))    
        self.connect((self.band_pass_filter, 0), (self.analog_agc2_xx_0, 0))    
        self.connect((self.blocks_complex_to_real_0, 0), (self.blocks_multiply_const_vxx_0, 0))    
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.audio_sink_0, 0))    
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.audio_sink_0, 1))    
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.band_pass_filter, 0))    
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.fftsink, 0))    
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.wxgui_waterfallsink2_0, 0))    
        self.connect((self.osmosdr_source_0, 0), (self.freq_xlating_fir_filter_xxx_0, 0))    
        self.connect((self.rational_resampler_xxx_0, 0), (self.blocks_complex_to_real_0, 0))    


    def get_width(self):
        return self.width

    def set_width(self, width):
        self.width = width
        self.set_low(self.center-self.width/2)
        self.set_high(self.center+self.width/2)
        self._width_slider.set_value(self.width)
        self._width_text_box.set_value(self.width)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_xlate_filter_taps(firdes.low_pass(1, self.samp_rate, 125000, 25000, firdes.WIN_HAMMING, 6.76))
        self.fftsink.set_sample_rate(self.samp_rate)
        self.osmosdr_source_0.set_sample_rate(self.samp_rate)
        self.wxgui_waterfallsink2_0.set_sample_rate(self.samp_rate)
        self.band_pass_filter.set_taps(firdes.complex_band_pass(1, self.samp_rate, -self.high, -self.low, self.trans, firdes.WIN_HAMMING, 6.76))

    def get_offset_fine(self):
        return self.offset_fine

    def set_offset_fine(self, offset_fine):
        self.offset_fine = offset_fine
        self._offset_fine_slider.set_value(self.offset_fine)
        self._offset_fine_text_box.set_value(self.offset_fine)
        self.set_rx_freq(self.LO+self.freq+(self.offset_coarse+self.offset_fine))

    def get_offset_coarse(self):
        return self.offset_coarse

    def set_offset_coarse(self, offset_coarse):
        self.offset_coarse = offset_coarse
        self.set_rx_freq(self.LO+self.freq+(self.offset_coarse+self.offset_fine))
        self._offset_coarse_slider.set_value(self.offset_coarse)
        self._offset_coarse_text_box.set_value(self.offset_coarse)

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.set_rx_freq(self.LO+self.freq+(self.offset_coarse+self.offset_fine))
        self._freq_text_box.set_value(self.freq)

    def get_center(self):
        return self.center

    def set_center(self, center):
        self.center = center
        self.set_low(self.center-self.width/2)
        self.set_high(self.center+self.width/2)
        self._center_slider.set_value(self.center)
        self._center_text_box.set_value(self.center)

    def get_LO(self):
        return self.LO

    def set_LO(self, LO):
        self.LO = LO
        self.set_rx_freq(self.LO+self.freq+(self.offset_coarse+self.offset_fine))
        self.set_lo_freq(self.LO)

    def get_xlate_filter_taps(self):
        return self.xlate_filter_taps

    def set_xlate_filter_taps(self, xlate_filter_taps):
        self.xlate_filter_taps = xlate_filter_taps
        self.freq_xlating_fir_filter_xxx_0.set_taps((self.xlate_filter_taps))

    def get_trans(self):
        return self.trans

    def set_trans(self, trans):
        self.trans = trans
        self._trans_slider.set_value(self.trans)
        self._trans_text_box.set_value(self.trans)
        self.band_pass_filter.set_taps(firdes.complex_band_pass(1, self.samp_rate, -self.high, -self.low, self.trans, firdes.WIN_HAMMING, 6.76))

    def get_rx_freq(self):
        return self.rx_freq

    def set_rx_freq(self, rx_freq):
        self.rx_freq = rx_freq
        self._rx_freq_static_text.set_value(self.rx_freq)
        self.fftsink.set_baseband_freq(self.rx_freq*self.display_selector)
        self.osmosdr_source_0.set_center_freq(self.rx_freq, 0)

    def get_rf_gain(self):
        return self.rf_gain

    def set_rf_gain(self, rf_gain):
        self.rf_gain = rf_gain
        self._rf_gain_slider.set_value(self.rf_gain)
        self._rf_gain_text_box.set_value(self.rf_gain)
        self.osmosdr_source_0.set_gain(self.rf_gain, 0)

    def get_low(self):
        return self.low

    def set_low(self, low):
        self.low = low
        self.band_pass_filter.set_taps(firdes.complex_band_pass(1, self.samp_rate, -self.high, -self.low, self.trans, firdes.WIN_HAMMING, 6.76))

    def get_lo_freq(self):
        return self.lo_freq

    def set_lo_freq(self, lo_freq):
        self.lo_freq = lo_freq
        self._lo_freq_static_text.set_value(self.lo_freq)

    def get_high(self):
        return self.high

    def set_high(self, high):
        self.high = high
        self.band_pass_filter.set_taps(firdes.complex_band_pass(1, self.samp_rate, -self.high, -self.low, self.trans, firdes.WIN_HAMMING, 6.76))

    def get_display_selector(self):
        return self.display_selector

    def set_display_selector(self, display_selector):
        self.display_selector = display_selector
        self._display_selector_chooser.set_value(self.display_selector)
        self.fftsink.set_baseband_freq(self.rx_freq*self.display_selector)

    def get_agc_decay(self):
        return self.agc_decay

    def set_agc_decay(self, agc_decay):
        self.agc_decay = agc_decay
        self.analog_agc2_xx_0.set_decay_rate(self.agc_decay)
        self._agc_decay_chooser.set_value(self.agc_decay)

    def get_af_gain(self):
        return self.af_gain

    def set_af_gain(self, af_gain):
        self.af_gain = af_gain
        self._af_gain_slider.set_value(self.af_gain)
        self._af_gain_text_box.set_value(self.af_gain)
        self.blocks_multiply_const_vxx_0.set_k((self.af_gain, ))


if __name__ == '__main__':
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    (options, args) = parser.parse_args()
    tb = ssb_rx()
    tb.Start(True)
    tb.Wait()
