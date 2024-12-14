class
    LINKED_QUEUE
inherit
    QUEUE
        undefine
            is_empty,
            copy,
            is_equal
        redefine
            linear_representation,
            prune_all,
            extend
        select
            item,
            put
        end
    LINKED_LIST
        rename
            item as ll_item,
            remove as ll_remove,
            make as ll_make,
            remove_left as remove,
            put as ll_put
        undefine
            fill,
            append,
            prune,
            readable,
            writable,
            prune_all,
            extend,
            force,
            is_inserted
        redefine
            duplicate,
            linear_representation
        select
            remove
        end
end
