# How the MCP Agent Deployment Works

## 🔧 **Architecture Overview**

```
User Browser → Render Load Balancer → Your Streamlit App → MCP Servers → AI Models
                                           ↓
                                    OpenAI API (GPT-4o-mini)
```

## 📋 **Required Environment Variables**

### **Essential (Required)**
- **`OPENAI_API_KEY`** - Your OpenAI API key for GPT model access
  - Get from: https://platform.openai.com/api-keys
  - Example: `sk-proj-abc123...`

### **Automatic (Provided by Render)**
- **`PORT`** - Port number Render assigns (automatically set)
- **`PYTHONPATH`** - Python module path (set to `.` in config)

### **Optional (Advanced)**
- **`MCP_LOG_LEVEL`** - Logging level (`debug`, `info`, `warning`, `error`)
- **`STREAMLIT_THEME`** - UI theme (`light`, `dark`, `auto`)

## 🚀 **How It Works Step-by-Step**

### 1. **Render Deployment Process**
```bash
# Render automatically runs these commands:
pip install -r requirements.txt  # Install dependencies
streamlit run app.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true
```

### 2. **Port Binding (Render Requirement)**
✅ **Correctly Configured**: 
- `--server.port=$PORT` - Uses Render's assigned port
- `--server.address=0.0.0.0` - Binds to all interfaces (required by Render)
- `--server.headless=true` - Runs without browser (server mode)

### 3. **MCP Agent Initialization**
```python
# When app starts:
app = MCPApp(name="mcp_basic_agent")  # Initialize MCP framework
await app.initialize()               # Connect to MCP servers

# Create agent with capabilities:
agent = Agent(
    name="finder",
    server_names=["fetch"],  # MCP servers this agent can use
    instruction="..."        # Agent's role and capabilities
)

# Attach AI model:
llm = await agent.attach_llm(OpenAIAugmentedLLM)  # Uses OPENAI_API_KEY
```

### 4. **MCP Server Management**
The system automatically manages MCP servers defined in `mcp_agent.config.yaml`:
```yaml
mcp:
  servers:
    fetch:
      command: "uvx"           # Package runner
      args: ["mcp-server-fetch"]  # MCP fetch server
```

## 💬 **User Interaction Flow**

1. **User visits your Render URL** → `https://your-app-name.onrender.com`
2. **Streamlit loads** → Chat interface appears
3. **User types message** → "Fetch content from https://example.com"
4. **Agent processes request**:
   - Analyzes user intent
   - Calls appropriate MCP server (fetch)
   - MCP server retrieves web content
   - AI model processes and responds
5. **Response displayed** → Formatted content shown to user

## 🔌 **MCP Server Capabilities**

### **Fetch Server** (Included)
- **Purpose**: Retrieve content from URLs
- **Tools Available**:
  - `fetch` - Get webpage content
  - `fetch_text` - Extract text from pages
- **Example Usage**: "Get the latest news from https://news.ycombinator.com"

### **Adding More Servers** (Optional)
```yaml
# In mcp_agent.config.yaml:
mcp:
  servers:
    fetch:
      command: "uvx"
      args: ["mcp-server-fetch"]
    filesystem:  # Add file system access
      command: "npx"
      args: ["-y", "@modelcontextprotocol/server-filesystem", "/tmp"]
    database:    # Add database access
      command: "python"
      args: ["-m", "your_database_server"]
```

## 🎛️ **Configuration Files Explained**

### **`render.yaml`** - Render Deployment Config
```yaml
services:
  - type: web                    # Web service type
    name: mcp-agent             # Service name
    env: python                 # Python runtime
    buildCommand: "pip install -r requirements.txt"  # Install deps
    startCommand: "streamlit run app.py --server.port=$PORT --server.address=0.0.0.0"
    envVars:
      - key: OPENAI_API_KEY     # Required API key
        sync: false             # Set manually in dashboard
```

