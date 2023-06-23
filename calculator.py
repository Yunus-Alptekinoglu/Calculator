

class Node:


    def __init__(self, value):
        self.value = value  
        self.next = None 
    

    def __str__(self):
        return "Node({})".format(self.value) 


    __repr__ = __str__
                          

#=============================================== Part I ==============================================


class Stack:


    def __init__(self):
        self.top = None
    

    def __str__(self):
        temp=self.top
        out=[]
        while temp:
            out.append(str(temp.value))
            temp=temp.next
        out='\n'.join(out)
        return ('Top:{}\nStack:\n{}'.format(self.top,out))


    __repr__=__str__


    # Checks if the stack is empty by checking if the top of the stack exists
    def isEmpty(self):
        if self.top == None:
            return True
        return False


    # Calculates the length of the stack by looping through the stack and incrementing length by one until the stack ends
    def __len__(self): 
        length = 0
        current = self.top
        while current != None:
            length += 1
            current = current.next
        return length


    # Adds a node to the stack by setting the top node to be the new node and the previous top node to be the next node
    def push(self, value):
        if self.top == None:
            self.top = Node(value)
        else:
            newnode = Node(value)
            newnode.next = self.top
            self.top = newnode


    # Removes the top node of the stack by setting the top node to be the next node and returns its value
    def pop(self):
        if self.isEmpty():
            return None
        temp = self.top
        self.top = self.top.next
        temp.next = None
        return temp.value
        

    # Returns the value of the top node of the stack
    def peek(self):
        if self.isEmpty():
            return None
        return self.top.value


#=============================================== Part II ==============================================


class Calculator:


    def __init__(self):
        self.__expr = None


    @property
    def getExpr(self):
        return self.__expr


    def setExpr(self, new_expr):
        if isinstance(new_expr, str):
            self.__expr=new_expr
        else:
            print('setExpr error: Invalid expression')
            return None
    

    # Checks if given input is a number by using a try/except block to type cast it to a float
    def _isNumber(self, txt):
        try:
            float(txt)
            return True
        except:
            return False


    def _getPostfix(self, txt):
        

        if not self.__expr:
            return None
        postfixStack = Stack() # method must use postfixStack to compute the postfix expression
        postfix = []
        order = {'+' : 1, '-' : 1, '*' : 2, '/' : 2, '^' : 3}
        tokens = txt.split()
        for token in tokens:
            # If token is a number, append it to the output list
            if self._isNumber(token):
                postfix.append(float(token))
            # If token is a left parenthesis, push it onto the stack
            elif token == '(':
                postfixStack.push(token)
            # If token is a right parenthesis, pop the operators from the stack and append them to the output list until a left parenthesis is met. If a left paranthesis is not met, return None
            elif token == ')':
                while not postfixStack.isEmpty() and postfixStack.top() != '(':
                    postfix.append(postfixStack.pop())
                if postfixStack.isEmpty() or postfixStack.top() != '(':
                    return None
                postfixStack.pop()
            # If token is an operator, pop the operators from the stack and append them to the output list until a lower-order operator or a left parenthesis is met. Then, push the operator onto the stack
            elif token in order:
                while not postfixStack.isEmpty() and postfixStack.top() != '(' and postfix[token] <= postfix[postfixStack.top()]:
                    postfix.append(postfixStack.pop())
                postfixStack.push(token)
            # If token is not a number, left parenthesis, or operator, return None
            else:
                return None
        # Pop any remaining operators from the stack and append them to the output list
        while not postfixStack.isEmpty():
            if postfixStack.top() == '(':
                return None
            postfix.append(postfixStack.pop())
        return ' '.join(postfix)

        
    @property
    def calculate(self):
        if not isinstance(self.__expr,str) or len(self.__expr)<=0:
            print("Argument error in calculate")
            return None
        calcStack = Stack() # method must use calcStack to compute the expression
        postfix = self._getPostfix(self.getExpr)
        if postfix is None:
            return None
        for token in postfix:
            # If token is a number, push it onto the value stack
            if self._isNumber(token):
                calcStack.push(float(token))
            # If token is an operator, pop two values from the value stack, perform the appropriate operation, and push the result
            else:
                token1 = calcStack.pop()
                token2 = calcStack.pop()
                if token == '+':
                    result = token1 + token2
                elif token == '-':
                    result = token1 - token2
                elif token == '*':
                    result = token1 * token2
                elif token == '/':
                    result = token1 / token2
                elif token == '^':
                    result = token1 ** token2
                calcStack.push(float(result))
        return calcStack.pop()
        

#=============================================== Part III ==============================================


class AdvancedCalculator:


    def __init__(self):
        self.expressions = ''
        self.states = {}


    def setExpression(self, expression):
        self.expressions = expression
        self.states = {}


    def _isVariable(self, word):
        # Checks if word is a variable by checking if word is alpha-numeric and the first letter of word is alpha
        return word.isalnum() and word[0].isalpha()


    def _replaceVariables(self, expr):


        tokens = expr.split(' ')
        newtokens = []
        for token in tokens:
            # If token is a variable and in states, its value is appended to newtokens
            if self._isVariable(token):
                if token not in self.states:
                    return None
                newtokens.append(str(self.states[token]))
            else:
                newtokens.append(token)
        newexpr = ' '.join(newtokens)
        return newexpr
    

    def calculateExpressions(self):
        # Split expressions into individual expressions
        exprs = self.expressions.strip().split(';')
        for expr in exprs:
            # Split expression into tokens
            tokens = expr.strip().split()
            variable = tokens[0]
            operator = tokens[1]
            # Replace the variables in each expression with their values
            expr = self._replaceVariables(' '.join(tokens[2:]))
            calcObj = Calculator()
            value = calcObj.calculate(expr)
            # If the operator is "=", set variable as the key and value as the value in states. Otherwise, return None
            if operator == '=':
                self.states[variable] = value
            else:
                return None
        # Replace the variables in the last expression with their values
        expr = self._replaceVariables(exprs[-1].strip())
        value = calcObj.calculate(expr)
        return value
    
    