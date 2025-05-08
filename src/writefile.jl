using DataFrames, CSV

function get_file_out(model_type,equil_flag,direct_flag)
      
   return "swift_equilibrium/results/$model_type/$equil_flag/$direct_flag/"


function save_results(model_type,
                        equil_flag,
                        direct_flag,
                        file_name,data_rows)
    
    row = ["t" "x1" "x2" "x3" "kappa"]
    header = DataFrame(row,["t", "x1", "x2", "x3", "kappa"])

    file_out = string(get_file_out(model_type),file_name)

    # Write the header to a new CSV file
    CSV.write(file_out, header; header =false)

    df = DataFrame(data_rows,
                        ["t", "x1", "x2", "x3", "kappa"])

    CSV.write(file_out, df, append =true)
end
