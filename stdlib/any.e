class ANY

create
    default_create

feature
-- Конструкторы

    default_create
    -- Конструктор по умолчанию.
    -- Вызывается в случае написания конструкции:
    --     create x и create {SOME_TYPE}
    -- Данные конструкции эквиваленты следующим:
    --     create x.default_create и create {SOME_TYPE}.default_create
    -- По умолчанию никаких действий не выполняет.
    do
    end

feature
-- Различные представления объекта

    to_string, out: STRING
    -- Строковое представление объекта.
    -- По умолчанию возвращает строку с описанием местоположения
    -- объекта в памяти.
    external "Java"
    end

feature
-- Операции ввода/вывода

    write (obj: ANY)
    -- Выводит объект в стандартный поток вывода.
    -- При необходимости пытается преобзовать его в строку 
    -- с помощью метода out.
    external "Java"
    end

    writeln (obj: ANY)
    -- Выводит объект в стандартный поток вывода с переводом строки.
    do
        write (obj.out + "%N")
    end

    print
    -- Печатает объект, у которого определен, на экран.
    -- Удобное сокращение для ситуаций вида:
    -- local
    --     a: INTEGER
    -- do
    --     a := 10
    --     a.print
    -- end
    do
        writeln (out)
    end
    
    readln: STRING
    -- Выполняет считывает строки с потока ввода и возращает ее.
    external "Java"
    end

end
