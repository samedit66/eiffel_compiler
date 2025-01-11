class ANY
create
    default_create
feature
-- Конструкторы

    default_create
    do
        -- По умолчанию тут ничего не происходит...
    end

feature
-- Строковое представление объекта

    to_string, out: STRING
        external "Java"
    end

feature
-- Операции ввода/вывода

    write (obj: ANY)
        external "Java"
    end

    writeln (obj: ANY)
        external "Java"
    end

    print
    do
        -- Удобное сокращение для печати:
        -- local
        --     a: INTEGER
        -- do
        --     a := 10
        --     a.print
        -- end
        writeln (out)
    end
    
    readln: STRING
        external "Java"
    end

end
