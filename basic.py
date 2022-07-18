from errors import (IllegalCharError)
from constant import (DIGITS, TT_INT, TT_FLOAT, TT_PLUS,TT_MINUS, TT_MUL, TT_DIV, TT_LPAREN, TT_RPAREN, TT_EOF)
from position import Position


class Token(object):
    # <token-name, attribute-value >
    def __init__(self, ttype: str, value=None, pos_start: Position = None, pos_end: Position = None):
        """
        :param ttype: 类型
        :param value:
        :param pos_start: Position类实例，当前起始位置
        :param pos_end: Position类实例，当前结束位置
        """
        self.ttype = ttype
        self.value = value
        if pos_start:
            # Token 单个字符, + => pos_start = pos_end, advance
            self.pos_start = pos_start.copy()
            self.pos_end = pos_start.copy()
            self.pos_end.advance(self.value)
        if pos_end:
            self.pos_end = pos_end.copy()

    def __repr__(self):
        if self.value:
            return f'{self.ttype}: {self.value}'
        return f'{self.ttype}'


class Lexer(object):
    def __init__(self, fn, text):
        self.fn = fn  # text source
        self.text = text
        self.pos = Position(-1, 0, -1, fn, text)
        self.current_char = None
        self.advance()

    def advance(self):
        self.pos.advance(self.current_char)
        if self.pos.idx < len(self.text):
            self.current_char = self.text[self.pos.idx]
        else:
            self.current_char = None

    def make_token(self):
        tokens = []

        """
        遍历text
        遍历过程中，分别判断获取的内容
        """
        while self.current_char is not None:
            if self.current_char in (' ', '\t'):
                # 空格，制表符，调过
                self.advance()
            elif self.current_char in DIGITS:
                tokens.append(self.make_number())
            elif self.current_char == '+':
                tokens.append(Token(TT_PLUS, pos_start=self.pos))
                self.advance()
            elif self.current_char == '-':
                tokens.append(Token(TT_MINUS, pos_start=self.pos))
                self.advance()
            elif self.current_char == '*':
                tokens.append(Token(TT_MUL, pos_start=self.pos))
                self.advance()
            elif self.current_char == '/':
                tokens.append(Token(TT_DIV, pos_start=self.pos))
                self.advance()
            elif self.current_char == '(':
                tokens.append(Token(TT_LPAREN, pos_start=self.pos))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(TT_RPAREN, pos_start=self.pos))
                self.advance()
            else:
                # 没有匹配到: 非法字符错误
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                return [], IllegalCharError(pos_start, self.pos, f"'{char};'")
        tokens.append(Token(TT_EOF, pos_start=self.pos))
        return tokens, None

    def make_number(self):
        """
        整数, 小数 => 0.1
        """
        num_str = ''
        dot_count = 0
        while self.current_char is not None and self.current_char in DIGITS + '.':
            if self.current_char == '.':
                if dot_count == 1:
                    break
                dot_count += 1
                num_str += '.'
            else:
                num_str += self.current_char
            self.advance()
        if dot_count == 0:
            return Token(TT_INT, int(num_str))
        else:
            return Token(TT_FLOAT, float(num_str))
