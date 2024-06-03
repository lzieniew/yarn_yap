#!/bin/bash

# Check if yt-dlp is installed
if ! command -v yt-dlp &>/dev/null; then
	echo "yt-dlp could not be found. Please install it before running this script."
	exit
fi

# Check if ffmpeg is installed
if ! command -v ffmpeg &>/dev/null; then
	echo "ffmpeg could not be found. Please install it before running this script."
	exit
fi

# Usage function
usage() {
	echo "Usage: $0 <youtube_url> <start> <stop> <output_name>"
	echo "Example: $0 https://www.youtube.com/watch?v=dQw4w9WgXcQ 5:21 7:30 output.wav"
	exit 1
}

# Check if the correct number of arguments are provided
if [ "$#" -ne 4 ]; then
	usage
fi

# Assign arguments to variables
YOUTUBE_URL=$1
START_TIME=$2
STOP_TIME=$3
OUTPUT_NAME=$4

# Download the video
yt-dlp -x --audio-format wav -o "temp_audio.%(ext)s" "$YOUTUBE_URL"

# Convert start and stop times to seconds
start_seconds=$(echo "$START_TIME" | awk -F: '{ print ($1 * 60) + $2 }')
stop_seconds=$(echo "$STOP_TIME" | awk -F: '{ print ($1 * 60) + $2 }')

# Extract the audio segment
ffmpeg -i temp_audio.wav -ss "$start_seconds" -to "$stop_seconds" -c copy "$OUTPUT_NAME"

# Clean up temporary file
rm temp_audio.wav

echo "Audio segment saved as $OUTPUT_NAME"
