# 🎛️ Pre-built MCP Configurations

Choose a configuration that matches your needs:

## 📁 **Available Configurations**

### **`basic.yaml`** - Starter Configuration
- **MCP Servers**: Fetch only
- **Use Case**: Web content retrieval, general Q&A
- **Environment Variables**: `OPENAI_API_KEY`
- **Cost**: Minimal

### **`developer.yaml`** - Development Configuration  
- **MCP Servers**: Fetch, Filesystem, GitHub, Memory
- **Use Case**: Coding assistance, repository management
- **Environment Variables**: `OPENAI_API_KEY`, `GITHUB_TOKEN`
- **Cost**: Low to moderate

### **`business.yaml`** - Team Collaboration
- **MCP Servers**: Fetch, Filesystem, GitHub, Slack, Memory, SQLite
- **Use Case**: Team productivity, business automation
- **Environment Variables**: `OPENAI_API_KEY`, `GITHUB_TOKEN`, `SLACK_BOT_TOKEN`
- **Cost**: Moderate

## 🔄 **How to Switch Configurations**

### **Option 1: Copy and Replace**
```bash
# Choose your configuration:
cp configs/developer.yaml mcp_agent.config.yaml

# Update app.py to use the new servers:
# Edit server_names=["fetch", "filesystem", "github", "memory"]
```

### **Option 2: Manual Customization**
1. **Start with `basic.yaml`**
2. **Add servers one by one** from other configs
3. **Test each addition** to ensure it works

## 🔧 **Customizing Server Lists in app.py**

After changing your config, update the agent in `app.py`:

```python
# For basic.yaml:
server_names=["fetch"]

# For developer.yaml:
server_names=["fetch", "filesystem", "github", "memory"]

# For business.yaml:
server_names=["fetch", "filesystem", "github", "slack", "memory"]
```

## 🌍 **Environment Variables Setup**

### **GitHub Token** (for developer/business configs)
1. Go to GitHub → Settings → Developer settings → Personal access tokens
2. Generate new token with `repo` and `user` scopes
3. Add to Render: `GITHUB_TOKEN=ghp_your_token`

### **Slack Bot Token** (for business config)
1. Create Slack app at https://api.slack.com/apps
2. Add bot token scopes: `chat:write`, `channels:read`
3. Install app to workspace
4. Add to Render: `SLACK_BOT_TOKEN=xoxb-your-token`

## 🧪 **Testing Your Configuration**

After switching configs:

1. **Deploy to Render** (or restart locally)
2. **Check "View Available Tools"** in the app
3. **Test each server**:
   - **Fetch**: "Get content from https://example.com"
   - **Filesystem**: "Create a file called test.txt"
   - **GitHub**: "List my repositories"
   - **Slack**: "Send a message to #general"
   - **Memory**: "Remember my favorite programming language is Python"

## 🚨 **Troubleshooting**

### **Server Won't Start**
- Check environment variables are set correctly
- Verify token permissions (GitHub, Slack)
- Check Render logs for specific errors

### **Tools Not Available**
- Ensure `server_names` in `app.py` matches your config
- Check MCP server installation (usually automatic)

### **Permission Errors**
- GitHub: Check token scopes
- Slack: Verify bot permissions
- Filesystem: Ensure using `/tmp` directory

---

**💡 Tip**: Start with `basic.yaml` and gradually add more servers as you need them!