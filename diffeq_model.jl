using DifferentialEquations;
using CSV;
using DataFrames;

#= we start by examining the situation of equilibirum transitions between
two gaussian states

=#

#select which penalty (update so this can be parsed from command line)
#model_type = "hard"

include("params.jl")

#vector of parameters
p = [epsilon]


###penalty function
function b(y)
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

#this is the system for 
#transition between states with different variance/fixed mean System(3)
#with first order optimality system (26). 
function varevolution!(du, u, p, t)
    x1,x2,x3,x4,y1,y2,y3,y4 = u
    #eps = p[1]
    du[1] = 2*epsilon*x3  #position var
    du[2] = -x2-epsilon*(x4*x1-x3) #cross corellation
    du[3] = 2*(1-x3-epsilon*x4*x2)  #momentum variance 
    du[4] = b(y4)  #control
    du[5] = epsilon*y2*x4
    du[6] = -2*epsilon*y1 + y2 + 2*epsilon*y3*x4
    du[7] = 1-epsilon*y2+2*y3
    du[8] = epsilon*y2*x1+2*epsilon*y3*x2
end


function varevolution_hard!(du, u, p, t)
    x1,x2,x3,x4,y1,y2,y3,y4 = u
    #eps = p[1]
    du[1] = 2*epsilon*x3  #position var
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
    residual1[4] = u1[4] - 1/sigma0 #stiffness
end

#boundary conditions at the end
function varbc_end!(residual2,u2,p)
    residual2[1] = u2[1] - sigmaT #position var
    residual2[2] = u2[2] - 0 #cross corr
    residual2[3] = u2[3] - 1 #mom var
    residual2[4] = u2[8] + sigmaT/2 
end


tspan = (0.0,T)

#initial guess
u0 = [0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0]


#plot(sol2)

if model_type=="log"

    bvp2 = TwoPointBVProblem(varevolution!, (varbc_start!, varbc_end!), u0, tspan, p;
    bcresid_prototype = (zeros(4), zeros(4)))
    sol2 = solve(bvp2, MIRK4(), dt = 0.05)
    
    ##SAVE CSV HERE
    CSV.write("swift_equilibrium/results/log/ep_noneq_diffeq_v1.csv",DataFrame(sol2))


elseif model_type=="harmonic"
    bvp2 = TwoPointBVProblem(varevolution!, (varbc_start!, varbc_end!), u0, tspan, p;
    bcresid_prototype = (zeros(promote_type(eltype(x),typeof(t)),4), zeros(promote_type(eltype(x),typeof(t)),4)))
    sol2 = solve(bvp2, MIRK4(), dt = 0.05

    ##SAVE CSV HERE
    CSV.write("swift_equilibrium/results/harmonic/ep_noneq_diffeq_v1.csv",DataFrame(sol2))

    
    #elseif model_type=="hard"
    #savefig("test_hard.png")
else
    print("No valid model specified. Use either log or harmonic. Hard penalty is not yet completed.")
    return
end

