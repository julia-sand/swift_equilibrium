using IfElse
#=
This file sets up boundary conditions and parameters for the models
Arguments can be passed from the command line and are parsed here
=#

function get_file_name(T,epsilon,g,Lambda)
    
    Ttemp = replace(string(T),"."=>"-")
    Lambdatemp = IfElse.ifelse(Lambda==sqrt(2), "1-4", replace(string(Lambda),"."=>"-"))
    epstemp = replace(string(epsilon),"."=>"-")
    gtemp = replace(string(g),"."=>"-")

    file_name = string("T$(Ttemp)_Lambda$(Lambdatemp)_eps$(epstemp)_g$(gtemp).csv")

    return file_name
end


