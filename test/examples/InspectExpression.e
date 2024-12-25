class INSPECT_TEST

feature

    inspect_example (value: INTEGER): STRING
        do
            Result := inspect value
                1: "One"
                2: "Two"
                else: "Other"
            end
        end

end
