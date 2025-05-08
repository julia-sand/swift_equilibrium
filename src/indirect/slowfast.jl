using DifferentialEquations;
using CSV;
using ODEInterface;
using DataFrames;

#= This script implements the invariant manifold equations. =#

include("../params.jl")

function slowfast()
    parsed_args = parse_commandline()
    file_name = get_file_name(parsed_args)
    model_type = parsed_args["penalty"]

    Lambda = sqrt(2) #parse_args["Lambda"]
    T = parse_args["tf"]
    sigma0 = parsed_args["sigma0"]
    sigmaT = parsed_args["sigmaT"]

    epsilon = parsed_args["epsilon"]
    g = parsed_args["g"]


    #vector of parameters
    p = [epsilon,g^4]

    #this is the system for 
    #transition between states with different variance/fixed mean System(3)
    #with first order optimality system (26). 
    function varevolution1!(du, u, p, t)
        epsilon,gscale = p
        f1,f2,f3,f4,x1,x2,x3,x4 = u
        du[1] = gscale*epsilon*f2 
        du[2] = gscale*2*f3 
        du[3] = -gscale*f4/(x1+1e-10)  
        du[4] = gscale*epsilon*f1*(x1^2)  
        du[5] = 2*epsilon*x2
        du[6] = -x2-epsilon*(x4*x1-x3)
        du[7] = 2*(1-x3-epsilon*x4*x2) 
        du[8] = f1-(2*epsilon*x2*(4*epsilon*x3-5*x2)+x1*(9*epsilon*x3-3*x2-6*epsilon)-3*epsilon*(x1^2)*x4-8*(epsilon^2)*((x2^3)/(x1+1e-10)))/(epsilon*((x1+1e-10)^2))
    end


    #the boundary conditions at the start
    #for system (3); see (5) and (6)
    function varbc_start!(residual1, u1, p)
        residual1[1] = u1[8] - (1/sigma0) #stiffness
        residual1[2] = u1[5] - sigma0 #position var
        residual1[3] = u1[6] - 0 #cross corr
        residual1[4] = u1[7] - 1 #mom var
    end

    #boundary conditions at the end
    function varbc_end!(residual2,u2,p)
        residual2[1] = u2[8] - (1/sigmaT)
        residual2[2] = u2[5] - sigmaT #position var
        residual2[3] = u2[6] - 0 #cross corr
        residual2[4] = u2[7] - 1 #mom var
    end


    tspan = (0.0,T)

    #initial guess
    u0 = [1.0,
            0.0,
            1.0,
            1.0,
            1.0,
            0.0,
            1.0,
            1.0]


    #plot(sol2)

    function b(y)
        return (Lambda^2)*y/(2*g) #harmonic
    end

    bvp2 = TwoPointBVProblem(varevolution!, (varbc_start!, varbc_end!), u0, tspan, p;
                        bcresid_prototype = (zeros(4),zeros(4)))
    sol2 = solve(bvp2, LobattoIIIc5(), dt = 0.01)

    file_out = string("results/harmonic/equil/slowfast/",file_name)

    #save as dataframe
    df_temp = DataFrame(sol2)

    rename!(df_temp, [:t, :f1, :f2, :f3, :f4, :x1, :x2, :x3, :kappa]) #rename 

    ##SAVE CSV HERE
    CSV.write(file_out,DataFrame(sol2))

    print("integration complete. Results in $file_out")

end

if abspath(PROGRAM_FILE) == @__FILE__
    slowfast()
end
