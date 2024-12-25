class ARRAY_CHECK

feature

    my_array: ARRAY [INTEGER]

    create_and_access_array (size: INTEGER)
        do
            create my_array.make(size)
            my_array[1] := 10
            Result := my_array[1]
        end

end
