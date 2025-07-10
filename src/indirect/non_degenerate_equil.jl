using DifferentialEquations;
using CSV;
using DataFrames;

#= Equilibrium transition where the stiffness is the control. 
minimising the ENTROPY PRODUCTION and with NON DEGENERATE dunamics. (see penalty (61))
We treat the stiffness as a STATE. 
=#

include("../getfilename.jl")

function solve_indirect(ARGS)

    T,g = parse(Float64,ARGS[1]), parse(Float64,ARGS[2])
    epsilon = 1
    Lambda = 3.0 #
    alpha = 0.1

    file_name = get_file_name(T,epsilon,g,Lambda)

    model_type = ARGS[3]
    
    sigma0 = 1
    sigmaT = 2

    #vector of parameters
    p = [epsilon]
    tspan = (0.0,T)

    function varevolution_control!(du, u, p, t)
        x1,x2,x3,x4,y1,y2,y3,y4 = u
        du[1] = 2*epsilon*x2 - 2*alpha*(epsilon^2)*(x4*x1-1)  #position var
        du[2] = -x2*(1+alpha*(epsilon^2)*x4) - epsilon*(x4*x1-x3)
        du[3] = 2*(1-x3-epsilon*x4*x2)  #momentum variance 
        du[4] = y4/g #harmonic penalty with \Lambda =\sqrt{2}
        du[5] = epsilon*x4*y2 + alpha*(epsilon^2)*x4*(2*y1+x4)
        du[6] = (1+alpha*(epsilon^2))*y2 + 2*epsilon*(y3*x4-y1)
        du[7] = 1-epsilon*y2+2*y3
        du[8] = epsilon*y2*x1+2*epsilon*y3*x2 + alpha*(epsilon^2)*(2*x1*(x4+y1)+x2*y2-1)
    end

    #the boundary conditions at the start
    #for system (3); see (5) and (6)
    function varbc_start_control!(residual1, u1, p)
        residual1[1] = u1[1] - sigma0 #position var
        residual1[2] = u1[2] - 0 #cross corr
        residual1[3] = u1[3] - 1 #mom var
        residual1[4] = u1[4] - (1/sigma0) #mom var
    end

    #boundary conditions at the end
    function varbc_end_control!(residual2,u2,p)
        residual2[1] = u2[1] - sigmaT #position var
        residual2[2] = u2[2] - 0 #cross corr
        residual2[3] = u2[3] - 1 #mom var
        residual1[4] = u2[4] - (1/sigmaT) #mom var
    end   

    u0 = [1.0,0.0,1.0,0.0,0.0,0.0]

    bvp3 = TwoPointBVProblem(varevolution_control!, (varbc_start_control!, varbc_end_control!), u0, tspan, p;
                        bcresid_prototype = (zeros(4),zeros(4)))
    sol = solve(bvp3, LobattoIIIa5(), dt = 0.1)


    ##SAVE CSV HERE
    file_out = string("results/control/equil/nondegenerate/",file_name)
    df_temp = DataFrame(sol)

    rename!(df_temp, [:t, :x1, :x2, :x3, :kappa, :y1, :y2, :y3, :y4]) #rename 
    #df_temp[!, :kappa] = x4.(df_temp.x1,df_temp.x2,df_temp.y2,df_temp.y3)

    CSV.write(file_out,df_temp)    
end

solve_indirect(ARGS)