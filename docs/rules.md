# Project Rules

## Style Guide Compliance

All code must follow the style guide located at `../amilib/docs/style_guide_compliance.md`

### Key Style Rules

#### Import Style
- **Use absolute imports with module prefix**
- ✅ CORRECT: `from atpoe.core.curve_generator import generate_initial_circle`
- ❌ WRONG: `from .curve_generator import generate_initial_circle`

#### __init__.py Files
- **All `__init__.py` files should be empty unless explicitly agreed**
- ✅ CORRECT: Empty `__init__.py` files
- ❌ WRONG: `__init__.py` files with import statements or other code

## Development Rules

### 1. Code Quality
- Write clear, readable code with meaningful variable names
- Add docstrings to all functions and classes
- Use type hints where appropriate
- Follow PEP 8 formatting guidelines

### 2. Testing
- Write unit tests for all new functionality
- Ensure all tests pass before committing
- Test edge cases and error conditions

### 3. Documentation
- Update documentation when changing functionality
- Keep README files current
- Document any non-obvious algorithms or design decisions

### 4. Git Practices
- **NEVER use `git clean -fd` or similar destructive commands**
- Create feature branches for significant changes
- Write clear commit messages
- Test before pushing to main branch

### 5. Algorithm Requirements
- Curves must be properly closed (start point ≈ end point)
- Use consistent segment lengths (e.g., 3 pixels)
- Iterate until closure: `while (dist(start, current) > segment_length): add new point`
- Avoid infinite loops - always have termination conditions
- Ensure curves don't cross or go outside boundaries

### 6. Performance
- Optimize algorithms for large numbers of curves
- Use efficient collision detection (O(k log n) or better)
- Monitor memory usage and execution time
- Profile code when performance issues arise

### 7. Error Handling
- Handle edge cases gracefully
- Provide meaningful error messages
- Don't let programs crash on invalid input
- Log errors for debugging

### 8. Package Structure
- Keep package structure clean and logical
- Use appropriate module separation
- Follow Python packaging best practices
- Maintain backward compatibility when possible

## Violation Consequences

- Style violations will be caught during code review
- Performance issues will be flagged for optimization
- Algorithm bugs will require immediate fixes
- Documentation gaps will delay releases

## Best Practices

### Before Making Changes
1. Read the style guide
2. Examine existing code patterns
3. Plan the implementation
4. Consider edge cases

### During Development
1. Follow established conventions
2. Test frequently
3. Document as you go
4. Keep commits small and focused

### After Changes
1. Verify style compliance
2. Run all tests
3. Update documentation
4. Review with team if needed 