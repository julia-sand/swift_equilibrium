using DataFrames, CSV

function save_results(model_type,file_name,data_rows)
    ####save a csv file  
    if model_type=="log"
        file_out = string("swift_equilibrium/results/log/equil/direct/" , file_name)
    elseif model_type=="harmonic"
        file_out = string("swift_equilibrium/results/harmonic/equil/direct/" , file_name)
    elseif model_type=="hard"
        file_out = string("swift_equilibrium/results/hard/equil/direct/" , file_name)
    elseif model_type=="control"
        file_out = string("swift_equilibrium/results/control/equil/direct/" , file_name)
    else
        print("No model found for this penalty type. Use either log, control, harmonic or hard.")
    end
    row = ["t" "x1" "x2" "x3" "kappa"]
    header = DataFrame(row,["t", "x1", "x2", "x3", "kappa"])

    # Write the header to a new CSV file
    CSV.write(file_out, header; header =false)

    df = DataFrame(data_rows,
                        ["t", "x1", "x2", "x3", "kappa"])

    CSV.write(file_out, df, append =true)
end
