using ArgParse
using IfElse;

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
            default = 301
        "--maxiters"
            help = "maximum iteration of the optimizer IPOpt."
            arg_type = Int
            default = 3000
        "--penalty"
            help = "Type of penalty used in the model. Choose from log, harmonic, control or hard"
            arg_type = String
            default = "log"
            required = false
        "--g"
            help = "penalty weighting parameter. Used for log and harmonic penalties"
            arg_type = Float64
            default = 0.01
        "--Lambda"
            help = "bound for the stiffness, used in the hard and log penalty models"
            arg_type = Float64
            default = sqrt(2)
        "--sigma0"
            help = "Assigned initial position variance"
            arg_type = Float64
            default = 1
        "--sigmaT"
            help = "Assigned final position variance"
            arg_type = Float64
            default = 2
        "--alpha"
            help = "penalty weighting parameter. Used for control penalties"
            arg_type = Float64
            default = 0.01        
    end

    return parse_args(s)
end



