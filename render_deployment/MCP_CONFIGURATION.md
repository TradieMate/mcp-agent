# 🔧 MCP Server Configuration Guide

## 📋 **What are MCP Servers?**

MCP (Model Context Protocol) servers are external tools that your AI agent can use. Think of them as "superpowers" you can give your agent:

- **Fetch Server**: Get content from websites
- **Filesystem Server**: Read/write files
- **Database Server**: Query databases
- **GitHub Server**: Interact with GitHub repositories
- **Slack Server**: Send messages to Slack
- **And many more...**

## 🎛️ **How to Configure MCP Servers**

### **Basic Configuration Structure**

Edit `mcp_agent.config.yaml`:

```yaml
mcp:
  servers:
    server_name:           # Choose any name
      command: "command"   # How to run the server
      args: ["arg1", "arg2"]  # Arguments to pass
      env:                 # Optional environment variables
        VAR_NAME: "value"
```

### **Current Configuration (Minimal)**

```yaml
mcp:
  servers:
    fetch:                    # Server name (you choose this)
      command: "uvx"          # Use uvx package runner
      args: ["mcp-server-fetch"]  # Run the fetch server
```

## 🚀 **Popular MCP Servers You Can Add**

### **1. Filesystem Server** (File Operations)
```yaml
filesystem:
  command: "npx"
  args: ["-y", "@modelcontextprotocol/server-filesystem", "/tmp"]
  # Gives access to /tmp directory for file operations
```

**What it does**: Read, write, create, delete files
**Example usage**: "Create a file called notes.txt with my meeting notes"

### **2. GitHub Server** (Repository Management)
```yaml
github:
  command: "npx"
  args: ["-y", "@modelcontextprotocol/server-github"]
  env:
    GITHUB_PERSONAL_ACCESS_TOKEN: "${GITHUB_TOKEN}"
```

**What it does**: Create issues, PRs, read repositories
**Example usage**: "Create an issue in my repo about this bug"

### **3. Slack Server** (Team Communication)
```yaml
slack:
  command: "npx"
  args: ["-y", "@modelcontextprotocol/server-slack"]
  env:
    SLACK_BOT_TOKEN: "${SLACK_BOT_TOKEN}"
```

**What it does**: Send messages, read channels
**Example usage**: "Send a message to #general channel"

### **4. SQLite Database Server**
```yaml
sqlite:
  command: "npx"
  args: ["-y", "@modelcontextprotocol/server-sqlite", "/path/to/database.db"]
```

**What it does**: Query and modify SQLite databases
**Example usage**: "Show me all users from the database"

### **5. Google Drive Server**
```yaml
gdrive:
  command: "npx"
  args: ["-y", "@modelcontextprotocol/server-gdrive"]
  env:
    GOOGLE_APPLICATION_CREDENTIALS: "${GOOGLE_CREDS}"
```

**What it does**: Access Google Drive files
**Example usage**: "Upload this document to my Google Drive"

### **6. Memory Server** (Persistent Memory)
```yaml
memory:
  command: "npx"
  args: ["-y", "@modelcontextprotocol/server-memory"]
```

**What it does**: Remember information between conversations
**Example usage**: "Remember that my favorite color is blue"

## 🔧 **Complete Example Configuration**

Here's a powerful configuration with multiple servers:

```yaml
execution_engine: asyncio
logger:
  type: console
  level: info
  progress_display: false

mcp:
  servers:
    # Web content fetching
    fetch:
      command: "uvx"
      args: ["mcp-server-fetch"]
    
    # File system operations (limited to /tmp for security)
    filesystem:
      command: "npx"
      args: ["-y", "@modelcontextprotocol/server-filesystem", "/tmp"]
    
    # GitHub integration
    github:
      command: "npx"
      args: ["-y", "@modelcontextprotocol/server-github"]
      env:
        GITHUB_PERSONAL_ACCESS_TOKEN: "${GITHUB_TOKEN}"
    
    # Persistent memory
    memory:
      command: "npx"
      args: ["-y", "@modelcontextprotocol/server-memory"]
    
    # SQLite database (if you have a database file)
    # sqlite:
    #   command: "npx"
    #   args: ["-y", "@modelcontextprotocol/server-sqlite", "/tmp/mydb.db"]

openai:
  default_model: gpt-4o-mini
```

## 🔗 **Connecting Servers to Your Agent**

After configuring servers, update `app.py` to use them:

```python
# Current (minimal):
server_names=["fetch"]

# With multiple servers:
server_names=["fetch", "filesystem", "github", "memory"]

# The agent will automatically get access to all tools from these servers
```

## 🌍 **Environment Variables for MCP Servers**

### **Required for Advanced Servers**

Add these to your Render environment variables:

```bash
# For GitHub server
GITHUB_TOKEN=ghp_your_github_token

# For Slack server  
SLACK_BOT_TOKEN=xoxb-your-slack-token

# For Google Drive
GOOGLE_APPLICATION_CREDENTIALS=path_to_service_account.json
```

### **Setting Environment Variables in Render**

1. **Render Dashboard** → Your Service → **Environment**
2. **Add Variable**:
   - Key: `GITHUB_TOKEN`
   - Value: Your GitHub personal access token
3. **Save** (triggers redeploy)

## 🛡️ **Security Considerations**

