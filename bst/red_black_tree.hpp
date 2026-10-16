//https://read.seas.harvard.edu/~kohler/notes/llrb.html
#pragma once
#include <iostream>
#include <queue>
#include <stack>

using namespace std;

enum Side
{
    RIGHT = 0,
    LEFT = 1
};

enum Color
{
    RED = 0,
    BLACK = 1
};

class RBNode
{
public:
    RBNode() : side{nullptr, nullptr}, parent(nullptr), color(RED), val(0) {}
    RBNode(int v, RBNode *p = nullptr) : side{nullptr, nullptr}, parent(p), color(RED), val(v) {}
    RBNode *side[2];
    RBNode *parent;
    Color color;
    int val;
};

class RBTree
{
public:
    RBTree()
    {
        nil = new RBNode(-1);
        nil->color = BLACK;
        nil->side[LEFT] = nil;
        nil->side[RIGHT] = nil;
        nil->parent = nil;
        root = nil;
    }
    ~RBTree()
    {
        stack<RBNode *> s;
        RBNode *x = root;
        RBNode *last_del = nil;
        while (!s.empty() || x != nil)
        {
            if (x != nil)
            {
                s.push(x);
                x = x->side[LEFT];
            }
            else
            {
                RBNode *t = s.top();
                if (t->side[RIGHT] != nil && t->side[RIGHT] != last_del)
                    x = t->side[RIGHT];
                else
                {
                    delete t;
                    last_del = t;
                    s.pop();
                }
            }
        }
        delete nil;
    }
    RBNode *root;
    RBNode *nil;
};

inline void rb_rotate(RBTree &tree, RBNode *curr, Side side)
{
    RBNode *y = curr->side[!side];
    curr->side[!side] = y->side[side];
    if (y->side[side] != tree.nil)
        y->side[side]->parent = curr;
    y->parent = curr->parent;
    if (curr->parent == tree.nil)
        tree.root = y;
    else if (curr == curr->parent->side[side])
        curr->parent->side[side] = y;
    else
        curr->parent->side[!side] = y;
    y->side[side] = curr;
    curr->parent = y;
}

inline void rb_insert_fixup(RBTree &tree, RBNode *curr)
{
    while (curr->parent->color == RED)
    {
        Side father_side = Side(curr->parent == curr->parent->parent->side[LEFT]);
        RBNode *unc = curr->parent->parent->side[!father_side];
        if (unc->color == RED)
        {
            curr->parent->color = BLACK;
            unc->color = BLACK;
            curr->parent->parent->color = RED;
            curr = curr->parent->parent;
        }
        else
        {
            if (curr == curr->parent->side[!father_side])
            {
                curr = curr->parent;
                rb_rotate(tree, curr, father_side);
            }
            curr->parent->color = BLACK;
            curr->parent->parent->color = RED;
            rb_rotate(tree, curr->parent->parent, Side(!father_side));
        }
    }
    tree.root->color = BLACK;
}

inline void rb_insert(RBTree &tree, int v)
{
    RBNode *tmp = new RBNode(v);
    RBNode *current = tree.root;
    RBNode *parent = tree.nil;
    Side s = RIGHT;
    while (current != tree.nil)
    {
        parent = current;
        s = Side(v < current->val);
        current = current->side[s];
    }
    tmp->parent = parent;
    if (parent == tree.nil)
        tree.root = tmp;
    else
        parent->side[s] = tmp;
    tmp->side[LEFT] = tree.nil;
    tmp->side[RIGHT] = tree.nil;

    rb_insert_fixup(tree, tmp);
}

inline void rb_print_queue(RBTree &tree)
{
    cout << "PRINT_QUEUE\n";
    if (tree.root == tree.nil)
        return;
    queue<RBNode *> q;
    q.push(tree.root);
    int i = 0;
    while (!q.empty())
    {
        RBNode *curr = q.front();
        q.pop();
        cout << i << ": " << curr->color << " " << curr->val << "\t";
        if (curr->side[LEFT] != tree.nil)
            q.push(curr->side[LEFT]), cout << curr->side[LEFT]->val;
        cout << "\t";
        if (curr->side[RIGHT] != tree.nil)
            q.push(curr->side[RIGHT]), cout << curr->side[RIGHT]->val;
        cout << "\t";
        if (curr->parent != nullptr)
            cout << curr->parent->val;
        cout << '\n';
        i++;
    }
}

inline RBNode *rb_tree_search(RBTree &tree, int curr)
{
    RBNode *tmp = tree.root;
    while (tmp != tree.nil && tmp->val != curr)
    {
        Side s = Side(curr < tmp->val);
        tmp = tmp->side[s];
    }
    return tmp;
}

inline void rb_transplant(RBTree &tree, RBNode *to_replace, RBNode *replacement)
{
    if (to_replace->parent == tree.nil)
        tree.root = replacement;
    else
        to_replace->parent->side[Side(to_replace->parent->side[LEFT] == to_replace)] = replacement;

    replacement->parent = to_replace->parent;
}

inline RBNode *tree_minimum(RBTree &tree, RBNode *node)
{
    while (node->side[LEFT] != tree.nil)
        node = node->side[LEFT];
    return node;
}

inline void rb_delete_fixup(RBTree &tree, RBNode *curr)
{
    while (curr != tree.root && curr->color == BLACK)
    {
        Side s = Side(curr == curr->parent->side[LEFT]);
        RBNode *b = curr->parent->side[!s];
        if (b->color == RED)
        {
            b->color = BLACK;
            curr->parent->color = RED;
            rb_rotate(tree, curr->parent, s);
            b = curr->parent->side[!s];
        }
        if (b->side[LEFT]->color == BLACK && b->side[RIGHT]->color == BLACK)
        {
            b->color = RED;
            curr = curr->parent;
        }
        else
        {
            if (b->side[!s]->color == BLACK)
            {
                b->side[s]->color = BLACK;
                b->color = RED;
                rb_rotate(tree, b, Side(!s));
                b = curr->parent->side[!s];
            }
            b->color = curr->parent->color;
            curr->parent->color = BLACK;
            b->side[!s]->color = BLACK;
            rb_rotate(tree, curr->parent, s);
            curr = tree.root;
        }
    }
    curr->color = BLACK;
}

inline void rb_delete(RBTree &tree, RBNode *curr)
{
    RBNode *rep;
    Color parent_original_color = curr->color;
    if (curr->side[LEFT] == tree.nil)
    {
        rep = curr->side[RIGHT];
        rb_transplant(tree, curr, curr->side[RIGHT]);
    }
    else if (curr->side[RIGHT] == tree.nil)
    {
        rep = curr->side[LEFT];
        rb_transplant(tree, curr, curr->side[LEFT]);
    }
    else
    {
        RBNode *parent = tree_minimum(tree, curr->side[RIGHT]);
        rep = parent->side[RIGHT];
        parent_original_color = parent->color;
        if (curr->side[RIGHT] != parent)
        {
            rb_transplant(tree, parent, parent->side[RIGHT]);
            parent->side[RIGHT] = curr->side[RIGHT];
            parent->side[RIGHT]->parent = parent;
        }
        else
            rep->parent = parent;

        rb_transplant(tree, curr, parent);
        parent->side[LEFT] = curr->side[LEFT];
        parent->side[LEFT]->parent = parent;
        parent->color = curr->color;
    }
    delete curr;
    if (parent_original_color == BLACK)
        rb_delete_fixup(tree, rep);
}