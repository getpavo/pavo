import frontmatter
import markdown2


class MarkdownParser:
    def __init__(self):
        # TODO: Implement Parser options
        pass

    def parse(self, file):
        if not self.__is_markdown(file):
            raise ValueError

        with open(file) as f:
            data = frontmatter.loads(f.read())

        code = markdown2.markdown(data.content, extras=["cuddled-lists"]).replace('\n\n', '\n').rstrip()

        if 'content' in data.metadata:
            raise KeyError

        return code, data.metadata

    @staticmethod
    def __is_markdown(file):
        try:
            extension = file.split('.')[1].lower()
            if not extension == 'md' and not extension == 'markdown':
                return False
            return True
        except IndexError:
            return False
