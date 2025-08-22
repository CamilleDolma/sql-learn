import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QTextEdit, QPushButton, QStackedWidget
)
from PyQt6.QtGui import QFont, QSyntaxHighlighter, QTextCharFormat, QColor
from PyQt6.QtCore import QRegularExpression
import markdown_it
from pygments import highlight
from pygments.lexers import get_lexer_by_name, guess_lexer
from pygments.formatters import HtmlFormatter

class MarkdownHighlighter(QSyntaxHighlighter):
    def __init__(self, parent):
        super().__init__(parent)
        self.highlighting_rules = []

        # Headers
        header_format = QTextCharFormat()
        header_format.setForeground(QColor("#98C379"))
        header_format.setFontWeight(QFont.Weight.Bold)
        self.highlighting_rules.append((QRegularExpression("^#{1,6} .*"), header_format))

        # Bold
        bold_format = QTextCharFormat()
        bold_format.setFontWeight(QFont.Weight.Bold)
        self.highlighting_rules.append((QRegularExpression("\\*\\*.*?\\*\\*"), bold_format))
        self.highlighting_rules.append((QRegularExpression("__.*?__"), bold_format))

        # Italic
        italic_format = QTextCharFormat()
        italic_format.setFontItalic(True)
        self.highlighting_rules.append((QRegularExpression("\\*.*?\\*"), italic_format))
        self.highlighting_rules.append((QRegularExpression("_.*?_"), italic_format))

        # Strikethrough
        strike_format = QTextCharFormat()
        strike_format.setFontStrikeOut(True)
        self.highlighting_rules.append((QRegularExpression("~~.*?~~"), strike_format))

        # Inline code
        inline_code_format = QTextCharFormat()
        inline_code_format.setBackground(QColor("#2C313A"))
        inline_code_format.setForeground(QColor("#ABB2BF"))
        self.highlighting_rules.append((QRegularExpression("`.*?`"), inline_code_format))

        # Code blocks
        self.code_block_format = QTextCharFormat()
        self.code_block_format.setBackground(QColor("#282c34"))
        self.code_block_format.setForeground(QColor("#abb2bf"))
        self.code_block_start_expression = QRegularExpression("^```.*")
        self.code_block_end_expression = QRegularExpression("^```")


    def highlightBlock(self, text):
        for pattern, format in self.highlighting_rules:
            expression = QRegularExpression(pattern)
            it = expression.globalMatch(text)
            while it.hasNext():
                match = it.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), format)

        self.setCurrentBlockState(0)

        self.match_multiline(text, self.code_block_start_expression, self.code_block_end_expression, self.code_block_format)


    def match_multiline(self, text, start_expression, end_expression, format):
        start_match = start_expression.match(text)

        if self.previousBlockState() == 1:
            end_match = end_expression.match(text)
            if not end_match.hasMatch() or end_match.capturedStart() != 0:
                self.setCurrentBlockState(1)
                self.setFormat(0, len(text), format)
                return True
            else:
                 self.setFormat(0, len(text), format)

        if start_match.hasMatch() and start_match.capturedStart() == 0:
            end_match = end_expression.match(text, start_match.capturedLength())
            if not end_match.hasMatch():
                self.setCurrentBlockState(1)
                self.setFormat(0, len(text), format)
                return True
            else:
                self.setFormat(0, len(text), format)

        return False


