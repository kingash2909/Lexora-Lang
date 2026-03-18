#!/bin/bash

# =============================================================================
# LEXORA - RENDER DEPLOYMENT PREPARATION
# =============================================================================

echo "============================================================================="
echo "🚀 LEXORA - PREPARING FOR RENDER DEPLOYMENT"
echo "============================================================================="
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

cd "$(dirname "$0")"

echo -e "${BLUE}Checking deployment requirements...${NC}"
echo ""

# Check 1: Git repository
if [ -d ".git" ]; then
    echo -e "${GREEN}✓${NC} Git repository initialized"
else
    echo -e "${YELLOW}!${NC} Initializing git repository..."
    git init
fi

# Check 2: Required files
echo ""
echo -e "${YELLOW}Checking required files:${NC}"

files_ok=true

if [ -f "render.yaml" ]; then
    echo -e "${GREEN}✓${NC} render.yaml exists"
else
    echo -e "${RED}✗${NC} render.yaml missing"
    files_ok=false
fi

if [ -f "lexora-web-editor/requirements.txt" ]; then
    echo -e "${GREEN}✓${NC} requirements.txt exists"
else
    echo -e "${RED}✗${NC} requirements.txt missing"
    files_ok=false
fi

if [ -f "lexora-web-editor/src/app.py" ]; then
    echo -e "${GREEN}✓${NC} app.py exists"
else
    echo -e "${RED}✗${NC} app.py missing"
    files_ok=false
fi

if [ "$files_ok" = false ]; then
    echo ""
    echo -e "${RED}Missing required files! Cannot deploy.${NC}"
    exit 1
fi

# Check 3: Git status
echo ""
echo -e "${YELLOW}Git Status:${NC}"
git status --short

echo ""
echo "============================================================================="
echo "📋 FILES TO BE UPLOADED:"
echo "============================================================================="

# Count files
file_count=$(git status --short | wc -l | tr -d ' ')
echo -e "${GREEN}$file_count files${NC} ready for deployment"

echo ""
echo "============================================================================="
echo "🎯 DEPLOYMENT STEPS:"
echo "============================================================================="
echo ""
echo "Step 1: Commit your changes"
echo -e "${BLUE}   git add .${NC}"
echo -e "${BLUE}   git commit -m \"Deploy to Render\"${NC}"
echo ""
echo "Step 2: Push to GitHub"
echo -e "${BLUE}   git remote add origin https://github.com/YOUR_USERNAME/lexora-lang.git${NC}"
echo -e "${BLUE}   git push -u origin main${NC}"
echo ""
echo "Step 3: Deploy on Render"
echo "   1. Visit: https://render.com"
echo "   2. Click: New + → Web Service"
echo "   3. Connect: Your GitHub repository"
echo "   4. Configure: Use settings from render.yaml"
echo "   5. Deploy!"
echo ""
echo "============================================================================="
echo -e "${GREEN}✓ PROJECT READY FOR RENDER!${NC}"
echo "============================================================================="
echo ""
echo "Your Lexora will be live at:"
echo -e "${BLUE}https://lexora-lang.onrender.com${NC}"
echo ""
echo "Estimated deployment time: 3-5 minutes"
echo ""

exit 0
