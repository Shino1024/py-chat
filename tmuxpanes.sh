#!/bin/bash

HOST=$1
PORT=$2
USER=$3

if [ "$#" -ne 3 ]; then
	echo -e "Illegal number of arguments. Usage:\n\t$0 host port name"
	return 1
fi

if [[ $PORT =~ ^([1-9][0-9]{3}|[1-6][0-9]{4})$ ]]; then
	if [ "$PORT" -lt 1024 ] || [ "$PORT" -gt 65536 ]; then
		echo "The port should be between 1024 and 65536."
		return 2
	fi
else
	echo "The port should be a number between 1024 and 65536."
	return 2
fi

if [[ ! $USER =~ ^[A-Za-z0-9]{1,16}$ ]]; then
	echo "The username should consist of alphabet characters or numbers, between 1 and 16 characters."
	return 3
fi

> TMUX_RESULT_TTY
> DATA_CHATTER
SHOST >> DATA_CHATTER
$PORT >> DATA_CHATTER
$USER >> DATA_CHATTER

clear

export BLANK_WIDTH=$(expr $(expr $(tput cols) - 40) / 2)
export BLANK_HEIGHT=$(expr $(expr $(tput lines) - 10) / 2)

printf "%0.s\n" $(seq 1 $BLANK_HEIGHT)

printf "%0.s " $(seq 1 $BLANK_WIDTH)
printf "       ____                             \n"
printf "%0.s " $(seq 1 $BLANK_WIDTH)
printf "      / __ \_________  ____  ____  ____ \n"
printf "%0.s " $(seq 1 $BLANK_WIDTH)
printf "     / / / / ___/ __ \\/ __ \\/ __ \/ __ \\ \n"
printf "%0.s " $(seq 1 $BLANK_WIDTH)
printf "    / /_/ / /  / /_/ / /_/ / /_/ / / / /\n"
printf "%0.s " $(seq 1 $BLANK_WIDTH)
printf "   /_____/_/   \__,_/\__, /\____/_/ /_/ \n"
printf "%0.s " $(seq 1 $BLANK_WIDTH)
printf "   ________         /____/_             \n"
printf "%0.s " $(seq 1 $BLANK_WIDTH)
printf "  / ____/ /_  ____  / /_/ /____  _____  \n"
printf "%0.s " $(seq 1 $BLANK_WIDTH)
printf " / /   / __ \/ __ \\/ __/ __/ _ \\/ ___/  \n"
printf "%0.s " $(seq 1 $BLANK_WIDTH)
printf "/ /___/ / / / /_/ / /_/ /_/  __/ /      \n"
printf "%0.s " $(seq 1 $BLANK_WIDTH)
printf "\\____/_/ /_/\\__,_/\\__/\\__/\\___/_/       \n"

sleep 2

tmux new-session -d -s pychat
tmux bind-key -n C-Right resize-pane -R 1
tmux bind-key -n C-Left resize-pane -L 1
tmux bind-key -n C-Up resize-pane -U 1
tmux bind-key -n C-Down resize-pane -D 1

tmux split-window -h -p 30
tmux select-pane -t 1
tmux split-window -v -p 40

tmux send-keys -t 0 "tty >> TMUX_RESULT_TTY" Enter
tmux send-keys -t 1 "tty >> TMUX_RESULT_TTY" Enter
tmux send-keys -t 2 "clear" Enter
tmux send-keys -t 0 "clear" Enter
tmux send-keys -t 0 "exec &>/dev/null" Enter
tmux send-keys -t 1 "clear" Enter
tmux send-keys -t 1 "exec &>/dev/null" Enter
tmux send-keys -t 1 "clear" Enter
tmux send-keys -t 2 "python client.py" Enter
tmux select-pane -t 2

TTY_CHAT=$(sed '1q;d' TMUX_RESULT_TTY)
TTY_USERS=$(sed '2q;d' TMUX_RESULT_TTY)

> REDIRECTION_FILE_CHAT
> REDIRECTION_FILE_USERS
echo "#!/bin/bash" >> REDIRECTION_FILE_CHAT
echo "echo -e \$1 > $TTY_CHAT" >> REDIRECTION_FILE_CHAT
echo "#!/bin/bash" >> REDIRECTION_FILE_USERS
echo "echo -e \$1 > $TTY_USERS" >> REDIRECTION_FILE_USERS

rm TMUX_RESULT_TTY

tmux attach
