#pragma once
#include <iostream>
#include <queue>
#include <stack>

using namespace std;

class Node
{
public:
    Node() : left(nullptr), right(nullptr), parent(nullptr), val(0) {}
    Node(int v, Node *p = nullptr) : left(nullptr), right(nullptr), parent(p), val(v) {}
    Node *left;
    Node *right;
    Node *parent;
    int val;
};

inline Node *insert(Node *root, int v)
{
    Node *tmp = new Node(v);
    if (root == nullptr)
        return tmp;

    Node *current = root;
    Node *parent = nullptr;
    while (current != nullptr)
    {
        parent = current;
        if (v <= current->val && current->left != nullptr)
            current = current->left;
        else if (v > current->val && current->right != nullptr)
            current = current->right;
        else
            break;
    }
    tmp->parent = parent;
    if (v <= current->val)
        current->left = tmp;
    else
        current->right = tmp;
    return root;
}

inline Node *insert_recurrence(Node *root, int v, Node *p = nullptr)
{
    if (root == nullptr)
        return new Node(v, p);

    if (v <= root->val)
        root->left = insert_recurrence(root->left, v, root);
    else
        root->right = insert_recurrence(root->right, v, root);
    return root;
}

inline void print_queue(Node *root)
{
    cout << "PRINT_QUEUE\n";
    if (root == nullptr)
        return;
    queue<Node *> q;
    q.push(root);
    int i = 0;
    while (!q.empty())
    {
        Node *x = q.front();
        q.pop();
        cout << i << ": " << x->val << "\t";
        if (x->left != nullptr)
            q.push(x->left), cout << x->left->val;
        cout << "\t";
        if (x->right != nullptr)
            q.push(x->right), cout << x->right->val;
        cout << "\t";
        if (x->parent != nullptr)
            cout << x->parent->val;
        cout << '\n';
        i++;
    }
}

inline void print_stack(Node *root)
{
    cout << "PRINT_STACK\n";
    if (root == nullptr)
        return;
    stack<Node *> s;
    s.push(root);
    int i = 0;
    while (!s.empty())
    {
        Node *x = s.top();
        s.pop();
        cout << i << ": " << x->val << "\t";
        if (x->left != nullptr)
            s.push(x->left), cout << x->left->val;
        cout << "\t";
        if (x->right != nullptr)
            s.push(x->right), cout << x->right->val;
        cout << "\t";
        if (x->parent != nullptr)
            cout << x->parent->val;
        cout << '\n';
        i++;
    }
}

inline void print_in_order_recurrence(Node *root)
{
    if (root != nullptr)
    {
        print_in_order_recurrence(root->left);
        cout << root->val << '\t';
        print_in_order_recurrence(root->right);
    }
}

inline void print_pre_order_recurrence(Node *root)
{
    if (root != nullptr)
    {
        cout << root->val << '\t';
        print_pre_order_recurrence(root->left);
        print_pre_order_recurrence(root->right);
    }
}

inline void print_post_order_recurrence(Node *root)
{
    if (root != nullptr)
    {
        print_post_order_recurrence(root->left);
        print_post_order_recurrence(root->right);
        cout << root->val << '\t';
    }
}

inline void print_in_order_stack(Node *root)
{
    if (root == nullptr)
        return;
    stack<Node *> s;
    Node *tmp = root;
    while (tmp != nullptr || !s.empty())
    {
        while (tmp != nullptr)
        {
            s.push(tmp);
            tmp = tmp->left;
        }
        tmp = s.top();
        s.pop();
        cout << tmp->val << '\t';
        tmp = tmp->right;
    }
}

inline void print_pre_order_stack(Node *root)
{
    if (root == nullptr)
        return;
    stack<Node *> s;
    s.push(root);
    while (!s.empty())
    {
        Node *x = s.top();
        s.pop();
        cout << x->val << "\t";
        if (x->right != nullptr)
            s.push(x->right);
        if (x->left != nullptr)
            s.push(x->left);
    }
}

