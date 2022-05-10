import pytest

from main import compile
from main import dummy
from util.exceptions import *


class TestSemanticOne:

    def test_dummy(self):
        with pytest.raises(SystemExit):
            dummy()

    def test_anattributenamedself(self):
        with pytest.raises(anattributenamedself):
            compile('resources/semantic/input/anattributenamedself.cool')

    def test_badredefineint(self):
        with pytest.raises(badredefineint):
            compile('resources/semantic/input/badredefineint.cool')

    def test_inheritsbool(self):
        with pytest.raises(inheritsbool):
            compile('resources/semantic/input/inheritsbool.cool')

    def test_inheritsselftype(self):
        with pytest.raises(inheritsselftype):
            compile('resources/semantic/input/inheritsselftype.cool')

    def test_inheritsstring(self):
        with pytest.raises(inheritsstring):
            compile('resources/semantic/input/inheritsstring.cool')

    def test_letself(self):
        with pytest.raises(letself):
            compile('resources/semantic/input/letself.cool')

    def test_nomain(self):
        with pytest.raises(nomain):
            compile('resources/semantic/input/nomain.cool')

    def test_redefinedobject(self):
        with pytest.raises(redefinedobject):
            compile('resources/semantic/input/redefinedobject.cool')

    def test_selfassignment(self):
        with pytest.raises(selfassignment):
            compile('resources/semantic/input/self-assignment.cool')

    def test_selfinformalparameter(self):
        with pytest.raises(selfinformalparameter):
            compile('resources/semantic/input/selfinformalparameter.cool')

    def test_selftypeparameterposition(self):
        with pytest.raises(selftypeparameterposition):
            compile('resources/semantic/input/selftypeparameterposition.cool')

    def test_selftyperedeclared(self):
        with pytest.raises(selftyperedeclared):
            compile('resources/semantic/input/selftyperedeclared.cool')
