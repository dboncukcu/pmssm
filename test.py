

import ROOT
from plotter import Plotter


h = ROOT.TH1F("h", "Histogram", 100, -5, 5)
h2 = ROOT.TH2F("h2", "Histogram2", 50, -3, 3, 25, -3, 3)
mean = 0
sigma = 2
for i in range(10000):
    x = ROOT.gRandom.Gaus(mean, sigma)
    h.Fill(x)
    y = ROOT.gRandom.Gaus(mean, sigma)
    z = ROOT.gRandom.Gaus(mean, sigma*0.9)
    h2.Fill(y,z)





p = Plotter(canvasSettings={
    "xmin": -5,
    "xmax": 5,
    "ymin": 0,
    "ymax": 0.025,
    "nameXaxis": "#Deltam(#tilde{#chi}^{#pm}_{1},#tilde{#chi}^{0}_{1})",
    "nameYaxis": "m_{#tilde{#chi}^{0}_{1}}",
    "canvName": "gaussian",
    "extraSpace": 0.02,
    "iPos": 11,
})

h.Scale(1/h.Integral())
h2.Scale(1/h2.Integral())


# p.tuning(tuning={"YaxisSetTitleOffset":1})
p.tuning(tuning={"XaxisSetTitleOffset":1.1})
p.tuning(tuning={"YaxisSetTitleOffset":1.1})
p.tuning(tuning={"YaxisSetMaxDigits":2})
p.tuning(tuning={"SetBottomMargin":0.03})
p.Draw(h,"h")

fit = ROOT.TF1("fit", "gaus", -5, 5)
fit.SetParameters(h.GetMaximum(), mean, sigma)
h.Fit("fit")
p.Draw(fit)

# p.canvas.Update()
# p.canvas.Draw()
p.SaveAs("histogram_with_gauss.png")

del(p)


p = Plotter(canvasSettings={
    "xmin": -3,
    "xmax": 3,
    "ymin": -3,
    "ymax": 3,
    "nameXaxis": "#Deltam(#tilde{#chi}^{#pm}_{1},#tilde{#chi}^{0}_{1})",
    "nameYaxis": "m_{#tilde{#chi}^{0}_{1}}",
    "canvName": "gaussian2",
    "extraSpace": 0,
    "iPos": 0,
    "is3D": True
})

# h2.GetZaxis().SetMaxDigits(3)
h2.GetZaxis().SetTitle("Survival probability")
p.Draw(h2,"colz")
p.tuning(tuning={"ZaxisSetMaxDigits":3},hist=h2)
p.tuning(tuning={"ZaxisSetTitleOffset":1.2},hist=h2)
p.tuning(tuning={"YaxisSetTitleOffset":0.9})
p.tuning(tuning={"XaxisSetTitleOffset":1})
p.tuning(tuning={"XaxisSetMaxDigits":2})
p.tuning(tuning={"SetBottomMargin":0.02})
p.SaveAs("histogram_with_gauss3d.png")
