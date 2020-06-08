#!/usr/bin/env python3

# Just call the script to obtain a help and usage message

import sys
import argparse

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import scipy.odr as sodr

##_Modify your Plot_##

# NOTICE: Do always read foreign code before exectuing! You can never know what some nasty people wrote in the code...
# Just cause this version is simpler to modify doesn't mean that you don't need to understand whats happening!

#Change the string following text to set yout plot labels 
#Warning: Make sure to keep the "%-Arguments" like %.2f untouched by changing you text!

#Modify Title
plot_title = "%d data points and line-fit"

#Modify axis labels
y_label = "y_change_me"
x_label = "x_change_me"
label_size = 14

#Text in legend-box
vals_legend = "data points"
fit_legend = "y=%.2f * x + %.2f"

#Modify thickness of graphs and axis
fit_size = 2
vals_size = 2
axis_size = 2.0

#Modify color
err_color = 'r.'
fit_color = "g"

#resolution
plt_size = 300

# Function definitions:

# The function lin_finc is internally used by the ODR fitting procedure.
# It is probably not useful to call it in other curcumstances.
def lin_func(p, x):
     """
     The function is internally used by the ODR-fit procedure

     function arguments:
     p: a numpy-array of two elements (slope and y-intersection of a line)
     x: value for which you want to evaluate the function

     The function calculates p[0] * x + p[1] and returns that value.
     """

     m, c = p
     return m * x + c

# main script tasks start here:

# lese Kommandozeilenparameter:
parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog="""
DESCRIPTION:
  The script performs a line-fit for data that contain errors in
  the x- and y-coordinates!

  Input is a file (command line option -i) with four columns:
  x, error_x, y, error_y.

  The input file may contaion comment lines starting with a hash (#).

  The program fits a two-parameter line (y = a * x + b) to approximate
  the data. The used algorithm, the orthogonal-distance regression
  is thoroughly documented at
  http://docs.scipy.org/doc/scipy/reference/odr.html.

  Program output are the ebst fit line-parameters a und b together with
  their estimated errors. In addition, the uise can ask for a plot
  of the data points together with the best fit-line (command line option
  '-h').

EXAMPLES:

  - ./chi2FitXYErr.py -i dataxy.txt
    Fits a line to the data in 'dataxy.txt' and print the fit results to
    screen
  
  - ./chi2FitXYErr.py -i dataxy.txt -o ergebnis.png
    The same as above. In addition, data points and best-fit line
    are shown in the plot 'result.png'.

AUTHOR:
  Thomas Erben (terben@astro.uni-bonn.de)
  Modified by Christoph Geron (https://github.com/ceron21/)
"""
)
parser.add_argument('-i', '--input_file', nargs=1,
                    required=True, help='Name der Datendatei')
parser.add_argument('-o', '--output_file', nargs=1,
                    help='Name des Ausgabeplots (OPTIONAL)')

args = parser.parse_args()

input_file = args.input_file[0]

# Read data:
data = np.loadtxt(input_file)

# Rough sanity check: Does the input file have 4 columns?
#if data.shape[1] != 4:
#  None
#else:
#  print("Datei %s hat keine 4 Spalten!" % (input_file), file=sys.stderr)
#  sys.exit(1)
     

# Give meaningful variable names to input data columns:
x = data[:,0]
x_error = data[:,1]
y = data[:,2]
y_error = data[:,3]

# Perform the fitting procedure. For an explanation of the following
# four code lines consult the help of the scipy.odr module:
lin_model = sodr.Model(lin_func)
fit_data = sodr.RealData(x, y, sx=x_error, sy=y_error)
odr = sodr.ODR(fit_data, lin_model, beta0=[0., 1.])
out = odr.run()

# We give meaningful names to the best-fit parameters and errors
# returned by 'odr.run':
a = out.beta[0]
b = out.beta[1]
err_a = out.sd_beta[0] # error on a
err_b = out.sd_beta[1] # error ob b


print("result of fit:\n")
print("y = a * x + b with\n")
print("a = %f +/- %f" % (a, err_a))
print("b = %f +/- %f" % (b, err_b))

# create a plot
# font size of labels etc,
matplotlib.rcParams['font.size'] = label_size
# line width of coordinate axes
matplotlib.rcParams['axes.linewidth'] = axis_size

y_fit = a * x + b

plt.figure()
plt.errorbar(x, y, xerr=x_error, yerr=y_error, lw=vals_size, fmt=err_color, label=vals_legend)
plt.plot(x, y_fit, fit_color, lw=fit_size, label=fit_legend % (a, b))
plt.xlabel(x_label)
plt.ylabel(y_label)
plt.title(plot_title % (x.shape[0]))
plt.legend()

