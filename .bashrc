#
# ~/.bashrc
#

HISTSIZE=10000
HISTFILESIZE=20000
# timestamp
HISTTIMEFORMAT="%F %T "

#export GOROOT=/usr/local/go
export GOPATH=$HOME/go
export PATH=$GOPATH/bin:$GOROOT/bin:$HOME/.local/bin:$PATH:

# Append to the history file, rather than overwriting it
shopt -s histappend

# Save history after every command
PROMPT_COMMAND="${PROMPT_COMMAND:+$PROMPT_COMMAND$'\n'}history -a; history -c; history -r"

# If not running interactively, don't do anything
[[ $- != *i* ]] && return

# Apply theme to new terminals (Pywal)
(cat ~/.cache/wal/sequences &)

alias ls='ls --color=auto'
alias grep='grep --color=auto'
PS1='[\u@\h \W]\$ '

eval "$(starship init bash)"

catnap