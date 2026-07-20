# Compilar con pdfLaTeX (esta plantilla NO usa xelatex/lualatex)
$pdf_mode = 1;

# Backend de bibliografia: bibtex (NO biber).
# La clase usa biblatex[backend=bibtex]; con esto latexmk corre bibtex.
$bibtex_use = 2;

# pdflatex con SyncTeX (click PDF <-> fuente) y errores legibles
$pdflatex = 'pdflatex -synctex=1 -interaction=nonstopmode -file-line-error %O %S';

# Archivos auxiliares a limpiar con: latexmk -c
$clean_ext = 'bbl run.xml synctex.gz';
