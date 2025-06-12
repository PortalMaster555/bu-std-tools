import ROOT
f = ROOT.TFile.Open("zmumu.root", "read")
f.ls()
hMass = f.Get("hMass")
hMass2 = f.Get("hMass2")
hPass = f.Get("hPass")


canvas = ROOT.TCanvas("canvas", "canvas", 600, 600)
canvas.cd()

hMass.Draw()
canvas.Update()
# canvas.SaveAs("~/Documents/BU/bu-std-tools/ZtoMuMu/dimuon_img/dimuon_masses_charge_filtered.png")
input()
hMass2.Draw()
canvas.Update()
# canvas.SaveAs("~/Documents/BU/bu-std-tools/ZtoMuMu/dimuon_img/dimuon_masses_0_20_charge_filtered.png")
input()
hPass.Draw()
canvas.Update()
# canvas.SaveAs("~/Documents/BU/bu-std-tools/ZtoMuMu/dimuon_img/pass_count_charge_filtered.png")
input()