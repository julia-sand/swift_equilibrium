.PHONY: dirs julia-env swiftequilibration submit-all-figs-batch

swiftequilibration-setup : dirs julia-env
swiftequilibration-all : dirs julia-env submit-all-figs-batch
experimental-setup : dirs julia-env
experimental-all : dirs julia-env submit-exp-figs-batch

DIR_NAME=results

dirs:
	./src/makedirs.sh $(DIR_NAME)

julia-env:
	julia --project=. -e 'using Pkg; Pkg.instantiate()'

submit-all-figs-batch:
	sbatch src/swiftequilibration/scripts/fig1.bash
	sbatch src/swiftequilibration/scripts/fig2.bash
	sbatch src/swiftequilibration/scripts/fig3.bash
	sbatch src/swiftequilibration/scripts/fig4.bash
	sbatch src/swiftequilibration/scripts/fig5.bash
	sbatch src/swiftequilibration/scripts/fig6.bash
	sbatch src/swiftequilibration/scripts/fig7.bash
	sbatch src/swiftequilibration/scripts/fig9.bash

