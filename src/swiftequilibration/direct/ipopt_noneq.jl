using InfiniteOpt, Ipopt;
using CSV;
using DataFrames;

#=
We minimize Work eq.(10) between non-equilibrium states
where the boundary conditions are given by GAUSSIANs
Example 4.1: 
-we keep the means constant, and look only at the change of variance problem
-minimization of dissipation between equilibrium states at fixed time horizon.
-stiffness (kappa) is a state 
=#

#get parsed parameters
include("../getfilename.jl")
include("initialisation_funs.jl")

############################

function solve_direct(ARGS)
    #=
    Sets up the infinite opt model using command line arguments. 
    Optimises the model
    Writes results to CSV
    =#

    #set parameters
    T,g = parse(Float64,ARGS[1]),parse(Float64,ARGS[2])
    epsilon = 1
    Lambda = parse(Float64,ARGS[4]) #sqrt(2)
    alpha=0.1

    #generate file name
    file_name = get_file_name(T,epsilon,g,Lambda)

    model_type = ARGS[3]
    constraint_kappa = ARGS[5]
    
    #initial and final values of \sigma
    sigma0 = 1
    sigmaT = 2
    
    #define model
    model = InfiniteModel(Ipopt.Optimizer);
    #set_optimizer_attributes(model,"max_iter" => 3000)

    #add variables
    #time
    @infinite_parameter(model, t in [0, T], num_supports = 6001, 
                        derivative_method=FiniteDifference(Forward(), true))

    #position variance
    @variable(model, 0<=x1, Infinite(t), start = 1)

    #cross corellation
    @variable(model, x2, Infinite(t), start = 0)

    #momentum variance 
    @variable(model, 0<=x3, Infinite(t), start = 1)

    #the stiffness (a state)
    @variable(model, kappa, Infinite(t), start = 1)

    #final value of kappa as a variable
    @variable(model, kappa_final)
    
    #function for the log penalty
    function logfun(y)
        
        return InfiniteOpt.ifelse(abs(y) <= Lambda-1e-4, log(1-((y/Lambda)^2)), 1000000)
    end

    #define the objective, see Eq. (20)
    if model_type=="log"
        @objective(model, Min, 
                    kappa_final + integral(x3-g*logfun(deriv(kappa,t)), t))
    elseif model_type=="harmonic"
        @objective(model, Min, 
                    kappa_final + integral(x3+(g/2)*(deriv(kappa,t))^2, t))
    elseif model_type=="hard"
        @objective(model, Min, 
                    (kappa_final*sigmaT)/2 + integral(x3, t))
    else
        print("No valid model penalty type specified. Use log, harmonic, or hard")
    end

    #boundary conditions
    #initial
    @constraint(model, x1(0) == sigma0)
    @constraint(model, x2(0) == 0)
    @constraint(model, x3(0) == 1)
    @constraint(model, kappa(0) == 1/sigma0)

    #final
    @constraint(model, x1(T) == sigmaT)
    @constraint(model, x2(T) == 0)
    @constraint(model, x3(T) == 1)
    
    @constraint(model, kappa(T) == kappa_final)

    if model_type=="hard"
        #penalty on the controls: in a compact set
        @constraint(model, -Lambda <= deriv(kappa,t) <= Lambda)
    end
    
    #Constraint on kappa, Eq. (50)
    if constraint_kappa=="kappa"
        @constraint(model, 0.2 <= kappa <= 1.2)
    end

    #enforce the dynamics, see system (3)
    @constraint(model, deriv(x1,t) == 2*epsilon*x2)
    @constraint(model, deriv(x2,t) == -x2-epsilon*(kappa*x1-x3))
    @constraint(model, deriv(x3,t) == 2*(1-x3-epsilon*kappa*x2))

    # SOLVE THE MODEL
    optimize!(model)

    ########################


    #save the results of the optimisation
    coords = hcat(collect.(supports(x1))...)'
    
    data_rows = [coords[:,1],value(x1),value(x2),value(x3),value(kappa)]
    
    
    df = DataFrame(data_rows,
                        ["t", "x1", "x2", "x3", "kappa"])

    folder = "results/$model_type/noneq/direct/"
    if constraint_kappa=="kappa"
        folder2 = string(folder,"constrained_kappa/")
        CSV.write(string(folder2,file_name), df)
    else 
        CSV.write(string(folder,file_name), df)
    end
    
end   
    
solve_direct(ARGS)