class LLMWriter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LLM Writer")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # API Key
        api_key_layout = QHBoxLayout()
        api_key_label = QLabel("LLM API Key:")
        self.api_key_input = QLineEdit()
        self.api_key_input.setPlaceholderText("Enter your API key here")
        api_key_layout.addWidget(api_key_label)
        api_key_layout.addWidget(self.api_key_input)
        self.layout.addLayout(api_key_layout)

        # System Prompt
        system_prompt_label = QLabel("System Prompt:")
        self.system_prompt_edit = QTextEdit()
        self.system_prompt_edit.setFont(QFont("Consolas", 12))
        self.system_highlighter = MarkdownHighlighter(self.system_prompt_edit.document())
        self.layout.addWidget(system_prompt_label)
        self.layout.addWidget(self.system_prompt_edit)

        # User Prompt
        user_prompt_label = QLabel("User Prompt:")
        self.user_prompt_edit = QTextEdit()
        self.user_prompt_edit.setFont(QFont("Consolas", 12))
        self.user_highlighter = MarkdownHighlighter(self.user_prompt_edit.document())
        self.layout.addWidget(user_prompt_label)
        self.layout.addWidget(self.user_prompt_edit)

        # Generate Button
        self.generate_button = QPushButton("Generate")
        self.generate_button.clicked.connect(self.generate_output)
        self.layout.addWidget(self.generate_button)

        # Output Area
        output_layout = QVBoxLayout()
        output_controls_layout = QHBoxLayout()
        self.output_label = QLabel("Output:")
        self.switch_view_button = QPushButton("Switch to Rendered View")
        self.switch_view_button.clicked.connect(self.switch_output_view)
        output_controls_layout.addWidget(self.output_label)
        output_controls_layout.addStretch()
        output_controls_layout.addWidget(self.switch_view_button)
        output_layout.addLayout(output_controls_layout)

        self.output_stack = QStackedWidget()
        self.output_source_edit = QTextEdit()
        self.output_source_edit.setFont(QFont("Consolas", 12))
        self.output_source_edit.setReadOnly(True)
        self.output_highlighter = MarkdownHighlighter(self.output_source_edit.document())

        try:
            from PyQt6.QtWebEngineWidgets import QWebEngineView
            self.output_rendered_view = QWebEngineView()
            self.output_stack.addWidget(self.output_source_edit)
            self.output_stack.addWidget(self.output_rendered_view)
        except ImportError:
            print("PyQt6-WebEngine not installed. Rendered view will not be available.")
            print("Please install it with: pip install PyQt6-WebEngine")
            self.output_rendered_view = None
            self.switch_view_button.setEnabled(False)
            self.output_stack.addWidget(self.output_source_edit)


        output_layout.addWidget(self.output_stack)
        self.layout.addLayout(output_layout)

        self.md = markdown_it.MarkdownIt(
            "gfm-like",
            {"highlight": self.highlight_code}
        )


    def highlight_code(self, code, name, attrs):
        try:
            lexer = get_lexer_by_name(name)
        except:
            lexer = guess_lexer(code)
        formatter = HtmlFormatter()
        return highlight(code, lexer, formatter)

    def switch_output_view(self):
        current_index = self.output_stack.currentIndex()
        if current_index == 0:
            self.output_stack.setCurrentIndex(1)
            self.switch_view_button.setText("Switch to Source View")
            self.render_markdown()
        else:
            self.output_stack.setCurrentIndex(0)
            self.switch_view_button.setText("Switch to Rendered View")

    def render_markdown(self):
        if self.output_rendered_view:
            markdown_text = self.output_source_edit.toPlainText()
            html = self.md.render(markdown_text)
            formatter = HtmlFormatter()
            html = f"<style>{formatter.get_style_defs()}</style>{html}"
            self.output_rendered_view.setHtml(html)

    def generate_output(self):
        user_prompt = self.user_prompt_edit.toPlainText()
        system_prompt = self.system_prompt_edit.toPlainText()

        generated_text = f"""
# This is a header


This is some generated text based on your prompt.

**System Prompt:**

```
{system_prompt}
```

**User Prompt:**
```
{user_prompt}
```

Here is some python code:
```python
def hello_world():
    print("Hello, World!")
```
"""
        self.output_source_edit.setPlainText(generated_text)
        if self.output_stack.currentIndex() == 1:
            self.render_markdown()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    writer = LLMWriter()
    writer.show()
    sys.exit(app.exec())
    