import ROOT
from itertools import combinations

def drawHist(histogram, canvas):
    histogram.Draw()
    canvas.Update()
    input()

# Read the file
file = ROOT.TFile.Open("~/Documents/BU/bu-std-tools/ZtoMuMu/43718dea-5cd4-48a7-b73b-df168edf1fac.root")

# Show what it is inside
# file.ls()

# Get the TTree
t = file.Get('Events')

# t.Print("Muon_*")

ROOT.gStyle.SetHistFillColor(ROOT.kMagenta + 1)

# make zoomed in hist from 0 to 20
hMass2 = ROOT.TH1F("hMass2", "hMass2", 15, 2.5, 4)
hMass2.GetXaxis().SetTitle("Invariant #mu#mu mass (GeV)")
hMass2.GetYaxis().SetTitle("Number of pairs")

from tqdm import tqdm # nukes performance but at least i have progress bars

p2List = []
for e in tqdm(range(t.GetEntries())):
# for e in tqdm(range(0, 10000)):
    t.GetEntry(e)
    nMuon = t.nMuon
    if nMuon < 2:
        continue
    # print("Event %i has %i muons"%(e, nMuon))

    # to-do: find a better way of doing this
    muonCharges = list(t.Muon_charge)
    muonpTs = list(t.Muon_pt)
    muonEtas = list(t.Muon_eta)
    muonPhis = list(t.Muon_phi)
    muonMs = list(t.Muon_mass)

    fourMomentaAndCharge = []
    for i in range(nMuon):
        fourVec = ROOT.Math.PtEtaPhiMVector(muonpTs[i], muonEtas[i], muonPhis[i], muonMs[i])
        if fourVec.pt() > 20 and abs(fourVec.eta()) < 2.4:
            fourMomentaAndCharge.append([fourVec, muonCharges[i]]) # not nice, but it works
    for pair in combinations(fourMomentaAndCharge, 2):
        # print(pair[0][1], pair[1][1]) # print charges of each
        if(pair[0][1] != pair[1][1]): # if the charges are NOT the same
            p2 = pair[0][0] + pair[1][0] # add four momenta
            p2List.append(p2)
            # print(p2)
            # print(p2.mass())
            if p2.mass() < 20:
                hMass2.Fill(p2.mass())

print("Ding!")

canvas = ROOT.TCanvas("canvas", "canvas", 1200, 800)
drawHist(hMass2, canvas)
canvas.SaveAs("~/Documents/BU/bu-std-tools/ZtoMuMu/dimuon_img/dimuon_mass_2p5_4_N15.png")

myFile = ROOT.TFile.Open("zmumu_fine_2p5_4.root", "RECREATE")
hMass2.Write()
myFile.Close()