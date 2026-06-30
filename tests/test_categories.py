"""Unit tests for bot/categories.py."""
import pytest

from bot.categories import CATEGORIES, get_category


def test_categories_have_unique_codes():
    codes = [category.code for category in CATEGORIES]
    assert len(codes) == len(set(codes))


def test_categories_is_non_empty():
    assert len(CATEGORIES) == 9


def test_get_category_returns_matching_category():
    category = get_category("bug")
    assert category.code == "bug"
    assert "Баг" in category.label


def test_get_category_raises_for_unknown_code():
    with pytest.raises(ValueError):
        get_category("does-not-exist")
