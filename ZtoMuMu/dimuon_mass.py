import ROOT
# Read the file
file = ROOT.TFile.Open("~/Documents/BU/bu-std-tools/ZtoMuMu/43718dea-5cd4-48a7-b73b-df168edf1fac.root")

# Show what it is inside
# file.ls()

# Get the TTree
t = file.Get('Events')

t.Print("Muon_*")

from itertools import combinations


hMass = ROOT.TH1F("hMass", "hMass", 50, 0, 150)
# make zoomed in hist from 0 to 20
hMass2 = ROOT.TH1F("hMass2", "hMass2", 20, 0, 20)

from tqdm import tqdm # nuke performance but at least i have progress bars
for e in tqdm(range(t.GetEntries())):
    t.GetEntry(e)
    nMuon = t.nMuon
    if nMuon < 2:
        continue
    
    # print("Event %i has %i muons"%(e, nMuon))
    muonpTs = list(t.Muon_pt)
    muonEtas = list(t.Muon_eta)
    muonPhis = list(t.Muon_phi)
    muonMs = list(t.Muon_mass)
    fourMomenta = []
    for i in range(nMuon):
        fourVec = ROOT.Math.PtEtaPhiMVector(muonpTs[i], muonEtas[i], muonPhis[i], muonMs[i])
        if fourVec.pt() > 20 and abs(fourVec.eta()) < 2.7:
            fourMomenta.append(fourVec)
        
    for pair in combinations(fourMomenta, 2):
        # print(pair[0], pair[1])
        p2 = pair[0] + pair[1]
        # print(p2)
        # print(p2.mass())
        hMass.Fill(p2.mass())
        if p2.mass() < 20:
            hMass2.Fill(p2.mass())
canvas = ROOT.TCanvas("canvas", "My first canvas", 600, 500) # 600 and 500 and width and height of the canvas
canvas.cd() # To indicate we are going to draw here
hMass.Draw()
canvas.SaveAs("~/Documents/BU/bu-std-tools/ZtoMuMu/dimuon_img/dimuon_masses.png")
hMass2.Draw()
canvas.SaveAs("~/Documents/BU/bu-std-tools/ZtoMuMu/dimuon_img/dimuon_masses_0_20.png")
print("ding")
