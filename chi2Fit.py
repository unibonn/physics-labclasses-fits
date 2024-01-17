#! /usr/bin/env python3
"""Dieses Programm fuehrt ein chi**2 Fit durch.
"""

import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as optimize

# Deklariere eine neue Funktion
def f(x,a,b):
    return a*x + b

def chi2(x, y, s, f, a, b):
    chi = (y - f(x,a,b))/s
    return np.sum(chi**2)

# Ihre Messdaten kommen hier hin
xdata = np.array([0.0,1.0,2.0,3.0,4.0,5.0])
ydata = np.array([1.1,1.3,2.1,2.7,2.8,3.6])
sigma = np.array([0.2,0.25,0.3,0.35,0.4,0.45])

# Startwerte fuer die Parameterbestimmung
x0    = np.array([1.0, 0.0])

# Die lineare Regression, so wie in den vorigen Beispielen behandelt,
# beruecksichtigt die Messungenauigkeiten weder fuer die richtige
# Gewichtung der einzelnen Messungen (falls die unterschiedlichen
# Messungen ueber unterschiedliche Unsicherheiten verfuegen), noch
# gehen diese Unsicherheiten direkt in die Abschaetzung der
# Unsicherheit der angepassten Parameter ein.

# Desweiteren ist die lineare Regression auf Modelle beschraenkt, in
# die alle zu bestimmenden Parameter *linear* eingehen. Dies ist
# natuerlich nicht allgemein gegeben. Ein chi2-Fit ist ein Spezialfall
# einer Optimierung mittels der Maximum Likelihood Methode, welche im
# Fall von linearen Abhaengigkeiten der Observablen *um das Minimum
# herum* (aber nicht notwendigerweie ueberall) und im Fall von
# gaussischen Messungenauigkeiten fuer alle Anpassungen angewendet
# werden kann, also auch im Fall unterschiedlicher sigma fuer jede
# Einzelmessung. Auch dafuer gibt es ein Modul in Pyhton. In diesem
# Modul koennen Sie nun *beliebige* Funktionen fitten, also auch
# solche, die nicht nur Parameter linear, sondern in beliebiger
# analytischer oder numerischer Form enthalten.
fitParams, fitCovariances = optimize.curve_fit(f, xdata, ydata, x0, sigma, absolute_sigma=True)
slope     = fitParams[0]
intercept = fitParams[1]
fitErrors = np.sqrt(np.diag(fitCovariances))
slope_std_err = fitErrors[0]
intercept_std_err = fitErrors[1]

# Leider sind die Unsicherheiten auf slope und intercept, die von
# curve_fit berechnet werden, so nicht nutzbar. Der Grund ist der,
# dass aus irgend einem unsinnigen Grund curve_fit die sigmas nur als
# *relative* Gewichte und nicht, so wie von uns gewuenscht, als
# *absolute* Unsicherheiten betrachtet. Dies koennen Sie einfach
# testen, indem Sie alle sigmas einfach mal verdoppeln: das von
# curve_fit ausgegebene Ergebnis bleibt identisch! Das muss also noch
# korrigiert werden.

# Das ist die wichtigste Lektion in diesem Teil: Vorgefertigter Code
# oder komplette Black-Box-Programme wie Excel sind fuer bestimmte
# Sachen nuetzlich.
# ABER: Es ist nicht immer klar, was dieses Programm/Code genau macht!
# Hier macht curve_fit ganz offensichtlich NICHT, was wir wollen. Und
# wir haetten das auch nicht unbedingt gemerkt! GENAU deshalb sollen
# Sie Rechnungen immer transparent ausfuehren und NIE mit schlecht
# dokumentiertem closed-source black-box Code!

# Der Wert chi2 ist ein Mass fuer die Uebereinstimmung der Daten mit der Messung
# chi2 = sum_i (ydata_i-f(x_data_i))**2/sigma_i**2
thischi2=chi2(xdata,ydata,sigma,f,fitParams[0],fitParams[1])

ndf = len(ydata)-len(fitParams)
# fitErrors = np.sqrt(np.diag(fitCovariances))
for i in range(0,2):
    print('parameter {0}:     {1:.3f} +- {2:.3f}'.format(i,fitParams[i], fitErrors[i]))
slope_std_err = fitErrors[0]
intercept_std_err = fitErrors[1]

# nun erschaffen wir einen plot
# fig = plt.figure()
# ax = fig.add_subplot(111)
fig, ax  = plt.subplots()

# Vielleicht wollen Sie noch etwas in den Plot schreiben, z.B. eine Formel?
formulaText1 = '$f(x)=%.2f x' % slope 
formulaText2 = '+ %.2f$' % intercept
formulaText  = formulaText1 + formulaText2
ax.text(0.95, 0.15, formulaText, verticalalignment='bottom', horizontalalignment='right', transform=ax.transAxes, fontsize=16)
formulaText3 = '$a = %.2f' % slope
formulaText4 = '\pm %.2f' % slope_std_err
formulaTextS = formulaText3 + formulaText4
formulaText5 = ',\,\, b = %.2f' % intercept
formulaText6 = '\pm %.2f$' % intercept_std_err
formulaTextI = formulaText5 + formulaText6
formulaTextErrors = formulaTextS + formulaTextI
ax.text(0.95, 0.05, formulaTextErrors, verticalalignment='bottom', horizontalalignment='right', transform=ax.transAxes, fontsize=16)
formulaTextChi2 = '$\chi^2=\sum\\frac{(y_i-f(x_i,\\vec{a}))^2}{s_i^2}=%.2f$' % thischi2
ax.text(0.95, 0.25, formulaTextChi2, verticalalignment='bottom', horizontalalignment='right', transform=ax.transAxes, fontsize=16)

# Die Achsen brauchen auf jeden Fall eine Beschriftung
ax.set_ylabel('Messwert y [Einheit]', fontsize = 16)
ax.set_xlabel('Messwert x [Einheit]', fontsize = 16)
ax.set_xlim(xdata[0]-1,xdata[-1]+1)

# Plotte die Funktion 
t = np.arange(xdata[0]-0.5,xdata[-1]+0.5, 0.02)
ax.plot(t,f(t,slope,intercept))
ax.errorbar(xdata, ydata, sigma, fmt='ro')

# Zeige den Plot
plt.show()

# Speichere den Plot
plotname = 'myplot.pdf'
fig.savefig(plotname, bbox_inches=0, dpi=600)
# fig.close()
