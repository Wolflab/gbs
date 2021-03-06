import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from matplotlib import pylab as plb
from matplotlib.backends.backend_pdf import PdfPages
######



pp = PdfPages('multipage.pdf')

#import the data
data = np.genfromtxt('Aspen_HapMap_hmp_1.csv', dtype=str, delimiter=',')

#put the first row and first column in their own arrays and remove them from
#the main array
indivID = data[0, 1:]
locus = data[1:, 0]
data = sp.delete(data, 0, 0)
data = sp.delete(data, 0, 1)

#get the row and column sums
data_not_N = data != 'N'
row_sums = -1*(np.sum(data_not_N, axis=1))
Mean_number_inds_per_SNP=-1*(np.mean(row_sums))
ord_row_sums = np.sort(row_sums)
col_sums = -1*(np.sum(data_not_N, axis=0))
Mean_number_SNPs_per_ind = -1*(np.mean(col_sums))

#get the rank orders for both rows and columns
row_order = row_sums.argsort()#need highest to lowest
col_order = col_sums.argsort()#need highest to lowest

#sort it all
indivID_sorted = indivID[col_order]
locus_sorted = locus[row_order]
data_sorted = data[row_order][:, col_order]
#

####################################
## PLOTTING
# Now plot Locus distributions:
loci_per_ind = -1*(col_sums)
plt.hist(loci_per_ind, 60)
plt.xlabel('Number of loci Represented', fontsize=20)
plt.ylabel('Number of Individuals', fontsize= 20)
plt.savefig(pp, format='pdf')
#plt.show()#This will need to change to plt.figure for multiple graphs
# Go to http://matplotlib.org/gallery.html - try heat map. Alsoexplore saving figures
#

#Next part works nicely on its own (when above plot removed) but fails when both together
#Also ask Ethan about savefile
# Now plot Individual distributions:
inds_per_locus = -1*(row_sums)
plt.hist(inds_per_locus, 140)# you can simply measure the length ofindivID or max of
# Inds_per_locus to make an appropriate number of bins!
plt.xlabel('Number of loci Represented', fontsize=20)
plt.ylabel('Number of Inds', fontsize= 20)
plt.savefig(pp, format='pdf')
#plt.show()

pp.close()
plot_data = data_sorted.copy()
#plot data is the sorted array(descening) converted to binary for plotting

for (x,y), value in np.ndenumerate(plot_data):
     if value == "N":
          plot_data[x,y] = 0
     else:
          plot_data[x,y] = 1
plot_data = np.array(plot_data, dtype=int)

# plot_data is now a simple binary array. But it seems hard to plot. Here is an alternative:
# Redo the above loop over plot data.sorted. ndenumerate returns the x,y coordinates (above
# I used it to loop through the array). But you could use it to create plot_data as
# x,y coordinates that can then feed into a scatter plot: see some great ideas at:
# www.prettygraph.com/blog/how-to-plot-a-scatter-plot-using-matplotlib/

# attempt at a start
#plot_data = np.array()
#for (x,y), value in np.ndenumerate(data_sorted):
#     if value == "N":
#          plot_data.append(index)
#
#print plot_data


#now give locus list and totals as two lines (may not need to keep this):
locus_totals = np.vstack([locus_sorted,ord_row_sums])
#Now as two columns But Numbers are not integers
loc_colstack = np.column_stack((locus_sorted,ord_row_sums))
#These above arrays are just saved for later in case.

#Don't put back the index names until you are done filtering?

#Now need to do same for ind totals then plot both

#then strip zero rows? (do later?)
