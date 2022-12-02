function total_score(fname; part)
    score = 0
    for line in eachline(fname)
        opponent = decrypt_to_RPS(line[1])

        if part == 1
            response = decrypt_to_RPS(line[3])
            score += round_score(opponent, response)
        elseif part == 2
            if line[3] == 'X'
                response = circshift(opponent, -1)
            elseif line[3] == 'Y'
                response = opponent
                score += 3 # tie
            elseif line[3] == 'Z'
                response = circshift(opponent, 1)
                score += 6 # win
            else
                error("Invalid response code.")
            end
        end

        score += response_score(response)
    end
    # println("My score is $score.")
    return score
end

function response_score(response)
    # 1 for R, 2 for P, 3 for S
    return response'*[1, 2, 3]
end

function round_score(opponent, response)
    if response == opponent
        # tie
        return 3
    elseif response == circshift(opponent, 1)
        # win
        return 6
    elseif response == circshift(opponent, -1)
        # loss
        return 0
    end
end

function decrypt_to_RPS(x)
    if x == 'A' || x == 'X'
        # R
        return [1, 0, 0]
    elseif x == 'B' || x == 'Y'
        # P
        return [0, 1, 0]
    elseif x == 'C' || x == 'Z'
        # S
        return [0, 0, 1]
    else
        error("Invalid encrypted key.")
    end
end

total_score("input_files/day02_hgp.txt"; part=1) # 345.971 μs
total_score("input_files/day02_hgp.txt"; part=2) # 279.882 μs