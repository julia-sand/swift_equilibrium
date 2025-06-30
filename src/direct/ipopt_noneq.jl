#get all the packages
using InfiniteOpt, Ipopt;
using CSV;
using DataFrames;

#=We minimize entropy production between non-equilibrium states
where the boundary conditions are given by GAUSSIANs
Example 4.1: 
-we keep the means constant, and look only at the change of variance problem
-minimization of dissipation between equilibrium states at fixed time horizon.
=#

#get parsed parameters
include("../getfilename.jl")
include("../initialisation_funs.jl")

############################

#=
Setup the infinite opt model 
=#
function solve_direct(ARGS)

    T,g = parse(Float64,ARGS[1]),parse(Float64,ARGS[2])
    epsilon = 1
    Lambda = sqrt(2) #parse(Float64,ARGS[4]) #sqrt(2)

    file_name = get_file_name(T,epsilon,g,Lambda)

    model_type = ARGS[3]
    
    sigma0 = 1
    sigmaT = 2
    
    model = InfiniteModel(Ipopt.Optimizer);

    #time
    @infinite_parameter(model, t in [0, T], num_supports = 3001)#, derivative_method=FiniteDifference(Forward(), true))

    #position variance
    @variable(model, x1>=0, Infinite(t), start = x1_init)

    #cross corellation
    @variable(model, x2, Infinite(t), start = x2_init)

    #momentum variance 
    @variable(model, x3>=0, Infinite(t), start = x3_init)

    #the optimal control
    @variable(model, kappa, Infinite(t), start = kappa_init)

    @variable(model, kappa_final)

    #function for the log penalty
    function logfun(y)
        
        return InfiniteOpt.ifelse(abs(y) <= Lambda-1e-4, log(1-((y/Lambda)^2)), 1000000)
    end

    #define the objective, see Eq. (20)
    if model_type=="log"
        @objective(model, Min, 
                    (kappa_final*sigmaT)/2 + integral(x3-g*logfun(deriv(kappa,t)), t))
    elseif model_type=="harmonic"
        @objective(model, Min, 
                    (kappa_final*sigmaT)/2 + integral(x3+g*(deriv(kappa,t)/Lambda)^2, t))
    elseif model_type=="hard"
        @objective(model, Min, 
                    (kappa_final*sigmaT)/2 + integral(x3, t))
    elseif model_type=="control"
        @objective(model, Min, 
                integral(x3 + g*kappa*(kappa*x1-1), t))
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
    
    if model_type !="control"
        @constraint(model, kappa(T) == kappa_final)
    end

    if model_type == "control"
        @constraint(model, kappa(0) == 1/sigma0)
        @constraint(model, kappa(T) == 1/sigmaT)
    end

    if model_type=="hard"
        #penalty on the controls: in a compact set
        @constraint(model, -Lambda <= deriv(kappa,t) <= Lambda)
    end
    
    #additional constraint on kappa
    @constraint(model, -Lambda/2 <= kappa <= Lambda/2)


    # SOLVE THE MODEL
    optimize!(model)

    ########################


    # Define the header as an array of strings
    coords = hcat(collect.(supports(x1))...)'
    
    data_rows = [coords[:,1],value(x1),value(x2),value(x3),value(kappa)]
    
    
    df = DataFrame(data_rows,
                        ["t", "x1", "x2", "x3", "kappa"])

    folder = "results/$model_type/noneq/direct/"
    CSV.write(string(folder,file_name), df)
    
end   
    

solve_direct(ARGS)



