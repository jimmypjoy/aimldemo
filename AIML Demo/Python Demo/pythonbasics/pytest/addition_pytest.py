# -*- coding: utf-8 -*-
"""
Created on Mon Sep  9 16:17:16 2024

@author: jimmy
"""

import pytest
from addition import addnumbers

@pytest.fixture
def additiontest_setup():
    print('additiontest_setup():')

def test_addnumbers(additiontest_setup):  # Fixture added as a parameter
    print('inisde test_addnumbers:')
    assert addnumbers(3, 4) == 7