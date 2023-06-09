from llvmlite import ir

variables = {}


class Integer():
    def __init__(self, builder, module, value):
        self.value = value
        self.builder = builder
        self.module = module

    def eval(self):
        if '.' not in self.value:
            i = ir.Constant(ir.IntType(32), int(self.value))
        else:
            i = ir.Constant(ir.DoubleType(), float(self.value))
        return i


class Id():
    def __init__(self, builder, module, id):
        self.id = id
        self.builder = builder
        self.module = module

    def eval(self):
        if self.id not in variables:
            raise NameError(f"Variables'{self.id}' is not defined")
        r = self.builder.load(variables[self.id])
        return r


class Float():
    def __init__(self, builder, module, value):
        self.value = value
        self.builder = builder
        self.module = module

    def eval(self):
        i = ir.Constant(ir.FloatType, float(self.value))
        return i


class BinaryOp():
    def __init__(self, builder, module, left, right):
        self.builder = builder
        self.module = module
        self.left = left
        self.right = right


class Div(BinaryOp):
    def eval(self):
        i = self.builder.sdiv(self.left.eval(), self.right.eval())
        return i


class Times(BinaryOp):
    def eval(self):
        i = self.builder.tim(self.left.eval(), self.right.eval())
        return i


class Plus(BinaryOp):
    def eval(self):
        i = self.builder.add(self.left.eval(), self.right.eval())
        return i


class Sub(BinaryOp):
    def eval(self):
        i = self.builder.sub(self.left.eval(), self.right.eval())
        return i


class LogicEqual(BinaryOp):
    def eval(self):
        i = self.builder.icmp_signed('==', self.left.eval(), self.right.eval())
        return i


class Less(BinaryOp):
    def eval(self):
        i = self.builder.icmp_signed('<', self.left.eval(), self.right.eval())
        return i


class More(BinaryOp):
    def eval(self):
        i = self.builder.icmp_signed('>', self.left.eval(), self.right.eval())
        return i


class PereASSIGN():
    def __init__(self, builder, module, id, value):
        self.builder = builder
        self.module = module
        self.id = id
        self.value = value

    def eval(self, builder=None):
        if builder == None:
            builder = self.builder

        if self.id not in variables:
            raise NameError(f"Variable '{self.id}' is not defined")

        if isinstance(self.value, str):
            builder.store(ir.Constant(ir.IntType(32), self.value), variables[self.id])


        else:
            value = self.value.eval(builder)
            builder.store(value, variables[self.id])


class Equal():
    def __init__(self, builder, module, id, value):
        self.builder = builder
        self.module = module
        self.id = id
        self.value = value

    def eval(self):
        print("EQUAL", type(self.value))
        print(self.id)
        print(self.value)

       # if isinstance(self.value, str):

        #    if "." not in self.value:
        i = self.builder.alloca(ir.IntType(32), name=self.id)
        variables[self.id] = i
        self.builder.store(ir.Constant(ir.IntType(32), self.value), i)

       #     elif "." in self.value:
         #       i = self.builder.alloca(ir.DoubleType(), name=self.id)
          #      variables[self.id] = i
           #     self.builder.store(ir.Constant(ir.DoubleType(), self.value), i)
            #else:
             #   i = self.builder.alloca(ir.IntType(32), name=self.id)
              #  variables[self.id] = i
               # value = self.value.eval()
                #self.builder.store(value, i)


class IfStatement:
    def __init__(self, builder, module, condition, if_body, else_body=None):
        self.builder = builder
        self.module = module
        self.condition = condition
        self.if_body = if_body
        self.else_body = else_body

    def eval(self):
        # вычисляем значение условного выражения
        condition_val = self.condition.eval()

        # создаем блоки базовых блоков для тела if и else
        if_bb = self.builder.append_basic_block("if")
        else_bb = self.builder.append_basic_block("else")
        merge_bb = self.builder.append_basic_block("merge")

        # создаем инструкцию условного перехода в блок if, если значение условия истинно,
        # и в блок else в противном случае
        self.builder.cbranch(condition_val, if_bb, else_bb)

        # выполняем тело if
        self.builder.position_at_start(if_bb)
        for statement in self.if_body:
            statement.eval()
        self.builder.branch(merge_bb)

        # выполняем тело else, если оно есть
        self.builder.position_at_start(else_bb)
        if self.else_body is not None:
            for statement in self.else_body:
                statement.eval()
        self.builder.branch(merge_bb)

        # переходим к блоку слияния
        self.builder.position_at_start(merge_bb)

        # self.builder.position_at_start(self.module.get_function("main").entry_basic_block)

class WhileStatement:
    def __init__(self, builder, module, condition, body):
        self.builder = builder
        self.module = module
        self.condition = condition
        self.body = body

    def eval(self, builder=None):
        if builder == None:
            builder = self.builder

        w_cond_head = builder.append_basic_block("w_cond_head")
        w_body_block = builder.append_basic_block("w_body")
        w_after_block = builder.append_basic_block("w_after")

        builder.branch(w_cond_head)
        builder.position_at_start(w_cond_head)

        condition_val = self.condition.eval(builder)
        builder.cbranch(condition_val, w_body_block, w_after_block)

        builder.position_at_start(w_body_block)

        for statement in self.body:
            statement.eval(builder)
        condition_val = self.condition.eval(builder)
        builder.cbranch(condition_val, w_body_block, w_after_block)
        # self.builder.branch(w_after_block)

        builder.position_at_start(w_after_block)

class Typecast():
    def __init__(self, builder, module, type, value):
        self.builder = builder
        self.module = module
        self.type = type
        self.value = value

    def eval(self, builder=None):
        if builder == None:
            builder = self.builder
        try:
            if self.type == "int":
                r = builder.load(variables[self.value])
                i = builder.fptosi(r, ir.IntType(32))
            elif self.type == "flo":
                r = builder.load(variables[self.value])
                i = builder.sitofp(r, ir.DoubleType())

            return i
        except:
            print("Error typecast")


class ReturnStatement():
    def __init__(self, builder, id):
        self.builder = builder
        self.id = id

    def eval(self, builder=None):
        if builder == None:
            builder = self.builder

        if self.id is not None:
            return_value = self.id.eval(builder)
            builder.ret(return_value)


class Print():
    def __init__(self, builder, module, printf, value, idfstr):
        self.value = value
        self.builder = builder
        self.module = module
        self.printf = printf
        self.idfstr = idfstr

    def eval(self):
        print(self.value)

        value = self.value.eval()
        print(value)

        # Объявление списка аргументов
        voidptr_ty = ir.IntType(8).as_pointer()
        fmt = "%i \n\0"
        c_fmt = ir.Constant(ir.ArrayType(ir.IntType(8), len(fmt)),
                            bytearray(fmt.encode("utf8")))
        namefstr = f"fstr{self.idfstr}"
        print(namefstr)
        global_fmt = ir.GlobalVariable(self.module, c_fmt.type, name=namefstr)
        global_fmt.linkage = 'internal'
        global_fmt.global_constant = True
        global_fmt.initializer = c_fmt
        fmt_arg = self.builder.bitcast(global_fmt, voidptr_ty)

        # Вызов ф-ии Print
        self.builder.call(self.printf, [fmt_arg, value])
