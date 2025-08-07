"""Formatter for converting essays to different output formats."""

from datetime import datetime
from typing import List

from ..models import Essay, OutputFormat, Citation


class Formatter:
    """Formats essays into different output formats."""
    
    def format(self, essay: Essay, format_type: OutputFormat) -> str:
        """Format an essay according to the specified output format."""
        if format_type == OutputFormat.MARKDOWN:
            return self._format_markdown(essay)
        elif format_type == OutputFormat.LATEX:
            return self._format_latex(essay)
        elif format_type == OutputFormat.HTML:
            return self._format_html(essay)
        else:
            raise ValueError(f"Unsupported format: {format_type}")
    
    def _format_markdown(self, essay: Essay) -> str:
        """Format essay as Markdown."""
        output = essay.content
        
        # Add metadata footer
        output += "\n\n---\n\n"
        output += self._format_metadata_markdown(essay)
        
        return output
    
    def _format_latex(self, essay: Essay) -> str:
        """Format essay as LaTeX."""
        output = r"\documentclass[12pt]{article}" + "\n"
        output += r"\usepackage[utf8]{inputenc}" + "\n"
        output += r"\usepackage{hyperref}" + "\n"
        output += r"\usepackage{cite}" + "\n\n"
        
        output += r"\title{" + self._escape_latex(essay.title) + "}\n"
        output += r"\author{EssayForge AI}" + "\n"
        output += r"\date{" + essay.generated_at.strftime("%B %d, %Y") + "}\n\n"
        
        output += r"\begin{document}" + "\n\n"
        output += r"\maketitle" + "\n\n"
        
        # Convert markdown content to LaTeX
        latex_content = self._markdown_to_latex(essay.content)
        output += latex_content
        
        output += "\n" + r"\end{document}"
        
        return output
    
    def _format_html(self, essay: Essay) -> str:
        """Format essay as HTML."""
        output = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }}
        h1, h2, h3 {{ color: #2c3e50; }}
        h1 {{ border-bottom: 2px solid #3498db; padding-bottom: 10px; }}
        h2 {{ margin-top: 30px; }}
        blockquote {{
            border-left: 4px solid #3498db;
            padding-left: 20px;
            margin-left: 0;
            color: #555;
        }}
        code {{
            background-color: #f4f4f4;
            padding: 2px 4px;
            border-radius: 3px;
        }}
        .metadata {{
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            margin-top: 40px;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
""".format(title=essay.title)
        
        # Convert markdown to HTML (simplified)
        html_content = self._markdown_to_html(essay.content)
        output += html_content
        
        # Add metadata
        output += '<div class="metadata">'
        output += self._format_metadata_html(essay)
        output += '</div>'
        
        output += "\n</body>\n</html>"
        
        return output
    
    def _escape_latex(self, text: str) -> str:
        """Escape special LaTeX characters."""
        replacements = {
            '&': r'\&',
            '%': r'\%',
            '$': r'\$',
            '#': r'\#',
            '_': r'\_',
            '{': r'\{',
            '}': r'\}',
            '~': r'\textasciitilde{}',
            '^': r'\^{}',
            '\\': r'\textbackslash{}',
        }
        for old, new in replacements.items():
            text = text.replace(old, new)
        return text
    
    def _markdown_to_latex(self, content: str) -> str:
        """Convert Markdown to LaTeX (simplified)."""
        lines = content.split('\n')
        latex_lines = []
        
        for line in lines:
            if line.startswith('# '):
                latex_lines.append(r'\section{' + self._escape_latex(line[2:]) + '}')
            elif line.startswith('## '):
                latex_lines.append(r'\subsection{' + self._escape_latex(line[3:]) + '}')
            elif line.startswith('### '):
                latex_lines.append(r'\subsubsection{' + self._escape_latex(line[4:]) + '}')
            elif line.strip() == '':
                latex_lines.append('')
            else:
                latex_lines.append(self._escape_latex(line))
        
        return '\n'.join(latex_lines)
    
    def _markdown_to_html(self, content: str) -> str:
        """Convert Markdown to HTML (simplified)."""
        lines = content.split('\n')
        html_lines = []
        in_paragraph = False
        
        for line in lines:
            if line.startswith('# '):
                if in_paragraph:
                    html_lines.append('</p>')
                    in_paragraph = False
                html_lines.append(f'<h1>{line[2:]}</h1>')
            elif line.startswith('## '):
                if in_paragraph:
                    html_lines.append('</p>')
                    in_paragraph = False
                html_lines.append(f'<h2>{line[3:]}</h2>')
            elif line.startswith('### '):
                if in_paragraph:
                    html_lines.append('</p>')
                    in_paragraph = False
                html_lines.append(f'<h3>{line[4:]}</h3>')
            elif line.strip() == '':
                if in_paragraph:
                    html_lines.append('</p>')
                    in_paragraph = False
            else:
                if not in_paragraph:
                    html_lines.append('<p>')
                    in_paragraph = True
                html_lines.append(line)
        
        if in_paragraph:
            html_lines.append('</p>')
        
        return '\n'.join(html_lines)
    
    def _format_metadata_markdown(self, essay: Essay) -> str:
        """Format metadata for Markdown output."""
        meta = essay.metadata
        output = f"**Generated:** {essay.generated_at.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        output += f"**Topic:** {meta.topic}\n\n"
        output += f"**Word Count:** {essay.word_count:,}\n\n"
        output += f"**Research Depth:** {meta.agents_used} agents\n\n"
        
        if meta.quality_metrics:
            output += "**Quality Metrics:**\n"
            output += f"- Overall Score: {meta.quality_metrics.overall_score:.2f}\n"
            output += f"- Coherence: {meta.quality_metrics.coherence:.2f}\n"
            output += f"- Depth: {meta.quality_metrics.depth_score:.2f}\n"
            output += f"- Originality: {meta.quality_metrics.originality:.2f}\n"
        
        return output
    
    def _format_metadata_html(self, essay: Essay) -> str:
        """Format metadata for HTML output."""
        meta = essay.metadata
        output = f"<p><strong>Generated:</strong> {essay.generated_at.strftime('%Y-%m-%d %H:%M:%S')}</p>"
        output += f"<p><strong>Topic:</strong> {meta.topic}</p>"
        output += f"<p><strong>Word Count:</strong> {essay.word_count:,}</p>"
        output += f"<p><strong>Research Depth:</strong> {meta.agents_used} agents</p>"
        
        if meta.quality_metrics:
            output += "<p><strong>Quality Metrics:</strong></p><ul>"
            output += f"<li>Overall Score: {meta.quality_metrics.overall_score:.2f}</li>"
            output += f"<li>Coherence: {meta.quality_metrics.coherence:.2f}</li>"
            output += f"<li>Depth: {meta.quality_metrics.depth_score:.2f}</li>"
            output += f"<li>Originality: {meta.quality_metrics.originality:.2f}</li>"
            output += "</ul>"
        
        return output