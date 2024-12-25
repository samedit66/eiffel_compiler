class TEST_CONTRACT

feature

    compute_sum (a, b: INTEGER): INTEGER
        require
            a_positive: a > 0
            b_positive: b > 0
        do
            Result := a + b
        ensure
            result_positive: Result > 0
        end

end

