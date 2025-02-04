#get all the packages
using InfiniteOpt, Ipopt;
#using Trapz;
#using Distributions;
using CSV;
using DataFrames;
using ForwardDiff;


#=We minimize entropy production between equilibrium states
where the boundary conditions are given by GAUsSIANs
Example 4.1: 
-we keep the means constant, and look only at the change of variance problem
-minimization of dissipation between equilibrium states at fixed time horizon.
=#

include("params.jl")

#boundary condtions


#=
Setup the infinite opt model 
=#

#model parameters 
#L = 10 #number of iterations
#num_supports_t = 11 #size of time mesh

##################################
#Setup the model
#create a new model object
model = InfiniteModel(Ipopt.Optimizer);

set_optimizer_attribute(model, "max_iter", L)

#time
@infinite_parameter(model, t in [0, T], num_supports = num_supports_t)#, derivative_method=FiniteDifference(Forward(), true))


#initialisations
###TODO###
function x_init(t)
    return t 
end 


#position variance
@variable(model, x1>=0, Infinite(t), start = x_init)

#cross corellation
@variable(model, x2, Infinite(t), start = x_init)

#momentum variance 
@variable(model, x3>=0, Infinite(t), start = x_init)

#the optimal control
@variable(model, lambda, Infinite(t), start = x_init)

#function for the 
if model_type=="log"
    @parameter_function(model,logfun==log(1-((lambda(t)^2)/Lambda)))
end

#define the objective, see Eq. (12)
if model_type=="log"
    @objective(model, Min, 
            integral(x3-g*logfun, t))
elseif model_type=="harmonic"
    @objective(model, Min, 
            integral(x3+g*(lambda^2)/2, t))
elseif model_type=="hard"
    @objective(model, Min, 
            integral(x3, t))
else
    print("No valid model penalty type specified. Use log, harmonic or hard")
end

        
#boundary conditions
#initial
@constraint(model, x1(0) == sigma0)
@constraint(model, x2(0) == 0)
@constraint(model, x3(0) == 1)
@constraint(model, lambda(0) == 1/sigma0)

#final
@constraint(model, x1(T) == sigmaT)
@constraint(model, x2(T) == 0)
@constraint(model, x3(T) == 1)
@constraint(model, lambda(T) == 1/sigmaT)

if model_type=="hard"
    #penalty on the controls: in a compact set
    @constraint(model, Lambda <= lambda <= Lambda)
end

# SOLVE THE MODEL
optimize!(model)


########################


####save a csv file  
if model_type=="log"
        file_name = "swift_equilibrium/results/log/ep_equil_ipopt_v1.csv"
    elseif model_type=="harmonic"
        file_name = "swift_equilibrium/results/harmonic/ep_equil_ipopt_v1.csv"
    elseif model_type=="hard"
        file_name = "swift_equilibrium/results/hard/ep_equil_ipopt_v1.csv"
    else
        print("No model found for this penalty type. Use either log, harmonic or hard.")
end

# Define the header as an array of strings
row = ["t" "x1" "x2" "x3" "lambda"]
header = DataFrame(row,["t", "x1", "x2", "x3", "lambda"])
coords = hcat(collect.(supports(x1))...)'

# Write the header to a new CSV file
CSV.write(file_name, header;header =false)

df = DataFrame([coords[:,1],value(x1),value(x2),value(x3),value(lambda)],
                    ["t", "x1", "x2", "x3", "lambda"])

CSV.write(file_name, df, append =true)
    




