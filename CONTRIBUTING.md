# Contributing to LexGuard Contract AI

Thank you for your interest in contributing! This guide will help you get started.

## Development Setup

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/YOUR_USERNAME/lexguard-contract-ai.git
   cd lexguard-contract-ai
   ```

3. Install dependencies:
   ```bash
   poetry install
   ```

4. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Code Standards

### Style Guide

- Follow PEP 8
- Use type hints for all functions
- Write docstrings for public functions
- Keep functions focused and under 50 lines when possible
- Use meaningful variable names

### Example:

```python
def calculate_risk_score(clause: Clause) -> float:
    """
    Calculate risk score for a clause.

    Args:
        clause: Clause object to analyze

    Returns:
        Risk score between 0.0 and 1.0
    """
    # Implementation here
    pass
```

## Testing

### Run Tests

```bash
make test
```

### Write Tests

- Add tests for new features
- Maintain >80% code coverage
- Use descriptive test names
- Follow AAA pattern: Arrange, Act, Assert

```python
def test_risk_scoring_high_liability():
    # Arrange
    clause = Clause(text="unlimited liability", ...)
    
    # Act
    risk = calculate_risk_score(clause)
    
    # Assert
    assert risk > 0.7
```

## Code Quality

### Before Committing

```bash
make lint      # Check for issues
make format    # Auto-format code
make test      # Run tests
```

### Pre-commit Checklist

- [ ] Code is formatted with black
- [ ] No linting errors from ruff
- [ ] All tests pass
- [ ] New tests added for new features
- [ ] Documentation updated if needed

## Submitting Changes

1. Commit your changes:
   ```bash
   git add .
   git commit -m "feat: add new risk scoring rule"
   ```

2. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

3. Create a Pull Request on GitHub

### Commit Message Format

Use conventional commits:

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `test:` Test additions/changes
- `refactor:` Code refactoring
- `perf:` Performance improvements

Example: `feat: add support for DOCX files`

## Pull Request Guidelines

### PR Description Should Include:

- What changes were made
- Why the changes were needed
- How to test the changes
- Screenshots (for UI changes)
- Related issue numbers

### Example PR Description:

```markdown
## Description
Adds support for analyzing DOCX files in addition to PDFs.

## Changes
- Added `docx_extractor.py` module
- Updated upload route to accept .docx files
- Added tests for DOCX extraction

## Testing
1. Upload a sample DOCX contract
2. Verify clauses are extracted correctly
3. Check risk scoring works as expected

Closes #123
```

## Areas to Contribute

### High Priority
- [ ] Additional clause classification patterns
- [ ] More comprehensive risk scoring rules
- [ ] Support for more document formats
- [ ] Improved chunking algorithms
- [ ] Better OCR integration

### Medium Priority
- [ ] Additional LLM provider support
- [ ] Enhanced UI features
- [ ] Performance optimizations
- [ ] Better error handling
- [ ] Internationalization

### Documentation
- [ ] More code examples
- [ ] Tutorial videos
- [ ] API usage guides
- [ ] Architecture deep-dives

## Questions?

- Open an issue for discussion
- Join our community chat (if available)
- Email maintainers

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on what's best for the project
- Show empathy toward other contributors

Thank you for contributing to LexGuard! 🙏


