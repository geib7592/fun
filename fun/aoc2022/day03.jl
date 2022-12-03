function sum_duplicates(fname; part)
    s = 0
    if part == 1
        for line in eachline(fname)
            s += priority(first(find_duplicates(line[1:Int64(length(line)/2)], line[Int64(length(line)/2+1):end])))
        end
    elseif part == 2
        open(fname, "r") do file
            while true
                if eof(file)
                    break
                end
                s += priority(first(find_duplicates(readline(file), readline(file), readline(file))))
            end
        end
    end
    return s
end

function find_duplicates(rucksack1, rucksack2)
    return rucksack2[findall(in(rucksack1), rucksack2)]
end

function find_duplicates(rucksack1, rucksack2, rucksack3)
    return find_duplicates(find_duplicates(rucksack1, rucksack2), rucksack3)
end

function priority(item::Char)
    # 'a'--'z' = 97--122 ↦ 1--26
    # 'A'--'Z' = 65--90  ↦ 27--52
    return Int64(item) - 38 - 58*islowercase(item)
end

println(sum_duplicates("input_files/day03_hgp.txt", part=1)) # 128.790 μs
println(sum_duplicates("input_files/day03_hgp.txt", part=2)) # 113.832 μs