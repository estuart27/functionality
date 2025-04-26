from docling.document_converter import DocumentConverter

# Caminho para o seu arquivo PDF
source = "dados.pdf"

# Inicializa o conversor de documentos
converter = DocumentConverter()

# Converte o documento
result = converter.convert(source)

# Exporta o conteúdo para Markdown
print(result.document.export_to_markdown())
