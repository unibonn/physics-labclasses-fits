#!/usr/bin/env python3

import sys
import argparse

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import scipy.odr as sodr

# Funktionsdefinitionen:

# Die Funktiomn lin_func wird intern von der ODR-Firprozedur benötigt.
# Ein direktes Aufrufen ist wahrscheinlich nicht allzu sinnvoll!
def lin_func(p, x):
     """
     Die Funktion wird von der ODR-Fitprozedur intern aufgerufen

     Funktionsargumente:
     p: ein numpy-array aus zwei Elementen (Steigung und y-Achsenabschnitt
        einer Gerade).
     x: Funktionswert

     Die Funktion berechnet den Ausdrck p[0] * x + p[1]
     und gibt diesen zurück.
     """
     m, c = p
     return m * x + c

#
# Skriptstart
#

# Lese Kommandozeilenparameter:
parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog="""
BESCHREIBUNG:

  Das Skript fuehrt einen Geradenfit für Daten die, sowohl in den x-,
  als auch in den y-Koordinaten, mit Fehlern behaftet sind.
  
  Programm Eingabe ist eine Datei (Programmoption -i) mit vier Spalten:
  x fehler_x y fehler_y
  
  Die Datei darf Kommentarzeilen, die mit einem '#' eingeleitet werden,
  enthalten,
  
  Gefittet wird eine Gerade y = a*x + b welche die Daten am besten
  repraesentiert. Der benutzte Algorithmus, die Orthogonal-Distance
  Regression, ist in http://docs.scipy.org/doc/scipy/reference/odr.html
  ausfuehrlich dokumentiert.
  
  Programmausgabe auf dem Bildschirm sind die Fitparameter a und b
  sowie deren Fehler.
  
  Optional erstellt das Programm einen Plot mit Daten und Fitgerade
  (Programmoption -o).

BEISPIELE:

  - ./chi2FitXYErr.py -i dataxy.txt
    Fittet die Daten in 'dataxy.txt' und gibt das Fitergebnis
    auf dem Bildschirm aus.
  
  - ./chi2FitXYErr.py -i dataxy.txt -o ergebnis.png
    Wie oben. Zusaetzlich werden Datenpunkte und Geradenfit
    in dem Plot 'ergebnis.png' gespeichert.

AUTOR:
  Thomas Erben (terben@astro.uni-bonn.de)
"""
)
parser.add_argument('-i', '--input_file', nargs=1,
                    required=True, help='Name der Datendatei')
parser.add_argument('-o', '--output_file', nargs=1,
                    help='Name des Ausgabeplots (OPTIONAL)')

args = parser.parse_args()

input_file = args.input_file[0]

# Lese Daten:
data = np.loadtxt(input_file)

# Hat die Datei vier Spalten?
if data.shape[1] != 4:
     print("Datei %s hat keine 4 Spalten!" % (input_file), file=sys.stderr)
     sys.exit(1)

# Extrahier Spalten aus den data-Datenkubus - nur
# um aussagekräftige Variablennanem zu haben:
x = data[:,0]
x_error = data[:,1]
y = data[:,2]
y_error = data[:,3]
     
# Führe den Fit durch. Für eine Erklärung der
# folgenden Fit-Befehle konsultiere man die Hilfe
# des scipy.odr Moduls:
lin_model = sodr.Model(lin_func)
fit_data = sodr.RealData(x, y, sx=x_error, sy=y_error)
odr = sodr.ODR(fit_data, lin_model, beta0=[0., 1.])
out = odr.run()

# Die Fitparameter und deren Fehler direkt aus der Ergebnisstruktur
# zu verwenden ist umständlich und fehleranfällig. Deshalb speichern
# diese Parameter in aussagekräftigere Variablen: 
a = out.beta[0]
b = out.beta[1]
err_a = out.sd_beta[0]
err_b = out.sd_beta[1]


print("Fitergebnis:\n")
print("y = a * x + b mit\n")
print("a = %f +/- %f" % (a, err_a))
print("b = %f +/- %f" % (b, err_b))

# Erstelle eventuell noch einen Plot mit Daten und Fitgerade:
if args.output_file != None:
    # Vernünftige Symbolgrößen etc:
    font = {'weight' : 'normal',
            'size'   : 14}

    matplotlib.rc('font', **font)

    y_fit = a * x + b

    #  plt.figure()
    fig, ax = plt.subplots()
    ax.errorbar(x, y, xerr=x_error, yerr=y_error,
                lw=2, fmt='.', label="Datenpunkte")
    ax.plot(x, y_fit, lw=2, label="y=%.2f * x + %.2f" % (a, b))
    ax.set_xlabel('x', fontsize=14)
    ax.set_ylabel('y', fontsize=14)
    ax.set_title("%d Datenpunkte mit Geradenfit" % (x.shape[0]))
    ax.legend()

    fig.savefig(args.output_file[0], bbox_inches='tight')

