# -*- coding: utf-8 -*-
"""
Embed Skim notes as PDF notes or convert PDF notes to Skim notes.
Date: 2022-01-27
Version: 1.2
Author: Dae Houlihan, based on original script by Alexander Gogl
"""

from pathlib import Path
import subprocess
import pandas as pd


class SkimPDF(object):
    """docstring for SkimPDF."""

    def __init__(self, skimpdf_path=None):
        if skimpdf_path is None:
            skimpdf_path_ = Path("/Applications/Skim.app/Contents/SharedSupport/skimpdf")
        else:
            skimpdf_path_ = Path(skimpdf_path)
        assert skimpdf_path_.is_file(), "SkimPDF not found"
        self.skimpdf_path = str(skimpdf_path_)
        self.skimnotes_path = str(skimpdf_path_.parent / 'skimnotes')
        self.embed_suffix = '_embedded'
        self.unembed_suffix = '_skim_notes'
        self.replace_original = True
        # self.processed = list()
        # self.bypassed = list()
        # self.warnings = list()
        # self.errors = list()
        self.results = list()

    def test_for_markup(self, in_pdf):
        """Test if PDF has Skim notes."""

        has_notes = False

        if in_pdf.is_file() and not in_pdf.is_symlink():
            cmd = [self.skimnotes_path, "test", f'{in_pdf}']
            result = subprocess.run(cmd)

            has_notes = result.returncode == 0

        return has_notes

    def convert_to_pdf_notes(self, in_pdf):
        """Embed skim notes to PDF notes."""
        if self.replace_original is False:
            out_pdf = (in_pdf.parent / f"{in_pdf.with_suffix('').name}{self.embed_suffix}").with_suffix('.pdf')
        else:
            out_pdf = in_pdf

        has_notes = self.test_for_markup(in_pdf)

        result = dict(
            path=str(in_pdf),
            action=None,
            errmsg=None,
            summary=None,
        )

        if has_notes:

            # Embed notes
            cmd = [self.skimpdf_path, 'embed', f'{in_pdf}', f'{out_pdf}']
            cmdres = subprocess.run(cmd, capture_output=True)

            success = cmdres.returncode == 0
            errmsg = cmdres.stderr.decode()

            # Compose message
            if success:
                if errmsg:
                    result['action'] = f"embed"
                    result['errmsg'] = errmsg
                    result['summary'] = f"warning"
                else:
                    result['action'] = f"embed"
                    result['errmsg'] = errmsg
                    result['summary'] = f"success"
            else:
                result['action'] = f"fail"
                result['errmsg'] = errmsg
                result['summary'] = f"fail"
        else:
            result['action'] = f"bypass"
            result['errmsg'] = f""
            result['summary'] = f"bypass"

        self.results.append(result)

    def convert_to_skim_notes(self, in_pdf):
        """Convert PDF notes to Skim notes (unembed)."""
        if self.replace_original is False:
            out_pdf = "%s%s.pdf" % (in_pdf[:-4], self.skim_suffix)
        else:
            out_pdf = in_pdf

        result = dict(
            path=str(in_pdf),
            action=None,
            errmsg=None,
            summary=None,
        )

        # Convert PDF notes to Skim notes
        cmd = [self.skimpdf_path, 'unembed', f'{in_pdf}', f'{out_pdf}']
        cmdres = subprocess.run(cmd, capture_output=True)

        success = cmdres.returncode == 0
        errmsg = cmdres.stderr.decode()

        # Compose message
        if success:
            if errmsg:
                result['action'] = f"embed"
                result['errmsg'] = errmsg
                result['summary'] = f"warning"
            else:
                result['action'] = f"embed"
                result['errmsg'] = errmsg
                result['summary'] = f"success"
        else:
            result['action'] = f"fail"
            result['errmsg'] = errmsg
            result['summary'] = f"fail"

        self.results.append(result)

    def batch_convert_to_pdf_notes(self, folder):
        """Loop through directories in given folder and embed notes."""
        base_dir = Path(folder)
        assert base_dir.is_dir(), "Folder not found"
        pdf_files = list(base_dir.rglob("*.pdf"))
        print(f"Processing {len(pdf_files)} pdf files")
        for i_file, pdf_file in enumerate(pdf_files):
            skim.convert_to_pdf_notes(pdf_file)
        print("\n\nProcessing PDFs done")

    def batch_convert_to_skim_notes(self, folder):
        """Loop through directories in given folder and embed notes."""
        base_dir = Path(folder)
        assert base_dir.is_dir(), "Folder not found"
        pdf_files = list(base_dir.rglob("*.pdf"))
        print(f"Processing {len(pdf_files)} pdf files")
        for i_file, pdf_file in enumerate(pdf_files):
            skim.convert_to_skim_notes(pdf_file)
        print("\n\nProcessing PDFs done")

    def report(self, save_path=None):
        """Print list of processed pdfs."""

        resultsdf = pd.DataFrame(self.results).sort_values(by=['summary'])

        if save_path is None:
            print(resultsdf)
        else:
            save_path_base = Path(save_path).expanduser()
            assert save_path_base.is_dir(), "Folder not found"
            message_dump_path = save_path_base / "skim_pdf_report.csv"
            if message_dump_path.is_file():
                message_dump_path.unlink()

            resultsdf.to_csv(message_dump_path, index=False)


# Initalize with path to skimpdf executable
skim = SkimPDF(skimpdf_path='/Applications/Skim.app/Contents/SharedSupport/skimpdf')

# Replace pdf or place a copy in place
skim.replace_original = True

# Convert Skim notes to PDF notes (embed)
skim.convert_to_pdf_notes('~/Desktop/pdf file.pdf')

# Convert PDF notes to Skim notes (unembed)
skim.convert_to_skim_notes('~/Desktop/to/pdf file.pdf')

# Batch convert notes in a folder
skim.batch_convert_to_pdf_notes('~/Documents/Zotero')

# Export a report to the Desktop
skim.report('~/Desktop')
