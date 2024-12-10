#include "./include/json.h"

void
add_type_to_node(Json *node, char *type_name) {
    Json_add_string_to_object(node, "type", type_name);
}

Json*
mk_empty() {
    Json *node = Json_new();
    add_type_to_node(node, "empty");
    return node;
}

Json*
mk_int_const(int val) {
    Json *node = Json_new();
    add_type_to_node(node, "int_const");
    Json_add_int_to_object(node, "value", val);
    return node;
}

Json*
mk_char_const(int val) {
    Json *node = Json_new();
    add_type_to_node(node, "char_const");
    Json_add_int_to_object(node, "value", val);
    return node;
}

Json*
mk_real_const(double val) {
    Json *node = Json_new();
    add_type_to_node(node, "real_const");
    Json_add_double_to_object(node, "value", val);
    return node;
}

Json*
mk_string_const(char *val) {
    Json *node = Json_new();
    add_type_to_node(node, "string_const");
    Json_add_string_to_object(node, "value", val);
    return node;
}

Json*
mk_result_const() {
    Json *node = Json_new();
    add_type_to_node(node, "result_const");
    return node;
}

Json*
mk_current_const() {
    Json *node = Json_new();
    add_type_to_node(node, "current_const");
    return node;
}

Json*
mk_boolean_const(bool val) {
    Json *node = Json_new();
    add_type_to_node(node, "boolean_const");
    Json_add_bool_to_object(node, "value", val);
    return node;
}

Json*
mk_void_const() {
    Json *node = Json_new();
    add_type_to_node(node, "void_const");
    return node;
}

Json*
mk_ident_lit(char *ident) {
    Json *node = Json_new();
    add_type_to_node(node, "ident_lit");
    Json_add_string_to_object(node, "value", ident);
    return node;
}

Json*
mk_bin_op(char *op_name, Json *left, Json *right) {
    Json *node = Json_new();
    add_type_to_node(node, op_name);
    Json_add_object_to_object(node, "left", left);
    Json_add_object_to_object(node, "right", right);
    return node;
}

Json*
mk_unary_op(char *op_name, Json *arg) {
    Json *node = Json_new();
    add_type_to_node(node, op_name);
    Json_add_object_to_object(node, "arg", arg);\
    return node;
}

Json*
mk_simple_call(char *feature_name, Json *args_list) {
    Json *simple_call = Json_new();
    Json_add_string_to_object(simple_call, "name", feature_name);
    Json_add_array_to_object(simple_call, "args_list", args_list);
    return simple_call;
}

Json*
mk_list() {
    return Json_new();
}

Json*
add_to_list(Json *list, Json *element) {
    Json_add_object_to_array(list, element);
    return list;
}

Json*
add_ident_to_list(Json *list, char *ident) {
    Json_add_string_to_array(list, ident);
    return list;
}

Json*
mk_simple_call_no_args(char *feature_name) {
    return mk_simple_call(feature_name, mk_list());
}

Json*
mk_precursor_args_call(Json *args_list) {
    Json *node = Json_new();
    add_type_to_node(node, "precursor_call");
    Json_add_array_to_object(node, "args_list", args_list);
    return node;
}

Json*
mk_precursor_no_args_call() {
    return mk_precursor_args_call(mk_list());
}

Json*
mk_feature_with_owner_call(Json *owner, Json *feature) {
    Json *node = Json_new();
    add_type_to_node(node, "feature_call");
    
    if (owner != NULL)
        Json_add_object_to_object(node, "owner", owner);
    else
        Json_add_object_to_object(node, "owner", mk_empty());
    Json_add_object_to_object(node, "feature", feature);
    return node;
}

Json*
mk_feature_with_unknown_owner_call(Json *feature) {
    return mk_feature_with_owner_call(NULL, feature);
}

Json*
mk_bracket_access(Json *source, Json *index) {
    Json *node = Json_new();
    add_type_to_node(node, "bracket_access");
    Json_add_object_to_object(node, "source", source);
    Json_add_object_to_object(node, "index", index);
    return node;
}

Json*
mk_if_expr(Json *cond, Json *then_expr, Json *alt_exprs, Json *else_expr) {
    Json *node = Json_new();
    add_type_to_node(node, "if_expr");
    Json_add_object_to_object(node, "cond", cond);
    Json_add_object_to_object(node, "then_expr", then_expr);
    Json_add_array_to_object(node, "elseif_exprs", alt_exprs);
    Json_add_object_to_object(node, "else_expr", else_expr);
    return node;
}

Json*
add_elseif_expr(Json *alts, Json *cond, Json *expr) {
    Json *alt = Json_new();
    add_type_to_node(alt, "elseif_expr");
    Json_add_object_to_object(alt, "cond", cond);
    Json_add_object_to_object(alt, "expr", expr);
    Json_add_object_to_array(alts, alt);
    return alts;
}

Json*
mk_program(Json *program) {
    Json *node = Json_new();
    add_type_to_node(node, "root");
    Json_add_array_to_object(node, "program", program);
    return node;
}

