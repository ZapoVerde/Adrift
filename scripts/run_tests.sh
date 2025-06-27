#!/bin/bash

# run_tests.sh
# Test runner when Adrift is the root directory

echo "🚦 Starting test suite..."

# Set PYTHONPATH to current directory
export PYTHONPATH=.

# Run pytest on test directory
pytest test --tb=short -v

RESULT=$?

if [ $RESULT -eq 0 ]; then
    echo "✅ All tests passed."
else
    echo "❌ Some tests failed. Check output above."
fi

exit $RESULT
