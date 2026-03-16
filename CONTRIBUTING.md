# 🤝 CONTRIBUTING TO LEXORA

Thank you for your interest in contributing to Lexora! This document provides guidelines and instructions for contributing to the project.

---

## 📋 TABLE OF CONTENTS

1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [Development Setup](#development-setup)
4. [How to Contribute](#how-to-contribute)
5. [Coding Standards](#coding-standards)
6. [Pull Request Guidelines](#pull-request-guidelines)
7. [Issue Reporting](#issue-reporting)
8. [Community](#community)

---

## 🎯 CODE OF CONDUCT

### Our Pledge

We pledge to make participation in our project a harassment-free experience for everyone. We welcome contributors of all backgrounds, identities, and experience levels.

### Expected Behavior

- ✅ Be respectful and inclusive
- ✅ Accept constructive criticism gracefully
- ✅ Focus on what's best for the community
- ✅ Show empathy towards other community members

### Unacceptable Behavior

- ❌ Harassment or discrimination
- ❌ Trolling or insulting comments
- ❌ Publishing others' private information
- ❌ Promoting illegal activities

---

## 🚀 GETTING STARTED

### First Time Contributors

New to open source? Here's how to start:

1. **Fork the repository** on GitHub
2. **Clone your fork** locally
   ```bash
   git clone https://github.com/YOUR_USERNAME/lexora-lang.git
   cd lexora-lang
   ```
3. **Set up upstream remote**
   ```bash
   git remote add upstream https://github.com/ORIGINAL_OWNER/lexora-lang.git
   ```
4. **Find a good first issue** - Look for labels like `good first issue` or `help wanted`
5. **Create a branch** for your work
   ```bash
   git checkout -b feature/your-feature-name
   ```

### Ways to Contribute

- 💻 **Code** - New features, bug fixes, performance improvements
- 📖 **Documentation** - Tutorials, examples, API docs
- 🐛 **Bug Reports** - Clear, detailed issue reports
- 💡 **Feature Requests** - Well-thought-out suggestions
- 🎨 **Design** - UI/UX improvements, logo design
- 📝 **Translations** - Internationalization support
- 🧪 **Testing** - Test cases, QA, edge case discovery

---

## 💻 DEVELOPMENT SETUP

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git
- Code editor (VS Code recommended)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/lexora-lang.git
   cd lexora-lang
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # macOS/Linux
   venv\Scripts\activate     # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install development tools**
   ```bash
   pip install pytest pytest-cov black flake8
   ```

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest --cov=lexora tests/

# Run specific test file
pytest tests/test_lexora.py
```

### Code Formatting

```bash
# Format code with Black
black lexora.py
black lexora-web-editor/src/

# Check style with Flake8
flake8 lexora.py
flake8 lexora-web-editor/src/
```

---

## 📝 HOW TO CONTRIBUTE

### Bug Fixes

1. **Find an issue** labeled `bug`
2. **Reproduce the bug** on latest version
3. **Write a test** that fails because of the bug
4. **Fix the bug** in the code
5. **Run tests** to ensure fix works
6. **Submit PR** referencing the issue

### New Features

1. **Discuss first!** Open an issue to discuss your idea
2. **Get feedback** from maintainers
3. **Create implementation plan**
4. **Write code** following standards
5. **Add tests** for new functionality
6. **Update documentation**
7. **Submit PR** with clear description

### Documentation

1. **Find gaps** in existing docs
2. **Clarify confusing** sections
3. **Add examples** where helpful
4. **Fix typos** and grammatical errors
5. **Update screenshots** if UI changes

---

## 🎨 CODING STANDARDS

### Python Style Guide

Follow **PEP 8** - Python Style Guide:

#### Naming Conventions

```python
# Classes - PascalCase
class SimpleEnglishInterpreter:
    pass

# Functions - snake_case
def execute_script(self, lines):
    pass

# Variables - snake_case
variable_name = "value"

# Constants - UPPER_CASE
MAX_RETRIES = 5

# Private methods - leading underscore
def _internal_method(self):
    pass
```

#### Code Layout

```python
# Use 4 spaces for indentation (no tabs!)
def my_function():
    if condition:
        do_something()
    
    # Blank line between logical sections
    return result

# Limit lines to 79 characters
long_variable_name = (
    value1 + value2 + value3
)

# Import order
import os              # Standard library first
import sys

import flask           # Third-party packages
from flask import Flask

import lexora          # Local application imports
from lexora.lexora import Interpreter
```

#### Comments & Docstrings

```python
"""
Module docstring explaining purpose.
"""

def complex_function(param1, param2):
    """
    One-line summary of function.
    
    Detailed description if needed.
    
    Args:
        param1 (type): Description
        param2 (type): Description
    
    Returns:
        type: Description
    
    Raises:
        ExceptionType: When this happens
    """
    # Comment explaining WHY, not WHAT
    if special_case:
        # Handle edge case
        handle_it()
    
    return result
```

### JavaScript Standards

```javascript
// Use const/let instead of var
const MAX_SIZE = 100;
let counter = 0;

// Use arrow functions for callbacks
items.forEach(item => {
    console.log(item);
});

// Template literals for strings
const greeting = `Hello, ${name}!`;

// Semicolons required
doSomething();

// Consistent brace style
if (condition) {
    doSomething();
}
```

### HTML Standards

```html
<!-- Use semantic tags -->
<nav class="navbar">
    <a href="/" class="logo">Lexora</a>
</nav>

<!-- Always close tags -->
<div class="container">
    <p>Content</p>
</div>

<!-- Use double quotes -->
<input type="text" id="name" class="form-control">
```

### CSS Standards

```css
/* Organize by component */
.navbar {
    display: flex;
    align-items: center;
}

/* Use BEM naming */
.card { }
.card__header { }
.card--featured { }

/* Specificity order */
.element { }           /* Tag */
.class { }             /* Class */
#id { }                /* ID */
!important { }         /* Avoid when possible */
```

---

## 🔀 PULL REQUEST GUIDELINES

### Before Submitting

- [ ] Code follows style guide
- [ ] All tests pass
- [ ] Code is commented
- [ ] Documentation updated
- [ ] No debug code left in
- [ ] Squashed unnecessary commits

### PR Title Format

```
feat: Add new file upload feature
fix: Fix newline visibility issue
docs: Update README deployment section
style: Format interpreter code
refactor: Simplify parser logic
test: Add unit tests for classes
chore: Update dependencies to latest
```

### PR Description Template

```markdown
## Description
Clear description of what was changed and why.

## Related Issue
Fixes #123 (if applicable)

## Type of Change
- [ ] Bug fix (non-breaking change fixing an issue)
- [ ] New feature (non-breaking change adding functionality)
- [ ] Breaking change (would cause existing functionality to change)
- [ ] Documentation update

## Testing Done
- [ ] Unit tests added/updated
- [ ] Integration tests passing
- [ ] Manual testing completed

## Screenshots
(If UI changes)

## Checklist
- [ ] My code follows project style guidelines
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have made corresponding changes to the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix is effective or feature works
- [ ] New and existing unit tests pass locally
```

### Review Process

1. **Automated checks** run on PR
2. **Maintainer review** within 48 hours
3. **Address feedback** from reviewers
4. **Approval** from at least 1 maintainer
5. **Merge** by maintainer

---

## 🐛 ISSUE REPORTING

### Bug Report Template

```markdown
**Describe the bug**
Clear, concise description of the bug.

**To Reproduce**
Steps to reproduce:
1. Run command '...'
2. Enter code '...'
3. See error

**Expected behavior**
What you expected to happen.

**Actual behavior**
What actually happened.

**Environment:**
- OS: [e.g., macOS 13.0]
- Python version: [e.g., 3.11.0]
- Lexora version: [e.g., 1.0.0]

**Screenshots**
If applicable, add screenshots.

**Additional context**
Any other relevant information.
```

### Feature Request Template

```markdown
**Problem statement**
What problem would this feature solve?

**Proposed solution**
How should this feature work?

**Examples**
Show example code or usage.

**Alternatives considered**
Other solutions you've considered.

**Additional context**
Any other relevant information.
```

---

## 📚 DOCUMENTATION GUIDELINES

### Writing Style

- ✅ Use **clear, simple language**
- ✅ Write for **beginner to intermediate** developers
- ✅ Include **code examples** where helpful
- ✅ Use **active voice** ("Click the button")
- ✅ Be **concise but thorough**

### Code Examples

```python
# Good: Complete, runnable example
interpreter = SimpleEnglishInterpreter()
interpreter.execute_script("""
    Set x to 10
    Display x
""")

# Bad: Incomplete snippet
interpreter.execute("Set x to 10")  # Missing setup
```

### Screenshots

- Use **PNG format** for clarity
- Keep file size **under 200KB**
- Highlight **relevant areas** with arrows/boxes
- Use **consistent styling** (macOS preferred)

---

## 🧪 TESTING REQUIREMENTS

### Test Coverage

- **Minimum 80%** for new code
- **Critical paths** must have 100% coverage
- **All public APIs** must be tested

### Test Structure

```python
class TestInterpreter(unittest.TestCase):
    """Test suite for interpreter functionality"""
    
    def setUp(self):
        """Setup test fixtures"""
        self.interpreter = SimpleEnglishInterpreter()
    
    def test_display_command(self):
        """Test Display command outputs correctly"""
        output = capture_output(lambda: 
            self.interpreter.execute_script("Display 'Hello'")
        )
        self.assertEqual(output.strip(), "Hello")
    
    def tearDown(self):
        """Cleanup after each test"""
        del self.interpreter
```

### Running Tests Locally

```bash
# All tests
pytest tests/ -v

# Specific test class
pytest tests/test_lexora.py::TestInterpreter -v

# With coverage report
pytest --cov=lexora --cov-report=html tests/
```

---

## 🌐 TRANSLATIONS

We welcome translations to make Lexora accessible globally!

### Adding Translations

1. Create `docs/i18n/<language-code>/`
2. Translate documentation files
3. Update navigation to include language selector
4. Test translated content renders correctly

### Translation Guidelines

- Keep technical terms in English if no good translation
- Maintain consistent terminology
- Include translator credits
- Update regularly as docs evolve

---

## 📦 RELEASE PROCESS

### Version Numbering

We follow **Semantic Versioning**:

```
MAJOR.MINOR.PATCH
  │     │     │
  │     │     └─ Backward-compatible bug fixes
  │     └─────── Backward-compatible new features
  └───────────── Backward-incompatible changes
```

Example: `1.2.3` → Major 1, Minor 2, Patch 3

### Release Checklist

- [ ] Update version in `setup.py`
- [ ] Update version in interpreter
- [ ] Update CHANGELOG.md
- [ ] Run all tests
- [ ] Update documentation
- [ ] Create release tag
- [ ] Build distribution packages
- [ ] Upload to PyPI
- [ ] Create GitHub release
- [ ] Announce on social media

---

## 🎓 LEARNING RESOURCES

### For New Contributors

- [How to Contribute to Open Source](https://opensource.guide/how-to-contribute/)
- [First Contributions](https://firstcontributions.github.io/)
- [GitHub Skills](https://skills.github.com/)

### For Learning Python

- [Python Official Tutorial](https://docs.python.org/3/tutorial/)
- [Real Python](https://realpython.com/)
- [Python for Beginners](https://www.python.org/about/gettingstarted/)

### For Learning Lexora

- [Lexora Quick Start](QUICKSTART.md)
- [Lexora Documentation](https://lexora.dev/docs)
- [Example Programs](examples/)

---

## 🏆 RECOGNITION

Contributors receive recognition through:

- 🌟 **GitHub Contributors page**
- 📝 **CHANGELOG mentions**
- 🎖️ **Contributor badge** (for significant contributions)
- 📢 **Social media shoutouts**
- 💬 **Direct thanks from maintainers**

---

## 📞 GETTING HELP

### Communication Channels

- **GitHub Issues** - Bug reports, feature requests
- **GitHub Discussions** - Questions, general discussion
- **Discord** - Real-time chat with community
- **Email** - security@lexora.dev (security issues only)

### Response Times

We aim to respond within:

- **Bug reports:** 24-48 hours
- **Feature requests:** 1 week
- **Questions:** 24-72 hours
- **PR reviews:** 48 hours

---

## 🙏 THANK YOU

Every contribution makes Lexora better! Whether it's fixing a typo, reporting a bug, or adding a major feature - **you're making a difference**.

Together, we're making programming accessible to everyone! 🚀

---

**Last Updated:** 2026-03-14  
**License:** MIT  
**Maintained By:** Lexora Team
