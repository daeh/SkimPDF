# SkimPDF

[Skim](https://skim-app.sourceforge.io/) is a PDF viewer with great search and annotation tools for OSX. It stores annotations in a non-standard format, thus the annotation can not viewed or edited in other PDF viewer like Adobe Acrobat Reader. However, Skim can convert Skim notes to standard PDF notes (embed) or make PDF notes editable in Skim (unembed).

![](img/example-skim.png)
PDF viewed in Skim with Skim annotations.

![](img/example-acrobat.png)
The same PDF with embedded annotations viewed in Adobe Acrobat Reader DC.

## How it works

The Python class `SkimPDF` builds on `skimpdf` to automate the conversion step:

1. Embed notes
2. Unembed notes
3. Batch embed and unembed notes (works with nested folders)

I have used the script to embed Skim notes of 568 pdfs scattered in a folder with various subfolders. It took about 5 minutes. Be aware, that the script won't process files with a `"` in its filepath and that the files are overwritten, so make a copy before running on large sets of files.

## How to install and use it

### Python module

Download the module from `skim_pdf.py`

#### Available options

```python
# Path to skimpdf
skim = SkimPDF(skimpdf_path='/Applications/Skim.app/Contents/SharedSupport/skimpdf')

# Replace pdf or place a copy in place
skim.replace_original = True

# If skim.replace_original is set to False,
# then you can set the embed or unembed suffix
skim.embed_suffix = '_embedded'
skim.unembed_suffix = '_skim_notes'
```

#### Available methods

```python
# Convert Skim notes to PDF notes (embed)
skim.convert_to_pdf_notes('~/Desktop/pdf file.pdf')

# Convert PDF notes to Skim notes (unembed)
skim.convert_to_skim_notes('~/Desktop/pdf file.pdf')

# Batch convert notes in a folder
skim.batch_convert_to_pdf_notes('~/Documents/Zotero')
skim.batch_convert_to_skim_notes('~/Documents/Zotero')

# Export a report to the Desktop
skim.report('~/Desktop')
```
