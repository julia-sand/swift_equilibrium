
#initialisations
function x1_init(t)
    return (t/3) + 1#t + 1 
end 

function x2_init(t)
    return sin(t*(2*pi/3))/3#(t-1)^3
end 

function x3_init(t)
    return 0.03*(((t-1.5)^2) - 1.5^2 )+ 1 #t^2
end 

function kappa_init(t)
    return (((0.5-t)^2)*(t-2.5)^2)/3 + 0.5
end 

function lambda_init(t)
    return 0*t
end 