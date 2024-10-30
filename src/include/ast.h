
#ifndef __AST_H__
#define __AST_H__

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef enum EXPR_TYPE {
    INT_CONST,
    REAL_CONST,
    NAME,
    ADD_OP,
    SUB_OP,
    MUL_OP,
    DIV_OP,
    NEG_OP,
    INT_DIV_OP,
    MOD_OP,
    POW_OP,
    AND_OP,
    OR_OP,
    NOT_OP,
    AND_THEN_OP,
    OR_ELSE_OP,
    XOR_OP,
    LT_OP,
    LE_OP,
    GT_OP,
    GE_OP,
    EQ_OP,
    NEQ_OP,
    IMPLIES_OP,
} EXPR_TYPE;

static int current_id = 1;

typedef struct Expr {
    int id;
    enum EXPR_TYPE expr_type;
    struct Expr *op1;
    struct Expr *op2;
    int int_num;
    double real_num;
    char *name;
} Expr;

Expr *Expr_int_const(int int_num) {
    Expr *expr = (Expr*) malloc(sizeof(Expr));
    expr->id = current_id++;
    expr->expr_type = INT_CONST;
    expr->int_num = int_num;
    return expr;
}

Expr *Expr_real_const(double real_num) {
    Expr *expr = (Expr*) malloc(sizeof(Expr));
    expr->id = current_id++;
    expr->expr_type = REAL_CONST;
    expr->real_num = real_num;
    return expr;
}

Expr *Expr_unary_op(EXPR_TYPE expr_type, Expr *op) {
    Expr *expr = (Expr*) malloc(sizeof(Expr));
    expr->id = current_id++;
    expr->expr_type = expr_type;
    expr->op1 = op;
    return expr;
}

Expr *Expr_bin_op(EXPR_TYPE expr_type, Expr *l, Expr *r) {
    Expr *expr = (Expr*) malloc(sizeof(Expr));
    expr->id = current_id++;
    expr->expr_type = expr_type;
    expr->op1 = l;
    expr->op2 = r;
    return expr;
}

Expr *Expr_name_lit(char *name) {
    char *copy = strdup(name);
    Expr *expr = (Expr*) malloc(sizeof(Expr));
    expr->expr_type = NAME;
    expr->name = copy;
    return expr;
}

static void print_tree_(Expr *expr);

// Вспомогательная функция для вывода бинарных операций
static void print_bin(Expr *op1, const char *op, Expr *op2) {
    print_tree_(op1);
    printf(" %s ", op);
    print_tree_(op2);
}

// Вспомогательная функция для вывода унарных операций
static void print_unary(const char *op, Expr *operand) {
    printf("%s", op);
    print_tree_(operand);
}

// Основная функция для вывода дерева выражений
static void print_tree_(Expr *expr) {
    if (expr == NULL)
        return;

    switch (expr->expr_type) {
        case INT_CONST:
            printf("%d", expr->int_num);
            break;
        case REAL_CONST:
            printf("%f", expr->real_num);
            break;
        case NAME:
            printf("%s", expr->name);
            break;

        // Арифметические операторы
        case ADD_OP:
            print_bin(expr->op1, "+", expr->op2);
            break;
        case SUB_OP:
            print_bin(expr->op1, "-", expr->op2);
            break;
        case MUL_OP:
            print_bin(expr->op1, "*", expr->op2);
            break;
        case DIV_OP:
            print_bin(expr->op1, "/", expr->op2);
            break;
        case INT_DIV_OP:
            print_bin(expr->op1, "//", expr->op2);
            break;
        case MOD_OP:
            print_bin(expr->op1, "%", expr->op2);
            break;
        case POW_OP:
            print_bin(expr->op1, "^", expr->op2);
            break;
        case NEG_OP:
            print_unary("-", expr->op1);
            break;

        // Операторы сравнения
        case EQ_OP:
            print_bin(expr->op1, "=", expr->op2);
            break;
        case NEQ_OP:
            print_bin(expr->op1, "/=", expr->op2);
            break;
        case LT_OP:
            print_bin(expr->op1, "<", expr->op2);
            break;
        case GT_OP:
            print_bin(expr->op1, ">", expr->op2);
            break;
        case LE_OP:
            print_bin(expr->op1, "<=", expr->op2);
            break;
        case GE_OP:
            print_bin(expr->op1, ">=", expr->op2);
            break;

        // Логические операторы
        case AND_OP:
            print_bin(expr->op1, "and", expr->op2);
            break;
        case OR_OP:
            print_bin(expr->op1, "or", expr->op2);
            break;
        case NOT_OP:
            print_unary("not ", expr->op1);
            break;
        case AND_THEN_OP:
            print_bin(expr->op1, "and then", expr->op2);
            break;
        case OR_ELSE_OP:
            print_bin(expr->op1, "or else", expr->op2);
            break;
        case IMPLIES_OP:
            print_bin(expr->op1, "implies", expr->op2);
            break;

        default:
            printf("Unknown operation");
            break;
    }
}

// Функция для вызова печати дерева выражений
void print_tree(Expr *expr) {
    if (expr == NULL)
        return;

    print_tree_(expr);
    printf("\n");
}

#endif
