import json
from dataclasses import dataclass
from typing import List

from memory_copilot.tools import submit_result


@dataclass
class MockType:
    a: str
    b: int
    c: List[str]


def test_submit_result():
    sample = {
        'a': 'test',
        'b': 1,
        'c': ['test', 'test2']
    }
    result, reason = submit_result(json.dumps(sample), 'test', MockType)
    assert result == MockType(**sample)
    assert reason == 'test'

    sample_error = {
        'a': 'test',
        'b_error': 1,
        'c': ['test', 'test2']
    }
    try:
        submit_result(json.dumps(sample_error), 'test', MockType)
    except ValueError as e:
        assert str(
            e) == "Keys of result dict_keys(['a', 'b_error', 'c']) not match with ['a', 'b', 'c']"
    else:
        raise AssertionError('ValueError not raised')
