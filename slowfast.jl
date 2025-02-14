using DifferentialEquations;
using CSV;
using DataFrames;

#= we start by examining the situation of equilibirum transitions between
two gaussian states

=#

include("params.jl")

#vector of parameters
p = [epsilon,gscale]

gscale = g^4

#this is the system for 
#transition between states with different variance/fixed mean System(3)
#with first order optimality system (26). 
function varevolution!(du, u, p, t)
    epsilon,gscale = p
    f1,f2,f3,f4,x1,x2,x3,x4 = u
    du[1] = gscale*epsilon*f2 #position var
    du[2] = gscale*2*f3 #cross corellation
    du[3] = -gscale*f4/x1  #momentum variance 
    du[4] = gscale*epsilon*f1*(x1^2)  #control
    du[5] = 2*epsilon*x2
    du[6] = epsilon*(x3-x1*x4)-x2
    du[7] = -2*(epsilon*x2*x4+x3-1)
    du[8] = f1-(2*epsilon*x2*(4*epsilon*x3-5*x2)+x1*(9*epsilon*x3-3*x2-6*epsilon)-3*epsilon*(x1^2)*x4-8*(epsilon^2)*((x2^3)/x1))/(epsilon*(x1^2))
end


#the boundary conditions at the start
#for system (3); see (5) and (6)
function varbc_start!(residual1, u1, p)
    residual1[1] = u1[1] - (1/sigma0) #stiffness
    residual1[2] = u1[5] - sigma0 #position var
    residual1[3] = u1[6] - 0 #cross corr
    residual1[4] = u1[7] - 1 #mom var
end

#boundary conditions at the end
function varbc_end!(residual2,u2,p)
    residual2[1] = u2[1] - (1/sigmaT)
    residual2[2] = u2[5] - sigmaT #position var
    residual2[3] = u2[6] - 0 #cross corr
    residual2[4] = u2[7] - 1 #mom var
    #residual2[4] = u2[8] + sigmaT/2 
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
bvp2 = TwoPointBVProblem(varevolution_invariant!, (varbc_start!, varbc_end!), u0, tspan, p;
                    bcresid_prototype = (zeros(4),zeros(4)))
sol2 = solve(bvp2, LobattoIIIa5(), dt = 0.05)

##SAVE CSV HERE
file_out = string("swift_equilibrium/results/harmonic/slowfast/",file_name)
CSV.write(file_out,DataFrame(sol2))

