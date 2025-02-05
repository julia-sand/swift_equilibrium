#get all the packages
using InfiniteOpt, Ipopt;
using CSV;
using DataFrames;
#using ForwardDiff;

#=We minimize entropy production between EQUILIBRIUM states
where the boundary conditions are given by GAUSSIANs
Example 4.1: 
-we keep the means constant, and look only at the change of variance problem
-minimization of dissipation between equilibrium states at fixed time horizon.
=#

#get parsed parameters
include("params.jl")

############################

#=
Setup the infinite opt model 
=#

model = InfiniteModel(Ipopt.Optimizer);

set_optimizer_attribute(model, "max_iter", L)

#time
@infinite_parameter(model, t in [0, T], num_supports = num_supports_t)#, derivative_method=FiniteDifference(Forward(), true))

#initialisations
function x1_init(t)
    return t + 1 
end 

function x2_init(t)
    return (t-1)^3
end 

function x3_init(t)
    return t^2
end 

function kappa_init(t)
    return 1
end 

function lambda_init(t)
    return 0*t
end 


#position variance
@variable(model, x1>=0, Infinite(t), start = x1_init)

#cross corellation
@variable(model, x2, Infinite(t), start = x2_init)

#momentum variance 
@variable(model, x3>=0, Infinite(t), start = x3_init)

#the optimal control
#Constraint on kappa, Eq. (50)
@variable(model, 0.2 <= kappa <=1.2, Infinite(t))

#the optimal control
@variable(model, lambda, Infinite(t))


#function for the log penalty
function logfun(y)
    
    return InfiniteOpt.ifelse(abs(y) <= Lambda-1e-4, log(1-((y/Lambda)^2)), 1000000)
end

#define the objective, see Eq. (20)
if model_type=="log"
    @objective(model, Min, 
            integral(x3^2-g*logfun(lambda), t))
elseif model_type=="harmonic"
    @objective(model, Min, 
            integral(x3^2+g*(lambda/Lambda)^2, t))
elseif model_type=="hard"
    @objective(model, Min, 
            integral(x3^2, t))
elseif model_type=="control"
    @objective(model, Min, 
            integral(x3^2 + g*lambda*(lambda*x1-1), t))
else
    print("No valid model penalty type specified. Use log, control, harmonic or hard")
end

        
#boundary conditions
#initial
@constraint(model, x1(0) == sigma0)
@constraint(model, x2(0) == 0)
@constraint(model, x3(0) == 1)
#final
@constraint(model, x1(T) == sigmaT)
@constraint(model, x2(T) == 0)
@constraint(model, x3(T) == 1)

#for model between equilibrium systems, we need the following constraint (7)&(8)
@constraint(model, kappa(0) == 1/sigma0)
@constraint(model, kappa(T) == 1/sigmaT)

if model_type=="hard"
    #penalty on the controls: in a compact set
    @constraint(model, -Lambda <= lambda <= Lambda)
end

#enforce the dynamics, see system (3)
@constraint(model, deriv(x1,t) == 2*epsilon*x3)
@constraint(model, deriv(x2,t) == -x2-epsilon*(kappa*x1-x3))
@constraint(model, deriv(x3,t) == 2*(1-x3-epsilon*kappa*x2))
#Constraint on kappa, Eq. (50)
#@constraint(model, 0.2 <= kappa <=1.2)

@constraint(model, deriv(kappa,t) == lambda)

# SOLVE THE MODEL
optimize!(model)


########################


####save a csv file  
if model_type=="log"
        file_name = "swift_equilibrium/results/log/ep_equil_ipopt_v3.csv"
    elseif model_type=="harmonic"
        file_name = "swift_equilibrium/results/harmonic/ep_equil_ipopt_v3.csv"
    elseif model_type=="hard"
        file_name = "swift_equilibrium/results/hard/ep_equil_ipopt_v3.csv"
    elseif model_type=="control"
        file_name = "swift_equilibrium/results/control/ep_equil_ipopt_v3.csv"
    else
        print("No model found for this penalty type. Use either log, control, harmonic or hard.")
end

# Define the header as an array of strings
row = ["t" "x1" "x2" "x3" "kappa" "lambda"]
header = DataFrame(row,["t", "x1", "x2", "x3", "kappa", "lambda"])
coords = hcat(collect.(supports(x1))...)'

# Write the header to a new CSV file
CSV.write(file_name, header;header =false)

df = DataFrame([coords[:,1],value(x1),value(x2),value(x3),value(kappa),value(lambda)],
                    ["t", "x1", "x2", "x3", "kappa", "lambda"])

CSV.write(file_name, df, append =true)
    




