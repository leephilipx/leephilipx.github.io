#include <bits/stdc++.h>
using namespace std;
int main () {
    ifstream cin ("D:\\orderid.txt");
    ofstream cout ("output1.csv");
    cout<<"orderid,is_fraud\n";
    vector <string> a (620947);
    srand(unsigned(time(NULL)));
    for (auto &i : a) {
        cin>>i;
        cout<<i<<','<<rand()%2<<'\n';
    }
    printf("OK!");
    return 0;
}
