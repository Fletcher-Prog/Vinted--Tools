#!/bin/bash

# Optimized Vinted Discord Bot - Startup Script
# This script handles the bot startup with proper environment setup

echo "🤖 Starting Optimized Vinted Discord Bot v2.0"
echo "=============================================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "❌ Failed to create virtual environment"
        exit 1
    fi
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Check if dependencies are installed
if [ ! -f "venv/lib/python*/site-packages/discord/__init__.py" ]; then
    echo "📦 Installing dependencies..."
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install dependencies"
        exit 1
    fi
    echo "✅ Dependencies installed"
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found"
    if [ -f "env_example.txt" ]; then
        echo "📋 Copying example environment file..."
        cp env_example.txt .env
        echo "✅ .env file created from example"
        echo ""
        echo "🔧 Please edit .env file with your configuration:"
        echo "   - Add your Discord bot token"
        echo "   - Configure proxy settings if needed"
        echo ""
        echo "Then run this script again."
        exit 1
    else
        echo "❌ No example environment file found"
        exit 1
    fi
fi

# Check for Discord token
if ! grep -q "DISCORD_BOT_TOKEN=.*[^[:space:]]" .env 2>/dev/null; then
    echo "❌ Discord bot token not configured in .env file"
    echo "   Please add your Discord bot token to .env:"
    echo "   DISCORD_BOT_TOKEN=your_token_here"
    exit 1
fi

# Run functionality test (optional)
if [ "$1" = "--test" ]; then
    echo "🧪 Running functionality tests..."
    python3 tests/test_functionality.py
    if [ $? -ne 0 ]; then
        echo "❌ Tests failed"
        exit 1
    fi
    echo "✅ Tests passed"
    echo ""
fi

# Start the bot
echo "🚀 Starting bot..."
echo "   Press Ctrl+C to stop the bot"
echo "   Logs are available in logs/vinted_bot.log"
echo ""

python3 main.py

echo ""
echo "🛑 Bot stopped"
