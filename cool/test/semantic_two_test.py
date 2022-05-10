import pytest

from main import compile
from util.exceptions import *
from util.structure import clearClassTree


def test_badarith():
    clearClassTree()
    with pytest.raises(badarith):
        compile('resources/semantic/input/badarith.cool')


def test_baddispatch():
    clearClassTree()
    with pytest.raises(baddispatch):
        compile('resources/semantic/input/baddispatch.cool')


def test_badequalitytest():
    clearClassTree()
    with pytest.raises(badequalitytest):
        compile('resources/semantic/input/badequalitytest.cool')


def test_badequalitytest2():
    clearClassTree()
    with pytest.raises(badequalitytest2):
        compile('resources/semantic/input/badequalitytest2.cool')


def test_badwhilebody():
    clearClassTree()
    with pytest.raises(badwhilebody):
        compile('resources/semantic/input/badwhilebody.cool')


def test_badwhilecond():
    clearClassTree()
    with pytest.raises(badwhilecond):
        compile('resources/semantic/input/badwhilecond.cool')


def test_caseidenticalbranch():
    clearClassTree()
    with pytest.raises(caseidenticalbranch):
        compile('resources/semantic/input/caseidenticalbranch.cool')


def test_missingclass():
    clearClassTree()
    with pytest.raises(missingclass):
        compile('resources/semantic/input/missingclass.cool')


def test_outofscope():
    clearClassTree()
    with pytest.raises(outofscope):
        compile('resources/semantic/input/outofscope.cool')


def test_redefinedclass():
    clearClassTree()
    with pytest.raises(redefinedclass):
        compile('resources/semantic/input/redefinedclass.cool')


def test_returntypenoexist():
    clearClassTree()
    with pytest.raises(returntypenoexist):
        compile('resources/semantic/input/returntypenoexist.cool')


def test_selftypebadreturn():
    clearClassTree()
    with pytest.raises(selftypebadreturn):
        compile('resources/semantic/input/selftypebadreturn.cool')
