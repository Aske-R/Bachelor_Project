from hep_ml.reweight import GBReweighter
import uproot
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

tree = uproot.open("../data/MixedTest.root")[b'tree;1']
reweight_data = tree.pandas.df(["averageInteractionsPerCrossing","p_et_calo","p_eta","Signal"])
reweight_data_small = reweight_data.sample(frac=1,replace=False, random_state=42)

signal_reweight_data = reweight_data_small.where(reweight_data['Signal'] == 1)
signal_reweight_data_s_dropped = signal_reweight_data.drop(['Signal'], axis=1)
signal_reweight_data_nan_s_dropped = signal_reweight_data_s_dropped.dropna(axis=0)
background_reweight_data = reweight_data_small.where(reweight_data['Signal'] ==0)
background_reweight_data_s_dropped = background_reweight_data.drop(['Signal'], axis=1)
background_reweight_data_nan_s_dropped =background_reweight_data_s_dropped.dropna(axis=0)

ratio=len(signal_reweight_data_nan_s_dropped)/len(background_reweight_data_nan_s_dropped)

reweighter = GBReweighter(n_estimators=40)
reweighter.fit(background_reweight_data_nan_s_dropped, signal_reweight_data_nan_s_dropped)
weights = reweighter.predict_weights(background_reweight_data_nan_s_dropped)
print(weights)

total_weights=ratio*weights /np.mean(weights)

#reweighted_background = background_reweight_data.multiply(weights, axis=0)

fig_weight, ax_weight = plt.subplots(3,2, figsize=(15,15))


ax_weight[0,0].hist(signal_reweight_data_nan_s_dropped.p_et_calo.ravel(),bins=50,range=(0,100000), color = 'r', alpha = 0.5, label = "Signal")
ax_weight[0,0].hist(background_reweight_data_nan_s_dropped.p_et_calo.ravel(), bins=50,range=(0,100000), color = 'blue', alpha = 0.5, label = "Background")
ax_weight[0,0].legend(loc="upper right")
ax_weight[0,0].set_title('P_et_calo (before weight)')


ax_weight[0,1].hist(signal_reweight_data_nan_s_dropped.p_et_calo.ravel(), bins=50,range=(0,100000), color = 'r', alpha = 0.5, label = "Signal")
ax_weight[0,1].hist(background_reweight_data_nan_s_dropped.p_et_calo.ravel(),  bins=50, range=(0,100000), color = 'blue', weights=total_weights, alpha = 0.5, label = "Background")
ax_weight[0,1].legend(loc="upper right")
ax_weight[0,1].set_title('P_et_calo (after weight)')

ax_weight[1,0].hist(signal_reweight_data_nan_s_dropped.p_eta.ravel(), bins=50, color = 'r', alpha = 0.5, label = "Signal")
ax_weight[1,0].hist(background_reweight_data_nan_s_dropped.p_eta.ravel(), bins=50, color = 'blue', alpha = 0.5, label = "Background")
ax_weight[1,0].legend(loc="upper right")
ax_weight[1,0].set_title('p_eta (before weight)')

#ax_weight[1,0].hist(background_reweight_data_nan_s_dropped.p_eta.ravel(), bins = 50, color = 'blue',weights=total_weights, alpha = 0.5, label = "Background")
#ax_weight[1,0].legend(loc="upper right")
#ax_weight[1,0].set_title('p_et_calo, background only, after')


ax_weight[1,1].hist(signal_reweight_data_nan_s_dropped.p_eta.ravel(), bins=50, color = 'r', alpha = 0.5, label = "Signal")
ax_weight[1,1].hist(background_reweight_data_nan_s_dropped.p_eta.ravel(), bins=50, color = 'blue',weights=weights, alpha = 0.5, label = "Background")
ax_weight[1,1].legend(loc="upper right")
ax_weight[1,1].set_title('p_eta(after weight)')

ax_weight[2,0].hist(signal_reweight_data_nan_s_dropped.averageInteractionsPerCrossing, bins=50, color = 'r', alpha = 0.5, label = "Signal")
ax_weight[2,0].hist(background_reweight_data_nan_s_dropped.averageInteractionsPerCrossing, bins=50, color = 'blue', alpha = 0.5, label = "Background")
ax_weight[2,0].legend(loc="upper right")
ax_weight[2,0].set_title('averageInteractionsPerCrossing (before weight)')

ax_weight[2,1].hist(signal_reweight_data_nan_s_dropped.averageInteractionsPerCrossing, bins=50, color = 'r', alpha = 0.5, label = "Signal")
ax_weight[2,1].hist(background_reweight_data_nan_s_dropped.averageInteractionsPerCrossing, bins=50, color = 'blue',weights=weights, alpha = 0.5, label = "Background")
ax_weight[2,1].legend(loc="upper right")
ax_weight[2,1].set_title('averageInteractionsPerCrossing(after weight)')


plt.savefig("../graphs/reweights_p_et-p_eta-average_interactions")

