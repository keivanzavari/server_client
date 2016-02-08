#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
KEIVAN . ZAVARI @ FRSROBOTICS.COM
"""
#import matplotlib as mpl
#mpl.use("pgf")
#pgf_with_pdflatex = {
#    "pgf.texsystem": "pdflatex",
#    "pgf.preamble": [
#         r"\usepackage[utf8x]{inputenc}",
#         r"\usepackage[T1]{fontenc}",
#         r"\usepackage{cmbright}",
#         ]
#}
#mpl.rcParams.update(pgf_with_pdfla<=tex)



#plt.rcParams['backend'] = 'svg' #['GTK', 'GTKAgg', 'GTKCairo', 'FltkAgg', 'MacOSX', 'QtAgg', 'Qt4Agg',
#'TkAgg', 'WX', 'WXAgg', 'CocoaAgg', 'agg', 'cairo', 'emf', 'gdk', 'pdf',
#'ps', 'svg', 'template']


# ------------------------------------------------
# Sine generation
# ------------------------------------------------



def gen_profile_sine(profile):
        # import necessary libraries
        import numpy as np
        import matplotlib.pyplot as plt

        # set the constants
        fs = profile.sampling       # sampling freq of the system [Hz]
        t_final = profile.t_final	# duration of the sine wave [sec]

        t_ext = 1	    # extension time [sec]
        dband_x  = 0.0    # sec

        freq = profile.freq # sine wave frequency

        ts = 1.0/fs     # sampling time [sec]    
        t = np.arange(0,t_final+ts,ts)


        # determine how many periods we will have
        no_periods = np.ceil(t_final*freq) 

        print 'The number of periods', no_periods

        # make the vector 
        sine_range = np.linspace(0.0, (no_periods*2*np.pi) ,no_periods/(freq*ts))

        # make the sine wave
        sine_wave = np.sin(sine_range)

        # scale the sine wave
        sine_des = profile.amp*sine_wave  #np.concatenate([part1_l, part2, part3])

        cosine_wave = np.gradient(sine_des,ts)


        # extending the vectors
        # ------------------------
        if profile.ext:
                ext_zero = np.zeros(t_ext*fs)
                sine_des    = np.concatenate([sine_des[0]*ext_zero, sine_des,sine_des[0]*ext_zero])
                t = np.linspace(0,len(sine_des)/fs,len(sine_des))

        if True:
                #plt.figure()
                sine_wave_plt = plt.plot(t,sine_des,'-*',linewidth=3.0)
                plt.grid(True)
                plt.ylabel('Sine Wave')
                #plt.setp(sinewave,linestyle='--',linewidth=2.0)
                plt.savefig('sine_wave.png')
                plt.show()


        return sine_des , t
