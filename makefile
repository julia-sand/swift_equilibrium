.PHONY: swiftequilibration submit-all-figs-batch

swiftequilibration-all : julia-env swift-equilibrium-all
experimental-setup : dirs julia-env
experimental-all : dirs julia-env submit-exp-figs-batch

julia-env:
	julia --project=. -e 'using Pkg; Pkg.instantiate()'

swift-equilibrium-all-figs:
	./src/makedirs.sh results2/swiftequilibrium
	sbatch src/swiftequilibration/scripts/fig1.bash
	sbatch src/scripts/swiftequilibration/fig2.bash
	sbatch src/scripts/swiftequilibration/fig3.bash
	sbatch src/scripts/swiftequilibration/fig4.bash
	sbatch src/scripts/swiftequilibration/fig5.bash
	sbatch src/scripts/swiftequilibration/fig6.bash
	sbatch src/scripts/swiftequilibration/fig7.bash
	sbatch src/scripts/swiftequilibration/fig9.bash

experimental-all-figs:
	./src/makedirs.sh results3/experimental
