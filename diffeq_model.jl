using DifferentialEquations;
using Plots;
#= we start by examining the situation of equilibirum transitions between
two gaussian states

=#

#select which penalty (update so this can be parsed from command line)
#model_type = "hard"

include("params.jl")

###penalty function
function lambda(y)
    if model_type=="log"
        return (g/y)*(sqrt(1+(Lambda*y/g)^2)-1)
    elseif model_type=="harmonic"
        return y/g #harmonic
    elseif model_type=="hard"
        return 0
    else
        print("No valid model specified. Use either log, harmonic or hard")
        return
    end
end


#boundary conditions
pos_mean_init = 0
pos_mean_final = 1
pos_var_init = 1
pos_var_final = 2

#this is the system for 
#transition between states with different variance/fixed mean System(3)
#with first order optimality system (26). 
function varevolution!(du, u, epsilon, t)
    x1,x2,x3,x4,y1,y2,y3,y4 = u
    #epsilon = p
    du[1] = 2*epsilon*x3  #position var
    du[2] = -x2-epsilon*(x4*x1-x3) #cross corellation
    du[3] = 2*(1-x3-epsilon*x4*x2)  #momentum variance 
    du[4] = lambda(y4)  #control
    du[5] = epsilon*y2*x4
    du[6] = -2*epsilon*y1 + y2 + 2*epsilon*y3*x4
    du[7] = 1-epsilon*y2+2*y3
    du[8] = epsilon*y2*x1+2*epsilon*y3*x2
end


function varevolution_hard!(du, u, epsilon, t)
    x1,x2,x3,x4,y1,y2,y3,y4 = u
    #epsilon = p
    du[1] = 2*epsilon*x3  #position var
    du[2] = -x2-epsilon*(x4*x1-x3) #cross corellation
    du[3] = 2*(1-x3-epsilon*x4*x2)  #momentum variance 
    du[4] = lambda(y4)  #control
    du[5] = epsilon*y2*x4
    du[6] = -2*epsilon*y1 + y2 + 2*epsilon*y3*x4
    du[7] = 1-epsilon*y2+2*y3
    du[8] = epsilon*y2*x1+2*epsilon*y3*x2
end

#this is the system for 
#transition between states with different MEAN/fixed VAR System(4)
function meanevolution!(du, u, epsilon, t)
    x4,x5,x6,x7 = u
    #epsilon = p
    du[1] = lambda(t)  #control
    du[2] = epsilon*x6  #position mean 
    du[3] = -x6+epsilon*(x7-x4*x5)   #momentum mean
    du[4] = gamma(t)  #control
end

#the boundary conditions at the start
#for system (3); see (5) and (6)
function varbc_start!(residual1, u, epsilon)
    residual1[1] = u[1][1] - pos_var_init #position var
    residual1[2] = u[1][2] - 0 #cross corr
    residual1[3] = u[1][3] - 1 #mom var
    residual1[4] = u[1][4] - 1/pos_var_init #gradient of stiffness
end

#boundary conditions at the end
function varbc_end!(residual2,u,epsilon)
    residual2[1] = u[end][1] - pos_var_final #position var
    residual2[2] = u[end][2] - 0 #cross corr
    residual2[3] = u[end][3] - 1 #mom var
    residual2[4] = u[end][4] - 1/pos_var_final #grad of stiffness
end


#the boundary condition function for system (4); see (5)
function meanbc!(residual, u, epsilon)
    residual[1] = u[1][3] - 0 #the mom mean at the start
    residual[2] = u[end][3] - 0 #the mom mean at the end
end

tspan = (0.0,T)

#p = epsilon

#initial guess
u0 = [0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0]

varresid_proto = (zeros(4), zeros(4))


bvp2 = TwoPointBVProblem(varevolution!, (varbc_start!, varbc_end!), u0, tspan;
                                bcresid_prototype = varresid_proto)
sol2 = solve(bvp2, MIRK4(), dt = 0.05)


plot(sol2)
savefig("test.png")