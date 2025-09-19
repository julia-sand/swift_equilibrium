using IfElse


function get_file_name(T,epsilon,g,Lambda)
    #=
    Generates a filename containing parameter values
    format:
    T$(T)_Lambda$(Lambda)_eps$(epsilon)_g$(g).csv
    =#

    Ttemp = replace(string(T),"."=>"-")
    Lambdatemp = IfElse.ifelse(Lambda==sqrt(2), "1-4", replace(string(Lambda),"."=>"-"))
    epstemp = replace(string(epsilon),"."=>"-")
    gtemp = replace(string(g),"."=>"-")

    file_name = string("T$(Ttemp)_Lambda$(Lambdatemp)_eps$(epstemp)_g$(gtemp).csv")

    return file_name
end


