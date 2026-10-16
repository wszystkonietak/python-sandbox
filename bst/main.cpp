#include <iostream>
#include <vector>
#include <numeric>
#include <algorithm>
#include <random>
#include <chrono>
#include <iomanip>
#include "bst.hpp"
#include "red_black_tree.hpp"

using namespace std;
using namespace std::chrono;

void run_benchmark(const string &case_name, const vector<int> &insert_data, const vector<int> &delete_data)
{
    Node *bst_root = nullptr;
    RBTree rbt;
    volatile long long sink = 0;

    auto t1 = high_resolution_clock::now();
    for (int x : insert_data)
        bst_root = insert(bst_root, x);
    auto t2 = high_resolution_clock::now();
    double bst_insert_ms = duration<double, milli>(t2 - t1).count();

    t1 = high_resolution_clock::now();
    for (int x : insert_data)
        rb_insert(rbt, x);
    t2 = high_resolution_clock::now();
    double rbt_insert_ms = duration<double, milli>(t2 - t1).count();

    t1 = high_resolution_clock::now();
    for (int x : insert_data)
        sink = sink + reinterpret_cast<uintptr_t>(tree_search(bst_root, x));
    t2 = high_resolution_clock::now();
    double bst_search_ms = duration<double, milli>(t2 - t1).count();

    t1 = high_resolution_clock::now();
    for (int x : insert_data)
        sink = sink + reinterpret_cast<uintptr_t>(rb_tree_search(rbt, x));
    t2 = high_resolution_clock::now();
    double rbt_search_ms = duration<double, milli>(t2 - t1).count();

    t1 = high_resolution_clock::now();
    for (int x : delete_data)
        bst_root = tree_delete(bst_root, tree_search(bst_root, x));
    t2 = high_resolution_clock::now();
    double bst_delete_ms = duration<double, milli>(t2 - t1).count();

    t1 = high_resolution_clock::now();
    for (int x : delete_data)
        rb_delete(rbt, rb_tree_search(rbt, x));
    t2 = high_resolution_clock::now();
    double rbt_delete_ms = duration<double, milli>(t2 - t1).count();

    cout << "=== " << case_name << " (N = " << insert_data.size() << ") ===\n";
    cout << left << setw(12) << "Operation"
         << right << setw(14) << "BST [ms]"
         << setw(14) << "RBTree [ms]"
         << setw(16) << "Ratio (BST/RB)" << "\n";
    cout << string(56, '-') << "\n";
    cout << fixed << setprecision(2);
    cout << left << setw(12) << "Insert"
         << right << setw(14) << bst_insert_ms
         << setw(14) << rbt_insert_ms
         << setw(15) << (bst_insert_ms / rbt_insert_ms) << "x\n";
    cout << left << setw(12) << "Search"
         << right << setw(14) << bst_search_ms
         << setw(14) << rbt_search_ms
         << setw(15) << (bst_search_ms / rbt_search_ms) << "x\n";
    cout << left << setw(12) << "Delete"
         << right << setw(14) << bst_delete_ms
         << setw(14) << rbt_delete_ms
         << setw(15) << (bst_delete_ms / rbt_delete_ms) << "x\n\n";
}

int main()
{
    mt19937 rng(42);

    int n_random = 100000;
    vector<int> random_data(n_random);
    iota(random_data.begin(), random_data.end(), 1);
    shuffle(random_data.begin(), random_data.end(), rng);
    run_benchmark("Random Data", random_data, random_data);

    int n_sorted = 15000;
    vector<int> sorted_data(n_sorted);
    iota(sorted_data.begin(), sorted_data.end(), 1);
    vector<int> reverse_data = sorted_data;
    reverse(reverse_data.begin(), reverse_data.end());
    run_benchmark("Sorted Ascending", sorted_data, reverse_data);

    int n_partial = 50000;
    vector<int> partial_data(n_partial);
    iota(partial_data.begin(), partial_data.end(), 1);
    for (int i = 0; i < n_partial; i += 500)
        shuffle(partial_data.begin() + i, partial_data.begin() + min(i + 500, n_partial), rng);
    vector<int> partial_del = partial_data;
    shuffle(partial_del.begin(), partial_del.end(), rng);
    run_benchmark("Partially Sorted (Blocks of 500)", partial_data, partial_del);

    return 0;
}