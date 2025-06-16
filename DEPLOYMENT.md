# MCP Agent Deployment Guide

This guide will help you deploy your MCP Agent to various platforms, with a focus on Render.com.

## Quick Start - Deploy to Render

### Prerequisites
- GitHub account with this repository
- Render account (free tier available)
- OpenAI API key

### Steps

1. **Prepare Your Repository**
   ```bash
   # Make sure the render_deployment folder is in your repo
   git add render_deployment/
   git commit -m "Add Render deployment configuration"
   git push origin main
   ```

2. **Deploy to Render**
   - Go to [render.com](https://render.com) and sign in
   - Click "New +" → "Blueprint"
   - Connect your GitHub repository
   - Select this repository
   - Render will detect the `render.yaml` file automatically

3. **Set Environment Variables**
   - In Render dashboard, go to your service
   - Add environment variable: `OPENAI_API_KEY` = `your_openai_api_key`

4. **Access Your App**
   - Your app will be available at: `https://your-app-name.onrender.com`

## Alternative Deployment Options

### Option 1: Manual Render Setup

If you prefer manual configuration:

1. **Create Web Service**
   - Render Dashboard → "New +" → "Web Service"
   - Connect GitHub repository

2. **Configuration**
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true --server.enableCORS=false --server.enableXsrfProtection=false`
   - **Environment**: Python 3
   - **Root Directory**: `render_deployment`

### Option 2: Docker Deployment

For containerized deployment:

```bash
cd render_deployment
docker build -t mcp-agent .
docker run -p 8501:8501 -e OPENAI_API_KEY=your_key mcp-agent
```

### Option 3: Other Platforms

The same configuration can be adapted for:
- **Heroku**: Use `Procfile` instead of `render.yaml`
- **Railway**: Similar to Render, supports `render.yaml`
- **Vercel**: For serverless deployment (requires modifications)
- **AWS/GCP/Azure**: Using container services

## Configuration

### Environment Variables

Required:
- `OPENAI_API_KEY`: Your OpenAI API key

Optional:
- `PYTHONPATH`: Set to `.` (usually automatic)

### MCP Agent Configuration

Edit `render_deployment/mcp_agent.config.yaml`:

```yaml
execution_engine: asyncio
logger:
  type: console
  level: info

mcp:
  servers:
    fetch:
      command: "uvx"
      args: ["mcp-server-fetch"]
    # Add more servers as needed

openai:
  default_model: gpt-4o-mini  # Cost-efficient option
```

## Features of the Deployed App

Your deployed MCP agent will have:

- **Web Interface**: Clean Streamlit chat interface
- **Web Fetching**: Can fetch and analyze content from URLs
- **Conversation Memory**: Maintains chat history
- **Tool Visibility**: Shows available MCP tools
- **Responsive Design**: Works on desktop and mobile

## Customization

### Adding More MCP Servers

1. **Update Configuration** (`mcp_agent.config.yaml`):
   ```yaml
   mcp:
     servers:
       fetch:
         command: "uvx"
         args: ["mcp-server-fetch"]
       filesystem:
         command: "npx"
         args: ["-y", "@modelcontextprotocol/server-filesystem", "/tmp"]
   ```

2. **Update Agent** (`app.py`):
   ```python
   server_names=["fetch", "filesystem"]
   ```

### Changing the Model

Update in `mcp_agent.config.yaml`:
```yaml
openai:
  default_model: gpt-4o  # or gpt-3.5-turbo, etc.
```

### Custom Styling

Add custom CSS in `app.py`:
```python
st.markdown("""
<style>
    .main-header {
        color: #1f77b4;
    }
</style>
""", unsafe_allow_html=True)
```

## Monitoring and Maintenance

### Logs
- **Render**: Check logs in the Render dashboard
- **Local**: Logs appear in terminal/console

### Health Monitoring
- Render provides automatic health checks
- Custom health endpoint available at `/_stcore/health`

### Updates
- Push to GitHub to trigger automatic redeployment
- Monitor resource usage in Render dashboard

## Cost Considerations

### Render Costs
- **Free Tier**: 750 hours/month (sufficient for personal projects)
- **Paid Plans**: Start at $7/month for always-on services

### OpenAI Costs
- **GPT-4o-mini**: ~$0.15 per 1M input tokens
- **GPT-4o**: ~$2.50 per 1M input tokens
- Monitor usage in OpenAI dashboard

## Troubleshooting

### Common Issues

1. **Build Failures**
   - Check `requirements.txt` for correct dependencies
   - Verify Python version compatibility

2. **Runtime Errors**
   - Ensure `OPENAI_API_KEY` is set
   - Check Render logs for specific errors

3. **MCP Server Issues**
   - Verify `uvx` is available (should be automatic)
   - Check MCP server configurations

4. **Streamlit Issues**
   - Ensure correct port configuration
   - Check CORS settings

### Getting Help

- **MCP Agent Issues**: [GitHub Issues](https://github.com/lastmile-ai/mcp-agent/issues)
- **Render Support**: [Render Documentation](https://render.com/docs)
- **Streamlit Issues**: [Streamlit Documentation](https://docs.streamlit.io)

## Security Best Practices

1. **API Keys**: Never commit API keys to repository
2. **Environment Variables**: Use platform-provided secret management
3. **CORS**: Configured appropriately for Streamlit
4. **Updates**: Keep dependencies updated regularly

## Next Steps

After deployment, consider:

1. **Custom Domain**: Configure custom domain in Render
2. **Analytics**: Add usage tracking
3. **Authentication**: Add user authentication if needed
4. **Rate Limiting**: Implement usage limits
5. **Monitoring**: Set up uptime monitoring

Your MCP agent is now ready for production use! 🚀