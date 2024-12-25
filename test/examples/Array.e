class ARRAY_TEST[T]

feature

    my_array: ARRAY[T]

    create_array (size: INTEGER)
        do
            create my_array.make(size)
        end

end

