using System.Linq.Expressions;
using System.Reflection;
using Microsoft.AspNetCore.Mvc;

namespace TaskMgrAPI.Attributes;

public class Helper
{
    // public string getHTTPMethod
}

[AttributeUsage(AttributeTargets.Method)]
public class RightTaskMgr : Attribute
{
    private string[] rights;
    public RightTaskMgr(params string[] rights)
    {
        this.rights = rights;
    }

    public virtual string[] Right
    {
        get { return rights; }
    }
}
