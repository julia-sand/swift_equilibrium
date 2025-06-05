

using DifferentialEquations;
using DataFrames;
using CSV;
   

function integrate_gaussian()
    #parameters
    T = 5
    tau = 1
    beta = 2
    m = 1

    p = [beta,tau,m]

    #boundary conds
    pos_sigma_start = 1
    x_sigma_start = 0 
    mom_sigma_start = 1 

    pos_sigma_end = 2

    #pos_sigma_end = 2
    Vqq_end = 1/(pos_sigma_end^2)
    Vqp_end = 0
    Vpp_end = 1

    pos_mu_start = 0 
    mom_mu_start = 0 

    pos_mu_end = 1
    mom_mu_end = 0
        
    tspan = (0.0,T)

    #copied from existing code

    #this is the function for the pde we are solving
    function varianceevolution!(du, u, p, t)
        Vqq, Vqp, Vpp, Qt, Ct, Pt = u
        beta,tau,m = p

        du[1] = 2*((Vpp*Ct)/Qt + Vqp)*Vqp - (beta*tau/(2*m))*(((Vpp*Ct)/Qt + Vqp)^2)
        du[2] = Vqp/tau + ((Vpp*Ct)/Qt + Vqp)*Vpp - Vqq/m
        du[3] = 2*Vpp/tau - 2*Vqp/m
        du[4] = 2*Ct/m 
        du[5] = -Ct/tau - ((Vpp*Ct)/Qt + Vqp)*Qt - Pt/m
        du[6] = -2*Pt/tau - 2*((Vpp*Ct)/Qt + Vqp)*Ct + (2*m/(tau*beta)) 
    end

    #the boundary condition function 
    function bc!(residual, u, p, t)
        residual[1] = u[1][4] - pos_sigma_start #the solution at the start
        residual[2] = u[1][5] - x_sigma_start
        residual[3] = u[1][6] - mom_sigma_start
        residual[4] = u[end][1] - Vqq_end #the solution at the end
        residual[5] = u[end][2] - Vqp_end
        residual[6] = u[end][3] - Vpp_end
    end



    #initial guess
    u0_var = [0.0,0.0,0.0,1.0,0.0,1.0]

    bvp1 = BVProblem(varianceevolution!, bc!, u0_var, tspan, p);

    sol1 = solve(bvp1,LobattoIIIa5(),dt=0.01)

    ##SAVE CSV HERE
    df_temp = DataFrame(sol1)

    rename!(df_temp, [:t, :Vqq, :Vqp, :Vpp, :Qt, :Ct, :Pt]) #rename 
    CSV.write("variance.csv",df_temp)
    
    println("variance csv ready.")

    #functions
    function Vqq(t) #
        return sol1(t)[1]
    end

    function Vqp(t) #
        return sol1(t)[2]
    end

    function Vpp(t) #
        return sol1(t)[3]
    end

    function Ut(t) 
        return Vpp(t)*sol1(t)[5]/sol1(t)[4]
    end


    #meansys
    function meanevolution!(du, u, p, t)
        
        qt,pt,vq,vp = u
        beta,tau,m = p
        
        du[1] = pt/m 
        
        du[2] = -(pt/tau + (-Ut(t)+ (2*m)/(beta*tau)*(vp+Vqp(t)*qt+Vpp(t)*pt)) + Ut(t)*qt)
        
        du[3] = Vqp(t)*(-Ut(t)+ (2*m)/(beta*tau)*(vp+Vqp(t)*qt+Vpp(t)*pt)) + Ut(t)*vp - (beta*tau/(2*m))*Ut(t)*(-Ut(t)+ (2*m)/(beta*tau)*(vp+Vqp(t)*qt+Vpp(t)*pt))
        
        du[4] = vp/tau - vq/m + Vpp(t)*(-Ut(t)+ (2*m)/(beta*tau)*(vp+Vqp(t)*qt+Vpp(t)*pt)) 

    end

    #the boundary condition function 
    function meanbc!(residual, u, p, t)
        residual[1] = u[1][1] - pos_mu_start #the solution at the start
        residual[2] = u[1][2] - mom_mu_start
        residual[3] = u[end][1] - (-pos_mu_end/(pos_sigma_end^2)) #the solution at the end
        residual[4] = u[end][2] - 0
    end


    #initial guess
    u0_mean = [0.0, 0.0, 0.1, 0.2]

    bvp2 = BVProblem(meanevolution!, meanbc!, u0_mean, tspan, p);

    #testing things out
    meansyssol2 = solve(bvp2, LobattoIIIa5(), dt = 0.01);

    ##SAVE CSV HERE
    df_temp = DataFrame(meansyssol2)
    rename!(df_temp, [:t, :qt, :pt, :vq, :vp]) #rename 
    CSV.write("mean.csv",df_temp)
    
    println("mean csv ready.")
    println("completed.")
        
end

     
integrate_gaussian()