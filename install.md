# Important
these install notes are for my personal use, just so i can remember how to
setup latex on my computer so i can run this script. Your latex resume might
be different.

# Install tex setup
brew cask install basictex
brew cask install texliveonfly
sudo tlmgr update --self
echo export PATH="/usr/local/texlive/2020basic/bin/x86_64-darwin:$PATH"
tlmgr update --self
sudo tlmgr install texliveonfly
sudo texliveonfly -c xelatex template.tex                                                                                                                                                                                         ~

# This seems to be the packages my resume needs
nopageno
datetime
fmtcount
enumitem