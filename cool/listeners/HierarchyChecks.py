from antlr.coolParser import coolParser
from util.KlassRegistry import klassRepeats
from util.exceptions import dupformals, overridingmethod4, signaturechange, inheritsselftype, inheritsbool, \
    inheritsstring, badredefineint, redefinedobject, selftyperedeclared, redefinedclass, attroverride, attrbadinit


def parseParams(ctx):
    parsedparams = None
    if ctx.params:
        parsedparams = set()
        seen_param_names = set()
        for param in ctx.params:
            if type(param) == coolParser.Formal_ExpressionContext:
                if param.ID().getText() in seen_param_names:
                    # Explanation: We keep track of the params that are parsed from text
                    # If any of them repeat, we simply raise the exception
                    raise dupformals()
                parsed = frozenset([param.TYPE().getText(), param.ID().getText()])
                seen_param_names.add(param.ID().getText())
                parsedparams.add(parsed)
    return parsedparams


def differentparamtypeoverridecheck(currentClass, ctx, parsedMethod):
    try:
        overridenmethod = currentClass.lookupMethod(ctx.ID().getText())
        # if match, check params are the same for current method
        if parsedMethod.params.values() != overridenmethod.params.values():
            raise overridingmethod4()
    except KeyError:
        # No override
        pass


def signaturechangecheck(currentClass, ctx, parsedMethod):
    try:
        overridenmethod = currentClass.lookupMethod(ctx.ID().getText())
        # if match, check params are the same for current method
        if len(parsedMethod.params) != len(overridenmethod.params):
            raise signaturechange()
    except KeyError:
        # No override
        pass


def classCreationChecks(mainType, inheritance=None):
    if inheritance:
        if inheritance == 'SELF_TYPE':
            raise inheritsselftype()
        if inheritance == 'Bool':
            raise inheritsbool()
        if inheritance == 'String':
            raise inheritsstring()
    # si no hay herencia
    else:
        if mainType == 'Int':
            raise badredefineint()
        if mainType == 'Object':
            raise redefinedobject()
        if mainType == 'SELF_TYPE':
            raise selftyperedeclared()
    if klassRepeats(mainType):
        raise redefinedclass()


def attroverride(currentClass, ctx):
    try:
        variablename = ctx.ID().getText()
        # First, check for the attribute existing on the class tree
        # A keyerror would mean the variable isn't defined
        # FIXME method params will not be checked.
        currentClass.lookupAttribute(variablename)
        # Secondly, if the attribute is on the class tree, but it's *not*
        # on the current class, it means we're redefining a parent attribute.
        if not currentClass.getOwnAttribute(variablename):
            # Explanation: See above
            raise attroverride()
    except KeyError:
        # Explanation: See above
        pass


def attrbadinitcheck(table, currentClass, ctx):
    # If this is an add attribute with the shape [ID : TYPE  '<-' expr]
    # where expr is a variable, check if said variable exists on the class
    if ctx.expr():
        if type(ctx.expr()) == coolParser.BaseContext:
            if type(ctx.expr().children[0]) == coolParser.VariableContext:
                try:
                    table[ctx.expr().children[0].getText()]
                except KeyError:
                    # Explanation: If the symbol isn't defined on the current scope, raise
                    raise attrbadinit()
