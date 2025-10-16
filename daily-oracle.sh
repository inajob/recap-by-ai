#!/bin/bash

# daily-oracle.sh
# This script provides daily "oracles" or advice on different topics
# based on the day of the week.

# Ensure the output directory exists
mkdir -p out

echo "Generating diary summaries..."
# First, run the get-same-month scripts to generate the source texts.
python get-same-month.py --deep > out/out-deep.txt
python get-same-month.py > out/out-shallow.txt
echo "Diary summaries generated."

# Get the current day of the week (1=Monday, 7=Sunday)
DAY_OF_WEEK=$(date +%u)

echo "Today is day $DAY_OF_WEEK. Generating oracle..."

# Use a case statement to run a different command based on the day.
case $DAY_OF_WEEK in
  1) # Monday
    echo "Topic: Work"
    python chat.py prompts/prelude-work.txt out/out-deep.txt > out/daily-oracle.txt
    ;;
  2) # Tuesday
    echo "Topic: Health"
    python chat.py prompts/prelude-health.txt out/out-shallow.txt > out/daily-oracle.txt
    ;;
  3) # Wednesday
    echo "Topic: Childcare"
    python chat.py prompts/prelude-childcare.txt out/out-deep.txt > out/daily-oracle.txt
    ;;
  4) # Thursday
    echo "Topic: Hobby"
    python chat.py prompts/prelude-hobby.txt out/out-deep.txt > out/daily-oracle.txt
    ;;
  5) # Friday
    echo "Topic: Work"
    python chat.py prompts/prelude-work.txt out/out-deep.txt > out/daily-oracle.txt
    ;;
  6) # Saturday
    echo "Topic: Hobby"
    python chat.py prompts/prelude-hobby.txt out/out-deep.txt > out/daily-oracle.txt
    ;;
  7) # Sunday
    echo "Topic: Health"
    python chat.py prompts/prelude-health.txt out/out-shallow.txt > out/daily-oracle.txt
    ;;
esac

echo "Oracle generated in out/daily-oracle.txt"
echo "--- Oracle Content ---"
cat out/daily-oracle.txt
echo "----------------------"

# Post the result to Discord
echo "Posting to Discord..."
python post-discord.py out/daily-oracle.txt
