#include <bits/stdc++.h>
#define ll long long

using namespace std;

bool isprime(ll n){
    for(ll i = 2; i * i <= n; i++){
        if(n % i == 0) return false;
    }
    return true;
}
bool comp(pair<ll,ll>a,pair<ll,ll>b){
    if(a.second==b.second)return a.first<b.first;
    return a.second>b.second;
}

void Hemal(){
    ll n;
    cin>>n;
    vector<pair<ll,ll>>v(n);
    for(ll i=0;i<n;i++){
    	cin>>v[i].first>>v[i].second;
    }
    sort(v.begin(),v.end());
    ll c=0;
    ll l=v[0].first,r=v[0].second;
    c=r-l+1;
    for(ll i=1;i<n;i++){
    	if(r>v[i].first && r<v[i].second){
    		l=r;
    		r=v[i].second;
    		c=c+r-l;
    	}
    	else if(r<v[i].first){
    		l=v[i].first;
    		r=v[i].second;
    		c=c+r-l+1;
    	}
    }
    cout<<c<<endl;
    
    
}



int main(){
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int T;
    T=1;
    //cin >> T;
    while(T--) Hemal();

    return 0;
}