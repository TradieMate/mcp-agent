# 🚀 Quick Start Guide

## 5-Minute Deployment to Render

### Prerequisites
- GitHub account
- OpenAI API key ([get one here](https://platform.openai.com/api-keys))
- Render account ([sign up free](https://render.com))

### Step 1: Get Your OpenAI API Key
1. Go to https://platform.openai.com/api-keys
2. Click "Create new secret key"
3. Copy the key (starts with `sk-proj-...`)
4. **Save it securely** - you'll need it in Step 3

### Step 2: Deploy to Render
1. **Fork/Clone this repository** to your GitHub account
2. **Go to Render**: https://render.com/dashboard
3. **Click "New +"** → **"Blueprint"**
4. **Connect GitHub** and select this repository
5. **Render detects `render.yaml`** automatically
6. **Click "Apply"** to start deployment

### Step 3: Set Environment Variables
1. **In Render dashboard**, go to your new service
2. **Click "Environment"** tab
3. **Add variable**:
   - **Key**: `OPENAI_API_KEY`
   - **Value**: Your API key from Step 1
4. **Save changes** (triggers redeploy)

### Step 4: Access Your Agent
1. **Wait for deployment** (2-3 minutes)
2. **Click your service URL** (e.g., `https://mcp-agent-abc123.onrender.com`)
3. **Start chatting!** 🎉

## 💬 Example Conversations

Try these prompts with your deployed agent:

```
"Fetch the latest news from https://news.ycombinator.com"
```

```
"Get the content from https://www.anthropic.com/research/building-effective-agents and summarize it"
```

```
"What's the weather like? Fetch data from https://wttr.in/london?format=j1"
```

## 🔧 Variables Reference

### Required Environment Variables
| Variable | Description | Where to Get |
|----------|-------------|--------------|
| `OPENAI_API_KEY` | Your OpenAI API key | https://platform.openai.com/api-keys |

### Automatic Variables (Set by Render)
| Variable | Description | Value |
|----------|-------------|-------|
| `PORT` | Port to bind to | Set by Render |
| `PYTHONPATH` | Python module path | `.` |

## 🎛️ Configuration Options

### Change AI Model (Optional)
Edit `mcp_agent.config.yaml`:
```yaml
openai:
  default_model: gpt-4o        # More capable (expensive)
  # or
  default_model: gpt-3.5-turbo # Faster (cheaper)
  # or  
  default_model: gpt-4o-mini   # Default (balanced)
```

### Add More Capabilities (Optional)
Edit `mcp_agent.config.yaml` to add more MCP servers:
```yaml
mcp:
  servers:
    fetch:
      command: "uvx"
      args: ["mcp-server-fetch"]
    # Add filesystem access:
    filesystem:
      command: "npx"
      args: ["-y", "@modelcontextprotocol/server-filesystem", "/tmp"]
```

Then update `app.py`:
```python
server_names=["fetch", "filesystem"]  # Add new server
```

## 💰 Cost Estimate

### Free Tier (Perfect for Testing)
- **Render**: Free (750 hours/month, sleeps after 15min)
- **OpenAI**: Pay per use (~$0.01-0.10 per conversation)
- **Total**: ~$1-5/month for personal use

### Production (Always-On)
- **Render**: $7/month (Starter plan)
- **OpenAI**: $10-50/month (depending on usage)
- **Total**: $17-57/month for small business

## 🐛 Troubleshooting

### "Service won't start"
- ✅ Check that `OPENAI_API_KEY` is set correctly
- ✅ View logs in Render dashboard for specific errors

### "Can't access the app"
- ✅ Wait 2-3 minutes for deployment to complete
- ✅ Check service status in Render dashboard

### "OpenAI errors"
- ✅ Verify API key is valid and has credits
- ✅ Check OpenAI usage dashboard for limits

### "MCP server errors"
- ✅ This is usually automatic - check logs if issues persist

## 🔄 Making Changes

### Update Your Deployment
1. **Make changes** to files in `render_deployment/`
2. **Commit and push** to GitHub
3. **Render automatically redeploys** (takes 2-3 minutes)

### Local Development
```bash
cd render_deployment
export OPENAI_API_KEY="your-key-here"
./start.sh
```

## 📚 Next Steps

- **Read the full guide**: `HOW_IT_WORKS.md`
- **Customize the interface**: Edit `app.py`
- **Add more MCP servers**: See examples in main repository
- **Set up monitoring**: Use Render dashboard analytics

## 🆘 Need Help?

- **MCP Agent Issues**: [GitHub Issues](https://github.com/lastmile-ai/mcp-agent/issues)
- **Render Support**: [Render Docs](https://render.com/docs)
- **OpenAI Issues**: [OpenAI Help](https://help.openai.com/)

---

**🎉 Congratulations!** Your MCP agent is now live and ready to help users!