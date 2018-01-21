
# coding: utf-8

# In[ ]:
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.gridspec import GridSpec
import math



import pymeteo.interp as interp
import skewt_modi as skewt


# In[ ]:

### Define colorbar colors
champ = 255.
blue = np.array([1,74,159])/champ           # for the date


# In[ ]:

def plot_skewT(T, Td, z, p, u, v, text, sfig, filename):
    fig = plt.figure(1, figsize=(16, 20))#, edgecolor = 'k')
    gs = GridSpec(1,12)
# sounding
    ax1 = plt.subplot(gs[0,0:11])
    skewt.plot_sounding_axes(ax1)
# plot Temperature
    linecolor_T = skewt.linecolor_T
    linewidth_T = skewt.linewidth_T
    ax1.semilogy(T + skewt.skew(p),p, basey=math.e, color =linecolor_T, linewidth = (linewidth_T+1.5))

# plot dewpoint
    linecolor_Td = skewt.linecolor_Td
    linewidth_Td = skewt.linewidth_Td
    ax1.semilogy(Td + skewt.skew(p), p, basey=math.e, color=linecolor_Td, linewidth = (linewidth_Td+1.5))

# wind barbs
    ax4 = plt.subplot(gs[0,-1])
    skewt.plot_wind_axes(ax4)
    skewt.plot_wind_barbs(ax4,z,p,u,v)

# Add labels for levels based on surface parcel
    Tmax = skewt.Tmax
    Tmin = skewt.Tmin

# plot labels for std heights
#    plevs_std = [100000,85000,70000,50000,40000,30000,25000,20000,15000]
    plevs_std = skewt.plevs_std
    for plvl in plevs_std:
        zlvl = interp.interp_height(z,p,plvl)
        skewt.label_m(Tmin+2.55,plvl, str(int(zlvl)), ax1)

# plot wind barbs on left side of plot.  move this?  right side?
    pt_plot = 10000

    if (u is not None and v is not None):
      #draw_wind_line(axes)
        for i in np.arange(0,len(z),2):
            if (p[i] > pt_plot):
                plt.barbs(Tmin+4,p[i],u[i],v[i], length=5, linewidth=.5)
                
# legend
    ax5 = fig.add_subplot(1,1,1)
    tT = r'Temperature'
    lT = Line2D(range(10), range(10), linestyle='-', marker='', linewidth=(linewidth_T+1.5), color=linecolor_T)
    
    tTd = r'Dew-point Temperature'
    lTd = Line2D(range(10), range(10), linestyle='-', marker='', linewidth=(linewidth_Td+1.5), color=linecolor_Td)

    plt.legend((lT, lTd,),(tT, tTd, ),
             loc=(0.01,0.95), fontsize=18, handlelength=10)
    ax5.set_axis_off()

# Adjust plot margins.
    plt.subplots_adjust(left=0.03, bottom=0.03, right=0.97, top=0.97, wspace=0.12, hspace=0.12)


# set day
    ax1.text(0.98,0.96, text,     # x, y
            verticalalignment = 'bottom',  horizontalalignment='right',
            transform = ax1.transAxes,
            color =blue, fontsize=26,
            bbox={'facecolor':'white','alpha':.8, 'pad':10})

# savefig
    if sfig == 1:
        plt.savefig(filename,orientation = 'portrait', papertype = 'a4')#, dpi=300,bbox_inches=0)

    plt.close()
