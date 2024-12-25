class TEST_IF

feature

    test_if (a: INTEGER): STRING
        do
            if a > 0 then
                Result := "Positive"
            elseif a < 0 then
                Result := "Negative"
            else
                Result := "Zero"
            end
        end

end
