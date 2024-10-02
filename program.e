note
    description : "root class of the application"
    date        : "$Date$"
    revision    : "$Revision$"

class
    APPLICATION

inherit
    ARGUMENTS_32

create
    make

feature {NONE} -- Initialization

    make
            -- Run application.
        local
            n1: INTEGER
            n2: REAL
        do
            n1 := 100__000_____000
            n2 := .5
            -- Add your code here
            print (n1)
            io.put_new_line
            print (n2)
            io.put_new_line
            print ("Hello Eiffel World!%N")
        end

end