deferred class NUMERIC
feature

    add (other: like Current): like Current
        deferred
    end

end


class REAL
inherit
    NUMERIC
feature

    add (other: like Current): like Current
        external
            "Java"
        alias
            "com.eiffel.base.REAL.add"
    end

    to_integer: INTEGER
        external
            "Java"
        alias
            "com.eiffel.base.INTEGER.to_real"
    end

end


class INTEGER
inherit
    NUMERIC
feature

    add (other: like Current): like Current
        external
            "Java"
        alias
            "com.eiffel.base.INTEGER.add"
    end
    
    to_real: REAL
        external
            "Java"
        alias
            "com.eiffel.base.INTEGER.to_real"
    end

end