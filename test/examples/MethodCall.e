class METHOD_CALL_TEST

feature

    current_value: INTEGER

    method_call_example (value: INTEGER)
        do
            current_value := value
            Result := simple_method
        end

    simple_method: INTEGER
        do
            Result := current_value + 1
        end

end