### **`mcp_agent.config.yaml`** - Agent Configuration
```yaml
execution_engine: asyncio       # Async runtime
logger:
  type: console                 # Log to console
  level: info                   # Log level
mcp:
  servers:                      # MCP servers to load
    fetch:
      command: "uvx"
      args: ["mcp-server-fetch"]
openai:
  default_model: gpt-4o-mini    # Cost-efficient model
```

### **`requirements.txt`** - Python Dependencies
```txt
mcp-agent[openai]==0.1.3       # Core framework with OpenAI support
streamlit>=1.28.0              # Web interface
uvicorn>=0.24.0                # ASGI server
```

## 🔐 **Security & Best Practices**

### **Environment Variables**
- ✅ **Never commit API keys** to code
- ✅ **Use Render's environment variables** for secrets
- ✅ **Set `sync: false`** for sensitive variables

### **Network Security**
- ✅ **CORS disabled** for Streamlit compatibility
- ✅ **XSRF protection disabled** for embedded usage
- ✅ **Headless mode** for server deployment

## 💰 **Cost Breakdown**

### **Render Hosting**
- **Free Tier**: 750 hours/month (sleeps after 15min inactivity)
- **Starter Plan**: $7/month (always-on, custom domains)
- **Pro Plan**: $25/month (more resources, autoscaling)

### **OpenAI API Usage**
- **GPT-4o-mini**: ~$0.15 per 1M input tokens, ~$0.60 per 1M output tokens
- **Typical chat**: ~100-500 tokens per message
- **Estimated cost**: $0.01-0.10 per conversation

### **Example Monthly Costs**
- **Personal use**: Free Render + $1-5 OpenAI = $1-5/month
- **Small business**: $7 Render + $10-50 OpenAI = $17-57/month

## 🛠️ **Customization Options**

### **Change AI Model**
```yaml
# In mcp_agent.config.yaml:
openai:
  default_model: gpt-4o         # More capable but expensive
  # or
  default_model: gpt-3.5-turbo  # Faster and cheaper
```

### **Add Authentication**
```python
# In app.py, add before main():
import streamlit_authenticator as stauth

authenticator = stauth.Authenticate(...)
name, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status:
    # Show main app
elif authentication_status == False:
    st.error('Username/password is incorrect')
```

### **Custom Styling**
```python
# In app.py:
st.markdown("""
<style>
    .main-header { color: #1f77b4; }
    .chat-message { border-radius: 10px; }
</style>
""", unsafe_allow_html=True)
```

## 🐛 **Troubleshooting**

### **Common Issues**

1. **"Port already in use"**
   - ✅ **Solution**: Render handles this automatically with `$PORT`

2. **"OpenAI API key not found"**
   - ✅ **Solution**: Set `OPENAI_API_KEY` in Render dashboard

3. **"MCP server failed to start"**
   - ✅ **Solution**: Check `uvx` is available (should be automatic)

4. **"Streamlit not accessible"**
   - ✅ **Solution**: Verify `0.0.0.0` binding and `$PORT` usage

### **Debug Commands**
```bash
# Check if app is running:
curl https://your-app-name.onrender.com/_stcore/health

# View logs in Render dashboard:
# Dashboard → Your Service → Logs
```

## 📊 **Monitoring & Analytics**

### **Built-in Monitoring**
- **Render Dashboard**: CPU, memory, request metrics
- **Streamlit Analytics**: User sessions, page views
- **OpenAI Dashboard**: Token usage, costs

### **Custom Monitoring**
```python
# Add to app.py:
import time
import streamlit as st

# Track usage
if 'session_start' not in st.session_state:
    st.session_state.session_start = time.time()
    # Log session start
```

## 🚀 **Scaling Considerations**

### **Horizontal Scaling**
- Render Pro plans support autoscaling
- Each instance handles ~50-100 concurrent users
- Stateless design allows multiple instances

### **Performance Optimization**
- Use connection pooling for MCP servers
- Implement caching for frequent requests
- Consider async processing for long tasks

---

**Ready to deploy?** Follow the main deployment guide in `README.md`!