#include<iostram>
#include<vector>
using namespace std;
inr main()
{
    int n;
    cin>>n;
    vector<int> x(n);
    vector<int> y(n);
    for(int i=0;i<n;i++)
    {
        cin>>x[i]>>y[i];
    }
    unorder_map<int,int> xmax;
    unorder_map<int,int> xmin;
    unorder_map<int,int> ymax;
    unorder_map<int,int> ymin;
    for(int i=0;i<n;i++)
    {
        if(xmax[x[i]])
        {
            xmax[x[i]]=max(xmax[x[i]],y[i]);
            xmin[x[i]]=min(xmin[x[i]],y[i]);
        }
        else
        {
            xmax[x[i]]=y[i];
            xmin[x[i]]=y[i];
        }
        if(ymax[y[i]])
        {
            ymax[y[i]]=max(ymax[y[i]],x[i]);
            ymin[y[i]]=min(ymin[y[i]],x[i]);
        }
        else
        {
            ymax[y[i]]=x[i];
            ymin[y[i]]=x[i];
        }
    }
    int ans=0;
    for(int i=0;i<n;i++)
    {
        if(xmax[x[i]]>y[i]&&ymax[y[i]]>x[i]&&xmin[x[i]]<y[i]&&ymin[y[i]]<x[i])
        {
            ans++;
        }
    }
    cout<<ans<<endl;


    return 0;
}