toRed() { gawk -v text="$1" 'BEGIN {
    printf "%s", "\033[1;31m" text "\033[0m" }';
}

toYellow() { gawk -v text="$1" 'BEGIN {
    printf "%s", "\033[1;33m" text "\033[0m" }';
}
