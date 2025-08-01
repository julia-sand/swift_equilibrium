

using DifferentialEquations;
using DataFrames;
using CSV;


function integrate_full_gaussian(ARGS)
    
    #parameters
    T = parse(Float64,ARGS[1])
    epsilon = parse(Float64,ARGS[2])
    outputloc = ARGS[3]

    p = epsilon #[epsilon]

    sigma0 = 1
    sigmaT = 4

    #boundary conds
    pos_var_start = (sigma0^2)#/beta
    x_var_start = 0 
    mom_var_start = 1#/beta 
    
    pos_var_end = (sigmaT^2)#/beta
    x_var_end = 0 
    mom_var_end = 1#/beta 

    Vqq_end(sig_end) = ((1/sigmaT^2) - (1/sig_end)) #beta*((1/sigmaT^2) - (1/sig_end))
    Vqp_end = 0
    Vpp_end = 0 #1/m

    pos_mu_start = 0 
    mom_mu_start = 0 

    pos_mu_end = 1
    mom_mu_end = 0

    vq_end(mu_end,sig_end) = ((mu_end/sig_end) - pos_mu_end/(sigmaT^2))
    #beta*((mu_end/sig_end) - pos_mu_end/(sigmaT^2))
    #
    vp_end = 0
        
    tspan = (0.0,T)

    #this is the function for the pde we are solving
    function varianceevolution!(du, u, p, t)
        v11, v12, v22, c11, c12, c22 = u
        epsilon = p
        
        du[1] = 6*v12^2 + 2*(v22*c12/c11)^2 + 8*c12*v12*v22/c11 #- 2*(v12^2) + 2*((c12*v22/c11)^2)
        du[2] = v12 + 2*v22*v12 -epsilon*v11 + 2*c12*(v22^2)/c11
        du[3] = 2.0*(v22-v12*epsilon) ##
        du[4] = 2.0*epsilon*c12
        du[5] = epsilon*c22 - 2*c11*v12 - c12 - 2*v22*c12 #-epsilon*(-c22) + 2*c11*v12 - c12*(1-2*v22)
        du[6] = 2 - 2*c22 - 4*c12*v12 - ((4*(c12^2)*v22)/(c11))
        
      end

    #the boundary condition function 
    function varbc!(residual, u, p, t)
        residual[1] = u[1][4] - pos_var_start #the solution at the start
        residual[2] = u[1][5] - x_var_start
        residual[3] = u[1][6] - mom_var_start
        residual[4] = u[end][4] - pos_var_end #Vqq_end #the solution at the end
        residual[5] = u[end][5] - x_var_end
        residual[6] = u[end][6] - mom_var_end
    end

    #initial guess
    u0_var = [0.0,0.0,0.0,1.0,0.0,1.0]

    bvp1 = BVProblem(varianceevolution!, varbc!, u0_var, tspan, p);

    sol1 = solve(bvp1,LobattoIIIa5(),dt=0.01)

    ##SAVE CSV HERE
    df_var = DataFrame(sol1)

    rename!(df_var, [:t, :Vqq, :Vqp, :Vpp, :Qt, :Ct, :Pt]) #rename 
    CSV.write("variance_full.csv",df_var)
    
    println("variance csv ready.")

   
    #this is the function for  pde we are solving
    function meanevolution!(du, u, p, t)
        
        s1,s2,v1,v2 = u
        epsilon = p
        v12(t) = sol1(t,idxs=2)
        v22(t) = sol1(t,idxs=3)
        c11(t) = sol1(t,idxs=4)
        c12(t) = sol1(t,idxs=5)
        
        #du[1] = epsilon*s2
        #du[2] = 2*s1*v12(t) +2*v2-s2*(1-2*v22(t))    
        #du[3] = -2*v12(t)*v2 - (2*(c12(t)^2)*s1*(v22(t)^2))/(c11(t)^2) + (2*c12(t)*s2*(v22(t)^2))/(c11(t))
        #du[4] = (2*c12(t)*s1*(v22(t)^2))/(c11(t)) - 2*s2*(v22(t)^2) - v2*(-1+2*v22(t)) - epsilon*(v1)

        du[1] = epsilon*s2
        du[2] = -s2 - 2*s1*v12(t) - 2*v2 - 2*s2*v22(t)
        du[3] = -2*s1*((c12(t)*v22(t)/c11(t))^2) - v12(t)*(-6*v2-4*s2*v22(t)) - (c12(t)/c11(t))*(4*s1*v12(t)*v22(t)-4*v2*v22(t)-2*s2*(v22(t)^2))
        du[4] = -epsilon*v1 + v2 + 2*v2*v22(t) - (2*c12(t)*s1*(v22(t)^2)/c11(t)) + 2*s2*(v22(t)^2)
   
    end


    #the boundary condition function 
    function meanbc!(residual, u, p, t)
        residual[1] = u[1][1] - pos_mu_start #the solution at the start
        residual[2] = u[1][2] - mom_mu_start
        residual[3] = u[end][1] - pos_mu_end #the solution at the end
        residual[4] = u[end][2] - mom_mu_end
    end

    #initial guess
    u0_mean = [0.0, 0.0, 0.1, 0.2]

    bvp2 = BVProblem(meanevolution!, meanbc!, u0_mean, tspan, p);

    #testing things out
    meansyssol2 = solve(bvp2, LobattoIIIa5(), dt = 0.01);

    ##SAVE CSV HERE
    df_mean = DataFrame(meansyssol2)
    rename!(df_mean, [:t, :qt, :pt, :vq, :vp]) #rename 
    CSV.write("mean_full.csv",df_mean)
    
    println("mean csv ready.")

    df = innerjoin(df_var, df_mean, on=:t)
    
    function u2(v22,v12,c12,c11)
        return 2*v12 + 2*(c12*v22)/c11
    end
    
    function u1(v2,s2,s1,v22,c12,c11)
        return 2*v2 + 2*s2*v22 - 2*(c12*s1*v22)/c11
    end
    
    df[!, "U2"] = u2.(df[!,"Vpp"], df[!,"Vqp"], df[!,"Ct"], df[!,"Qt"])
    df[!, "u1"] = u1.(df[!,"vp"],df[!,"pt"],df[!,"qt"],df[!,"Vpp"], df[!,"Ct"], df[!,"Qt"])
    CSV.write(string(outputloc,"/refsol.csv"),df)
    println("completed.")
        
end

     
integrate_full_gaussian(ARGS)
