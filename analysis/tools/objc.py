import re


def format_msgSend(selector, args):
    name_with_args = ""
    num_args = len(re.findall(":", selector))
    parts = selector.split(":")
    for param_idx in range(0, num_args):
        if param_idx != 0: name_with_args += " "
        name_with_args += parts[param_idx] + ":" + args[param_idx]
    if num_args == 0:
        name_with_args = selector

    return name_with_args


def format_c_function_declaration(returntype, name, arg_types, arg_names):
    args = ""
    num_args = len(arg_types)
    for param_idx in range(0, num_args):
        args += "%s %s" % (arg_types[param_idx], arg_names[param_idx])
        if param_idx != num_args - 1: args += ", "

    return "%s %s(%s)" % (returntype, name, args)


def format_objc_function_declaration(static, returntype, selector, arg_types, arg_names):
    name_with_args = ""
    num_args = len(re.findall(":", selector))
    parts = selector.split(":")
    for param_idx in range(0, num_args):
        if param_idx != 0: name_with_args += " "
        name_with_args += parts[param_idx] + ":" + "(%s)%s" % (arg_types[param_idx], arg_names[param_idx])
    if num_args == 0:
        name_with_args = selector

    return "%s (%s)%s" % ("+" if static else "-", returntype, name_with_args)
