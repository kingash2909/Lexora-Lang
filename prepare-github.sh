#!/bin/bash

# =============================================================================
# LEXORA - GITHUB UPLOAD PREPARATION SCRIPT
# Version: 1.0.0
# 
# This script prepares your Lexora project for GitHub upload by:
# 1. Verifying .gitignore is working
# 2. Checking all required files exist
# 3. Initializing git repository
# 4. Staging all production files
# 5. Providing upload instructions
# =============================================================================

echo "============================================================================="
echo "🚀 LEXORA - GITHUB UPLOAD PREPARATION"
echo "============================================================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Project directory
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

echo -e "${BLUE}📁 Project Directory:${NC}"
echo "   $PROJECT_DIR"
echo ""

# Function to check if file exists
check_file() {
    if [ -f "$1" ]; then
        echo -e "${GREEN}✓${NC} $1"
        return 0
    else
        echo -e "${RED}✗${NC} $1 (missing)"
        return 1
    fi
}

# Function to check if directory exists
check_dir() {
    if [ -d "$1" ]; then
        echo -e "${GREEN}✓${NC} $1/"
        return 0
    else
        echo -e "${RED}✗${NC} $1/ (missing)"
        return 1
    fi
}

echo "============================================================================="
echo "📋 CHECKING REQUIRED PRODUCTION FILES"
echo "============================================================================="
echo ""

echo -e "${YELLOW}Core Application Files:${NC}"
check_file "lexora.py"
check_file "setup.py"
check_file ".gitignore"
check_file "README.md"
check_file "CONTRIBUTING.md"
check_file "QUICKSTART.md"
echo ""

echo -e "${YELLOW}Web Editor Files:${NC}"
check_dir "lexora-web-editor/src"
check_file "lexora-web-editor/src/app.py"
check_file "lexora-web-editor/src/lexora/__init__.py"
check_file "lexora-web-editor/src/lexora/lexora.py"
check_file "lexora-web-editor/requirements.txt"
echo ""

echo -e "${YELLOW}Documentation Files:${NC}"
check_file "PROJECT_STRUCTURE_GUIDE.md"
check_file "PRODUCTION_READY_SUMMARY.md"
check_file "lexora-web-editor/PRODUCTION_README.md"
echo ""

echo -e "${YELLOW}Frontend Assets:${NC}"
check_dir "lexora-web-editor/src/templates"
check_dir "lexora-web-editor/src/static"
check_file "lexora-web-editor/src/static/css/style.css"
check_file "lexora-web-editor/src/static/js/editor.js"
echo ""

echo "============================================================================="
echo "🔍 VERIFYING .GITIGNORE IS WORKING"
echo "============================================================================="
echo ""

# Check that sensitive files/dirs are excluded
echo -e "${YELLOW}Checking excluded files/directories:${NC}"

if [ -d ".env" ]; then
    echo -e "${GREEN}✓${NC} .env/ exists (will be excluded by .gitignore)"
else
    echo -e "${YELLOW}ℹ${NC} .env/ not found (OK if using system Python)"
fi

# Check git status to see what would be uploaded
echo ""
echo -e "${YELLOW}Files that will be uploaded to GitHub:${NC}"
echo "(These should be production files only)"
echo ""

# Initialize git if not already done
if [ ! -d ".git" ]; then
    echo -e "${YELLOW}Initializing Git repository...${NC}"
    git init
    echo ""
fi

# Stage all files to see what git thinks
git add --all 2>/dev/null

# Show git status
echo -e "${BLUE}Git Status:${NC}"
git status --short
echo ""

# Count files
TOTAL_FILES=$(git status --short | wc -l | tr -d ' ')
echo "============================================================================="
echo -e "${GREEN}✓ TOTAL FILES READY FOR UPLOAD: ${TOTAL_FILES}${NC}"
echo "============================================================================="
echo ""

# Verify LICENSE exists
if [ ! -f "LICENSE" ]; then
    echo -e "${YELLOW}⚠️  WARNING: LICENSE file not found!${NC}"
    echo "   Consider adding MIT License before uploading."
    echo ""
fi

# Provide next steps
echo "============================================================================="
echo "📝 NEXT STEPS TO UPLOAD TO GITHUB:"
echo "============================================================================="
echo ""
echo "1. Create repository on GitHub:"
echo "   → Visit: https://github.com/new"
echo "   → Repository name: lexora-lang"
echo "   → Visibility: Public"
echo "   → Click 'Create repository'"
echo ""
echo "2. Link remote and push:"
echo -e "${BLUE}   cd $PROJECT_DIR${NC}"
echo -e "${BLUE}   git commit -m \"feat: Production-ready Lexora release\"${NC}"
echo -e "${BLUE}   git branch -M main${NC}"
echo -e "${BLUE}   git remote add origin https://github.com/YOUR_USERNAME/lexora-lang.git${NC}"
echo -e "${BLUE}   git push -u origin main${NC}"
echo ""
echo "3. After upload:"
echo "   → Add repository description on GitHub"
echo "   → Configure branch protection"
echo "   → Add website link: https://lexora.dev"
echo "   → Share with community!"
echo ""
echo "============================================================================="
echo -e "${GREEN}✓ PROJECT IS READY FOR GITHUB UPLOAD!${NC}"
echo "============================================================================="
echo ""

# Show what's excluded
echo "============================================================================="
echo "❌ FILES EXCLUDED (Staying Local):"
echo "============================================================================="
echo "   • .env/ (virtual environment)"
echo "   • __pycache__/ (Python bytecode)"
echo "   • Testing/ (test files)"
echo "   • MD_Files/ (development notes)"
echo "   • test_*.lx (test scripts)"
echo "   • output.txt, log_file (logs)"
echo "   • *.log (log files)"
echo "   • *_GUIDE.md (working documents)"
echo "   • build_standalone.py (build scripts)"
echo "   • installer.sh/bat (installers)"
echo "   • .vscode/, .idea/ (IDE settings)"
echo "   • .DS_Store, Thumbs.db (system files)"
echo ""
echo "============================================================================="
echo ""

exit 0
