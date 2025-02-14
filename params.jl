using ArgParse

#=
This file sets up boundary conditions and parameters for the models
Arguments can be passed from the command line and are parsed here
=#


function parse_commandline()
    s = ArgParseSettings()

    @add_arg_table s begin
        "--tf"
            help = "final time"
            arg_type = Float64
            default = 3
        "--epsilon"
            help = "dimensionless parameter"
            arg_type = Float64
            default = 1
        "--tsteps"
            help = "number of time coordinates in discretisation"
            arg_type = Int
            default = 11
        "--maxiters"
            help = "maximum iteration of the optimizer IPOpt."
            arg_type = Int
            default = 3000
        "--penalty"
            help = "Type of penalty used in the model. Choose from log, harmonic or hard"
            arg_type = String
            default = "log"
        "--g"
            help = "penalty weighting parameter. Used for log and harmonic penalties"
            arg_type = Float64
            default = 0.01
        "--Lambda"
            help = "bound for the stiffness, used in the hard and log penalty models"
            arg_type = Float64
            default = 1
        "--sigma0"
            help = "Assigned initial position variance"
            arg_type = Float64
            default = 1
        "--sigmaT"
            help = "Assigned final position variance"
            arg_type = Float64
            default = 2
        #"--equilibrium"
        #    help = "Whether to model a transition between equilibrium states or out of equilibrium"
        #    arg_type = Bool
        #    default = false    
    end

    return parse_args(s)
end

parsed_args = parse_commandline()

##get parsed parameters
const T = parsed_args["tf"]
const num_supports_t = parsed_args["tsteps"]
const epsilon = parsed_args["epsilon"]
const L = parsed_args["maxiters"]
const model_type = parsed_args["penalty"]
const Lambda = parsed_args["Lambda"]
const g = parsed_args["g"]
const sigma0 = parsed_args["sigma0"]
const sigmaT = parsed_args["sigmaT"]
#const equilibrium = parse_args["equilibrium"]

#add constant params
const pos_mean = 1
const mom_mean = 1

Ttemp = replace(string(T),"."=>"-")
Lambdatemp = replace(string(Lambda),"."=>"-")
epstemp = replace(string(epsilon),"."=>"-")
gtemp = replace(string(g),"."=>"-")


file_name = string("T$(Ttemp)_Lambda$(Lambdatemp)_eps$(epstemp)_g$(gtemp).csv")
