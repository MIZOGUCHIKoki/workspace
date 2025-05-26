#!/usr/bin/env perl

$latex = 'pdflatex -synctex=1 -halt-on-error -file-line-error';
# $bibtex = 'biber --bblencoding=utf8 -u -U --output_safechars';
# $biber = 'biber --bblencoding=utf8 -u -U --output_safechars';
$bibtex = 'bibtex';
$pdf_mode = 3;

@generated_exts = ( 'aux', 'bcf', 'fls', 'idx', 'ind', 'lof', 'lot',
                'out', 'toc', 'dvi', 'snm', 'nav', 'bbl-SAVE-ERROR', 'log', 'run.xml');