### **Filesystem Server**
```yaml
# ✅ SAFE: Limited to /tmp directory
filesystem:
  command: "npx"
  args: ["-y", "@modelcontextprotocol/server-filesystem", "/tmp"]

# ❌ DANGEROUS: Full system access
# filesystem:
#   command: "npx"
#   args: ["-y", "@modelcontextprotocol/server-filesystem", "/"]
```

### **Database Access**
```yaml
# ✅ SAFE: Read-only database
sqlite:
  command: "npx"
  args: ["-y", "@modelcontextprotocol/server-sqlite", "/tmp/readonly.db", "--readonly"]

# ⚠️ CAREFUL: Full database access
sqlite:
  command: "npx"
  args: ["-y", "@modelcontextprotocol/server-sqlite", "/tmp/mydb.db"]
```

## 🔍 **Finding More MCP Servers**

### **Official Servers**
- Browse: https://github.com/modelcontextprotocol
- Search for: `@modelcontextprotocol/server-*`

### **Community Servers**
- Awesome MCP: https://github.com/punkpeye/awesome-mcp-servers
- NPM search: `npm search mcp-server`
- Python packages: `pip search mcp-server`

### **Custom Servers**
You can build your own MCP server:
```yaml
custom_server:
  command: "python"
  args: ["/path/to/your/server.py"]
  env:
    CUSTOM_API_KEY: "${YOUR_API_KEY}"
```

## 🧪 **Testing Your Configuration**

### **1. Local Testing**
```bash
cd render_deployment
export OPENAI_API_KEY="your-key"
export GITHUB_TOKEN="your-github-token"  # if using GitHub server
streamlit run app.py
```

### **2. Check Available Tools**
In your Streamlit app, expand "View Available Tools" to see all MCP tools loaded.

### **3. Test Each Server**
Try prompts like:
- **Fetch**: "Get content from https://example.com"
- **Filesystem**: "Create a file called test.txt"
- **GitHub**: "List my repositories"
- **Memory**: "Remember that I prefer Python over JavaScript"

## 🚨 **Troubleshooting MCP Servers**

### **Common Issues**

1. **"Server failed to start"**
   ```bash
   # Check if the server package exists:
   npx @modelcontextprotocol/server-filesystem --help
   ```

2. **"Permission denied"**
   ```yaml
   # Make sure paths are accessible:
   filesystem:
     args: ["-y", "@modelcontextprotocol/server-filesystem", "/tmp"]  # ✅ Works
     # Not: ["-y", "@modelcontextprotocol/server-filesystem", "/root"]  # ❌ No access
   ```

3. **"Environment variable not found"**
   ```bash
   # Check Render environment variables are set correctly
   # Variable names must match exactly
   ```

### **Debug Mode**
```yaml
logger:
  level: debug  # Shows detailed MCP server logs
```

## 📊 **Performance Considerations**

### **Server Startup Time**
- **NPM servers**: ~2-3 seconds startup
- **Python servers**: ~1-2 seconds startup
- **uvx servers**: ~1-2 seconds startup

### **Memory Usage**
- Each MCP server: ~10-50MB RAM
- Recommended: Start with 2-3 servers, add more as needed

### **Cost Impact**
- MCP servers themselves are free
- Cost comes from:
  - API calls they make (GitHub API, etc.)
  - Render compute resources
  - AI model usage

## 🎯 **Recommended Configurations**

### **Starter Configuration** (Free Tier Friendly)
```yaml
mcp:
  servers:
    fetch:
      command: "uvx"
      args: ["mcp-server-fetch"]
    memory:
      command: "npx"
      args: ["-y", "@modelcontextprotocol/server-memory"]
```

### **Developer Configuration**
```yaml
mcp:
  servers:
    fetch:
      command: "uvx"
      args: ["mcp-server-fetch"]
    filesystem:
      command: "npx"
      args: ["-y", "@modelcontextprotocol/server-filesystem", "/tmp"]
    github:
      command: "npx"
      args: ["-y", "@modelcontextprotocol/server-github"]
      env:
        GITHUB_PERSONAL_ACCESS_TOKEN: "${GITHUB_TOKEN}"
    memory:
      command: "npx"
      args: ["-y", "@modelcontextprotocol/server-memory"]
```

### **Business Configuration**
```yaml
mcp:
  servers:
    fetch:
      command: "uvx"
      args: ["mcp-server-fetch"]
    filesystem:
      command: "npx"
      args: ["-y", "@modelcontextprotocol/server-filesystem", "/tmp"]
    github:
      command: "npx"
      args: ["-y", "@modelcontextprotocol/server-github"]
      env:
        GITHUB_PERSONAL_ACCESS_TOKEN: "${GITHUB_TOKEN}"
    slack:
      command: "npx"
      args: ["-y", "@modelcontextprotocol/server-slack"]
      env:
        SLACK_BOT_TOKEN: "${SLACK_BOT_TOKEN}"
    memory:
      command: "npx"
      args: ["-y", "@modelcontextprotocol/server-memory"]
    sqlite:
      command: "npx"
      args: ["-y", "@modelcontextprotocol/server-sqlite", "/tmp/business.db"]
```

---

**🎉 Ready to supercharge your agent?** Pick a configuration above and update your `mcp_agent.config.yaml`!