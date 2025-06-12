import ROOT
f = ROOT.TFile.Open("zmumu.root", "read")
f.ls()

def drawHist(histogram, canvas):
    histogram.Draw()
    canvas.Update()
    input()

hMass = f.Get("hMass")
hMass2 = f.Get("hMass2")
hPass = f.Get("hPass")



canvas = ROOT.TCanvas("canvas", "canvas", 1200, 800)
canvas.cd()

drawHist(hMass, canvas)
# canvas.SaveAs("~/Documents/BU/bu-std-tools/ZtoMuMu/dimuon_img/dimuon_masses_charge_filtered.png")
drawHist(hMass2, canvas)
canvas.SaveAs("~/Documents/BU/bu-std-tools/ZtoMuMu/dimuon_img/dimuon_masses_0_20_charge_filtered.png")
drawHist(hPass, canvas)
# canvas.SaveAs("~/Documents/BU/bu-std-tools/ZtoMuMu/dimuon_img/pass_count_charge_filtered.png")
