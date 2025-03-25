using DifferentialEquations;
using CSV;
using DataFrames;

#= we start by examining the situation of equilibirum transitions between
two gaussian states

=#

include("params.jl")

#vector of parameters
p = [epsilon]

###penalty function

#this is the system for 
#transition between states with different variance/fixed mean System(3)
#with first order optimality system (26). 
function varevolution!(du, u, p, t)
    x1,x2,x3,x4,y1,y2,y3,y4 = u
    du[1] = 2*epsilon*x2  #position var
    du[2] = -x2-epsilon*(x4*x1-x3) #cross corellation
    du[3] = 2*(1-x3-epsilon*x4*x2)  #momentum variance 
    du[4] = b(y4) #control
    du[5] = epsilon*y2*x4
    du[6] = -2*epsilon*y1 + y2 + 2*epsilon*y3*x4
    du[7] = 1 - epsilon*y2 + 2*y3
    du[8] = epsilon*y2*x1 + 2*epsilon*y3*x2
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
    residual2[4] = u2[4] - (1/sigmaT)
    #residual2[4] = u2[8] + sigmaT/2 
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

if model_type=="log"
    function b(y)
        
        return (g/(y+1e-10))*(sqrt(1+(Lambda*y/g)^2)-1)
    end

    bvp2 = TwoPointBVProblem(varevolution!, (varbc_start!, varbc_end!), u0, tspan, p;
                        bcresid_prototype = (zeros(4),zeros(4)))
    sol2 = solve(bvp2, LobattoIIIa5(),#nested_nlsolve=true), 
                        dt = 0.1, 
                        progress=true)

    ##SAVE CSV HERE
    file_out = string("swift_equilibrium/results/log/equil/indirect/",file_name)
    df_temp = DataFrame(sol2)
    rename!(df_temp, [:t, :x1, :x2, :x3, :kappa, :y1, :y2, :y3, :y4]) #rename 
    CSV.write(file_out,df_temp)


elseif model_type=="harmonic"
    function b(y)
        return (Lambda^2)*y/(2*g) #harmonic
    end

    bvp2 = TwoPointBVProblem(varevolution!, (varbc_start!, varbc_end!), u0, tspan, p;
                        bcresid_prototype = (zeros(4),zeros(4)))
    sol2 = solve(bvp2, LobattoIIIa5(), dt = 0.05)
    
    ##SAVE CSV HERE
    file_out = string("swift_equilibrium/results/harmonic/equil/indirect/",file_name)
    df_temp = DataFrame(sol2)
    rename!(df_temp, [:t, :x1, :x2, :x3, :kappa, :y1, :y2, :y3, :y4]) #rename 
    CSV.write(file_out,df_temp)

elseif model_type=="control"
    
    alpha = g
    
    function varevolution!(du, u, p, t)
        x1,x2,x3,y1,y2,y3 = u
        x4 = (alpha*epsilon - x1*y2 - 2*x2*y3)/(2*alpha*epsilon*x1)
        du[1] = 2*epsilon*x2  #position var
        du[2] = -x2-epsilon*(x4*x1-x3) #cross corellation
        du[3] = 2*(1-x3-epsilon*x4*x2)  #momentum variance 
        du[4] = epsilon*y2*x4
        du[5] = -2*epsilon*y1 + y2 + 2*epsilon*y3*x4
        du[6] = 1 - epsilon*y2 + 2*y3
    end

    #the boundary conditions at the start
    #for system (3); see (5) and (6)
    function varbc_start!(residual1, u1, p)
        residual1[1] = u1[1] - sigma0 #position var
        residual1[2] = u1[2] - 0 #cross corr
        residual1[3] = u1[3] - 1 #mom var
    end

    #boundary conditions at the end
    function varbc_end!(residual2,u2,p)
        residual2[1] = u2[1] - sigmaT #position var
        residual2[2] = u2[2] - 0 #cross corr
        residual2[3] = u2[3] - 1 #mom var
    end   

    u0 = [1.0,0.0,1.0,0.0,0.0,0.0]

    bvp2 = TwoPointBVProblem(varevolution!, (varbc_start!, varbc_end!), u0, tspan, p;
                        bcresid_prototype = (zeros(3),zeros(3)))
    sol = solve(bvp2, LobattoIIIa5(), dt = 0.05)
    

    function x4(t)
        return (alpha*epsilon-sol(t)[1]*sol(t)[5]-2*sol(t)[2]*sol(t)[6])/(2*alpha*epsilon*sol(t)[1])
    end


    ##SAVE CSV HERE
    file_out = string("swift_equilibrium/results/control/equil/indirect/",file_name)
    df_temp = DataFrame(sol)

    rename!(df_temp, [:t, :x1, :x2, :x3, :y1, :y2, :y3]) #rename 
    
    df_temp[!, :kappa] = x4.(df_temp.t)
    CSV.write(file_out,df_temp)
        
else
    print("No valid model specified. Only log or harmonic available for now.")
    return
end

