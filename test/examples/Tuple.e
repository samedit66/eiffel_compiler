class TUPLE_TEST

feature

    my_tuple: TUPLE [INTEGER, STRING]

    create_tuple (a: INTEGER; b: STRING)
        do
            my_tuple := [a, b]
        end

    get_first: INTEGER
        do
            Result := my_tuple.item1
        end

    get_second: STRING
        do
            Result := my_tuple.item2
        end

end
