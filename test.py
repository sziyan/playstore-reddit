import markdown
import html2text

input_text = "``This is a test!``"
text_maker = html2text.HTML2Text()
text_maker.ignore_emphasis = True
text_maker.IGNORE_ANCHORS = True
text_maker.IGNORE_IMAGES = True
text = markdown.markdown(input_text)
output = text_maker.handle(text)

print(output)