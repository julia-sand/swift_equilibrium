import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

#set up fontsizes
fontsize = 22
fontsizeticks = 18
fontsizetitles = 22

model_type = "hard"

#get the right folder 
if model_type=="hard":
    folder_path ="swift_equilibrium/results/hard/"
elif model_type =="log":
    folder_path ="swift_equilibrium/results/log/"
elif model_type =="harmonic":
    folder_path ="swift_equilibrium/results/harmonic/"
else:
    print("Please specify a valid model. Use log, harmonic or hard.")

df_ipopt = pd.DataFrame(pd.read_csv(folder_path + "EP_Hardv1.csv"))
#df_diffeq = pd.DataFrame(pd.read_csv(folder_path + "EP_diffeqv1.csv"))

# Create a 2x2 grid of plots
fig, axs = plt.subplots(2, 2, figsize=(10, 8))

# Plot on the first subplot (top-left)
#"Position variance"
axs[0, 0].plot(df_ipopt.t, df_ipopt.x1)
axs[0, 0].set_title('Position Variance')

# Plot on the second subplot (top-right)
axs[0, 1].plot(df_ipopt.t, df_ipopt.x2)
axs[0, 1].set_title('Cross Correlation')

# Plot on the third subplot (bottom-left)
axs[1, 0].plot(df_ipopt.t, df_ipopt.x3)
axs[1, 0].set_title('Momentum Variance')

# Plot on the fourth subplot (bottom-right)
axs[1, 1].plot(df_ipopt.t, df_ipopt["lambda"])
axs[1, 1].set_title('Stiffness')

# Adjust layout to prevent overlap
plt.tight_layout()

plt.savefig(folder_path+"test.png")

plt.close()
