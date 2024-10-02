class
    EXAMPLE_STRING

create
    make

feature {NONE} -- Initialization

    make
            -- Initialize the object.
        local
            s: STRING
            length: INTEGER
            s1: STRING
        do
            s1 := "[
                Some long
                long
                string
            ]"

            s := "Hello, World!";
            length := s.count; -- Calculate the length of the string

            -- Output the string and its length
            io.put_string("String: ");
            io.put_string(s);
            io.put_new_line;
            io.put_string("Length: ");
            io.put_integer(length);
            io.put_new_line;

            -- Concatenate strings
            s := s + " Welcome!";
            io.put_string("Concatenated String: ");
            io.put_string(s);
            io.put_new_line;

            -- Extract a substring
            s := s.substring(7, 5);
            io.put_string("Substring: ");
            io.put_string(s);
            io.put_new_line;
        end
end

100_0000
10e4
10.5e-15
0b1010100101001
0c1451
0O4124
0xcafebabe

"%(%)"

'%/65/'