

using DifferentialEquations;
using DataFrames;
using CSV;
   

function integrate_gaussian(ARGS)
    
    #parameters
    T = parse(Float64,ARGS[1])
    outputloc = ARGS[2]

    tau = 1
    beta = 2
    m = 1

    p = [beta,tau,m]

    sigma0 = 1
    sigmaT = 2

    #boundary conds
    pos_var_start = (sigma0^2)/beta
    x_var_start = 0 
    mom_var_start = 1/beta 

    Vqq_end = 1/(sigmaT^2)
    Vqp_end = 0
    Vpp_end = 1/m

    pos_mu_start = 0 
    mom_mu_start = 0 

    pos_mu_end = 1
    mom_mu_end = 0

    vq_end = -pos_mu_end/(sigmaT^2)
    vp_end = 0
        
    tspan = (0.0,T)

    function Ut(Vpp, Vqp, Ct, Qt)
        return ((2*m)/(beta*tau))*(Vpp*Ct/Qt + Vqp)
    end

    function u1(qt, Vpp, Vqp, Ct, Qt)
        return -Ut(Vpp, Vqp, Ct, Qt)*qt
    end

    function u2(vp,pt,qt,Vpp,Vqp)
        return ((2*m)/(beta*tau))*(vp + Vqp*qt + Vpp*pt)
    end
    
    function ut(vp,pt,qt,Vpp, Vqp, Ct, Qt)
        return u1(qt, Vpp, Vqp, Ct, Qt) + u2(vp,pt,qt,Vpp,Vqp)
    end

    #this is the function for the pde we are solving
    function varianceevolution!(du, u, p, t)
        Vqq, Vqp, Vpp, Qt, Ct, Pt = u
        beta,tau,m = p

        du[1] = 2*Vqp*Ut(Vpp, Vqp, Ct, Qt) - ((beta*tau)/(2*m))*(Ut(Vpp, Vqp, Ct, Qt)^2)
        du[2] = Vqp/tau + Ut(Vpp, Vqp, Ct, Qt)*Vpp - Vqq/m
        du[3] = 2*Vpp/tau - 2*Vqp/m
        du[4] = 2*Ct/m 
        du[5] = -Ct/tau - Ut(Vpp, Vqp, Ct, Qt)*Qt + Pt/m
        du[6] = -2*Pt/tau - 2*Ut(Vpp, Vqp, Ct, Qt)*Ct + (2*m/(tau*beta)) 
    end

    #the boundary condition function 
    function varbc!(residual, u, p, t)
        residual[1] = u[1][4] - pos_var_start #the solution at the start
        residual[2] = u[1][5] - x_var_start
        residual[3] = u[1][6] - mom_var_start
        residual[4] = u[end][1] - Vqq_end #the solution at the end
        residual[5] = u[end][2] - Vqp_end
        residual[6] = u[end][3] - Vpp_end
    end

    #initial guess
    u0_var = [0.0,0.0,0.0,1.0,0.0,1.0]

    bvp1 = BVProblem(varianceevolution!, varbc!, u0_var, tspan, p);

    sol1 = solve(bvp1,LobattoIIIa5(),dt=0.01)

    ##SAVE CSV HERE
    df_var = DataFrame(sol1)

    rename!(df_var, [:t, :Vqq, :Vqp, :Vpp, :Qt, :Ct, :Pt]) #rename 
    CSV.write("variance.csv",df_var)
    
    println("variance csv ready.")

    #meansys
    function meanevolution!(du, u, p, t)
        
        qt,pt,vq,vp = u
        beta,tau,m = p

        U_0(t) = Ut(sol1(t,idxs=3), sol1(t,idxs=2), sol1(t,idxs=5), sol1(t,idxs=4))
        u_0(vp,pt,qt,t) = ut(vp,pt,qt,sol1(t,idxs=3), sol1(t,idxs=2), sol1(t,idxs=5), sol1(t,idxs=4))
        #u_1_0(qt,t) = u1(qt, sol1(t,idxs=3), sol1(t,idxs=2), sol1(t,idxs=5), sol1(t,idxs=4))
        u_2_0(vp,pt,qt,t) = u2(vp,pt,qt,sol1(t,idxs=3), sol1(t,idxs=2))

        du[1] = pt/m 
        du[2] = - (pt/tau + u_2_0(vp,pt,qt,t))
        du[3] = sol1(t,idxs=2)*u_0(vp,pt,qt,t) + vp*U_0(t) - ((beta*tau)/(2*m))*U_0(t)*u_0(vp,pt,qt,t)
        du[4] = vp/tau - vq/m + sol1(t,idxs=3)*u_0(vp,pt,qt,t)

    end

    #the boundary condition function 
    function meanbc!(residual, u, p, t)
        residual[1] = u[1][1] - pos_mu_start #the solution at the start
        residual[2] = u[1][2] - mom_mu_start
        residual[3] = u[end][3] - vq_end #the solution at the end
        residual[4] = u[end][4] - vp_end
    end

    #initial guess
    u0_mean = [0.0, 0.0, 0.1, 0.2]

    bvp2 = BVProblem(meanevolution!, meanbc!, u0_mean, tspan, p);

    #testing things out
    meansyssol2 = solve(bvp2, LobattoIIIa5(), dt = 0.01);

    ##SAVE CSV HERE
    df_mean = DataFrame(meansyssol2)
    rename!(df_mean, [:t, :qt, :pt, :vq, :vp]) #rename 
    CSV.write("mean.csv",df_mean)
    
    println("mean csv ready.")

    df = innerjoin(df_var, df_mean, on=:t)

    df[!, "U2"] = Ut.(df[!,"Vpp"], df[!,"Vqp"], df[!,"Ct"], df[!,"Qt"])
    df[!, "u1"] = ut.(df[!,"vp"],df[!,"pt"],df[!,"qt"],df[!,"Vpp"], df[!,"Vqp"], df[!,"Ct"], df[!,"Qt"])
    CSV.write(string(outputloc,"/refsol.csv"),df)
    println("completed.")
        
end

     
integrate_gaussian(ARGS)