inline void print_post_order_stack(Node *root)
{
    stack<Node *> s;
    Node *x = root;
    Node *last_print = nullptr;
    while (!s.empty() || x != nullptr)
    {
        if (x != nullptr)
        {
            s.push(x);
            x = x->left;
        }
        else
        {
            Node *t = s.top();
            if (t->right != nullptr && t->right != last_print)
                x = t->right;
            else
            {
                cout << t->val << '\t';
                last_print = t;
                s.pop();
            }
        }
    }
}

inline void print_in_order(Node *root)
{
    Node *curr = root;
    while (curr != nullptr)
    {
        if (curr->left == nullptr)
        {
            cout << curr->val << '\t';
            curr = curr->right;
        }
        else
        {
            Node *pred = curr->left;
            while (pred->right != nullptr && pred->right != curr)
                pred = pred->right;

            if (pred->right == nullptr)
            {
                pred->right = curr;
                curr = curr->left;
            }
            else
            {
                cout << curr->val << '\t';
                pred->right = nullptr;
                curr = curr->right;
            }
        }
    }
}

inline Node *tree_search(Node *root, int x)
{
    while (root != nullptr && root->val != x)
    {
        if (x > root->val)
            root = root->right;
        else
            root = root->left;
    }
    return root;
}

inline Node *tree_search_recurrence(Node *root, int x)
{
    if (root == nullptr || root->val == x)
        return root;
    if (x > root->val)
        return tree_search_recurrence(root->right, x);
    else
        return tree_search_recurrence(root->left, x);
}

inline Node *tree_maximum(Node *root)
{
    while (root->right != nullptr)
        root = root->right;
    return root;
}

inline Node *tree_minimum(Node *root)
{
    while (root->left != nullptr)
        root = root->left;
    return root;
}

inline Node *find_succesor(Node *node)
{
    if (node->right != nullptr)
        return tree_minimum(node->right);

    Node *tmp = node->parent;
    while (tmp != nullptr && tmp->right == node)
    {
        node = tmp;
        tmp = tmp->parent;
    }
    return tmp;
}

inline Node *find_predcessor(Node *node)
{
    if (node->left != nullptr)
        return tree_maximum(node->left);

    Node *tmp = node->parent;
    while (tmp != nullptr && tmp->left == node)
    {
        node = tmp;
        tmp = tmp->parent;
    }
    return tmp;
}

inline Node *tree_transplant(Node *root, Node *to_replace, Node *replacement)
{
    if (to_replace->parent == nullptr)
        root = replacement;
    else if (to_replace->parent->left == to_replace)
        to_replace->parent->left = replacement;
    else
        to_replace->parent->right = replacement;
    if (replacement != nullptr)
        replacement->parent = to_replace->parent;
    return root;
}

inline Node *tree_delete(Node *root, Node *curr)
{
    if (curr->left == nullptr)
        root = tree_transplant(root, curr, curr->right);
    else if (curr->right == nullptr)
        root = tree_transplant(root, curr, curr->left);
    else
    {
        Node *parent = tree_minimum(curr->right);
        if (curr->right != parent)
        {
            root = tree_transplant(root, parent, parent->right);
            parent->right = curr->right;
            parent->right->parent = parent;
        }
        root = tree_transplant(root, curr, parent);
        parent->left = curr->left;
        parent->left->parent = parent;
    }
    delete curr;
    return root;
}

inline void tree_clear(Node *root)
{
    stack<Node *> s;
    Node *x = root;
    Node *last_print = nullptr;
    while (!s.empty() || x != nullptr)
    {
        if (x != nullptr)
        {
            s.push(x);
            x = x->left;
        }
        else
        {
            Node *t = s.top();
            if (t->right != nullptr && t->right != last_print)
                x = t->right;
            else
            {
                delete t;
                last_print = t;
                s.pop();
            }
        }
    }
}