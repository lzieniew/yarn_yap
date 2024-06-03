# Save the enhanced Lua filter
cat <<'EOF' >clean_filter.lua
function Image(el)
  -- Remove all images
  return {}
end

function Div(el)
  -- Remove divs with certain attributes, otherwise keep them
  if el.attributes["style"] then
    return {}
  else
    return el
  end
end

function Span(el)
  -- Remove spans with certain attributes, otherwise keep them
  if el.attributes["style"] then
    return {}
  else
    return el
  end
end

function RawBlock(el)
  -- Remove raw HTML blocks
  return {}
end

function RawInline(el)
  -- Remove raw HTML inlines
  return {}
end

function Str(el)
  -- Remove stray numbers
  if el.text:match("^%d+$") then
    return {}
  end
  return el
end
EOF

# Convert EPUB to temporary TXT file using the enhanced Lua filter
pandoc input.epub --lua-filter=clean_filter.lua -t plain -o temp_output.txt

# Inspect the file to identify unwanted characters (this step is manual)
od -c temp_output.txt | less
# or
hexdump -C temp_output.txt | less
# or
xxd temp_output.txt | less

# Remove unwanted whitespace characters and normalize spaces
# (adjust the characters to remove based on the inspection results)
sed 's/\xC2\xA0/ /g; s/ \{2,\}/ /g' temp_output.txt >output.txt

# Optionally clean up by removing the Lua filter file and temporary output
rm clean_filter.lua temp_output.txt
