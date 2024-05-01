import re
from typing import List
from graphviz import Digraph


class TokenType:
    TEXT = 'TEXT'
    HASH = 'HASH'
    UNDERSCORE = 'UNDERSCORE'
    STAR = 'STAR'
    NEWLINE = 'NEWLINE'
    DASH = 'DASH'
    BRACKET_OPEN = 'BRACKET_OPEN'
    BRACKET_CLOSE = 'BRACKET_CLOSE'
    PAREN_OPEN = 'PAREN_OPEN'
    PAREN_CLOSE = 'PAREN_CLOSE'
    LINK = 'LINK'
    IMAGE = 'IMAGE'
    WHITESPACE = 'WHITESPACE'
    OTHER = 'OTHER'


PATTERN_RULES = [
    (TokenType.LINK, re.compile(r'\[([^\]]+)\]\(([^\)]+)\)')),
    (TokenType.IMAGE, re.compile(r'!\[([^\]]+)\]\(([^\)]+)\)')),
    (TokenType.HASH, re.compile(r'^#+')),
    (TokenType.UNDERSCORE, re.compile(r'^_+')),
    (TokenType.STAR, re.compile(r'^\*+')),
    (TokenType.NEWLINE, re.compile(r'^\n')),
    (TokenType.DASH, re.compile(r'^-+')),
    (TokenType.BRACKET_OPEN, re.compile(r'^\[+')),
    (TokenType.BRACKET_CLOSE, re.compile(r'^\]+')),
    (TokenType.PAREN_OPEN, re.compile(r'^\(+')),
    (TokenType.PAREN_CLOSE, re.compile(r'^\)+')),
    (TokenType.WHITESPACE, re.compile(r'^\s+')),
    (TokenType.TEXT, re.compile(r'^[^\s\[\]#!\*_\(\)-]+')),
]


class Lexeme:
    def __init__(self, token_type, content, offset):
        self.token_type = token_type
        self.content = content
        self.offset = offset

    def __str__(self):
        return f"{self.token_type} {self.content if len(self.content) > 1 else str()}"


def tokenize(text):
    lexemes = []
    cursor = 0
    ignored_types = {TokenType.WHITESPACE}
    while cursor < len(text):
        found = None
        for token_type, pattern in PATTERN_RULES:
            found = pattern.match(text[cursor:])
            if found:
                content = found.group(0)
                if token_type in [TokenType.LINK, TokenType.IMAGE]:
                    content = found.groups()
                if token_type not in ignored_types:
                    if lexemes and lexemes[-1].token_type == TokenType.TEXT and token_type == TokenType.TEXT:
                        lexemes[-1].content += ' ' + content
                    else:
                        lexemes.append(Lexeme(token_type, content, cursor))
                cursor += len(found.group(0))
                break
        if not found:
            lexemes.append(Lexeme(TokenType.OTHER, text[cursor], cursor))
            print("Can't match token to any pattern")
            cursor += 1
    return lexemes


class ElementKind:
    ROOT = 'ROOT'
    PARAGRAPH = 'PARAGRAPH'
    HEADING = 'HEADING'
    BOLD = 'BOLD'
    ITALIC = 'ITALIC'
    IMAGE = 'IMAGE'
    LINK = 'LINK'
    TEXT = 'TEXT'


class Element:
    def __init__(self, element_kind, element_value, input_lexemes: List[Lexeme], progeny=None):
        if progeny is None:
            progeny = []
        self.element_kind = element_kind
        self.element_value = element_value
        self.progeny = progeny
        self.lexemes = input_lexemes

        if element_kind == ElementKind.ROOT:
            self.__parse_paragraphs__()
        else:
            self.__parse_content__()

    def __parse_paragraphs__(self):
        content_blocks = []
        for lexeme in self.lexemes:
            if lexeme.token_type == TokenType.NEWLINE and len(content_blocks) > 0:
                if content_blocks[0].token_type == TokenType.HASH:
                    element_value = len(content_blocks[0].content)
                    content_blocks.pop(0)
                    self.progeny.append(Element(ElementKind.HEADING, element_value, content_blocks))
                else:
                    self.progeny.append(Element(ElementKind.PARAGRAPH, None, content_blocks))
                content_blocks = []

            if lexeme.token_type != TokenType.NEWLINE:
                content_blocks.append(lexeme)

    def __parse_content__(self):
        emphasis_tokens = []
        emphasis_level = 0
        for lexeme in self.lexemes:
            if lexeme.token_type == TokenType.STAR and emphasis_level == 0:
                emphasis_level = len(lexeme.content)
                continue

            if emphasis_level != 0 and not (lexeme.token_type == TokenType.STAR and len(lexeme.content) == emphasis_level):
                emphasis_tokens.append(lexeme)

            if emphasis_level == 0:
                if lexeme.token_type == TokenType.TEXT:
                    self.progeny.append(Element(ElementKind.TEXT, lexeme.content, []))
                elif lexeme.token_type == TokenType.LINK:
                    link_text_tokens = tokenize(lexeme.content[0])
                    self.progeny.append(Element(ElementKind.LINK, lexeme.content[1], link_text_tokens))
                elif lexeme.token_type == TokenType.IMAGE:
                    image_alt_tokens = tokenize(lexeme.content[0])
                    self.progeny.append(Element(ElementKind.IMAGE, lexeme.content[1], image_alt_tokens))

            if lexeme.token_type == TokenType.STAR and len(lexeme.content) == emphasis_level:
                if emphasis_level == 1:
                    self.progeny.append(Element(ElementKind.ITALIC, None, emphasis_tokens))
                elif emphasis_level == 2:
                    self.progeny.append(Element(ElementKind.BOLD, None, emphasis_tokens))
                elif emphasis_level == 3:
                    new_element = Element(ElementKind.ITALIC, None, emphasis_tokens)
                    self.progeny.append(Element(ElementKind.BOLD, None, [], progeny=[new_element]))
                else:
                    raise SyntaxError("Incorrect number of stars")
                emphasis_tokens = []
                emphasis_level = 0

    def __str__(self, depth=0):
        output = "  " * depth + f"{self.element_kind} {self.element_value if self.element_value else ''}\n"
        for child in self.progeny:
            output += child.__str__(depth + 1)
        return output

    def render_graph(self, digraph=None, parent_id=None):
        if digraph is None:
            digraph = Digraph(node_attr={'shape': 'rectangle', 'fontname': 'Arial'})

        element_label = f"{self.element_kind}: {self.element_value if self.element_value else ''}"
        element_id = str(id(self))
        digraph.node(element_id, label=element_label)

        if parent_id:
            digraph.edge(parent_id, element_id)

        for child in self.progeny:
            child.render_graph(digraph, element_id)

        return digraph


example_text = """
## Updated Title
Sample plain text
*stylized text* **emphasized text** ***both styles***
**primarily emphasized but also *stylized* **
[a sample link](http://example.org) and ![a sample image](http://example.org/pic.jpg)
**[a different link](http://example.org) additional text**.
[a **highlighted** link](https://youtu.be/example)
"""


parsed_tokens = tokenize(example_text)
print("Lexer output:\n")
for token in parsed_tokens:
    print(token)


print("\n===========================\nAbstract Syntax Tree:\n")
ast_root = Element(ElementKind.ROOT, None, parsed_tokens)
print(ast_root)

visual_graph = ast_root.render_graph()
visual_graph.render('modified_output', view=True)
