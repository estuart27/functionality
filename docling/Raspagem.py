from docling.document_converter import DocumentConverter

source = 'https://silvestrecode.shop/'

converter = DocumentConverter()
result = converter.convert(source)

print(result.document.export_to_markdown())

