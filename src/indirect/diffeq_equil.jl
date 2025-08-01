using DifferentialEquations;
using CSV;
using DataFrames;

#= we start by examining the situation of equilibirum transitions between
two gaussian states

=#

include("../getfilename.jl")


function solve_indirect_equil(ARGS)

    T,g = parse(Float64,ARGS[1]),parse(Float64,ARGS[2])
    Lambda = parse(Float64,ARGS[4]) #sqrt(2)
    epsilon = 1

    file_name = get_file_name(T,epsilon,g,Lambda)
    alpha = 0.1

    model_type = ARGS[3]
    
    sigma0 = 1
    sigmaT = 2
    
    #vector of parameters
    p = epsilon



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
        residual2[4] = u2[4] - (1/sigmaT)
    end

    tspan = (0.0,T)

    #initial guess
    u0 = [1.0,
            0.0,
            1.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0]

    function format_sol(sol,model_type)
        df_temp = DataFrame(sol)

        ##SAVE CSV HERE
        file_out = string("results/$model_type/contract/indirect/",file_name)
        rename!(df_temp, [:t, :x1, :x2, :x3, :kappa, :y1, :y2, :y3, :y4]) #rename 
        CSV.write(file_out,df_temp)
    end   

    if model_type=="control"

        function varevolution_control!(du, u, p, t)
            x1,x2,x3,x4,y1,y2,y3,y4 = u
            du[1] = 2*epsilon*x2  #position var
            du[2] = -x2-epsilon*(x4*x1-x3) #cross corellation
            du[3] = 2*(1-x3-epsilon*x4*x2)  #momentum variance 
            du[4] = y4/g #b_control(y4)
            du[5] = x4*(epsilon*y2+2*alpha*(x1*x4-1))#epsilon*y2*x4 + alpha*((epsilon*x4)^2)
            du[6] = -2*epsilon*y1 + y2 + 2*epsilon*y3*x4
            du[7] = 1 - epsilon*y2 + 2*y3
            du[8] = epsilon*y2*x1 + 2*epsilon*y3*x2 + 2*alpha*x1*(x1*x4-1)
        end

        u0 = [1.0,0.0,1.0,0.0,0.0,0.0,0.0,0.0]

        bvp1 = TwoPointBVProblem(varevolution_control!, (varbc_start!, varbc_end!), u0, tspan, p;
                            bcresid_prototype = (zeros(4),zeros(4)))
        sol = solve(bvp1, LobattoIIIa5(), dt = 0.1)
        format_sol(sol,model_type)
    
    elseif model_type=="log"


        #this is the system for 
        #transition between states with different variance/fixed mean System(3)
        #with first order optimality system (26). 
        function varevolution_log!(du, u, p, t)
            x1,x2,x3,x4,y1,y2,y3,y4 = u
            du[1] = 2*epsilon*x2  #position var
            du[2] = -x2-epsilon*(x4*x1-x3) #cross corellation
            du[3] = 2*(1-x3-epsilon*x4*x2)  #momentum variance 
            du[4] = (g/(y4+1e-10))*(sqrt(1+(Lambda*y4/g)^2)-1) #control
            du[5] = epsilon*y2*x4
            du[6] = -2*epsilon*y1 + y2 + 2*epsilon*y3*x4
            du[7] = 1 - epsilon*y2 + 2*y3
            du[8] = epsilon*y2*x1 + 2*epsilon*y3*x2
        end


        bvp2 = TwoPointBVProblem(varevolution_log!, (varbc_start!, varbc_end!), u0, tspan, p;
        bcresid_prototype = (zeros(4),zeros(4)))
        sol2 = solve(bvp2, LobattoIIIa5(),#nested_nlsolve=true), 
                                dt = 0.1, 
                                progress=true)

        format_sol(sol2,model_type) 

    elseif (model_type=="harmonic")
    
        #this is the system for 
        #transition between states with different variance/fixed mean System(3)
        #with first order optimality system (26). 
        function varevolution_harmonic!(du, u, p, t)
            x1,x2,x3,x4,y1,y2,y3,y4 = u
            du[1] = 2*epsilon*x2  #position var
            du[2] = -x2-epsilon*(x4*x1-x3) #cross corellation
            du[3] = 2*(1-x3-epsilon*x4*x2)  #momentum variance 
            du[4] = y4/g #control
            du[5] = epsilon*y2*x4
            du[6] = -2*epsilon*y1 + y2 + 2*epsilon*y3*x4
            du[7] = 1 - epsilon*y2 + 2*y3
            du[8] = epsilon*y2*x1 + 2*epsilon*y3*x2
        end


        bvp3 = TwoPointBVProblem(varevolution_harmonic!, (varbc_start!, varbc_end!), u0, tspan, p;
        bcresid_prototype = (zeros(4),zeros(4)))
        sol3 = solve(bvp3, LobattoIIIa5(),#nested_nlsolve=true), 
                                dt = 0.1, 
                                progress=true)

        format_sol(sol3,model_type) 
    else
        print("No valid model specified. Only log or harmonic available for now.")
        return
    end


end

solve_indirect_equil(ARGS)

