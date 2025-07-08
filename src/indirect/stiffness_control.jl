using DifferentialEquations;
using CSV;
using DataFrames;

#= non-equilibrium transition where the stiffness is the control. 
minimising the ENTROPY PRODUCTION 
=#

include("../getfilename.jl")

function solve_indirect(ARGS)

    T,g = parse(Float64,ARGS[1]),parse(Float64,ARGS[2])
    epsilon = 1
    Lambda = parse(Float64,ARGS[4])
    alpha = 0.1

    file_name = get_file_name(T,epsilon,g,Lambda)

    model_type = ARGS[3]
    
    sigma0 = 1
    sigmaT = 2

    #vector of parameters
    p = [epsilon]
    
    function x4(x1,x2,y2,y3) 
        return (x1*(2*alpha-epsilon*y2)-2*epsilon*x2*y3)/(2*alpha*(x1^2))
    end

    function varevolution_control!(du, u, p, t)
        x1,x2,x3,y1,y2,y3 = u
        du[1] = 2*epsilon*x2  #position var
        du[2] = -x2-epsilon*(x4(x1,x2,y2,y3)*x1-x3) #cross corellation
        du[3] = 2*(1-x3-epsilon*x4(x1,x2,y2,y3)*x2)  #momentum variance 
        du[4] = x4(x1,x2,y2,y3)*(epsilon*y2 + 2*alpha*(x1*x4(x1,x2,y2,y3)-1))#epsilon*y2*x4
        du[5] = -2*epsilon*y1 + y2 + 2*epsilon*y3*x4(x1,x2,y2,y3)
        du[6] = 1 - epsilon*y2 + 2*y3
    end

    #the boundary conditions at the start
    #for system (3); see (5) and (6)
    function varbc_start_control!(residual1, u1, p)
        residual1[1] = u1[1] - sigma0 #position var
        residual1[2] = u1[2] - 0 #cross corr
        residual1[3] = u1[3] - 1 #mom var
    end

    #boundary conditions at the end
    function varbc_end_control!(residual2,u2,p)
        residual2[1] = u2[1] - sigmaT #position var
        residual2[2] = u2[2] - 0 #cross corr
        residual2[3] = u2[3] - 1 #mom var
    end   

    u0 = [1.0,0.0,1.0,0.0,0.0,0.0]

    bvp3 = TwoPointBVProblem(varevolution_control!, (varbc_start_control!, varbc_end_control!), u0, tspan, p;
                        bcresid_prototype = (zeros(3),zeros(3)))
    sol = solve(bvp3, LobattoIIIa5(), dt = 0.1)
    


    ##SAVE CSV HERE
    file_out = string("results/control/noneq/indirect/",file_name)
    df_temp = DataFrame(sol)

    rename!(df_temp, [:t, :x1, :x2, :x3, :y1, :y2, :y3]) #rename 
    df_temp[!, :kappa] = x4.(df_temp.x1,df_temp.x2,df_temp.y2,df_temp.y3)

    CSV.write(file_out,df_temp)    