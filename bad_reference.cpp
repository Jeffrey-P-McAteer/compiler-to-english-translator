#include <iostream>

using namespace std;

int dub(int& int_ref) {
  return int_ref * 2;
}

int main() {
    cout << dub(10) << endl;
}

