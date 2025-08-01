using DifferentialEquations;
using CSV;
using DataFrames;

#= we start by examining the situation of equilibirum transitions between
two gaussian states
=#

include("../getfilename.jl")

function solve_indirect(ARGS)
    print("hello")
    T,g = parse(Float64,ARGS[1]),parse(Float64,ARGS[2])
    epsilon = 1
    Lambda = sqrt(2)
    alpha = 0.1

    file_name = get_file_name(T,epsilon,g,Lambda)

    model_type = ARGS[3]
    
    sigma0 = 1
    sigmaT = 2

    function b(y) #initialise function b

        if model_type=="log"
            return (g/(y+1e-10))*(sqrt(1+(Lambda*y/g)^2)-1)
        elseif model_type=="harmonic"    
            return y/g #harmonic
        else 
            return 0
        end
        
    end

    #vector of parameters
    p = [epsilon]
    
    #with first order optimality system (26). 
    function varevolution!(du, u, p, t)
        x1,x2,x3,x4,y1,y2,y3,y4 = u
        du[1] = 2*epsilon*x2  #position var
        du[2] = -x2-epsilon*(x4*x1-x3) #cross corellation
        du[3] = 2*(1-x3-epsilon*x4*x2)  #momentum variance 
        du[4] = b(y4)  #control
        du[5] = epsilon*y2*x4
        du[6] = -2*epsilon*y1 + y2 + 2*epsilon*y3*x4
        du[7] = 1-epsilon*y2+2*y3
        du[8] = epsilon*y2*x1+2*epsilon*y3*x2
    end


    #the boundary conditions at the start
    #for system (3); see (5) and (6)
    function varbc_start!(residual1, u1, p)
        residual1[1] = u1[1] - sigma0 #position var
        residual1[2] = u1[2] - 0 #cross corr
        residual1[3] = u1[3] - 1 #mom var
        residual1[4] = u1[4] - (1/sigma0) #stiffness
    end
    
    #boundary conditions at the end
    function varbc_end!(residual2,u2,p)
        residual2[1] = u2[1] - sigmaT #position var
        residual2[2] = u2[2] - 0 #cross corr
        residual2[3] = u2[3] - 1 #mom var
        #residual2[4] = u2[4] - (1/sigmaT)
        residual2[4] = u2[8] + (sigmaT/2)#u2[8] + (u2[4]/2)
    end


    tspan = (0.0,T)

    #initial guess
    u0 = [1.0,
            0.0,
            1.0,
            1.0,
            0.0,
            0.0,
            0.0,
            0.0]
    
    function format_sol(sol,model_type)
        df_temp = DataFrame(sol)
        ##SAVE CSV HERE
        file_out = string("results/$model_type/noneq/indirect/",file_name)
        rename!(df_temp, [:t, :x1, :x2, :x3, :kappa, :y1, :y2, :y3, :y4]) #rename 
        CSV.write(file_out,df_temp)
    end

    bvp2 = TwoPointBVProblem(varevolution!, (varbc_start!, varbc_end!), u0, tspan, p;
                        bcresid_prototype = (zeros(4),zeros(4)))
    sol = solve(bvp2, LobattoIIIa5(), dt = 0.1)
    
    format_sol(sol,model_type)

end


solve_indirect(ARGS)