Json*
mk_if_stmt(Json *cond, Json *then_stmt_list, Json *alt_stmts, Json *else_stmt_list) {
    Json *node = Json_new();
    add_type_to_node(node, "if_stmt");
    Json_add_object_to_object(node, "cond", cond);
    Json_add_array_to_object(node, "then_clause", then_stmt_list);
    Json_add_array_to_object(node, "elseif_clauses", alt_stmts);
    Json_add_array_to_object(node, "else_clause", else_stmt_list);
    return node;
}

Json*
add_elseif_stmt(Json *alts, Json *cond, Json *stmt_list) {
    Json *alt = Json_new();
    add_type_to_node(alt, "elseif_clause");
    Json_add_object_to_object(alt, "cond", cond);
    Json_add_array_to_object(alt, "body", stmt_list);
    Json_add_object_to_array(alts, alt);
    return alts;
}

Json*
mk_assign_stmt(Json *left, Json *right) {
    Json *node = Json_new();
    add_type_to_node(node, "assign_stmt");
    Json_add_object_to_object(node, "left", left);
    Json_add_object_to_object(node, "right", right);
    return node;
}

Json*
mk_loop_stmt(Json *init_stmt_list, Json *cond, Json *body_stmt_list) {
    Json *node = Json_new();
    add_type_to_node(node, "loop_stmt");
    Json_add_object_to_object(node, "init", init_stmt_list);
    Json_add_object_to_object(node, "cond", cond);
    Json_add_array_to_object(node, "body", body_stmt_list);
    return node;
}

Json*
mk_inspect_stmt(Json *expr, Json *when_clauses, Json *else_stmt_list) {
    Json *node = Json_new();
    add_type_to_node(node, "inspect_stmt");
    Json_add_object_to_object(node, "expr", expr);
    Json_add_array_to_object(node, "when_clauses", when_clauses);
    Json_add_array_to_object(node, "else_clause", else_stmt_list);
    return node;
}

Json*
add_alt_when_clause(Json *when_clauses, Json *choices, Json *body) {
    Json *when_stmt = Json_new();
    Json_add_array_to_object(when_stmt, "choices", choices);
    Json_add_object_to_object(when_stmt, "body", body);
    Json_add_object_to_array(when_clauses, when_stmt);
    return when_clauses;
}

Json*
mk_choice_interval(Json *start, Json *end) {
    Json *node = Json_new();
    add_type_to_node(node, "choice_interval");
    Json_add_object_to_object(node, "start", start);
    Json_add_object_to_object(node, "end", end);
    return node;
}

Json*
mk_type(char *type_name) {
    Json *user_type = Json_new();
    add_type_to_node(user_type, "type_spec");
    Json_add_string_to_object(user_type, "type_name", type_name);
    return user_type;
}

Json*
mk_integer_type() {
    return mk_type("INTEGER");
}

Json*
mk_real_type() {
    return mk_type("REAL");
}

Json*
mk_string_type() {
    return mk_type("STRING");
}

Json*
mk_character_type() {
    return mk_type("CHARACTER");
}

Json*
mk_boolean_type() {
    return mk_type("BOOLEAN");
}

Json*
mk_like_type(Json *like_what) {
    Json *type_spec_like = Json_new();
    add_type_to_node(type_spec_like, "type_spec_like");
    Json_add_object_to_object(type_spec_like, "like_what", like_what);
    return type_spec_like;
}

Json*
mk_like_current_type() {
    return mk_like_type(mk_current_const());
}

Json*
mk_like_other_field_type(char *field_name) {
    return mk_like_type(mk_ident_lit(field_name));
}

Json*
mk_generic_user_type(char *type_name, Json *type_list) {
    Json *generic_type_spec = Json_new();
    add_type_to_node(generic_type_spec, "generic_type_spec");
    Json_add_string_to_object(generic_type_spec, "type_name", type_name);
    Json_add_array_to_object(generic_type_spec, "type_list", type_list);
    return generic_type_spec;
}

Json*
mk_generic_array_type(Json *type_list) {
    return mk_generic_user_type("ARRAY", type_list);
}

Json*
mk_generic_tuple_type(Json *type_list) {
    return mk_generic_user_type("TUPLE", type_list);
}

Json*
mk_class_decl(Json *header, Json *inheritance, Json *creators, Json *features) {
    Json *class_decl = Json_new();

    Json_add_object_to_object(class_decl, "header", header);
    Json_add_array_to_object(class_decl, "inheritance", inheritance);
    Json_add_array_to_object(class_decl, "creators", creators);
    Json_add_array_to_object(class_decl, "features", features);

    return class_decl;
}

Json*
mk_class_header(char *class_name, Json *generics_list) {
    Json *class_header = Json_new();

    Json_add_string_to_object(class_header, "name", class_name);
    Json_add_array_to_object(class_header, "generics", generics_list);

    return class_header;
}

Json*
mk_constrained_generic(Json *generic_type, Json *parent) {
    Json *constrained_generic = Json_new();

    Json_add_object_to_object(constrained_generic, "generic_type", generic_type);
    Json_add_object_to_object(constrained_generic, "parent", parent);

    return constrained_generic;
}
