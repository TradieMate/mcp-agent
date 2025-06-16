# MCP Agent Deployment on Render

This directory contains the deployment configuration for running your MCP Agent on Render.

## What This Deploys

This deploys a Streamlit web application that provides a chat interface for your MCP agent. The agent has access to web fetching capabilities through the MCP fetch server.

## Prerequisites

1. **OpenAI API Key**: You'll need an OpenAI API key to use the GPT models
2. **Render Account**: Sign up at [render.com](https://render.com)
3. **GitHub Repository**: Your code needs to be in a GitHub repository

## Deployment Steps

### Option 1: Using render.yaml (Recommended)

1. **Push to GitHub**: Make sure this code is in your GitHub repository

2. **Connect to Render**:
   - Go to [render.com](https://render.com) and sign in
   - Click "New +" and select "Blueprint"
   - Connect your GitHub repository
   - Select the repository containing this code
   - Render will automatically detect the `render.yaml` file

3. **Set Environment Variables**:
   - In the Render dashboard, go to your service settings
   - Add environment variable: `OPENAI_API_KEY` with your OpenAI API key

4. **Deploy**: Render will automatically build and deploy your application

### Option 2: Manual Setup

1. **Create Web Service**:
   - Go to Render dashboard
   - Click "New +" → "Web Service"
   - Connect your GitHub repository

2. **Configure Service**:
   - **Name**: `mcp-agent`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true --server.enableCORS=false --server.enableXsrfProtection=false`
   - **Root Directory**: `render_deployment` (if this folder is not in the root)

3. **Environment Variables**:
   - Add `OPENAI_API_KEY` with your OpenAI API key
   - Add `PYTHONPATH` with value `.`

4. **Deploy**: Click "Create Web Service"

## Configuration

### MCP Servers

The application is configured to use:
- **Fetch Server**: Allows the agent to fetch content from URLs

### Model Configuration

- **Default Model**: `gpt-4o-mini` (cost-efficient)
- **Provider**: OpenAI

You can modify these settings in `mcp_agent.config.yaml`.

## Usage

Once deployed, your application will be available at your Render URL (e.g., `https://your-app-name.onrender.com`).

The chat interface allows users to:
- Ask questions
- Request web content to be fetched
- Have conversations with the AI agent

## Troubleshooting

### Common Issues

1. **Build Failures**:
   - Check that all dependencies are correctly specified in `requirements.txt`
   - Ensure Python version compatibility

2. **Runtime Errors**:
   - Verify `OPENAI_API_KEY` is set correctly
   - Check logs in Render dashboard for specific error messages

3. **MCP Server Issues**:
   - The fetch server requires `uvx` to be available
   - If you encounter issues, you may need to modify the server configuration

### Logs

Check the Render dashboard logs for detailed error information and debugging.

## Customization

### Adding More MCP Servers

To add more capabilities, modify `mcp_agent.config.yaml`:

```yaml
mcp:
  servers:
    fetch:
      command: "uvx"
      args: ["mcp-server-fetch"]
    # Add more servers here
    your_server:
      command: "your-command"
      args: ["your-args"]
```

Then update the agent configuration in `app.py`:

```python
server_names=["fetch", "your_server"]
```

### Changing the Model

Modify the model in `mcp_agent.config.yaml`:

```yaml
openai:
  default_model: gpt-4o  # or any other OpenAI model
```

## Cost Considerations

- Using `gpt-4o-mini` keeps costs low
- Monitor your OpenAI usage through their dashboard
- Consider implementing usage limits if needed

## Security

- Never commit API keys to your repository
- Use Render's environment variables for sensitive data
- The application runs with CORS disabled for Streamlit compatibility

## Support

For issues with:
- **MCP Agent Framework**: Check the [main repository](https://github.com/lastmile-ai/mcp-agent)
- **Render Deployment**: Check [Render documentation](https://render.com/docs)
- **Streamlit**: Check [Streamlit documentation](https://docs.streamlit.io)