class OPERATORS_TEST

feature

    calculate (a, b: INTEGER): INTEGER
        do
            Result := a + b * (a - b) / (a + b)
        end

    logic_test (a, b: BOOLEAN): BOOLEAN
        do
            Result := a or else b
        end

end

