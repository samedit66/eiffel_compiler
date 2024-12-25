class INSPECT_TEST

feature

    inspect_example (value: INTEGER): STRING
        local
            a: INTEGER
        do
            inspect a
                when 10 then
                    a := 20
                when 20, 10, 30 then
                    a := 30
                when 1..10 then
                    a := 5
                else
                    a := 19
            end
        end

end

