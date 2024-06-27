#
# conftest.py
import sys
from os.path import dirname as d
from os.path import abspath, join
root_dir = d(d(abspath(__file__)))
sys.path.append(root_dir)
sys.path.append(f'{root_dir}/src')
print(root_dir)
print(sys.path)

import pytest

@pytest.fixture
def test_root():
  return root_dir