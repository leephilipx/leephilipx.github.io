#include <bits/stdc++.h>
using namespace std;
int main () {
    ofstream cout ("output6.csv");
    cout<<"index,groups_found\n";
    srand(unsigned(time(NULL)));
    for (int i=0;i<800000;++i)
    {
        cout<<i<<',';
        int num=rand()%3;
        cout<<(!num? "[" : "\"[");
            for (int j=0;j<num;++j)
                cout<<rand()%281<<", ";
        cout<<rand()%281<<(!num? "]\n" : "]\"\n");
    }
    printf("OK");
    return 0;
}
