class
    DAY
feature
    month_offset(mm: INTEGER): INTEGER
    local
        months: ARRAY[INTEGER]
        i: INTEGER
    do
        months := <<31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31>>
        from
            i := 1
        until
            i = mm
        loop
            Result := Result + months[i]
        end
    end
end
