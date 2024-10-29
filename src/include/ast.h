
#ifndef __AST_H__
#define __AST_H__

#include <stdio.h>
#include <stdlib.h>

typedef enum EXPR_TYPE {
    INT_CONST,
    REAL_CONST,
    ADD_OP,
    SUB_OP,
    MUL_OP,
    DIV_OP
} EXPR_TYPE;

typedef struct Expr {
    enum EXPR_TYPE expr_type;
    struct Expr *op1;
    struct Expr *op2;
    int int_num;
    double real_num;
} Expr;

Expr *Expr_int_const(int int_num) {
    Expr *expr = (Expr*) malloc(sizeof(Expr));
    expr->expr_type = INT_CONST;
    expr->int_num = int_num;
    return expr;
}

Expr *Expr_real_const(double real_num) {
    Expr *expr = (Expr*) malloc(sizeof(Expr));
    expr->expr_type = REAL_CONST;
    expr->real_num = real_num;
    return expr;
}

static Expr *Expr_bin_op(EXPR_TYPE expr_type, Expr *l, Expr *r) {
    Expr *expr = (Expr*) malloc(sizeof(Expr));
    expr->expr_type = expr_type;
    expr->op1 = l;
    expr->op2 = r;
    return expr;
}

Expr *Expr_add_op(Expr *l, Expr *r) {
    return Expr_bin_op(ADD_OP, l, r);
}

Expr *Expr_sub_op(Expr *l, Expr *r) {
    return Expr_bin_op(SUB_OP, l, r);
}

Expr *Expr_mul_op(Expr *l, Expr *r) {
    return Expr_bin_op(MUL_OP, l, r);
}

Expr *Expr_div_op(Expr *l, Expr *r) {
    return Expr_bin_op(DIV_OP, l, r);
}

static void print_tree_(Expr *expr) {
    switch (expr->expr_type) {
        case INT_CONST:
            printf("%d", expr->int_num);
            break;
        case REAL_CONST:
            printf("%f", expr->real_num);
            break;
        case ADD_OP:
            print_tree_(expr->op1);
            printf(" + ");
            print_tree_(expr->op2);
            break;
        case SUB_OP:
            print_tree_(expr->op1);
            printf(" - ");
            print_tree_(expr->op2);
            break;
        case MUL_OP:
            print_tree_(expr->op1);
            printf(" * ");
            print_tree_(expr->op2);
            break;
        case DIV_OP:
            print_tree_(expr->op1);
            printf(" * ");
            print_tree_(expr->op2);
            break;
    }
} 

void print_tree(Expr *expr) {
    if (expr == NULL)
        return;

    print_tree_(expr);
    printf("\n");
}

#endif
