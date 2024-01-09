def get_unclosed_tag(markdown):
  tags = ["```", "`", "*", "_"]
  current_tag = ""

  i = 0
  while i < len(markdown):
    if markdown[i] == '\\' and current_tag == "":
      i += 2
      continue
    if current_tag != "":
      if markdown[i:].startswith(current_tag):
        i += len(current_tag)
        current_tag = ""
        continue
    else:
      for tag in tags:
        if markdown[i:].startswith(tag):
          current_tag = tag
          i += len(current_tag)
          break
    i += 1

  return current_tag


def is_valid_markdown(markdown):
  return get_unclosed_tag(markdown) == ""


def escape_markdown(text):
  special_chars = ["*", "_", "`"]

  for char in special_chars:
    open_tags = text.count(char) % 2 != 0
    if open_tags:
      text = text.replace(char, "\\" + char)

  return text
