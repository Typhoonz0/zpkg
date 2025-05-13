#!/usr/bin/bash
if [[ "$SHELL" = "/usr/bin/bash" ]]; then
    echo "export PATH=$PATH:$(pwd)" >> ~/.bashrc
fi

if [[ "$SHELL" = "/usr/bin/zsh" ]]; then
    echo "export PATH=$PATH:$(pwd)" >> ~/.zshrc
fi

echo "Done. Open a new terminal."