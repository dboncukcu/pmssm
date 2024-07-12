import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)
# Open the ROOT files
file1 = ROOT.TFile("/eos/cms/store/group/phys_susy/pMSSMScan/MasterTrees/lildd_exc_val_withlz.root")
file2 = ROOT.TFile("/eos/cms/store/group/phys_susy/pMSSMScan/MasterTrees/pmssmtree_11aug2023.root")

# Get the trees
tree1 = file1.Get("mcmc")
tree2 = file2.Get("mcmc")
print(tree1.GetEntries(), tree2.GetEntries())

# Add tree2 as a friend to tree1
tree1.AddFriend(tree2, "friendTree")
tree1.Show(0)

# Create a canvas to draw the histogram
c1 = ROOT.TCanvas("c1", "c1", 800, 600)

# Draw the histogram using TTree::Draw method
# Assuming pval1 is in tree1 and pval2 is in tree2 (friendTree)
tree1.Draw("dd_exclusion_pval_withlz:dd_exclusion_pval>>hadc(40,0,1.01,40,0,1.01)", "", "COLZ text")
# tree1.Draw("abs(friendTree.chi20)-abs(friendTree.chi10):abs(friendTree.chi10)","dd_exclusion_pval_withlz>0.05 && friendTree.dd_exclusion_pval<0.05", "COLZ text")

# Update the canvas to display the histogram
c1.Update()

# Save the canvas as an image

c1.Print("sam_out.pdf")