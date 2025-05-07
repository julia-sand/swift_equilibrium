#get all the packages
using InfiniteOpt, Ipopt;

#=We minimize entropy production between EQUILIBRIUM states
where the boundary conditions are given by GAUSSIANs
Example 4.1: 
-we keep the means constant, and look only at the change of variance problem
-minimization of dissipation between equilibrium states at fixed time horizon.
=#

#get parsed parameters
include("params.jl")
include("initialisation_funs.jl")
include("writefile.jl")
############################

#=
Setup the infinite opt model 
=#
function solve_direct_equil()
    
    parsed_args = parse_commandline()
    file_name = get_file_name(parsed_args)
    model_type = parse_args["penalty"]


    Lambda =parse_args["Lambda"]
    T =parse_args["tf"]
    sigma0 = parsed_args["sigma0"]
    sigmaT = parsed_args["sigmaT"]

    epsilon = parsed_args["epsilon"]
    g = parsed_args["g"]


    model = InfiniteModel(Ipopt.Optimizer);

    set_optimizer_attribute(model, "max_iter", L)

    #time
    @infinite_parameter(model, 
                            t in [0, T], 
                            num_supports = num_supports_t, 
                            derivative_method=FiniteDifference(Forward(), true))

    #position variance
    @variable(model, 0<=x1, Infinite(t), start=0)

    #cross corellation
    @variable(model, x2, Infinite(t), start=0)

    #momentum variance 
    @variable(model, 0<=x3, Infinite(t), start=0)

    #the optimal control
    #Constraint on kappa, Eq. (50)
    #@variable(model, 0.2 <= kappa <=1.2, Infinite(t), start=0)
    @variable(model, kappa, Infinite(t), start=0)

    #function for the log penalty
    function logfun(y)
        
        return InfiniteOpt.ifelse(abs(y) <= Lambda-1e-4, log(1-((y/Lambda)^2)), 1000000)
    end

    #define the objective, see Eq. (20)
    if model_type=="log"
        @objective(model, Min, 
                integral(x3-g*logfun(deriv(kappa,t)), t))
    elseif model_type=="harmonic"
        @objective(model, Min, 
                integral(x3+g*(deriv(kappa,t)/Lambda)^2, t))
    elseif model_type=="hard"
        @objective(model, Min, 
                integral(x3, t))
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

    #for model between equilibrium systems, we need the following constraint (7)&(8)
    if model_type != "control"
        @constraint(model, kappa(0) == 1/sigma0)
        @constraint(model, kappa(T) == 1/sigmaT)
    end

    if model_type=="hard"
        #penalty on the controls: in a compact set
        @constraint(model, -Lambda <= deriv(kappa,t) <= Lambda)
    end

    #enforce the dynamics, see system (3)
    @constraint(model, deriv(x1,t) == 2*epsilon*x2)
    @constraint(model, deriv(x2,t) == -x2-epsilon*(kappa*x1-x3))
    @constraint(model, deriv(x3,t) == 2*(1-x3-epsilon*kappa*x2))
    #Constraint on kappa, Eq. (50)
    #@constraint(model, 0.2 <= kappa <=1.2)

    #@constraint(model, deriv(kappa,t) == lambda)

    # SOLVE THE MODEL
    optimize!(model)

    ########################


    # Define the header as an array of strings
    coords = hcat(collect.(supports(x1))...)'
    
    data_rows = [coords[:,1],value(x1),value(x2),value(x3),value(kappa)]
    
    save_results(model_type,file_name,data_rows)

end


if abspath(PROGRAM_FILE) == @__FILE__
    solve_direct_equil()
end
