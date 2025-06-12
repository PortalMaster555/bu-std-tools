import ROOT
from itertools import combinations

# Read the file
file = ROOT.TFile.Open("~/Documents/BU/bu-std-tools/ZtoMuMu/43718dea-5cd4-48a7-b73b-df168edf1fac.root")

# Show what it is inside
# file.ls()

# Get the TTree
t = file.Get('Events')

# t.Print("Muon_*")

ROOT.gStyle.SetHistFillColor(ROOT.kMagenta + 1)

hMass = ROOT.TH1F("hMass", "hMass", 50, 0, 150)
hMass.GetXaxis().SetTitle("Invariant #mu#mu mass (GeV)")
hMass.GetYaxis().SetTitle("Number of pairs")

# make zoomed in hist from 0 to 20
hMass2 = ROOT.TH1F("hMass2", "hMass2", 40, 0, 20)
hMass2.GetXaxis().SetTitle("Invariant #mu#mu mass (GeV)")
hMass2.GetYaxis().SetTitle("Number of pairs")

hPass = ROOT.TH1F("hPass", "hPass", 4, 2, 6)
hPass.GetXaxis().SetTitle("Number of filter-allowed muons per event")
hPass.GetYaxis().SetTitle("Number of events")
hPass.GetXaxis().SetNdivisions(4, 0) # extremely hacky way of making the bar chart
hPass.GetXaxis().CenterLabels() # there is almost certainly a more efficient class/function

from tqdm import tqdm # nukes performance but at least i have progress bars

for e in tqdm(range(t.GetEntries())):
# for e in tqdm(range(0, 3000)):
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
    nPasses = 0
    for i in range(nMuon):
        fourVec = ROOT.Math.PtEtaPhiMVector(muonpTs[i], muonEtas[i], muonPhis[i], muonMs[i])
        if fourVec.pt() > 20 and abs(fourVec.eta()) < 2.4:
            fourMomentaAndCharge.append([fourVec, muonCharges[i]]) # not nice, but it works
            nPasses = nPasses + 1
    hPass.Fill(nPasses)
    pT = 0
    invMass = 0
    for pair in combinations(fourMomentaAndCharge, 2):
        # print(pair[0][1], pair[1][1]) # print charges of each
        if(pair[0][1] != pair[1][1]): # if the charges are NOT the same
            p2 = pair[0][0] + pair[1][0] # add four momenta
            invMass = p2.mass()
            # tqdm.write(str(pT)+' '+str(invMass))
            hMass.Fill(invMass)
            if invMass < 20:
                hMass2.Fill(invMass)

print("Ding!")

canvas = ROOT.TCanvas("canvas", "canvas", 600, 600)
canvas.cd() # To indicate we are going to draw here
hMass.Draw()
input()
canvas.SaveAs("~/Documents/BU/bu-std-tools/ZtoMuMu/dimuon_img/dimuon_masses_charge_filtered.png")
hMass2.Draw()
canvas.Update()
input()
canvas.SaveAs("~/Documents/BU/bu-std-tools/ZtoMuMu/dimuon_img/dimuon_masses_0_20_charge_filtered.png")
hPass.Draw()
canvas.Update()
canvas.SaveAs("~/Documents/BU/bu-std-tools/ZtoMuMu/dimuon_img/pass_count_charge_filtered.png")
input()

myFile = ROOT.TFile.Open("zmumu.root", "RECREATE")
hMass.Write()
hMass2.Write()
hPass.Write()
myFile.Close()